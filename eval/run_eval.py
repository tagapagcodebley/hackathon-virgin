"""Runs baseline and/or advanced against the fixture sequence in
fixtures/ (per CASES.md) and prints the comparison table in the format
the rulebook suggests (metric | simple baseline | agent solution | change).

Stage 1 scaffolding only. Real implementation lands alongside each
solution: baseline scoring in Stage 2, advanced scoring in Stage 3.
"""

from __future__ import annotations

import argparse


def load_cases(cases_dir: str) -> list:
    """TODO: load each fixture + its expected outcome from CASES.md/fixtures/."""
    raise NotImplementedError


def score_baseline(cases: list) -> dict:
    """TODO: run baseline/watcher.py's functions against each case, score
    against expected outcome.
    """
    raise NotImplementedError


def score_advanced(cases: list) -> dict:
    """TODO: run advanced/watcher.py's pipeline against each case, score
    against expected outcome.
    """
    raise NotImplementedError


def print_comparison(baseline_scores: dict, advanced_scores: dict) -> None:
    """TODO: print the metric / simple baseline / agent solution / change table."""
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solution", choices=["baseline", "advanced", "both"], default="both")
    parser.parse_args()
    raise NotImplementedError("eval runner not yet implemented — Stage 1 placeholder")


if __name__ == "__main__":
    main()
