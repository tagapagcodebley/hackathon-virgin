"""Tests for advanced/watcher.py's orchestration -- run() and
next_poll_interval(). `classify`/`fetch_fn`/`notifier`/`approve_fn`/
`submit_fn` are always injected fakes here, never the real Anthropic
call or real network -- see CLAUDE.md's testing rule and
advanced/test_detector.py's docstring for why that's the right scope
for these tests (plumbing correctness, not model quality).

Case numbers below refer to eval/CASES.md.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from advanced.watcher import next_poll_interval, run
from advanced.criteria import WatchConfig

FIXTURES = Path(__file__).parent.parent / "eval" / "fixtures"


def load(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def write_config(tmp_path, source_fixture: str, **overrides) -> str:
    data = {
        "source": str(FIXTURES / source_fixture),
        "watch_for": "a Saturday 9-11am court booking for 4 people",
        "release_date": None,
        "auto_expire": "2026-09-28T00:00:00",
        "poll_interval_minutes": 15,
    }
    data.update(overrides)
    path = tmp_path / "config.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


def const_classify(is_match: bool, reasoning: str = "fake"):
    def classify(watch_for, page_text):
        return is_match, reasoning

    return classify


def raising_classify(watch_for, page_text):
    raise AssertionError("classify should not have been called")


def raising_fetch(source):
    raise AssertionError("fetch should not have been called")


class Recorder:
    def __init__(self):
        self.calls = []

    def __call__(self, *args):
        self.calls.append(args)


# --- Case 01: steady state -----------------------------------------------


def test_unchanged_page_never_calls_classify(tmp_path):
    """Case 01: has_changed() short-circuits before any LLM call happens."""
    config_path = write_config(tmp_path, "00-baseline.html")
    state_path = tmp_path / "state.txt"
    state_path.write_text(load("00-baseline.html"), encoding="utf-8")

    run(config_path, str(state_path), str(tmp_path / "memory.json"), classify=raising_classify)
    # no assertion needed beyond "didn't raise" -- raising_classify would
    # have failed the test if it were called


# --- Case 05: the core win condition --------------------------------------


def test_real_match_notifies_and_submits_on_approval(tmp_path):
    config_path = write_config(tmp_path, "05-real-match.html")
    notifier = Recorder()
    submit_fn = Recorder()

    run(
        config_path,
        str(tmp_path / "state.txt"),
        str(tmp_path / "memory.json"),
        classify=const_classify(True, "matches criteria"),
        notifier=notifier,
        approve_fn=lambda action: True,
        submit_fn=submit_fn,
    )

    assert len(notifier.calls) == 1
    assert len(submit_fn.calls) == 1
    action = submit_fn.calls[0][0]
    assert "Slot available" in action.matched_snippet


def test_real_match_declined_does_not_submit(tmp_path):
    config_path = write_config(tmp_path, "05-real-match.html")
    submit_fn = Recorder()

    run(
        config_path,
        str(tmp_path / "state.txt"),
        str(tmp_path / "memory.json"),
        classify=const_classify(True),
        approve_fn=lambda action: False,
        submit_fn=submit_fn,
    )

    assert submit_fn.calls == []


# --- Case 13: recall gap -- a real match with zero keyword overlap ---------


def test_recall_gap_notifies_and_submits_where_baseline_would_stay_silent(tmp_path):
    """Case 13: "Book now — 4 players" appears for the Saturday 9-11am
    row -- a genuine match baseline's keyword check structurally cannot
    see (no "slot", no "available" anywhere). Confirmed against the real
    Anthropic API (CHANGELOG.md): advanced correctly fires here, holding
    recall at 1.00 while baseline's drops to 0.75 on this exact case.
    """
    config_path = write_config(tmp_path, "13-recall-gap.html")
    notifier = Recorder()
    submit_fn = Recorder()

    run(
        config_path,
        str(tmp_path / "state.txt"),
        str(tmp_path / "memory.json"),
        classify=const_classify(True, "a new booking link appeared for the matching row"),
        notifier=notifier,
        approve_fn=lambda action: True,
        submit_fn=submit_fn,
    )

    assert len(notifier.calls) == 1
    assert len(submit_fn.calls) == 1
    action = submit_fn.calls[0][0]
    assert "Book now" in action.matched_snippet


# --- Cases 02-04: decoys ---------------------------------------------------


@pytest.mark.parametrize("fixture", ["02-ad-rotates.html", "03-timestamp-changes.html", "04-unrelated-copy.html"])
def test_decoys_never_notify_or_submit(tmp_path, fixture):
    config_path = write_config(tmp_path, fixture)
    notifier = Recorder()
    submit_fn = Recorder()

    run(
        config_path,
        str(tmp_path / "state.txt"),
        str(tmp_path / "memory.json"),
        classify=const_classify(False, "decoy"),
        notifier=notifier,
        submit_fn=submit_fn,
    )

    assert notifier.calls == []
    assert submit_fn.calls == []


# --- Case 06: negation ------------------------------------------------------


def test_negation_never_notifies(tmp_path):
    config_path = write_config(tmp_path, "06-negation.html")
    notifier = Recorder()

    run(
        config_path,
        str(tmp_path / "state.txt"),
        str(tmp_path / "memory.json"),
        classify=const_classify(False, "explicitly unavailable"),
        notifier=notifier,
    )

    assert notifier.calls == []


# --- Cases 07-09: criteria near-misses -------------------------------------


@pytest.mark.parametrize("fixture", ["07-wrong-date.html", "08-wrong-time.html", "09-wrong-party-size.html"])
def test_criteria_near_miss_never_submits(tmp_path, fixture):
    config_path = write_config(tmp_path, fixture)
    submit_fn = Recorder()

    run(
        config_path,
        str(tmp_path / "state.txt"),
        str(tmp_path / "memory.json"),
        classify=const_classify(False, "wrong criteria"),
        approve_fn=lambda action: True,
        submit_fn=submit_fn,
    )

    assert submit_fn.calls == []


# --- Case 10: ambiguous FAQ mention -----------------------------------------


def test_ambiguous_faq_never_notifies(tmp_path):
    config_path = write_config(tmp_path, "10-ambiguous-faq.html")
    notifier = Recorder()

    run(
        config_path,
        str(tmp_path / "state.txt"),
        str(tmp_path / "memory.json"),
        classify=const_classify(False, "generic FAQ copy, not a listing"),
        notifier=notifier,
    )

    assert notifier.calls == []


# --- Case 11: memory dedup, and its documented limit ------------------------


def test_revisited_exact_match_is_deduped_via_memory(tmp_path):
    """Poll 1: a real match, approved. Poll 2: a decoy. Poll 3: the page
    reverts to the EXACT same match text as poll 1 -- memory recognizes
    it as already-surfaced and skips re-drafting entirely, without even
    calling classify.
    """
    state_path = str(tmp_path / "state.txt")
    memory_path = str(tmp_path / "memory.json")
    submit_fn = Recorder()

    run(
        write_config(tmp_path, "05-real-match.html"),
        state_path,
        memory_path,
        classify=const_classify(True),
        approve_fn=lambda action: True,
        submit_fn=submit_fn,
    )
    assert len(submit_fn.calls) == 1

    run(
        write_config(tmp_path, "02-ad-rotates.html"),
        state_path,
        memory_path,
        classify=const_classify(False),
        submit_fn=submit_fn,
    )
    assert len(submit_fn.calls) == 1  # unchanged

    run(
        write_config(tmp_path, "05-real-match.html"),
        state_path,
        memory_path,
        classify=raising_classify,  # must NOT be called -- memory short-circuits first
        approve_fn=lambda action: True,
        submit_fn=submit_fn,
    )
    assert len(submit_fn.calls) == 1  # still unchanged -- deduped


def test_evolved_variant_is_not_deduped_documented_limitation(tmp_path):
    """Case 11's harder half: memory keys on an exact snippet match, so
    a *slightly evolved* restatement of the same underlying opening
    (e.g. "1 spot claimed, 3 remaining" added to the same row) is NOT
    recognized as already-surfaced -- a real, documented limitation
    (see PROBLEM_STATEMENT.md / CHANGELOG.md), not a bug to silently fix
    here.
    """
    state_path = str(tmp_path / "state.txt")
    memory_path = str(tmp_path / "memory.json")
    submit_fn = Recorder()

    run(
        write_config(tmp_path, "11a-duplicate-match.html"),
        state_path,
        memory_path,
        classify=const_classify(True),
        approve_fn=lambda action: True,
        submit_fn=submit_fn,
    )
    assert len(submit_fn.calls) == 1

    run(
        write_config(tmp_path, "11b-duplicate-match-variant.html"),
        state_path,
        memory_path,
        classify=const_classify(True),
        approve_fn=lambda action: True,
        submit_fn=submit_fn,
    )
    assert len(submit_fn.calls) == 2  # NOT deduped -- documented limitation


# --- Case 12: the challenging flappy-slot case ------------------------------


def test_flappy_slot_is_declined_after_verification(tmp_path):
    """detect() sees the opening (12a); verify()'s fresh re-fetch sees it
    already claimed again (12b) and declines. Baseline would have fired
    on the initial read with no way to catch this -- see
    eval/CASES.md's design note on this case.
    """
    fetch_calls = {"n": 0}

    def fetch_fn(source):
        fetch_calls["n"] += 1
        return load("12a-flappy-open.html") if fetch_calls["n"] == 1 else load("12b-flappy-closed.html")

    def keyed_classify(watch_for, page_text):
        if "Slot available" in page_text:
            return True, "open"
        return False, "closed"

    submit_fn = Recorder()
    notifier = Recorder()

    run(
        write_config(tmp_path, "12a-flappy-open.html"),  # source value itself unused -- fetch_fn overridden
        str(tmp_path / "state.txt"),
        str(tmp_path / "memory.json"),
        fetch_fn=fetch_fn,
        classify=keyed_classify,
        notifier=notifier,
        approve_fn=lambda action: True,
        submit_fn=submit_fn,
    )

    assert fetch_calls["n"] == 2  # initial poll + verification re-fetch
    assert submit_fn.calls == []
    assert notifier.calls == []  # never got far enough to alert the human


# --- Case 14: auto_expire failsafe ------------------------------------------


def test_expired_watch_never_fetches(tmp_path):
    config_path = write_config(tmp_path, "05-real-match.html", auto_expire="2020-01-01T00:00:00")
    run(
        config_path,
        str(tmp_path / "state.txt"),
        str(tmp_path / "memory.json"),
        fetch_fn=raising_fetch,
        classify=raising_classify,
        now=datetime(2026, 1, 1),
    )
    # no assertion needed beyond "didn't raise" -- both fakes would have
    # failed the test if called


# --- Robustness --------------------------------------------------------------


def test_fetch_error_does_not_crash(tmp_path):
    config_path = write_config(tmp_path, "05-real-match.html")

    def failing_fetch(source):
        raise OSError("network down")

    run(
        config_path,
        str(tmp_path / "state.txt"),
        str(tmp_path / "memory.json"),
        fetch_fn=failing_fetch,
        classify=raising_classify,
    )


def test_run_creates_missing_parent_directories_for_state_and_memory(tmp_path):
    """--state/--memory paths whose parent directories don't exist yet
    must not crash -- the same class of bug as baseline's equivalent
    test: a POSIX-style path like /tmp/... resolves to a nonexistent
    directory on Windows PowerShell instead of the MSYS /tmp git-bash
    provides, and write_text()/WatcherMemory.save() don't create missing
    parent directories on their own.
    """
    config_path = write_config(tmp_path, "00-baseline.html")
    state_path = str(tmp_path / "fresh-state-dir" / "state.txt")
    memory_path = str(tmp_path / "fresh-memory-dir" / "memory.json")

    # A fresh state file means has_changed() is unconditionally True on
    # this first poll, so detect() -- and therefore classify() -- WILL
    # be called here, unlike the unchanged-page tests elsewhere in this
    # file; a non-match keeps the run short.
    run(config_path, state_path, memory_path, classify=const_classify(False))  # must not raise

    assert Path(state_path).exists()


# --- Case 15: adaptive polling around release_date, not auto_expire --------


def test_poll_interval_unchanged_when_release_date_unset():
    config = WatchConfig(source="x", watch_for="x", auto_expire=datetime(2099, 1, 1), poll_interval=timedelta(minutes=15))
    assert next_poll_interval(config, datetime(2026, 1, 1)) == timedelta(minutes=15)


def test_poll_interval_unchanged_when_far_from_release_date():
    config = WatchConfig(
        source="x", watch_for="x", auto_expire=datetime(2099, 1, 1),
        poll_interval=timedelta(minutes=15), release_date=datetime(2026, 6, 1),
    )
    far = datetime(2026, 1, 1)  # months away
    assert next_poll_interval(config, far) == timedelta(minutes=15)


def test_poll_interval_tightens_near_release_date():
    config = WatchConfig(
        source="x", watch_for="x", auto_expire=datetime(2099, 1, 1),
        poll_interval=timedelta(minutes=15), release_date=datetime(2026, 6, 1, 12, 0, 0),
    )
    near = datetime(2026, 6, 1, 11, 59, 0)  # one minute before release
    interval = next_poll_interval(config, near)
    assert interval < timedelta(minutes=15)
    assert interval >= timedelta(minutes=1)  # never below the floor


def test_poll_interval_monotonically_shrinks_as_release_date_nears():
    config = WatchConfig(
        source="x", watch_for="x", auto_expire=datetime(2099, 1, 1),
        poll_interval=timedelta(minutes=15), release_date=datetime(2026, 6, 1, 12, 0, 0),
    )
    farther = next_poll_interval(config, datetime(2026, 6, 1, 10, 0, 0))
    closer = next_poll_interval(config, datetime(2026, 6, 1, 11, 30, 0))
    assert closer <= farther


def test_poll_interval_reverts_after_release_date_passes():
    config = WatchConfig(
        source="x", watch_for="x", auto_expire=datetime(2099, 1, 1),
        poll_interval=timedelta(minutes=15), release_date=datetime(2026, 6, 1, 12, 0, 0),
    )
    after = datetime(2026, 6, 1, 12, 30, 0)
    assert next_poll_interval(config, after) == timedelta(minutes=15)


def test_poll_interval_ignores_auto_expire_entirely():
    """The whole point of the auto_expire/release_date split: identical
    release_date and poll_interval, wildly different auto_expire, must
    give identical results.
    """
    near_expiry = WatchConfig(
        source="x", watch_for="x", auto_expire=datetime(2026, 6, 1, 12, 1, 0),
        poll_interval=timedelta(minutes=15), release_date=datetime(2026, 6, 1, 12, 0, 0),
    )
    far_expiry = WatchConfig(
        source="x", watch_for="x", auto_expire=datetime(2099, 1, 1),
        poll_interval=timedelta(minutes=15), release_date=datetime(2026, 6, 1, 12, 0, 0),
    )
    now = datetime(2026, 5, 1)
    assert next_poll_interval(near_expiry, now) == next_poll_interval(far_expiry, now)
