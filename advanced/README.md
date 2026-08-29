# Advanced Solution — Sauron

A meaningful improvement over the baseline — in capability, reliability, efficiency, coverage, or engineering quality. Not a cosmetic variation.

See [`PROBLEM_STATEMENT.md`](../PROBLEM_STATEMENT.md) for the full framing, including the "Prior art" section this is meant to beat and the "On automated holds" decision this design follows.

## Approach

An LLM-agent pipeline built from six pieces. Semantic judgment is a real
[Anthropic API](https://docs.anthropic.com/) call (`claude-haiku-4-5`,
tool-use for structured output — see `detector.py`'s `_classify_via_llm`)
— injectable everywhere it's used, so tests and `eval/run_eval.py --fake`
never touch the network or cost anything, while the real, default eval
and deployment paths do (see `../docs/REPRODUCTION.md`'s "Approx cost").

| Module | Role |
|---|---|
| [`criteria.py`](criteria.py) | `WatchConfig` — source, plain-language `watch_for`, `release_date` (drives urgency), `auto_expire` (failsafe unregister, decoupled from timing), `poll_interval` — the **context** given to the agent on every poll. Generic across watch domains, not booking-specific. |
| [`memory.py`](memory.py) | Tracks prior page states, previously-seen decoy patterns, and already-surfaced matches, so known noise and duplicate detections stop across polls. |
| [`detector.py`](detector.py) | Agent call that semantically judges whether the new page state is a real, criteria-matching opening (catching negation and near-miss cases the baseline can't) — plus a **verification** re-pass before treating a detection as real. |
| [`action_drafter.py`](action_drafter.py) | On a confirmed match, drafts the structured next step (a reservation request, for the demo scenario). |
| [`approval.py`](approval.py) | Holds the drafted action for explicit **human approval** before a *simulated* submit call — never a real booking endpoint (rulebook ground rule 04; see PROBLEM_STATEMENT.md's "On automated holds"). |
| [`watcher.py`](watcher.py) | Orchestrates the above into the poll loop — stops entirely once `auto_expire` (failsafe) passes, and tightens the poll interval as `release_date` (urgency) approaches. Two distinct dates, not one. |

## What's different from baseline, and why

Baseline can only tell *that* the page changed and whether a keyword
substring is present — it can't tell a negation from a match, or a real
opening from a criteria near-miss. This adds: full `watch_for` context
(semantic judgment, not substring matching), memory (known decoys and
already-surfaced matches stop causing repeat noise), a verification pass
(fewer false positives from a transient glitch), drafting the actual next
step instead of stopping at a notification, a hard stop once `auto_expire`
(the failsafe) passes so a forgotten watcher doesn't run forever, and
adaptive polling that tightens the interval as `release_date` (a
separate, optional field — the user's guess at *when* the thing will
happen, not when to give up) nears — while keeping the one consequential
action (the submit) behind a live human approval gate.

## Measured improvement

Real run (`python -m eval.run_eval --solution advanced`, real Anthropic
`claude-haiku-4-5` calls — see [`../CHANGELOG.md`](../CHANGELOG.md) for
the full entry):

```
TP=3  FP=0  TN=9  FN=0
Precision:            1.00
Recall:               1.00
False-positive rate:  0.00
```

vs. baseline's precision 0.38 / recall 1.00 / false-positive rate 0.56
on the same 12 cases. Perfect classification, including every case
baseline gets wrong: negation, all three criteria near-misses, and the
ambiguous FAQ mention.

## Status

Implemented (Stage 3) and verified with a real API run — not just
`--fake`. 70/70 tests pass (`python -m pytest advanced/ baseline/
test_notifications.py -v`), the unit tests all against injected fakes
(no network, no API key, no cost) and the real CLI additionally run live
end-to-end: config loading, fixture fetch, real semantic detection +
verification, a drafted action with genuine LLM reasoning, and the
interactive approval prompt (confirmed both declining safely on
non-interactive/EOF stdin and completing the approve → simulated-submit
→ log-write path). See [`../docs/REPRODUCTION.md`](../docs/REPRODUCTION.md)
for exact commands.
