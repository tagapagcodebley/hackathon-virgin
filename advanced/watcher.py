"""Sauron (advanced): watch-and-act orchestrator wiring config, memory,
detector, action_drafter, and approval into the poll loop — stopping at
the `auto_expire` failsafe, and tightening the poll interval as
`release_date` nears (two distinct dates — see criteria.py and
PROBLEM_STATEMENT.md's "Auto-expire vs. release date").

Stage 1 scaffolding only — everything below is a placeholder. Real
implementation lands in Stage 3.
"""

from __future__ import annotations

from .action_drafter import draft
from .approval import request_approval, simulated_submit
from .criteria import WatchConfig, load_config
from .detector import detect, verify
from .memory import WatcherMemory


def fetch_page_state(source: str) -> str:
    """TODO: same contract as baseline/watcher.py's fetch_page_state —
    `source` is a URL in production, a fixture path in tests/eval.
    """
    raise NotImplementedError


def next_poll_interval(config: WatchConfig, now) -> "timedelta":
    """TODO: adaptive polling — return `config.poll_interval` unmodified
    when `config.release_date` is unset or far away, tightened as
    `release_date` approaches (see PROBLEM_STATEMENT.md's "Auto-expire
    vs. release date" and eval/CASES.md case 14). Must NOT reference
    `config.auto_expire` — that field is a failsafe only, not a timing
    signal. `now` is an injectable clock, never datetime.now() directly,
    so tests can control it (CLAUDE.md's testing rule).
    """
    raise NotImplementedError


def run(config_path: str, state_path: str, now=None) -> None:
    """TODO: poll loop — stop entirely once `auto_expire` has passed
    (eval/CASES.md case 13, the failsafe, independent of release_date);
    otherwise fetch, detect + verify against config and memory, draft an
    action on a confirmed match, hold for human approval, then
    simulated_submit on approval; sleep for next_poll_interval() between
    polls (which tightens near release_date, not auto_expire).
    """
    raise NotImplementedError


if __name__ == "__main__":
    raise NotImplementedError("advanced watcher not yet implemented — Stage 1 placeholder")
