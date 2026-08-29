"""Tests for the advanced (Sauron) watcher, run against local fixtures —
never the live network (see CLAUDE.md's testing rule). LLM calls in
detector.py must be an injectable parameter with a real default so tests
can inject a fake/deterministic response. Time-dependent behavior
(expiry, adaptive interval) must take an injectable clock, never
datetime.now() directly.

Stage 1 scaffolding only — case bodies are TODOs, one per case in
../eval/CASES.md.
"""

import pytest


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_no_change_does_not_detect():
    """TODO: case 01 — repeated fully-booked snapshot -> no detection."""


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_decoy_change_does_not_detect():
    """TODO: cases 02-04 — ad/timestamp/unrelated-copy decoy -> no detection."""


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_known_decoy_short_circuits_via_memory():
    """TODO: a decoy seen once and recorded should not trigger a fresh
    detector call on the next poll.
    """


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_real_match_drafts_action_and_requires_approval():
    """TODO: case 05 -> draft() produces a DraftedAction, and
    simulated_submit() only runs after request_approval() returns True.
    """


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_negation_does_not_detect():
    """TODO: case 06 — unlike baseline, semantic detection correctly
    reads "no slots available" as not a match.
    """


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_near_miss_criteria_does_not_act():
    """TODO: cases 07-09 — real opening, but wrong date/time/party size ->
    no drafted action.
    """


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_ambiguous_faq_mention_does_not_detect():
    """TODO: case 10 — watch_for phrase in unrelated FAQ copy -> no detection."""


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_duplicate_match_not_redrafted():
    """TODO: case 11 — same real opening seen twice -> detected/drafted
    once, memory suppresses the second.
    """


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_flappy_slot_race_case():
    """TODO: case 12, the challenging case — a slot that opens and closes
    within a single poll cycle. Document what this reveals as the
    project's Hot Take, per eval/CASES.md's design note.
    """


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_expired_watch_does_not_poll_or_act():
    """TODO: case 13 — injected fake clock past auto_expire (the
    failsafe) -> run() does not fetch or act even if the fixture behind
    it is a real match, regardless of release_date.
    """


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_poll_interval_tightens_near_release_date():
    """TODO: case 14 — next_poll_interval() returns a shorter interval as
    the injected fake clock approaches config.release_date than when far
    from it, with auto_expire held constant/far away to prove the
    tightening tracks release_date and not auto_expire.
    """


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 3")
def test_fetch_error_does_not_crash():
    """TODO: a broken/malformed page fetch should not raise past run()."""
