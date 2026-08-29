# Sauron

> The eye that watches so you don't have to. Solo submission for the
> [micro1 Frontier Engineering Challenge 2026](https://www.hackerearth.com/community/challenges/hackathon/micro1-frontier-engineering-challenge-2026/).

**Status:** 🚧 Stage 2 (Baseline) — baseline implemented and passing
(18/18 tests; precision 0.38 / recall 1.00 / false-positive rate 0.56 —
see [`CHANGELOG.md`](CHANGELOG.md)), and deployable standalone (real
email notifications + Windows Scheduled Task — see
[`deploy/README.md`](deploy/README.md)). Advanced solution not started
yet. Full process log: [`trajectories/session-trajectory.md`](trajectories/session-trajectory.md).
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

- **Agent(s) used:** *(e.g. Claude Code, Cursor, ...)*
- **Model(s) used:** *(e.g. claude-sonnet-5)*
- Trajectories for every agent used are in [`trajectories/`](trajectories/) — see that folder's README for how to read them.

## Quickstart

See [`docs/REPRODUCTION.md`](docs/REPRODUCTION.md) for full setup and run instructions from a clean environment.

```bash
pip install -r baseline/requirements.txt
python -m pytest baseline/ test_notifications.py -v
python -m eval.run_eval --solution baseline
```

## Improvement changelog

See [`CHANGELOG.md`](CHANGELOG.md) for the full iteration history with evidence links.

## Demo video

*(Link to the ≤5 minute solution video once recorded.)*

## Main failure mode & hot take

*(Fill in at the end: what breaks, and your one-sentence opinionated takeaway.)*

## Future work (out of scope for this submission)

- **Browser extension front-end.** Point-and-click element selection and
  free access to logged-in pages are real advantages of the
  Distill.io/Wachete model — but a Manifest V3 extension is a lot of
  install/permission overhead for a judge reproducing the main result
  from a clean environment, so this submission stays a CLI/service. See
  [`PROBLEM_STATEMENT.md`](PROBLEM_STATEMENT.md) for the full reasoning.
- **Live-site holds.** Always out of scope here — see
  PROBLEM_STATEMENT.md's "On automated holds."
