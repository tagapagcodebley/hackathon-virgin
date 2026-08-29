"""Tests for the baseline watcher, run against local fixtures — never the
live network (see CLAUDE.md's testing rule). Fixture paths reference
../eval/fixtures/, one fixture per case in ../eval/CASES.md.
"""

from pathlib import Path

import pytest

from baseline.watcher import DEFAULT_KEYWORD, has_changed, matches_watch_for, run

FIXTURES = Path(__file__).parent.parent / "eval" / "fixtures"


def load(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_no_change_does_not_notify():
    """Case 01: repeated fully-booked snapshot -> has_changed() is False."""
    text = load("00-baseline.html")
    assert has_changed(text, text) is False


@pytest.mark.parametrize(
    "fixture",
    ["02-ad-rotates.html", "03-timestamp-changes.html", "04-unrelated-copy.html"],
)
def test_decoy_change_without_keyword_does_not_notify(fixture):
    """Cases 02-04: the page changed, but the diff doesn't contain the
    keyword, so baseline correctly stays quiet.
    """
    previous = load("00-baseline.html")
    current = load(fixture)
    assert has_changed(previous, current) is True
    assert matches_watch_for(current) is False


def test_real_match_notifies():
    """Case 05: the core win condition — baseline correctly fires."""
    current = load("05-real-match.html")
    assert matches_watch_for(current) is True


def test_negation_is_a_documented_false_positive():
    """Case 06: baseline's sharpest failure. "No slot available this
    week" contains the substring "slot available", so the naive check
    fires anyway — documented in PROBLEM_STATEMENT.md, not a bug to fix
    here.
    """
    current = load("06-negation.html")
    assert matches_watch_for(current) is True


@pytest.mark.parametrize(
    "fixture",
    ["07-wrong-date.html", "08-wrong-time.html", "09-wrong-party-size.html"],
)
def test_criteria_mismatch_still_notifies(fixture):
    """Cases 07-09: a real opening that doesn't match the user's actual
    criteria still trips the keyword check, since baseline has no concept
    of date/time/party-size criteria at all.
    """
    current = load(fixture)
    assert matches_watch_for(current) is True


def test_ambiguous_faq_mention_is_a_documented_false_positive():
    """Case 10: a new FAQ paragraph explaining the phrase "slot available"
    trips the keyword check even though it's generic help text, not an
    actual booking entry.
    """
    current = load("10-ambiguous-faq.html")
    assert matches_watch_for(current) is True


def test_duplicate_match_notifies_every_time():
    """Case 11: baseline has no memory, so two different-but-both-matching
    snapshots of the same underlying opening both trip a notification —
    duplicate alert, not deduplicated.
    """
    first = load("11a-duplicate-match.html")
    second = load("11b-duplicate-match-variant.html")
    assert has_changed(first, second) is True
    assert matches_watch_for(first) is True
    assert matches_watch_for(second) is True


def test_flappy_slot_fires_on_the_open():
    """Case 12 (the challenging case): baseline has no verification pass,
    so it fires as soon as it sees the open snapshot — it has no way to
    know the slot may already be gone by the time a human reads the
    notification. Contrasted with advanced's verification behavior in
    Stage 3.
    """
    current = load("12a-flappy-open.html")
    assert matches_watch_for(current) is True


def test_fetch_error_does_not_crash(tmp_path):
    """A broken/missing source should not raise past run()."""
    missing_source = str(tmp_path / "does-not-exist.html")
    state_path = str(tmp_path / "state.txt")
    run(missing_source, state_path)  # must not raise
    assert not Path(state_path).exists()


def test_run_writes_state_and_notifies_on_real_match(tmp_path, capsys):
    """End-to-end: first poll (no prior state) always counts as
    "changed"; a matching fixture triggers a notification and persists
    state for the next poll.
    """
    state_path = str(tmp_path / "state.txt")
    run(str(FIXTURES / "05-real-match.html"), state_path)
    captured = capsys.readouterr()
    assert DEFAULT_KEYWORD in captured.out
    assert Path(state_path).read_text(encoding="utf-8") == load("05-real-match.html")


def test_run_uses_injected_notifier_not_console(tmp_path, capsys):
    """The notifier is genuinely pluggable — swapping it out means
    nothing goes to stdout, and the injected callable receives the call
    instead. This is what makes real unattended delivery (e.g.
    notifications.email_notify) possible without changing run()/notify().
    """
    received = []
    state_path = str(tmp_path / "state.txt")
    run(str(FIXTURES / "05-real-match.html"), state_path, notifier=lambda subject, body: received.append((subject, body)))
    captured = capsys.readouterr()
    assert captured.out == ""
    assert len(received) == 1
    subject, body = received[0]
    assert DEFAULT_KEYWORD in subject
