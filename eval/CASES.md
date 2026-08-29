# Evaluation Cases

Same fixture sequence and same `WatchConfig` (source, `watch_for`,
`auto_expire`, `poll_interval`) given to both `baseline/` and
`advanced/`, per the rulebook's "keep the comparison fair." Each
content-diff case below becomes one fixture file in `fixtures/` (built in
Stage 2/3) named `NN-slug.html` matching the ID here.

**Fixed watch config for this run** (see `advanced/criteria.py`): TODO —
a concrete `watch_for` string and matching fixture content, defined once
fixtures are written so config and fixtures agree. Sketch:
`watch_for: "a Saturday 9-11am court booking for 4 people"`,
`release_date` unset (no announced opening date for a public court —
polling stays at the fixed base rate for this scenario; case 14 below
uses a separate config with `release_date` set to exercise tightening).

## Content-diff cases (fixture-based)

| ID | Case | What it tests | Expected: baseline (keyword-diff) | Expected: advanced (semantic) |
|---|---|---|---|---|
| 01 | Steady fully-booked state, repeated across polls | No spurious detections on a stable page | No notification | No detection |
| 02 | Ad banner rotates | Decoy resistance (no keyword overlap) | No notification | No detection |
| 03 | "Last updated" timestamp changes | Decoy resistance | No notification | No detection |
| 04 | Unrelated copy edit (e.g. a footer link changes) | Decoy resistance | No notification | No detection |
| 05 | Real opening, matches `watch_for` exactly | The core win condition | Fires (keyword match), no drafted action | Detects, drafts action, holds for approval |
| 06 | **Negation:** page text changes to "no Saturday slots available" | Baseline's sharpest failure — substring match can't see negation | **Fires (false positive)** | No detection |
| 07 | Real opening, wrong date (keyword phrase present, date differs) | Criteria disambiguation, not just keyword presence | **Fires (false positive re: usefulness)** | No action (near-miss, not a match) |
| 08 | Real opening, wrong time window | Criteria disambiguation | **Fires** | No action |
| 09 | Real opening, wrong party size | Criteria disambiguation | **Fires** | No action |
| 10 | `watch_for` phrase appears in unrelated static FAQ copy, added as part of an unrelated page update | Semantic context vs. keyword presence | **Fires (false positive)** | No detection |
| 11 | Same real opening (case 05) seen on two consecutive polls | Memory / no duplicate action | Fires twice (duplicate notification) | Detects once, does not re-draft on poll 2 |
| 12 | **Challenging case:** a slot opens and is claimed by someone else within one poll interval (flappy/race) | What "detected" even means under a race condition | Fires on the open, then fires again on the close (two contradictory notifications) | TODO — decide and document the intended behavior; expected to reveal a real design gap (see note below), not just pass |

## Orchestration cases (injected fake clock, not fixture content)

| ID | Case | What it tests | Expected: baseline | Expected: advanced |
|---|---|---|---|---|
| 13 | Poll attempted after `auto_expire` (the failsafe) has passed | The watch stops entirely once its safety-net deadline is reached, regardless of `release_date` | No poll fires; no action even if the underlying page has a real match | Same |
| 14 | Poll interval as `release_date` approaches, with `auto_expire` set well past it | Adaptive polling — same total poll budget skewed toward the window that matters, driven by `release_date`, not `auto_expire` | N/A (baseline uses a fixed interval only — documented limitation, not tested here) | Interval measurably tightens as `release_date` nears vs. a poll made far from it; unaffected by how far `auto_expire` is |

## Design note on case 12

The flappy-slot case is deliberately left open in this table. It's
plausible that no purely reactive polling design can fully solve a race
condition faster than the poll interval itself — the honest fix may be
that **case 14's adaptive polling** (tightening the interval as
`release_date` nears) is what actually narrows the race window, not
smarter detection. Document whatever the eval reveals here as the
project's Hot Take (rubric criterion: Hot Take/Insights, 5 pts) rather
than forcing a false "solved" claim.

## Primary metric

Precision/recall over "correctly identified an actionable,
criteria-matching opening and correctly gated it behind human approval,"
computed across cases 01–11 (case 12 is analyzed separately as the
challenging case; cases 13–14 are orchestration checks, not scored for
precision/recall).

## Secondary metrics

- False-positive rate (how many of cases 01–04, 06–10 incorrectly fire)
- Human time per task (time from the fixture representing "opening
  appears" to a drafted action being ready for approval) — measured on
  the advanced solution only, since baseline never drafts an action

## Status

TODO — this is the Stage 1 case list/spec. Fixture files and `run_eval.py`
scoring land in Stage 2 (baseline scoring) and Stage 3 (advanced scoring,
plus the injected-clock harness for cases 13–14).
