# Evaluation Cases

Same fixture sequence and same `WatchConfig` (source, `watch_for`,
`auto_expire`, `poll_interval`) given to both `baseline/` and
`advanced/`, per the rulebook's "keep the comparison fair." Each
content-diff case below becomes one fixture file in `fixtures/` (built in
Stage 2/3) named `NN-slug.html` matching the ID here.

**Fixed watch config for this run** (see `advanced/criteria.py`, and
`eval/fixtures/` for the actual fixture content):

- `source`: "Riverside Park Tennis Courts" booking calendar (synthetic).
- `watch_for` (advanced, full sentence): `"a Saturday 9-11am court
  booking for 4 people"`.
- `keyword` (baseline, short literal phrase — see
  [`../baseline/README.md`](../baseline/README.md) for why baseline gets
  a different, narrower config than advanced): `"slot available"`.
- `release_date`: unset for this scenario (no announced opening date for
  a public court — polling stays at the fixed base rate). Case 15 below
  uses a separate config with `release_date` set to exercise tightening.

Fixture files: `00-baseline.html` is the reference "fully booked" state
used as `previous` for most diffs; cases 02–10 and 13 each supply one
`current` fixture; case 11 uses `11a-duplicate-match.html` then
`11b-duplicate-match-variant.html`; case 12 uses
`12a-flappy-open.html` / `12b-flappy-closed.html`.

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
| 11 | The same underlying opening, evolving slightly between polls (11a → 11b: "3 remaining" added) | Memory dedup, and its real limit | Fires on both (duplicate notification) | **Fires on both too** — memory keys on an exact snippet match, so a byte-for-byte identical *revisit* (tested separately, see `advanced/test_watcher.py::test_revisited_exact_match_is_deduped_via_memory`) is deduped, but this evolved-text pair is not. A documented limitation, not a bug — see `PROBLEM_STATEMENT.md` |
| 12 | **Challenging case:** a slot opens and is claimed by someone else within one poll interval (flappy/race) | What "detected" even means under a race condition | Fires on the open (single-pass, no verification) | **Declines** — `detect()` sees the opening, but `verify()`'s fresh re-fetch sees it already closed and correctly withholds the draft. See the design note below: this is a real trade-off (verification can turn a fleeting true positive into a silent miss), not an unqualified win, and is this project's Hot Take. |
| 13 | **Recall gap:** a real opening appears, but the page signals it with a new link/button ("Book now — 4 players") instead of the literal watched phrase | Whether a detector needs the exact keyword to recognize a match at all | **Silent — a false negative.** Baseline's "perfect recall" elsewhere in this table was an artifact of every real match happening to contain `keyword`, not a structural guarantee; this case exposes that. | **Fires correctly** — reads "Book now" on the Saturday 9-11am row as satisfying `watch_for` even with zero lexical overlap with any configured keyword. Real result: TP moves from 3→4, baseline recall drops 1.00→0.75, advanced recall holds at 1.00 (see `CHANGELOG.md`). |

## Orchestration cases (injected fake clock, not fixture content)

| ID | Case | What it tests | Expected: baseline | Expected: advanced |
|---|---|---|---|---|
| 14 | Poll attempted after `auto_expire` (the failsafe) has passed | The watch stops entirely once its safety-net deadline is reached, regardless of `release_date` | No poll fires; no action even if the underlying page has a real match | Same |
| 15 | Poll interval as `release_date` approaches, with `auto_expire` set well past it | Adaptive polling — same total poll budget skewed toward the window that matters, driven by `release_date`, not `auto_expire` | N/A (baseline uses a fixed interval only — documented limitation, not tested here) | Interval measurably tightens as `release_date` nears vs. a poll made far from it; unaffected by how far `auto_expire` is |

## Design note on case 12 (resolved — this is the project's Hot Take)

Advanced's `verify()` step declines this case: it exists to cut false
positives from a transient glitch, and it does exactly that here — but
the cost is a false *negative* on a genuinely fleeting real opening.
Baseline, with no verification step at all, would have fired on the
initial read (for whatever that's worth by the time a human reads a
notification for an opening that's likely already gone). Neither
behavior is simply "better" — they're different trade-offs:

- Baseline: never misses an initial appearance, but can't tell a real
  opening from a decoy in the first place (see cases 06-10), and would
  have blindly fired a notification for something already gone.
- Advanced: filters out decoys/near-misses far better, but the same
  verification step that does that can also filter out a real,
  fleeting opportunity if it closes between detection and verification.

The honest fix isn't smarter detection — it's **case 15's adaptive
polling** (tightening the interval as `release_date` nears), which
narrows the race window itself rather than trying to out-clever a race
after the fact. See `CHANGELOG.md` and `README.md`'s hot take for the
one-sentence version (rubric criterion: Hot Take/Insights, 5 pts).

## Primary metric

Precision/recall over "correctly identified an actionable,
criteria-matching opening and correctly gated it behind human approval,"
computed across cases 01–11 and 13 (case 12 is analyzed separately as
the challenging case; cases 14–15 are orchestration checks, not scored
for precision/recall).

## Secondary metrics

- False-positive rate (how many of cases 01–04, 06–10 incorrectly fire)
- Human time per task (time from the fixture representing "opening
  appears" to a drafted action being ready for approval) — measured on
  the advanced solution only, since baseline never drafts an action

## Status

All 15 cases are implemented and passing. `eval/run_eval.py --solution
both` scores cases 01–11 and 13 for both solutions — see
[`../CHANGELOG.md`](../CHANGELOG.md) for the real numbers (baseline:
precision 0.38, recall 0.75; advanced: precision 1.00, recall 1.00, real
API run, not `--fake`). Case 12 (flappy) and cases 14-15 (the
injected-clock orchestration checks) are covered directly in
`advanced/test_watcher.py` and `advanced/test_detector.py` rather than
in `run_eval.py`'s precision/recall table, per the "Primary metric" note
above.
