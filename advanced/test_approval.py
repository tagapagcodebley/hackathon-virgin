"""Tests for advanced/approval.py -- the human-approval gate and the
simulated-only submit. No real network, no real submission, ever.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from advanced.action_drafter import DraftedAction
from advanced.approval import _default_approve, request_approval, simulated_submit

ACTION = DraftedAction(
    watch_for="a Saturday 9-11am court booking for 4 people",
    matched_snippet="Saturday 9-11am slot available",
    reasoning="matches criteria",
    source="eval/fixtures/05-real-match.html",
)


def test_request_approval_notifies_and_returns_approve_fn_result():
    notified = []
    approved = request_approval(
        ACTION,
        notifier=lambda subject, body: notified.append((subject, body)),
        approve_fn=lambda action: True,
    )
    assert approved is True
    assert len(notified) == 1
    assert "approval" in notified[0][0].lower()
    assert ACTION.matched_snippet in notified[0][1]


def test_request_approval_can_decline():
    approved = request_approval(ACTION, notifier=lambda s, b: None, approve_fn=lambda action: False)
    assert approved is False


def test_default_approve_declines_when_not_interactive(monkeypatch):
    """pytest's captured stdin is never a tty -- this is exactly the
    Scheduled Task scenario: no live human present, so decline rather
    than guess (see approval.py's module docstring).
    """
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    assert _default_approve(ACTION) is False


def test_default_approve_honors_interactive_yes(monkeypatch):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    assert _default_approve(ACTION) is True


def test_default_approve_honors_interactive_no(monkeypatch):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    assert _default_approve(ACTION) is False


def test_simulated_submit_writes_a_local_record_only(tmp_path):
    log_path = str(tmp_path / "submissions.log")
    simulated_submit(ACTION, log_path=log_path)

    lines = Path(log_path).read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["watch_for"] == ACTION.watch_for
    assert record["matched_snippet"] == ACTION.matched_snippet
    assert record["source"] == ACTION.source
    assert "submitted_at" in record


def test_simulated_submit_appends_across_calls(tmp_path):
    log_path = str(tmp_path / "submissions.log")
    simulated_submit(ACTION, log_path=log_path)
    simulated_submit(ACTION, log_path=log_path)
    lines = Path(log_path).read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
