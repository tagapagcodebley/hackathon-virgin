"""Sauron (baseline): keyword-diff watcher for a page. Fetches, diffs
against the last-seen snapshot, and fires a plain notification if the new
text contains a short literal `keyword` — the same approach real
keyword-watch tools use (you configure a short phrase like "in stock" or
"slots available", not a full sentence). No semantic judgment, no
criteria disambiguation, no drafted action, no adaptive polling.

See ../PROBLEM_STATEMENT.md for what this is expected to get wrong
(notably the negation case) and ../eval/CASES.md for the cases it's
evaluated against.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

import requests

from fetching import fetch_page_state
from notifications import NOTIFIERS, console_notify

DEFAULT_KEYWORD = "slot available"
_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


def _visible_text(html: str) -> str:
    """Strip markup and collapse whitespace. Not HTML parsing or
    semantic understanding — just enough cleanup that a notification
    shows readable text instead of a wall of tags.
    """
    return _WHITESPACE_RE.sub(" ", _TAG_RE.sub(" ", html)).strip()


def has_changed(previous: str | None, current: str) -> bool:
    """Return True if `current` differs from `previous` (raw text compare)."""
    if previous is None:
        return True
    return previous != current


def matches_watch_for(current: str, keyword: str = DEFAULT_KEYWORD) -> bool:
    """Naive case-insensitive substring check.

    Intentionally naive — this is the documented limitation: it cannot
    tell "no slot available" (a negation) from a real match, since both
    contain the same substring. See eval/CASES.md case 06.
    """
    return keyword.lower() in current.lower()


def notify(
    current: str,
    keyword: str = DEFAULT_KEYWORD,
    notifier: Callable[[str, str], None] = console_notify,
) -> None:
    """Surface a notification with a snippet of visible text around the
    matched keyword, via an injectable `notifier` (see notifications.py).
    Defaults to console output — safe for tests/eval, no credentials, no
    network. Pass `notifications.email_notify` for real unattended
    delivery. No drafted next step; that's advanced-only.
    """
    text = _visible_text(current)
    match_at = text.lower().find(keyword.lower())
    start = max(0, match_at - 60)
    end = min(len(text), match_at + len(keyword) + 60)
    snippet = text[start:end]
    subject = f"Sauron: page changed and contains '{keyword}'"
    body = f"...{snippet}..."
    notifier(subject, body)


def run(
    source: str,
    state_path: str,
    keyword: str = DEFAULT_KEYWORD,
    notifier: Callable[[str, str], None] = console_notify,
) -> None:
    """Poll loop (single poll per call, meant to be re-invoked on a
    schedule — see ../deploy/) — fetch, compare against last-seen state,
    notify when changed AND matches_watch_for(). Fixed behavior only —
    no expiry handling, no adaptive interval (those are advanced-only,
    see eval/CASES.md cases 13-14). A fetch failure is logged and
    skipped rather than crashing the caller.
    """
    state_file = Path(state_path)
    previous = state_file.read_text(encoding="utf-8") if state_file.exists() else None

    try:
        current = fetch_page_state(source)
    except (OSError, requests.RequestException) as exc:
        print(f"[Sauron baseline] fetch failed, skipping this poll: {exc}")
        return

    if has_changed(previous, current) and matches_watch_for(current, keyword):
        notify(current, keyword, notifier)

    state_file.write_text(current, encoding="utf-8")


if __name__ == "__main__":
    import argparse
    import sys

    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--keyword", default=DEFAULT_KEYWORD)
    parser.add_argument("--notify", choices=sorted(NOTIFIERS), default="console")
    args = parser.parse_args()
    run(args.source, args.state, args.keyword, NOTIFIERS[args.notify])
