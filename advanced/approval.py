"""Human-approval gate: holds a drafted action for explicit human
approval, then runs a *simulated* submit. No code path in this project
ever calls a real booking endpoint — per the rulebook's ground rule 04
("keep consequential actions controlled through a sandbox or simulation;
add human approval before the action happens").

Stage 1 scaffolding only.
"""

from __future__ import annotations

from .action_drafter import DraftedAction


def request_approval(action: DraftedAction) -> bool:
    """TODO: alert the human that a drafted action is waiting (reuse
    ../notifications.py — the same console/email channels baseline
    already uses, don't build a second notification path), then present
    the drafted action for explicit approval and return whether they
    approved it. In the demo this can be a CLI prompt; in eval it's an
    injected fake, per CLAUDE.md's testing rule.
    """
    raise NotImplementedError


def simulated_submit(action: DraftedAction) -> None:
    """TODO: pretend to submit the approved reservation request (log it,
    write it to a file, etc.) — this function must never make a real
    network call to a live booking endpoint.
    """
    raise NotImplementedError
