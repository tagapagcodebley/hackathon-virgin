# CLAUDE.md

Guidance for Claude Code when working in this repo.

## What this repo is

A solo submission for the [micro1 Frontier Engineering Challenge 2026](https://www.hackerearth.com/community/challenges/hackathon/micro1-frontier-engineering-challenge-2026/).
The real problem statement is unknown until kickoff — both the pre-event
orientation and kickoff happen at **1AM in the user's local time**.

Submission format (per the actual rulebook): for the challenge problem,
build **two solutions** —

- `baseline/` — the simplest solution that's correct on the core
  requirement. It's fine, and expected, for it to visibly fail a secondary
  requirement — document that failure, don't hide or work around it.
- `advanced/` — a meaningful improvement over baseline (capability,
  reliability, efficiency, coverage, or engineering quality), passing all
  acceptance tests.

Plus: an evidence-linked `CHANGELOG.md` (each entry cites the failing
test/eval that motivated it), `docs/REPRODUCTION.md` for a clean-environment
setup, agent trajectories, and a ≤5 min demo video.

## Working process: stage-gated

Every activity in this repo (a practice run, the real submission, or any
standalone tool built along the way) is built in four stages, and **each
stage ends with an explicit checkpoint — stop and ask the user to validate
before starting the next stage.** Don't self-advance even when the next
step seems obvious.

1. **Stage 1 — Scaffolding.** Create all files/folders for the activity
   with TODOs or placeholder inserts only. No real implementation.
2. **Stage 2 — Basic/baseline solution.** Implement the simplest correct
   solution.
3. **Stage 3 — Advanced solution.** Implement the meaningful improvement
   over baseline.
4. **Stage 4 — Finalize.** Fill in remaining deliverables (changelog, demo
   video/notes, README claims, final polish) against the rubric.

## Trajectory recording

Keep **one running trajectory file per activity**, not the numbered
per-step files described in `trajectories/README.md` — delineate sections
by stage-gate header instead (`## Stage 1 — Scaffolding`, `## Stage 2 —
Basic solution`, etc). The file must:

- Include **verbatim user inputs** at each step, not paraphrases.
- Record what the agent did, the tool responses/evidence (command output,
  test results), and an explicit human-checkpoint note per stage.
- Be updated as the work happens, not reconstructed after the fact.

## Practice runs

`practice/`, `practice2/`, and any future `practiceN/` folders are
gitignored dry runs used to rehearse this workflow (and, sometimes, to
build genuinely useful side tools) — they are never part of the actual
submission. Add new ones to `.gitignore` alongside the existing entries.

## Credentials

Any tool that needs credentials (e.g. an email-sending watcher) uses the
pattern from `C:\Users\bley\tennis-booker`:

- A committed `secrets.example.ps1` template.
- A gitignored, never-committed `secrets.ps1` that dot-sources into
  `$env:` vars.
- Code reads credentials from `os.environ` only — never hardcoded, never
  entered by the agent.

## Testing

Tests and eval scripts run against local, deterministic fixtures —
never the live network. Where a real dependency exists (an HTTP fetch, an
email send), make it an injectable parameter with a real default, so
production code takes one path and tests inject a fake.
