# Advanced Solution — Sauron

A meaningful improvement over the baseline — in capability, reliability, efficiency, coverage, or engineering quality. Not a cosmetic variation.

See [`PROBLEM_STATEMENT.md`](../PROBLEM_STATEMENT.md) for the full framing, including the "Prior art" section this is meant to beat and the "On automated holds" decision this design follows.

## Approach

An LLM-agent pipeline built from five pieces:

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

TODO — filled in Stage 3/4 once both solutions run against
[`../eval/CASES.md`](../eval/CASES.md), with the comparison table and
links to the relevant [`../CHANGELOG.md`](../CHANGELOG.md) entries.

## Status

TODO — placeholder only, Stage 1 (scaffolding). Implementation lands in
Stage 3.
