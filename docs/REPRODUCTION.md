# Reproduction Guide

Written for someone starting from a clean environment with none of this set up.

See [`../PROBLEM_STATEMENT.md`](../PROBLEM_STATEMENT.md) for what's being
built, and [`../eval/CASES.md`](../eval/CASES.md) for the evaluation
cases referenced below.

## Requirements

- **OS / runtime:** Python 3.14 (developed/tested on 3.14.3; anything
  3.10+ should work — no version-specific syntax used).
- **Dependencies:** `baseline/requirements.txt` (`requests`, `pytest`);
  `notifications.py` (repo root, shared by baseline/advanced) is stdlib
  only, no extra install; `advanced/requirements.txt` — TODO, lands in
  Stage 3.
- **Data:** fully synthetic — the fixtures in `eval/fixtures/` (a fake
  tennis-court reservation portal, "Riverside Park Tennis Courts"). No
  live network calls, no real booking site, no credentials required to
  run this project.
- **Approx runtime:** baseline test suite + eval run: under 1 second.
- **Approx cost:** $0 for baseline (no API calls). Advanced solution
  will make LLM calls per poll — cost reported once Stage 3 lands.

## 1. Setup

```bash
# clone
git clone <repo-url>
cd micro1-hackathon

# install deps
pip install -r baseline/requirements.txt
# pip install -r advanced/requirements.txt  # Stage 3
```

## 2. Run the baseline

```bash
python -m baseline.watcher --source eval/fixtures/05-real-match.html --state /tmp/sauron-state.txt
```

**Expected output:** two lines to stdout —
`[Sauron] Sauron: page changed and contains 'slot available'` followed
by a text snippet around the match — plus `/tmp/sauron-state.txt`
written with the fetched page text, used as `previous` on the next run.
Run it again against the same source and nothing prints, since the page
"hasn't changed" from the persisted state. Add `--notify email` for a
real email instead of console output (needs credentials — see
[`../deploy/README.md`](../deploy/README.md)).

Run the full test suite (baseline + the shared notification module):

```bash
python -m pytest baseline/ test_notifications.py -v
```

**Expected output:** `18 passed`.

## 3. Run the advanced solution

```bash
# TODO: exact command, e.g.
# python -m advanced.watcher --config advanced/watch_config.example.json --state /tmp/state.json
```

**Expected output:** TODO — describe the drafted reservation request held
for approval, and what approving/declining does. Lands in Stage 3.

## 4. Run the evaluation

```bash
python -m eval.run_eval --solution baseline
```

**Expected output:** a per-case classification table plus
`TP=3  FP=5  TN=4  FN=0`, `Precision: 0.38`, `Recall: 1.00`,
`False-positive rate: 0.56` — see
[`../CHANGELOG.md`](../CHANGELOG.md) for the full baseline entry. Once
Stage 3 lands, `--solution both` will print the same table for advanced
alongside baseline for a direct comparison.

## 5. Deploy it for real (optional)

Everything above stays offline against fixtures, which is what makes the
main result reproducible. To actually run Sauron unattended against a
real page with real email notifications, see
[`../deploy/README.md`](../deploy/README.md) — a poll wrapper and a
Windows Scheduled Task registration script. Not required to reproduce
the eval result above.

## Troubleshooting

*(Common issues you hit while building, and the fix — saves judges time.)*
