# Improvement Changelog

One entry per meaningful iteration. Each entry should connect *what changed* to *the evidence that motivated it* (a failing test, a bad eval score, an agent trajectory that revealed a gap, etc).

Keep cosmetic/no-op changes out of this file — only entries that moved a metric or fixed a real gap.

## Template

```
### [YYYY-MM-DD HH:MM] Short title of the change

**Evidence:** What told you this was needed (test failure, eval result, trajectory excerpt, user feedback). Link to the file/line if possible.

**Change:** What you actually did.

**Result:** What improved, with numbers if you have them.
```

---

<!-- Newest entries at the top -->

### [2026-08-29] Hidden-window execution moved from shared infra to an advanced-only improvement

**Evidence:** User feedback: the hidden-window scheduling wrapper "was a
real quality-of-life improvement" and belonged specifically to the
advanced solution, not shared equally with baseline. Fair — the previous
commit made it shared infrastructure via a `-Solution` flag, which
diluted a genuine, demonstrable engineering-quality difference into
something both solutions got "for free."

**Change:** Moved the hidden-window wrapper to
[`advanced/deploy/run_hidden.vbs`](advanced/deploy/run_hidden.vbs) (out
of the shared `deploy/` folder) with its own
[`advanced/deploy/README.md`](advanced/deploy/README.md) explaining the
rationale. Rewrote [`deploy/register_task.ps1`](deploy/register_task.ps1)
so `-Solution` now changes *how* the task runs, not just what it runs:
`baseline` invokes PowerShell directly (a console window visibly flashes
every poll), `advanced` routes through the vbs wrapper (silent). Also
reworded every judge/user-facing doc (`README.md`, `PROBLEM_STATEMENT.md`,
`baseline/README.md`, `deploy/README.md`, `docs/REPRODUCTION.md`) to
drop references to the author's other, unrelated local projects — a
judge or user with no context on those shouldn't need it to follow the
docs; that context is unpacked in `trajectories/` instead, where it's
appropriate (process transparency, not product messaging).

**Result:** Verified end-to-end: invoking the vbs wrapper directly (not
via a registered task) against a matching fixture correctly resolves
paths from its new location and fires a real poll (exit code 0, state
file written). `deploy/register_task.ps1` parses cleanly. This is now a
genuine, visible baseline-vs-advanced contrast for the demo video (one
flashes a window every cycle, the other doesn't) rather than a hidden
implementation detail neither solution got credit for.

### [2026-08-29] Baseline made genuinely deployable, not just an eval harness

**Evidence:** User feedback: "why doesn't baseline contain the
notification parts, windows register task, readme deployment
instructions? it should still be a deployable standalone solution
right?" Correct — `notify()` only `print()`ed to a console, so even
baseline never actually addressed the stated bottleneck ("they can't
watch the page 24/7"): nothing delivered a notification to someone who
wasn't staring at a terminal, and there were no docs or scripts for
running it unattended.

**Change:** Added [`notifications.py`](notifications.py) (repo root,
shared by baseline/advanced) with two injectable channels —
`console_notify` (default, no credentials) and `email_notify` (real
Gmail SMTP, credentials from the environment). Wired an injectable
`notifier` through [`baseline/watcher.py`](baseline/watcher.py)'s
`notify()`/`run()` and its CLI (`--notify {console,email}`). Added
[`deploy/`](deploy/) — `run_watcher.ps1`, `register_task.ps1`,
`secrets.example.ps1` — using a standard SMTP-App-Password pattern for
scheduled, credentialed tools, plus a Windows Scheduled Task
registration script.

**Result:** Verified end-to-end: `deploy\run_watcher.ps1` against a
matching fixture fires a real console notification through the full
wrapper; requesting `-Notify email` without `secrets.ps1` fails with a
clear, actionable message instead of crashing. Test count 14 → 18, all
passing (`python -m pytest baseline/ test_notifications.py -v`).
Detection numbers unchanged (precision 0.38 / recall 1.00 / FP rate
0.56) — this closed a delivery-layer gap, not a detection-layer one.
Did **not** register a live Scheduled Task — that's a standing
background automation on a real machine, left as an opt-in step
documented in [`deploy/README.md`](deploy/README.md) for whoever runs it.

### [2026-08-29] Baseline established: keyword-diff watcher

**Evidence:** `python -m eval.run_eval --solution baseline` against the
12 content-diff cases in [`eval/CASES.md`](eval/CASES.md) (fixtures in
[`eval/fixtures/`](eval/fixtures/)):

```
TP=3  FP=5  TN=4  FN=0
Precision:            0.38
Recall:               1.00
False-positive rate:  0.56
```

14/14 tests pass in [`baseline/test_watcher.py`](baseline/test_watcher.py).

**Change:** Implemented [`baseline/watcher.py`](baseline/watcher.py) — a
literal keyword-substring watcher: diffs the page against the last-seen
snapshot and fires when the diff contains a short configured `keyword`
("slot available"), same approach real tools like changedetection.io use.

**Result:** Recall is perfect (1.00) — baseline never misses a real
opening, since any actionable change necessarily contains the keyword.
But precision is poor (0.38): it misclassifies 5 of 8 non-matching cases
as real — negation ("no slot available"), all three criteria near-misses
(wrong date/time/party size), and an unrelated FAQ mention. This is the
expected, documented baseline failure mode, not a bug — it's the gap
[`advanced/`](advanced/) exists to close in Stage 3. Target for advanced:
hold recall at 1.00 while pushing precision well above 0.38 by adding
semantic criteria matching on top of the same detection surface.
