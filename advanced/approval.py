"""Human-approval gate: alerts a human that a drafted action is waiting,
then holds it for explicit approval before a *simulated* submit. No
code path in this project ever calls a real booking endpoint -- per the
rulebook's ground rule 04 ("keep consequential actions controlled
through a sandbox or simulation; add human approval before the action
happens").

Approval is deliberately never auto-granted in headless/unattended runs
(e.g. under a Scheduled Task): there's no live human to approve, so the
default behavior there is "notify and stop" -- the same honest limit
baseline has, just with a far richer, pre-drafted message instead of a
bare "page changed."
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from notifications import console_notify

from .action_drafter import DraftedAction

ApproveFn = Callable[[DraftedAction], bool]


def _default_approve(action: DraftedAction) -> bool:
    """Real default: prompt synchronously if there's a live human at a
    terminal; otherwise (a Scheduled Task, piped stdin, or a tty-like
    handle with nothing actually behind it) there's no one to ask, so
    decline rather than guess. The prompt itself is short -- the full
    action was already shown by `request_approval`'s notifier call, no
    need to repeat it.
    """
    if not sys.stdin.isatty():
        return False
    try:
        response = input("Approve and simulate-submit? [y/N] ")
    except EOFError:
        return False
    return response.strip().lower() in ("y", "yes")


def request_approval(
    action: DraftedAction,
    notifier: Callable[[str, str], None] = console_notify,
    approve_fn: Optional[ApproveFn] = None,
) -> bool:
    """Alert the human via `notifier`, then get an approve/decline
    decision via `approve_fn` (defaults to `_default_approve`; tests
    inject a fixed True/False).
    """
    notifier("Sauron: drafted action ready for approval", action.format_for_human())
    approve = approve_fn if approve_fn is not None else _default_approve
    return approve(action)


def simulated_submit(action: DraftedAction, log_path: str = "deploy/simulated_submissions.log") -> None:
    """Pretend to submit the approved action -- appends a record to a
    local log. Never makes a real network call to a live booking
    endpoint; this function has no network access at all.
    """
    record = {
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "watch_for": action.watch_for,
        "source": action.source,
        "matched_snippet": action.matched_snippet,
        "reasoning": action.reasoning,
    }
    log_file = Path(log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
