"""Tests for advanced/action_drafter.py -- drafting only, no side effects."""

from __future__ import annotations

from advanced.action_drafter import draft
from advanced.detector import Detection


class FakeConfig:
    watch_for = "a Saturday 9-11am court booking for 4 people"
    source = "eval/fixtures/05-real-match.html"


def test_draft_carries_detection_and_config_fields():
    detection = Detection(is_match=True, reasoning="matches criteria", snippet="Saturday 9-11am slot available")
    action = draft(detection, FakeConfig())
    assert action.watch_for == FakeConfig.watch_for
    assert action.source == FakeConfig.source
    assert action.matched_snippet == detection.snippet
    assert action.reasoning == detection.reasoning


def test_format_for_human_mentions_no_submission_happened():
    detection = Detection(is_match=True, reasoning="matches criteria", snippet="Saturday 9-11am slot available")
    action = draft(detection, FakeConfig())
    text = action.format_for_human()
    assert "Nothing has been submitted" in text
    assert detection.snippet in text
    assert detection.reasoning in text
