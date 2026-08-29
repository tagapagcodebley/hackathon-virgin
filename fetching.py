"""Page fetching, shared by baseline/ and advanced/ so both watchers use
identical fetch semantics for a fair comparison. `source` is a URL in
production, a fixture file path in tests/eval -- keeping it this simple
(no separate injected fake) is enough to keep tests off the live
network, since eval always passes a local fixture path (see CLAUDE.md's
testing rule).
"""

from __future__ import annotations

from pathlib import Path

import requests


def fetch_page_state(source: str) -> str:
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source, timeout=10)
        response.raise_for_status()
        return response.text
    return Path(source).read_text(encoding="utf-8")
