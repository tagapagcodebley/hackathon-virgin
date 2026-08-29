"""Tests for the baseline watcher, run against local fixtures — never the
live network (see CLAUDE.md's testing rule).

Stage 1 scaffolding only — case bodies are TODOs. Fixture paths reference
../eval/fixtures/, one fixture per case in ../eval/CASES.md.
"""

import pytest


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 2")
def test_no_change_does_not_notify():
    """TODO: repeated fully-booked snapshot (case 01) -> has_changed() is False."""


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 2")
def test_decoy_change_without_keyword_does_not_notify():
    """TODO: decoy fixtures (cases 02-04) don't contain watch_for -> no notification."""


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 2")
def test_real_match_notifies():
    """TODO: case 05 -> matches_watch_for() True, notify() called."""


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 2")
def test_negation_is_a_documented_false_positive():
    """TODO: case 06 ("no Saturday slots available") -> baseline's naive
    substring check incorrectly fires. This is the headline documented
    limitation, not a bug to fix here — assert the (wrong) fire, per
    PROBLEM_STATEMENT.md.
    """


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 2")
def test_criteria_mismatch_still_notifies():
    """TODO: cases 07-09 (wrong date/time/party size) -> baseline still
    fires since it only checks keyword presence, not full criteria.
    """


@pytest.mark.skip(reason="Stage 1 placeholder — implemented in Stage 2")
def test_fetch_error_does_not_crash():
    """TODO: a broken/malformed page fetch should not raise past run()."""
