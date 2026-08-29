"""Runs baseline and advanced against the fixture cases in fixtures/
(per CASES.md) and prints a comparison in the format the rulebook
suggests (metric | simple baseline | agent solution | change).

Advanced scoring calls the real Anthropic API by default (see
advanced/detector.py's _classify_via_llm) -- needs ANTHROPIC_API_KEY and
costs a small amount per run, same as running advanced/watcher.py for
real (see docs/REPRODUCTION.md's "Approx cost"). Pass --fake for a
zero-cost sanity check of the *pipeline* (memory, verification,
orchestration) against a stubbed, hand-written classifier -- that mode
proves the plumbing is correct, not that the real model's judgment is
good; don't quote its numbers as the measured result.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from advanced.criteria import WatchConfig
from advanced.detector import detect, verify
from advanced.memory import WatcherMemory
from baseline.watcher import has_changed, matches_watch_for

FIXTURES = Path(__file__).parent / "fixtures"

# (case_id, previous_fixture, current_fixture, ground_truth_is_actionable_match)
# Cases 12-14 are excluded here — 12 (the challenging flappy case) and
# 13-14 (clock-based orchestration cases) aren't meaningful for a
# precision/recall pass over content detection; see eval/CASES.md.
CASES = [
    ("01-steady", "00-baseline.html", "00-baseline.html", False),
    ("02-ad-rotates", "00-baseline.html", "02-ad-rotates.html", False),
    ("03-timestamp-changes", "00-baseline.html", "03-timestamp-changes.html", False),
    ("04-unrelated-copy", "00-baseline.html", "04-unrelated-copy.html", False),
    ("05-real-match", "00-baseline.html", "05-real-match.html", True),
    ("06-negation", "00-baseline.html", "06-negation.html", False),
    ("07-wrong-date", "00-baseline.html", "07-wrong-date.html", False),
    ("08-wrong-time", "00-baseline.html", "08-wrong-time.html", False),
    ("09-wrong-party-size", "00-baseline.html", "09-wrong-party-size.html", False),
    ("10-ambiguous-faq", "00-baseline.html", "10-ambiguous-faq.html", False),
    ("11a-duplicate", "00-baseline.html", "11a-duplicate-match.html", True),
    (
        "11b-duplicate-variant",
        "11a-duplicate-match.html",
        "11b-duplicate-match-variant.html",
        True,
    ),
]

WATCH_FOR = "a Saturday 9-11am court booking for 4 people"


def load(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def _confusion_matrix(rows: list) -> dict:
    tp = fp = tn = fn = 0
    for _case_id, ground_truth, predicted in rows:
        if predicted and ground_truth:
            tp += 1
        elif predicted and not ground_truth:
            fp += 1
        elif not predicted and ground_truth:
            fn += 1
        else:
            tn += 1
    precision = tp / (tp + fp) if (tp + fp) else float("nan")
    recall = tp / (tp + fn) if (tp + fn) else float("nan")
    false_positive_rate = fp / (fp + tn) if (fp + tn) else float("nan")
    return {
        "rows": rows,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "false_positive_rate": false_positive_rate,
    }


def score_baseline() -> dict:
    """Run baseline/watcher.py's detection logic against each case and
    score against the ground-truth label.
    """
    rows = []
    for case_id, prev_name, curr_name, ground_truth in CASES:
        previous = load(prev_name)
        current = load(curr_name)
        predicted = has_changed(previous, current) and matches_watch_for(current)
        rows.append((case_id, ground_truth, predicted))
    return _confusion_matrix(rows)


def _stubbed_perfect_classify(watch_for: str, page_text: str) -> "tuple[bool, str]":
    """A hand-written stand-in classifier for --fake runs -- NOT the
    real agent. Exists to verify the pipeline (memory short-circuiting,
    verification, orchestration) behaves correctly when given a good
    classification, without spending money or requiring an API key.
    Real semantic judgment is only exercised by the default (non--fake)
    path, which calls advanced/detector.py's real Anthropic-backed
    classifier.
    """
    negation = re.search(r"\bno\b[^.]{0,20}slot available", page_text, re.IGNORECASE)
    if negation:
        return False, "[fake] explicit negation near the match phrase"

    if "slot available" not in page_text.lower():
        return False, "[fake] no match phrase present"

    has_day = "Saturday" in page_text
    has_time = "9:00-11:00 AM" in page_text
    has_party = "4 players" in page_text
    if has_day and has_time and has_party:
        return True, "[fake] matches day, time, and party size"
    return False, "[fake] match phrase present but criteria (day/time/party size) don't all match"


def score_advanced(classify) -> dict:
    """Run advanced's detect()+verify() pipeline against each case and
    score against the same ground-truth labels as score_baseline(), for
    an apples-to-apples comparison. Each case gets a fresh, ephemeral
    WatcherMemory (never persisted) so memory dedup doesn't skew one
    case's score based on another's -- matching score_baseline()'s
    independent-row scoring.
    """
    config = WatchConfig(
        source="unused-in-eval",  # verify()'s fetch_fn below ignores this
        watch_for=WATCH_FOR,
        auto_expire=datetime(2099, 1, 1),
    )
    rows = []
    api_calls = 0

    def counting_classify(watch_for: str, page_text: str):
        nonlocal api_calls
        api_calls += 1
        return classify(watch_for, page_text)

    for case_id, prev_name, curr_name, ground_truth in CASES:
        previous = load(prev_name)
        current = load(curr_name)
        memory = WatcherMemory("__ephemeral__.json")  # never saved -- fresh per case

        detection = detect(previous, current, config, memory, classify=counting_classify)
        if detection.is_match:
            detection = verify(detection, config, fetch_fn=lambda source, _t=current: _t, classify=counting_classify)

        rows.append((case_id, ground_truth, detection.is_match))

    result = _confusion_matrix(rows)
    result["classify_calls"] = api_calls
    return result


def print_report(name: str, scores: dict) -> None:
    print(f"=== {name} ===")
    for case_id, ground_truth, predicted in scores["rows"]:
        mark = "match" if ground_truth == predicted else "MISCLASSIFIED (documented limitation)"
        print(f"  {case_id:24s} ground_truth={str(ground_truth):5s} predicted={str(predicted):5s}  {mark}")
    print()
    print(f"  TP={scores['tp']}  FP={scores['fp']}  TN={scores['tn']}  FN={scores['fn']}")
    print(f"  Precision:            {scores['precision']:.2f}")
    print(f"  Recall:               {scores['recall']:.2f}")
    print(f"  False-positive rate:  {scores['false_positive_rate']:.2f}")
    if "classify_calls" in scores:
        print(f"  classify() calls:     {scores['classify_calls']} (~2 per confirmed match: detect + verify)")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solution", choices=["baseline", "advanced", "both"], default="baseline")
    parser.add_argument(
        "--fake",
        action="store_true",
        help="Score advanced with a stubbed classifier instead of the real, paid Anthropic API call.",
    )
    args = parser.parse_args()

    if args.solution in ("baseline", "both"):
        print_report("Baseline (keyword-diff)", score_baseline())

    if args.solution in ("advanced", "both"):
        if args.fake:
            print("(--fake: pipeline sanity check with a stubbed classifier, NOT the real measured result)")
            print_report("Advanced (semantic, --fake)", score_advanced(_stubbed_perfect_classify))
        else:
            from advanced.detector import _classify_via_llm

            try:
                print_report("Advanced (semantic, real Anthropic API)", score_advanced(_classify_via_llm))
            except RuntimeError as exc:
                print(f"[Sauron eval] {exc}")
                print("[Sauron eval] Or pass --fake for a zero-cost pipeline sanity check instead.")
                raise SystemExit(1)


if __name__ == "__main__":
    main()
