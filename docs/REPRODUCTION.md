# Reproduction Guide

Written for someone starting from a clean environment with none of this set up.

See [`../PROBLEM_STATEMENT.md`](../PROBLEM_STATEMENT.md) for what's being
built, and [`../eval/CASES.md`](../eval/CASES.md) for the evaluation
cases referenced below.

## Requirements

- **OS / runtime:** Python 3.x — *(exact version TODO once implementation starts)*
- **Dependencies:** `baseline/requirements.txt`, `advanced/requirements.txt`
- **Data:** fully synthetic — the fixtures in `eval/fixtures/` (a fake
  tennis-court reservation portal). No live network calls, no real
  booking site, no credentials required to run this project.
- **Approx runtime:** TODO
- **Approx cost:** TODO — advanced solution makes LLM calls per poll; cost
  will be reported per full eval run

## 1. Setup

```bash
# clone
git clone <repo-url>
cd micro1-hackathon

# install deps
pip install -r baseline/requirements.txt
pip install -r advanced/requirements.txt
```

## 2. Run the baseline

```bash
# TODO: exact command, e.g.
# python -m baseline.watcher --source eval/fixtures/05-real-match.html --state /tmp/state.json
```

**Expected output:** TODO — describe the plain "page changed" notification.

## 3. Run the advanced solution

```bash
# TODO: exact command, e.g.
# python -m advanced.watcher --config advanced/watch_config.example.json --state /tmp/state.json
```

**Expected output:** TODO — describe the drafted reservation request held
for approval, and what approving/declining does.

## 4. Run the evaluation

```bash
# TODO: exact command, e.g.
# python -m eval.run_eval --solution both
```

**Expected output:** the metric / simple baseline / agent solution /
change comparison table from [`../eval/CASES.md`](../eval/CASES.md),
covering all 12 cases including the flappy-slot challenging case (#11).

## Troubleshooting

*(Common issues you hit while building, and the fix — saves judges time.)*
