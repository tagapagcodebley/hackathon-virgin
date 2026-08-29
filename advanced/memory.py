"""Cross-poll memory: prior page states and previously-seen decoy or
already-surfaced-match snippets, so the detector stops re-flagging the
same noise -- or re-drafting the same already-seen opportunity -- every
cycle. Persisted to a small JSON file between polls.
"""

from __future__ import annotations

import json
from pathlib import Path


class WatcherMemory:
    def __init__(self, state_path: str) -> None:
        self.state_path = Path(state_path)
        if self.state_path.exists():
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
        else:
            data = {}
        self._decoys: set[str] = set(data.get("decoys", []))
        self._surfaced: set[str] = set(data.get("surfaced", []))

    def record_decoy(self, snippet: str) -> None:
        self._decoys.add(snippet)

    def is_known_decoy(self, snippet: str) -> bool:
        return snippet in self._decoys

    def record_surfaced_match(self, snippet: str) -> None:
        self._surfaced.add(snippet)

    def is_already_surfaced(self, snippet: str) -> bool:
        return snippet in self._surfaced

    def save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps({"decoys": sorted(self._decoys), "surfaced": sorted(self._surfaced)}, indent=2),
            encoding="utf-8",
        )
