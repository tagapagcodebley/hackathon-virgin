"""Cross-poll memory: prior page states and previously-seen decoy
patterns, so the detector stops re-flagging the same noise every cycle.

Stage 1 scaffolding only.
"""

from __future__ import annotations


class WatcherMemory:
    """TODO: persisted state — last-seen page snapshot, a running set of
    patterns already judged to be decoys (e.g. "that ad banner text",
    "that FAQ sentence"), and matches already surfaced to the human, so
    the detector can short-circuit known noise and never re-draft an
    action for something already presented for approval (see eval/CASES.md
    case 11).
    """

    def __init__(self, state_path: str) -> None:
        # TODO: load persisted state from state_path if it exists
        raise NotImplementedError

    def record_decoy(self, snippet: str) -> None:
        """TODO: remember a confirmed-decoy text snippet."""
        raise NotImplementedError

    def is_known_decoy(self, snippet: str) -> bool:
        """TODO: check the snippet against remembered decoys."""
        raise NotImplementedError

    def record_surfaced_match(self, snippet: str) -> None:
        """TODO: remember a match already drafted/surfaced for approval,
        so an unchanged repeat of the same opening doesn't re-draft.
        """
        raise NotImplementedError

    def is_already_surfaced(self, snippet: str) -> bool:
        """TODO: check whether this match was already surfaced."""
        raise NotImplementedError

    def save(self) -> None:
        """TODO: persist state to disk."""
        raise NotImplementedError
