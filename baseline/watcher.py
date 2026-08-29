"""Sauron (baseline): keyword-diff watcher for a page. Fetches, diffs
against the last-seen snapshot, and fires a plain notification if the new
text contains a substring from `watch_for`. No semantic judgment, no
criteria disambiguation, no drafted action, no adaptive polling.

See ../PROBLEM_STATEMENT.md for what this is expected to get wrong
(notably the negation case) and ../eval/CASES.md for the cases it's
evaluated against.

Stage 1 scaffolding only — everything below is a placeholder. Real
implementation lands in Stage 2.
"""

from __future__ import annotations


def fetch_page_state(source: str) -> str:
    """TODO: return the current page text from `source`.

    `source` is a URL in production, a fixture file path in tests/eval —
    keep it an injectable parameter (see CLAUDE.md's testing rule), never
    hit the live network from a test.
    """
    raise NotImplementedError


def has_changed(previous: str | None, current: str) -> bool:
    """TODO: return True if `current` differs from `previous` (raw
    text/hash compare).
    """
    raise NotImplementedError


def matches_watch_for(current: str, watch_for: str) -> bool:
    """TODO: plain substring check of `watch_for` against `current`.

    Intentionally naive — this is the documented limitation: it cannot
    tell "no slots available" (a negation) from a real match, since both
    contain the same substring. See eval/CASES.md case 06.
    """
    raise NotImplementedError


def notify(current: str) -> None:
    """TODO: surface a plain notification. No drafted next step."""
    raise NotImplementedError


def run(source: str, watch_for: str, state_path: str) -> None:
    """TODO: poll loop — fetch, compare against last-seen state, notify
    when changed AND matches_watch_for(). Fixed poll interval only — no
    expiry handling, no adaptive interval (those are advanced-only, see
    eval/CASES.md cases 13-14).
    """
    raise NotImplementedError


if __name__ == "__main__":
    raise NotImplementedError("baseline watcher not yet implemented — Stage 1 placeholder")
