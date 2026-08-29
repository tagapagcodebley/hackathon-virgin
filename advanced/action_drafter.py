"""Drafts a structured reservation request from a confirmed, verified
detection. Drafting only — never submits; see approval.py for the gate.

Stage 1 scaffolding only.
"""

from __future__ import annotations

from dataclasses import dataclass

from .criteria import WatchConfig
from .detector import Detection


@dataclass
class DraftedAction:
    """TODO: the structured next step ready for human review — generic
    across watch domains (a reservation request for the demo scenario;
    could be something else for a different `watch_for`). Should capture
    what was found, which part of `watch_for` it matched, and why (for
    the approval prompt and for the trajectory record). Never includes an
    automated hold/submit — see PROBLEM_STATEMENT.md's "On automated
    holds" section; that step always waits for a live human approval.
    """


def draft(detection: Detection, config: WatchConfig) -> DraftedAction:
    """TODO: turn a confirmed detection into a structured, human-reviewable
    next step. No network call here — drafting only.
    """
    raise NotImplementedError
