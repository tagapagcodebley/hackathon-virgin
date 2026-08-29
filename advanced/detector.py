"""Semantic detection: does the new page state represent a real,
criteria-matching opening? Includes a verification re-pass before a
detection is treated as real, to cut false positives from a transient
glitch or stale fetch.

The real classifier is an Anthropic API call using tool-use for
structured output (see _classify_via_llm). It's an injectable parameter
everywhere it's used -- tests and eval/run_eval.py's --fake mode inject
a deterministic fake instead, per CLAUDE.md's testing rule. Needs
ANTHROPIC_API_KEY in the environment to run for real.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Callable, Optional

import anthropic

from .criteria import WatchConfig
from .memory import WatcherMemory

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")

ClassifyFn = Callable[[str, str], "tuple[bool, str]"]


def _visible_text(html: str) -> str:
    """Strip markup and collapse whitespace -- same cleanup baseline
    does, kept as a small local copy rather than a shared import since
    it's two lines and each solution should stay independently readable.
    """
    return _WHITESPACE_RE.sub(" ", _TAG_RE.sub(" ", html)).strip()


@dataclass
class Detection:
    is_match: bool
    reasoning: str
    snippet: str
    already_surfaced: bool = False
    from_memory: bool = False


_CLASSIFY_TOOL = {
    "name": "report_page_analysis",
    "description": (
        "Report whether the current page state represents a real, actionable "
        "opening that matches exactly what the user is watching for."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "is_match": {
                "type": "boolean",
                "description": (
                    "True only if the page currently shows a genuine, available "
                    "opening matching ALL stated criteria (date, time, party size, "
                    "etc., if given). False for: no real opening, a decoy/unrelated "
                    "mention, an explicit negation (says unavailable), or a real "
                    "opening that fails to match one or more stated criteria."
                ),
            },
            "reasoning": {
                "type": "string",
                "description": "One or two sentences citing the specific text that drove the judgment.",
            },
        },
        "required": ["is_match", "reasoning"],
    },
}


def _classify_via_llm(watch_for: str, page_text: str, model: str = DEFAULT_MODEL) -> "tuple[bool, str]":
    """Real default classifier. Needs ANTHROPIC_API_KEY in the
    environment -- this is the one piece of Sauron that costs money to
    run for real, see docs/REPRODUCTION.md's "Approx cost".

    Some API keys are "identity-linked" (issued against a specific
    workspace/account rather than a standalone developer key) and are
    rejected with a 400 unless the request also carries an
    `anthropic-workspace-id` header -- the SDK's plain API-key client
    doesn't attach this automatically even when ANTHROPIC_WORKSPACE_ID is
    set (that auto-attach only happens in its separate OAuth/identity
    credentials-chain code path). Send it as an explicit header when
    present; a standard key works fine without it.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable is not set -- cannot "
            "classify. This is the one real dependency advanced/ has that "
            "baseline/ doesn't: a live LLM call. Set it, or pass a fake "
            "`classify` function for testing (see advanced/test_detector.py)."
        )
    default_headers = {}
    workspace_id = os.environ.get("ANTHROPIC_WORKSPACE_ID")
    if workspace_id:
        default_headers["anthropic-workspace-id"] = workspace_id
    client = anthropic.Anthropic(default_headers=default_headers or None)
    message = client.messages.create(
        model=model,
        max_tokens=300,
        tools=[_CLASSIFY_TOOL],
        tool_choice={"type": "tool", "name": "report_page_analysis"},
        messages=[
            {
                "role": "user",
                "content": (
                    f"The user is watching a page for: {watch_for}\n\n"
                    f"Current page text:\n{page_text}\n\n"
                    "Carefully consider negation (e.g. \"no slots available\" is NOT "
                    "a match even though it contains matching words), unrelated "
                    "mentions (e.g. an FAQ explaining what a phrase means is NOT a "
                    "match), and whether every stated criterion (date, time, party "
                    "size, etc.) is actually met, not just the general topic."
                ),
            }
        ],
    )
    for block in message.content:
        if block.type == "tool_use":
            return bool(block.input["is_match"]), str(block.input["reasoning"])
    raise RuntimeError("Anthropic response did not include the expected tool call.")


def detect(
    previous: Optional[str],
    current: str,
    config: WatchConfig,
    memory: WatcherMemory,
    classify: ClassifyFn = _classify_via_llm,
) -> Detection:
    """Judge whether `current` is a real, matching opening. Checks
    `memory` for a known decoy or an already-surfaced match first, to
    skip a redundant LLM call on an exact repeat.
    """
    snippet = _visible_text(current)

    if memory.is_known_decoy(snippet):
        return Detection(
            is_match=False,
            reasoning="Matches a previously-confirmed decoy pattern.",
            snippet=snippet,
            from_memory=True,
        )

    if memory.is_already_surfaced(snippet):
        return Detection(
            is_match=True,
            reasoning="Same opening already surfaced for approval in an earlier poll.",
            snippet=snippet,
            already_surfaced=True,
            from_memory=True,
        )

    is_match, reasoning = classify(config.watch_for, snippet)
    return Detection(is_match=is_match, reasoning=reasoning, snippet=snippet)


def verify(
    detection: Detection,
    config: WatchConfig,
    fetch_fn: Callable[[str], str],
    classify: ClassifyFn = _classify_via_llm,
) -> Detection:
    """Re-fetch the page right now and re-classify against the FRESH
    state, to catch a transient glitch or a race where the match already
    disappeared between the original poll and this check (see
    eval/CASES.md case 12, the flappy-slot challenging case). A no-op
    for a non-match or a memory short-circuit -- nothing to verify.
    """
    if not detection.is_match or detection.from_memory:
        return detection

    try:
        fresh_current = fetch_fn(config.source)
    except OSError:
        # Couldn't re-confirm -- safer to decline than to act on a stale read.
        return Detection(
            is_match=False,
            reasoning="Verification re-fetch failed; declining rather than acting on a stale read.",
            snippet=detection.snippet,
        )
    fresh_snippet = _visible_text(fresh_current)
    is_match, reasoning = classify(config.watch_for, fresh_snippet)
    return Detection(
        is_match=is_match,
        reasoning=reasoning,
        snippet=fresh_snippet,
        already_surfaced=detection.already_surfaced,
    )
