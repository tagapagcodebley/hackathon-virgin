# Reproduction Guide

Written for someone starting from a clean environment with none of this set up.

See [`../PROBLEM_STATEMENT.md`](../PROBLEM_STATEMENT.md) for what's being
built, and [`../eval/CASES.md`](../eval/CASES.md) for the evaluation
cases referenced below.

## Requirements

- **OS / runtime:** Python 3.14 (developed/tested on 3.14.3; anything
  3.10+ should work — no version-specific syntax used).
- **Dependencies:** `baseline/requirements.txt` (`requests`, `pytest`);
  `advanced/requirements.txt` (`requests`, `anthropic`, `pytest`);
  `notifications.py`/`fetching.py` (repo root, shared by both) are
  stdlib-only, no extra install.
- **Data:** fully synthetic — the fixtures in `eval/fixtures/` (a fake
  tennis-court reservation portal, "Riverside Park Tennis Courts"). No
  live network calls to a real booking site, ever. No credentials
  required for baseline or for the test suites; advanced's real
  (non-`--fake`) run needs `ANTHROPIC_API_KEY` — see "Approx cost" below.
- **Approx runtime:** either test suite: under 3 seconds. A real
  (non-`--fake`) advanced eval run: a few seconds per case (one Anthropic
  API round-trip per `classify()` call — see below).
- **Approx cost:** $0 for baseline and for both test suites (no API
  calls). Advanced's real eval run makes one `claude-haiku-4-5` call per
  case for detection, plus one more for each positive detection to
  verify — 15 calls total for the actual 12-case run (confirmed, see
  `CHANGELOG.md`), well under a cent at Haiku 4.5 pricing. `--fake` mode
  (see below) runs the same pipeline for $0 against a stubbed
  classifier, useful for a quick sanity check but NOT the measured
  result.

## 1. Setup

```bash
# clone
git clone <repo-url>
cd micro1-hackathon

# install deps
pip install -r baseline/requirements.txt
pip install -r advanced/requirements.txt

# only needed to run advanced for real (not --fake, not its test suite)
export ANTHROPIC_API_KEY=sk-ant-...
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
python -m advanced.watcher --config advanced/watch_config.example.json --state /tmp/sauron-adv-state.txt --memory /tmp/sauron-adv-memory.json
```

**Expected output:** with the shipped example config (which points at
the static `eval/fixtures/00-baseline.html` — a "fully booked" page that
never changes), the first poll fetches it, finds no match, and prints
nothing; run it again and nothing happens either, since the page hasn't
changed. To see a real detection, drafted action, and approval prompt,
point `--config` at a copy of the example with `"source"` changed to
`eval/fixtures/05-real-match.html` — Sauron will call the Anthropic API,
correctly detect the match, verify it with a second call, print the
alert, and (in an interactive terminal) prompt
`Approve and simulate-submit? [y/N]`. Approving appends a JSON record to
`deploy/simulated_submissions.log` — never a real network call anywhere.
Run non-interactively (e.g. under a Scheduled Task) and it notifies but
declines automatically, the same honest limit baseline has — see
`advanced/approval.py`.

Run the full test suite (all fakes, no API key needed, no cost):

```bash
python -m pytest advanced/ -v
```

**Expected output:** `51 passed`.

## 4. Run the evaluation

```bash
python -m eval.run_eval --solution baseline
python -m eval.run_eval --solution advanced          # real Anthropic API calls, needs the key, small cost
python -m eval.run_eval --solution advanced --fake    # $0, pipeline sanity check only -- see eval/run_eval.py's docstring
python -m eval.run_eval --solution both               # both reports back to back
```

**Expected output for baseline:** a per-case classification table plus
`TP=3  FP=5  TN=4  FN=0`, `Precision: 0.38`, `Recall: 1.00`,
`False-positive rate: 0.56` — see [`../CHANGELOG.md`](../CHANGELOG.md)
for the full entry. **Expected output for advanced (real, not `--fake`):**
`TP=3  FP=0  TN=9  FN=0`, `Precision: 1.00`, `Recall: 1.00`,
`False-positive rate: 0.00` — see `../CHANGELOG.md`'s "Real advanced
numbers" entry for the full run, including sample reasoning from the
model. `--fake` mode gives a different, lower-precision result (a $0
pipeline sanity check against a deliberately-imperfect stub, not the
measured result — see `eval/run_eval.py`'s docstring).

## 5. Deploy it for real (optional)

Everything above stays offline against fixtures, which is what makes the
main result reproducible. To actually run Sauron unattended against a
real page with real email notifications, see
[`../deploy/README.md`](../deploy/README.md) — a poll wrapper and a
Windows Scheduled Task registration script. Not required to reproduce
the eval result above.

## Troubleshooting

*(Common issues you hit while building, and the fix — saves judges time.)*
