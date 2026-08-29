"""Semantic detection: does the new page state represent a real,
criteria-matching opening? Includes a verification re-pass before a
detection is treated as real, to cut false positives from a transient
glitch or stale fetch.

Stage 1 scaffolding only.
"""

from __future__ import annotations

from dataclasses import dataclass

from .criteria import WatchConfig
from .memory import WatcherMemory


@dataclass
class Detection:
    """TODO: result of a detection pass."""

    # TODO: is_match: bool
    # TODO: confidence / reasoning: str (for the trajectory record)


def detect(
    previous: str | None,
    current: str,
    config: WatchConfig,
    memory: WatcherMemory,
) -> Detection:
    """TODO: agent call — given the page diff and `config.watch_for`
    (plain language, not a keyword list), judge whether this is a real,
    matching opening: not a decoy, not a negation (e.g. "no slots
    available" containing the watch_for substring — see eval/CASES.md
    case 06), not a criteria near-miss. Check `memory` for known decoys
    and already-surfaced matches first.
    """
    raise NotImplementedError


def verify(detection: Detection, current: str) -> Detection:
    """TODO: second-pass re-confirmation before acting on a detection —
    reduces false positives from a transient glitch or stale fetch.
    """
    raise NotImplementedError
