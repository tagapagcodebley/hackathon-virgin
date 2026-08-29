"""Drafts a structured, human-reviewable next step from a confirmed,
verified detection. Drafting only -- never submits; see approval.py for
the gate.
"""

from __future__ import annotations

from dataclasses import dataclass

from .criteria import WatchConfig
from .detector import Detection


@dataclass
class DraftedAction:
    watch_for: str
    matched_snippet: str
    reasoning: str
    source: str

    def format_for_human(self) -> str:
        return (
            f"Sauron found a match for: {self.watch_for}\n\n"
            f"Page: {self.source}\n"
            f"Why: {self.reasoning}\n\n"
            f"Matched text:\n{self.matched_snippet}\n\n"
            "Nothing has been submitted anywhere -- this is a draft "
            "waiting for your approval before any (simulated) next step."
        )


def draft(detection: Detection, config: WatchConfig) -> DraftedAction:
    """Turn a confirmed detection into a structured, human-reviewable
    draft. No network call here -- drafting only.
    """
    return DraftedAction(
        watch_for=config.watch_for,
        matched_snippet=detection.snippet,
        reasoning=detection.reasoning,
        source=config.source,
    )
