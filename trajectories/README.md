# Agent Trajectories

Representative trajectories for every coding agent used in this submission, from the instructions given to the agent through to the final result.

Each trajectory should make it easy for a judge to follow:

1. **The instructions/prompt given to the agent** at that step.
2. **What the agent did** — tool calls, commands run, files touched.
3. **How its tools responded** — command output, test results, errors.
4. **The feedback that shaped the next step** — what you (or the agent) noticed and how it changed direction.
5. **Any retries or human checkpoints** — where a human approved/redirected a consequential action.

## Naming convention

```
trajectories/
  01-baseline-setup.md
  02-baseline-implementation.md
  03-advanced-approach-exploration.md
  04-advanced-implementation.md
  05-eval-and-fix-loop.md
```

Number them roughly in chronological order. Prefer a few well-curated, representative trajectories over dumping every raw session log — but keep the raw logs too (e.g. in `trajectories/raw/`) in case judges want to dig in.

## Template for one trajectory file

```markdown
# NN — Short title

**Agent / model:** e.g. Claude Code, claude-sonnet-5
**Date:** YYYY-MM-DD
**Goal of this step:**

## Instructions given

...

## What happened

...

## Tool responses / evidence

...

## Human checkpoint(s)

...

## Outcome

...
```
