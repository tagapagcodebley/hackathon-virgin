# Baseline Solution — Sauron

The simplest correct solution to the problem — no cleverness, just correctness. This is the comparison point for the advanced solution.

See [`PROBLEM_STATEMENT.md`](../PROBLEM_STATEMENT.md) for the full framing.

## Approach

A keyword-diff script (the same approach most existing page-watch tools
use — see PROBLEM_STATEMENT.md's "Prior art" section): fetch the page,
diff it against the last-seen snapshot, and fire a plain notification if
the new text contains a substring from `watch_for`. No semantic
judgment, no criteria disambiguation, no drafted action, no expiry or
adaptive polling — fixed interval only.

## What it does and doesn't handle

- Handles: reliably detects *that* the page text changed and whether the
  diff contains the watch_for keyword(s); never crashes on a fetch error.
- Does **not** handle: negation ("no slots available" contains the same
  substring as a real match — its sharpest documented failure); telling
  a real opening apart from one that doesn't match the user's full
  criteria (date/time/party size); doing anything with a confirmed match
  besides notifying — no drafted action, no approval gate, no memory
  (repeats the same alert every poll); no auto-expire or adaptive
  polling.

## Known limitations (expected failures)

Expected to visibly fail the negation, criteria-mismatch, and duplicate
cases in [`../eval/CASES.md`](../eval/CASES.md) — documented, not hidden
or worked around, per the competition rules.

## Status

TODO — placeholder only, Stage 1 (scaffolding). Implementation lands in
Stage 2.
