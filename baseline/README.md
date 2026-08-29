# Baseline Solution — Sauron

The simplest correct solution to the problem — no cleverness, just correctness. This is the comparison point for the advanced solution.

See [`PROBLEM_STATEMENT.md`](../PROBLEM_STATEMENT.md) for the full framing.

## Approach

A keyword-diff script (the same approach most existing page-watch tools
use — see PROBLEM_STATEMENT.md's "Prior art" section): fetch the page,
diff it against the last-seen snapshot, and fire a plain notification if
the new text contains a short literal `keyword` (default: `"slot
available"`). No semantic judgment, no criteria disambiguation, no
drafted action, no expiry or adaptive polling — fixed interval only.

`keyword` is deliberately a *separate, narrower* input than advanced's
`watch_for`. A real keyword-watch tool is configured with a short phrase
you type in (like "in stock" or "slots available"), not a full sentence
like "a Saturday 9-11am court booking for 4 people" — that sentence would
almost never appear verbatim on a real page. Advanced gets the full
sentence and reasons over it with an LLM; baseline only ever sees the
short phrase, which is exactly why it can't disambiguate criteria — it
was never given the criteria to begin with.

## What it does and doesn't handle

- Handles: reliably detects *that* the page text changed and whether the
  diff contains `keyword`; never crashes on a fetch error; can notify for
  real (email) and run unattended (see "Deployment" below).
- Does **not** handle: negation ("no slots available" contains the same
  substring as a real match — its sharpest documented failure); telling
  a real opening apart from one that doesn't match the user's full
  criteria (date/time/party size); doing anything with a confirmed match
  besides notifying — no drafted action, no approval gate, no memory
  (repeats the same alert every poll); no auto-expire or adaptive
  polling.

## Deployment (making it a real, unattended tool)

`run()` notifies via an injectable channel — `notifications.console_notify`
by default (safe, used by tests/eval), or `notifications.email_notify`
for real delivery via Gmail SMTP. Combined with
[`../deploy/`](../deploy/)'s scripts (a poll wrapper + a Windows
Scheduled Task registration), this *is* a deployable standalone tool,
not just an eval harness — see [`../deploy/README.md`](../deploy/README.md)
for the one-off-run, real-email, and run-forever-unattended instructions.

Registered as a Scheduled Task, baseline's poll runs with a plain,
visible console window flashing on-screen every cycle — functional, if a
little annoying, and an honest reflection of "simplest correct solution,
no cleverness." Advanced's task runs silently instead; see
[`../advanced/deploy/README.md`](../advanced/deploy/README.md) for why
that's counted as one of advanced's own improvements, not shared here.

## Known limitations (measured, not hidden)

`python -m eval.run_eval --solution baseline` against the 12
content-diff cases in [`../eval/CASES.md`](../eval/CASES.md):

```
TP=3  FP=5  TN=4  FN=0
Precision:            0.38
Recall:               1.00
False-positive rate:  0.56
```

Recall is perfect — baseline never misses a real opening. Precision is
poor — it misclassifies negation, all three criteria near-misses, and
the unrelated FAQ mention as real matches. See
[`../CHANGELOG.md`](../CHANGELOG.md) for the full entry.

## Status

Implemented (Stage 2). 18/18 tests pass
(`python -m pytest baseline/ test_notifications.py -v`). See
[`../docs/REPRODUCTION.md`](../docs/REPRODUCTION.md) for exact commands.
