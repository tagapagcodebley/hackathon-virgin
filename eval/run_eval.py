"""Runs baseline (and, from Stage 3, advanced) against the fixture cases
in fixtures/ (per CASES.md) and prints a comparison in the format the
rulebook suggests (metric | simple baseline | agent solution | change).

Stage 2: baseline scoring is real. Advanced scoring is a Stage 3 TODO —
run with --solution baseline until then.
"""

from __future__ import annotations

import argparse
from pathlib import Path

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


def load(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def score_baseline() -> dict:
    """Run baseline/watcher.py's detection logic against each case and
    score against the ground-truth label.
    """
    rows = []
    tp = fp = tn = fn = 0
    for case_id, prev_name, curr_name, ground_truth in CASES:
        previous = load(prev_name)
        current = load(curr_name)
        predicted = has_changed(previous, current) and matches_watch_for(current)
        rows.append((case_id, ground_truth, predicted))
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
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solution", choices=["baseline", "advanced", "both"], default="baseline")
    args = parser.parse_args()

    if args.solution in ("baseline", "both"):
        print_report("Baseline (keyword-diff)", score_baseline())

    if args.solution in ("advanced", "both"):
        print("=== Advanced (semantic) ===")
        print("  Not implemented yet — lands in Stage 3.\n")


if __name__ == "__main__":
    main()
