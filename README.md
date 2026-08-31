# Sauron

> The eye that watches so you don't have to. Solo submission for the
> [micro1 Frontier Engineering Challenge 2026](https://www.hackerearth.com/community/challenges/hackathon/micro1-frontier-engineering-challenge-2026/).

**Status:** ✅ Stage 3 (Advanced) complete and measured for real — both
solutions implemented and passing (75/75 tests across the repo), both
deployable standalone (real email/console notifications + Windows
Scheduled Task — see [`deploy/README.md`](deploy/README.md)). Baseline:
precision 0.38 / recall 0.75 / false-positive rate 0.56. **Advanced
(real Anthropic API, not a stub): precision 1.00 / recall 1.00 /
false-positive rate 0.00** — perfect on all 13 cases, including every
one baseline gets wrong on precision *and* the one it misses outright
(a real opening signaled without the literal keyword). See
[`CHANGELOG.md`](CHANGELOG.md) for the full story. Full process log:
[`trajectories/session-trajectory.md`](trajectories/session-trajectory.md).
Full problem framing: [`PROBLEM_STATEMENT.md`](PROBLEM_STATEMENT.md).

## The problem

Point Sauron at a page, tell it in plain language what you're watching
for, say how long to watch and how often to check — it drafts your next
move the moment a real match shows up, then waits for you to approve it.

- **Who is the intended user?** Someone trying to grab a rare,
  unpredictably-released reservation slot on a booking portal that offers
  no alert feature of its own — a public tennis court, a DMV/visa
  appointment, a campsite permit. Demoed against a synthetic tennis-court
  reservation portal; the config (source page, `watch_for`, `auto_expire`,
  `poll_interval`) is generic, not booking-specific.
- **What is their current bottleneck?** They can't watch the page 24/7.
  Existing page-watch tools (changedetection.io, Distill.io, Visualping,
  and others — see [`PROBLEM_STATEMENT.md`](PROBLEM_STATEMENT.md)'s
  "Prior art" section) only do keyword/CSS-diff matching: they can't tell
  a negation ("no slots available" contains the same substring as a real
  match) from a real opening, can't tell a match against the user's full
  criteria from a near-miss, and even on a correct hit, only notify —
  the user still reads, judges, and fills out the form by hand, under
  time pressure.
- **Why does solving it matter?** It collapses the time between "a
  matching opening appears" and "a drafted next step is ready for
  one-tap approval" from human-reaction-time down to seconds, without
  ever letting an agent take a consequential action (like placing a hold)
  on its own — see PROBLEM_STATEMENT.md's "On automated holds."

## Solutions

This repo contains two solutions, per the competition rules:

| | Path | Description |
|---|---|---|
| **Baseline** | [`baseline/`](baseline/) | Simplest correct solution to the problem. |
| **Advanced** | [`advanced/`](advanced/) | Meaningful improvement over baseline — in capability, reliability, efficiency, coverage, or engineering quality. |

## Agent disclosure

- **Agent(s) used:** Claude Code, to build and test this entire repo (this README included).
- **Model(s) used:** `claude-sonnet-5` (Claude Code, building this repo); `claude-haiku-4-5` (Sauron's own detector — the agent Sauron *is*, not the agent that built it, see `advanced/detector.py`).
- Trajectories for every agent used are in [`trajectories/`](trajectories/) — see that folder's README for how to read them.

## Quickstart

See [`docs/REPRODUCTION.md`](docs/REPRODUCTION.md) for full setup and run instructions from a clean environment.

```bash
pip install -r baseline/requirements.txt
pip install -r advanced/requirements.txt
python -m pytest baseline/ advanced/ test_notifications.py -v
python -m eval.run_eval --solution both               # needs ANTHROPIC_API_KEY for advanced's real numbers
python -m eval.run_eval --solution advanced --fake     # $0 pipeline sanity check instead, if you don't have a key handy
```

## Measured improvement

Same 13 cases, same `watch_for`, both solutions given identical fixture
input — `python -m eval.run_eval --solution both` (real Anthropic API
for advanced, not `--fake`; see [`CHANGELOG.md`](CHANGELOG.md) for the
full run and sample model reasoning):

| Metric | Simple baseline | Agent solution | Change |
|---|---|---|---|
| Precision | 0.38 | 1.00 | **+0.62** |
| Recall | 0.75 | 1.00 | **+0.25** |
| False-positive rate | 0.56 | 0.00 | **−0.56** |
| Human action per detected match | Read a bare "page changed" alert → re-check the page yourself → judge whether it actually matches → fill out the booking form | Read a pre-drafted, pre-verified match with cited reasoning → tap approve | Qualitative, not stopwatch-timed: "read and judge from scratch" vs. "confirm a draft" |
| Cost per poll | $0 | ~$0.0001–0.0005 (1–2 `claude-haiku-4-5` calls) | +a fraction of a cent |

Two distinct wins here, not one. On five of eight non-matches, baseline
fires when it shouldn't (negation, three criteria near-misses, an FAQ
mention) — that's the precision column. But baseline also *misses* a
genuine opening outright when the page signals it without the exact
configured keyword: a "Book now" link appearing instead of the word
"available" still means a real match, and a substring check has no way
to see it. Advanced doesn't just filter noise better — it recognizes
openings baseline is structurally blind to, holding recall at 1.00
while baseline's drops to 0.75 on that one case alone.

## Improvement changelog

See [`CHANGELOG.md`](CHANGELOG.md) for the full iteration history with evidence links.

## Demo video

*https://1drv.ms/v/c/1697629eee313eb4/IQBR5gYLrAU7R7-0v64hA4xtAQPKGA-NR5h0wwvMOW2Y20M?e=hOP66x*

## Main failure mode & hot take

**Main failure mode:** the flappy-slot race (`eval/CASES.md` case 12).
Advanced's verification step — added specifically to cut false
positives from a transient glitch — correctly declines to draft an
action when the opening closes between the initial detection and the
re-fetch. That's the intended behavior, but it means a genuinely
fleeting real opportunity gets silently missed, not just flagged with
lower confidence. Baseline, with no verification step at all, would
have fired a notification on the initial read for whatever that's worth
by the time a human reads it.

**Hot take:** verification is a trade, not a strict improvement —
turning false positives into false negatives on anything that's racing
against real time. The fix for a race isn't smarter detection, it's
tighter polling near the moment that actually matters (`release_date`-driven
adaptive polling, see `advanced/watcher.py`'s `next_poll_interval()`),
because no amount of reasoning about a page state can out-run how often
you actually looked at it.

## Future work (out of scope for this submission)

- **Browser extension front-end.** Point-and-click element selection and
  free access to logged-in pages are real advantages of the
  Distill.io/Wachete model — but a Manifest V3 extension is a lot of
  install/permission overhead for a judge reproducing the main result
  from a clean environment, so this submission stays a CLI/service. See
  [`PROBLEM_STATEMENT.md`](PROBLEM_STATEMENT.md) for the full reasoning.
- **Live-site holds.** Always out of scope here — see
  PROBLEM_STATEMENT.md's "On automated holds."
