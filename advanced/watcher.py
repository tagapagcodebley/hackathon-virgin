"""Sauron (advanced): watch-and-act orchestrator wiring config, memory,
detector, action_drafter, and approval into the poll loop -- stopping at
the `auto_expire` failsafe, and tightening the poll interval as
`release_date` nears (two distinct dates -- see criteria.py and
PROBLEM_STATEMENT.md's "Auto-expire vs. release date").
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Optional

import requests

from fetching import fetch_page_state
from notifications import NOTIFIERS, console_notify

from .action_drafter import DraftedAction, draft
from .approval import ApproveFn, request_approval, simulated_submit
from .criteria import WatchConfig, load_config
from .detector import ClassifyFn, _classify_via_llm, detect, verify
from .memory import WatcherMemory

TIGHTEN_WINDOW = timedelta(hours=2)
MIN_POLL_INTERVAL = timedelta(minutes=1)


def has_changed(previous: Optional[str], current: str) -> bool:
    if previous is None:
        return True
    return previous != current


def next_poll_interval(config: WatchConfig, now: datetime) -> timedelta:
    """Adaptive polling -- tightens as `release_date` approaches. Must
    NOT reference `auto_expire`: that field is a failsafe only, not a
    timing signal (see PROBLEM_STATEMENT.md).
    """
    if config.release_date is None:
        return config.poll_interval

    time_to_release = config.release_date - now
    if time_to_release <= timedelta(0) or time_to_release >= TIGHTEN_WINDOW:
        return config.poll_interval

    fraction = time_to_release / TIGHTEN_WINDOW  # in (0, 1)
    base_seconds = config.poll_interval.total_seconds()
    floor_seconds = MIN_POLL_INTERVAL.total_seconds()
    interval_seconds = floor_seconds + fraction * (base_seconds - floor_seconds)
    return timedelta(seconds=interval_seconds)


def run(
    config_path: str,
    state_path: str,
    memory_path: str = "deploy/advanced_memory.json",
    now: Optional[datetime] = None,
    fetch_fn: Callable[[str], str] = fetch_page_state,
    classify: ClassifyFn = _classify_via_llm,
    notifier: Callable[[str, str], None] = console_notify,
    approve_fn: Optional[ApproveFn] = None,
    submit_fn: Callable[[DraftedAction], None] = simulated_submit,
) -> None:
    """One poll. Stops entirely once `auto_expire` has passed (the
    failsafe, independent of `release_date`); otherwise fetches, detects
    + verifies against config and memory, drafts an action on a
    confirmed match, holds it for human approval, then
    submit_fn()s (default: simulated_submit) on approval.
    """
    now = now or datetime.now()
    config = load_config(config_path)

    if now >= config.auto_expire:
        print(f"[Sauron advanced] auto_expire ({config.auto_expire.isoformat()}) has passed -- not polling.")
        return

    memory = WatcherMemory(memory_path)
    state_file = Path(state_path)
    state_file.parent.mkdir(parents=True, exist_ok=True)
    previous = state_file.read_text(encoding="utf-8") if state_file.exists() else None

    try:
        current = fetch_fn(config.source)
    except (OSError, requests.RequestException) as exc:
        print(f"[Sauron advanced] fetch failed, skipping this poll: {exc}")
        return

    if not has_changed(previous, current):
        state_file.write_text(current, encoding="utf-8")
        return

    detection = detect(previous, current, config, memory, classify=classify)

    if not detection.is_match:
        memory.record_decoy(detection.snippet)
        memory.save()
        state_file.write_text(current, encoding="utf-8")
        return

    if detection.already_surfaced:
        state_file.write_text(current, encoding="utf-8")
        return

    verified = verify(detection, config, fetch_fn, classify=classify)

    if not verified.is_match:
        memory.record_decoy(verified.snippet)
        memory.save()
        state_file.write_text(current, encoding="utf-8")
        return

    action = draft(verified, config)
    approved = request_approval(action, notifier=notifier, approve_fn=approve_fn)
    memory.record_surfaced_match(verified.snippet)
    memory.save()

    if approved:
        submit_fn(action)

    state_file.write_text(current, encoding="utf-8")


if __name__ == "__main__":
    import argparse
    import sys

    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--memory", default="deploy/advanced_memory.json")
    parser.add_argument("--notify", choices=sorted(NOTIFIERS), default="console")
    args = parser.parse_args()
    try:
        run(args.config, args.state, args.memory, notifier=NOTIFIERS[args.notify])
    except RuntimeError as exc:
        print(f"[Sauron advanced] {exc}")
        raise SystemExit(1)
