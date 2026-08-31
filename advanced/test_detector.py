"""Tests for advanced/detector.py's orchestration logic -- memory
short-circuiting, and the verify() re-check. `classify` is always an
injected deterministic fake here (never the real Anthropic call): these
tests prove detect()/verify() correctly propagate and act on a
classification, not that the LLM's judgment itself is good -- that's
what eval/run_eval.py --solution advanced measures for real, against
the same fixtures, per CLAUDE.md's testing rule.
"""

from __future__ import annotations

from pathlib import Path

from advanced.detector import Detection, _visible_text, detect, verify
from advanced.memory import WatcherMemory

FIXTURES = Path(__file__).parent.parent / "eval" / "fixtures"


def load(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


class FakeConfig:
    def __init__(self, watch_for="a Saturday 9-11am court booking for 4 people", source="unused"):
        self.watch_for = watch_for
        self.source = source


def const_classify(is_match: bool, reasoning: str = "fake"):
    calls = []

    def classify(watch_for, page_text):
        calls.append((watch_for, page_text))
        return is_match, reasoning

    classify.calls = calls
    return classify


def new_memory(tmp_path) -> WatcherMemory:
    return WatcherMemory(str(tmp_path / "memory.json"))


def test_real_match_detected(tmp_path):
    current = load("05-real-match.html")
    detection = detect(None, current, FakeConfig(), new_memory(tmp_path), classify=const_classify(True))
    assert detection.is_match is True
    assert detection.from_memory is False


def test_decoy_not_detected(tmp_path):
    current = load("02-ad-rotates.html")
    detection = detect(None, current, FakeConfig(), new_memory(tmp_path), classify=const_classify(False))
    assert detection.is_match is False


def test_recall_gap_detected_without_the_literal_keyword(tmp_path):
    """Case 13: the page signals a real opening with a new "Book now"
    link, never using baseline's literal keyword ("slot available") or
    any lexical overlap with it at all. Confirmed against the real
    Anthropic API (see CHANGELOG.md): recall stays 1.00 for advanced
    while baseline's drops to 0.75 on this exact fixture. This test
    proves the plumbing correctly acts on whatever `classify` reports --
    same scope note as the rest of this file.
    """
    current = load("13-recall-gap.html")
    detection = detect(
        None, current, FakeConfig(), new_memory(tmp_path), classify=const_classify(True, "a new booking link appeared for the matching row")
    )
    assert detection.is_match is True


def test_negation_not_detected(tmp_path):
    """Case 06 -- unlike baseline's keyword substring match, a real LLM
    call is expected to correctly read a negation. This test proves the
    plumbing honors that verdict; it doesn't re-prove the LLM is right.
    """
    current = load("06-negation.html")
    classify = const_classify(False, "explicitly says no slots available")
    detection = detect(None, current, FakeConfig(), new_memory(tmp_path), classify=classify)
    assert detection.is_match is False


def test_known_decoy_short_circuits_without_calling_classify(tmp_path):
    current = load("02-ad-rotates.html")
    snippet = _visible_text(current)
    memory = new_memory(tmp_path)
    memory.record_decoy(snippet)

    classify = const_classify(True)  # would be wrong if actually called
    detection = detect(None, current, FakeConfig(), memory, classify=classify)

    assert detection.is_match is False
    assert detection.from_memory is True
    assert classify.calls == []  # never invoked -- the whole point of the short-circuit


def test_already_surfaced_short_circuits_without_calling_classify(tmp_path):
    current = load("05-real-match.html")
    snippet = _visible_text(current)
    memory = new_memory(tmp_path)
    memory.record_surfaced_match(snippet)

    classify = const_classify(False)  # would be wrong if actually called
    detection = detect(None, current, FakeConfig(), memory, classify=classify)

    assert detection.is_match is True
    assert detection.already_surfaced is True
    assert classify.calls == []


def test_verify_reconfirms_a_real_match():
    detection = Detection(is_match=True, reasoning="initial", snippet="x")
    fetch_fn = lambda source: load("05-real-match.html")
    verified = verify(detection, FakeConfig(), fetch_fn, classify=const_classify(True))
    assert verified.is_match is True


def test_verify_catches_the_flappy_slot_closing(tmp_path):
    """Case 12, the challenging case: detect() sees the slot open
    (12a); by the time verify() re-fetches, it's gone (12b). This is
    the honest limit of reactive polling -- see eval/CASES.md's design
    note and PROBLEM_STATEMENT.md's hot take.
    """
    opened = load("12a-flappy-open.html")
    detection = detect(None, opened, FakeConfig(), new_memory(tmp_path), classify=const_classify(True))
    assert detection.is_match is True

    fetch_fn = lambda source: load("12b-flappy-closed.html")
    verified = verify(detection, FakeConfig(), fetch_fn, classify=const_classify(False, "now shows fully booked"))
    assert verified.is_match is False


def test_verify_skips_a_non_match():
    """No point re-fetching to verify something that was never a match."""
    detection = Detection(is_match=False, reasoning="decoy", snippet="x")
    fetch_fn = lambda source: (_ for _ in ()).throw(AssertionError("should not be called"))
    verified = verify(detection, FakeConfig(), fetch_fn, classify=const_classify(True))
    assert verified is detection


def test_verify_skips_a_memory_short_circuit():
    """A memory-based detection doesn't need a fresh network round-trip
    to re-confirm -- it's already known, not a fresh guess.
    """
    detection = Detection(is_match=True, reasoning="known", snippet="x", from_memory=True)
    fetch_fn = lambda source: (_ for _ in ()).throw(AssertionError("should not be called"))
    verified = verify(detection, FakeConfig(), fetch_fn, classify=const_classify(False))
    assert verified is detection


def test_verify_declines_on_fetch_failure():
    detection = Detection(is_match=True, reasoning="initial", snippet="x")
    fetch_fn = lambda source: (_ for _ in ()).throw(OSError("network down"))
    verified = verify(detection, FakeConfig(), fetch_fn, classify=const_classify(True))
    assert verified.is_match is False
