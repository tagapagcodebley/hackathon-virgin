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

### [2026-08-31] Case 13: baseline's recall wasn't actually perfect, it was untested

**Evidence:** User: "I think a test case where the baseline solution
would not fire but the advanced would is a good demonstration for the
advanced solution... maybe the user is waiting for signups to open but
the page just adds a link without the actual signup keyword." Correct,
and it exposed something the eval design hadn't earned: every prior
"real match" fixture (05, 11a, 11b) happened to contain baseline's
literal `keyword` ("slot available") by construction, so baseline's
1.00 recall was never a demonstrated structural property — it was an
artifact of how the fixtures were written.

**Change:** Added `eval/fixtures/13-recall-gap.html` — the Saturday
9-11am row changes from "Fully booked" to "Book now — 4 players" (zero
lexical overlap with "slot available"). Added it to `eval/run_eval.py`'s
scored case set (ground truth: a real match). Renumbered `eval/CASES.md`'s
orchestration cases 13→14, 14→15 to make room, and added new tests:
`baseline/test_watcher.py::test_recall_gap_is_a_documented_false_negative`,
`advanced/test_detector.py::test_recall_gap_detected_without_the_literal_keyword`,
`advanced/test_watcher.py::test_recall_gap_notifies_and_submits_where_baseline_would_stay_silent`.
Updated `PROBLEM_STATEMENT.md`'s prior-art gap list from three gaps to
four (the new one: "a real opening can be missed entirely, not just
misclassified").

**Result:** Ran both solutions for real against the expanded 13-case
set. Baseline:

```
TP=3  FP=5  TN=4  FN=1
Precision:            0.38
Recall:               0.75
False-positive rate:  0.56
```

Baseline's recall dropped from a previously-reported 1.00 to 0.75 — not
a regression, a correction: the earlier number never measured what it
appeared to. Advanced, real API, same case set:

```
TP=4  FP=0  TN=9  FN=0
Precision:            1.00
Recall:               1.00
False-positive rate:  0.00
```

Advanced holds perfect precision *and* recall even with the harder case
included — it correctly reads "Book now" appearing on the Saturday
9-11am row as satisfying `watch_for`, with no keyword to lean on at all.
This is a stronger demonstration than the previous evaluation could
offer: advanced isn't just more conservative than baseline (better
precision, same recall) — it genuinely sees things baseline structurally
cannot. 75/75 tests pass. Propagated the real numbers through
`README.md`, `baseline/README.md`, `advanced/README.md`,
`docs/REPRODUCTION.md`, and `eval/CASES.md`.

### [2026-08-31] Demo scripts told users to point at a real match, then showed a command that didn't

**Evidence:** User: "what am i supposed to see when i demo the advanced
run? there's no terminal output." Traced it: `DEMO_SCRIPT.md`'s Beat 5
said "(config pointed at a real match — see setup note below)" directly
above a command that literally used
`--config advanced/watch_config.example.json` unmodified — which points
at the boring `00-baseline.html` fixture and correctly prints nothing.
The actual fix (edit a copy's `source` field) was described in prose in
a separate section near the bottom of the file, disconnected from the
beat that needed it. `VIDEO_GUIDE.md` had the identical structural flaw
in its own Beat 2.

**Change:** Rather than patch the misleading sentence, removed the
ambiguity entirely: both files' "before you record" setup now includes
a concrete, verified-in-its-actual-shell one-liner (PowerShell
`-replace`, tested directly) that builds `sauron-run/demo-config.json`
— the example config with `source` swapped to a matching fixture — and
each file's advanced-demo beat now runs that file directly instead of
the shipped example. Deleted the now-redundant prose-only setup note.
Also tightened `docs/REPRODUCTION.md` section 3 the same way, adding
both a `sed` (bash) and a PowerShell one-liner, each verified in its
actual shell before being written down — per the `/tmp/` lesson two
entries below this one, "I tested it" now specifies which shell.

**Result:** Confirmed manually: the shipped example config silently
finds no match (intended); `sauron-run/demo-config.json` produces the
full detect → verify → draft → approve flow with real model reasoning.
Both PowerShell and bash config-transform one-liners verified to
produce identical, valid JSON.

### [2026-08-31] Fixed a real /tmp/ path bug in every reproduction example

**Evidence:** User ran `docs/REPRODUCTION.md`'s exact documented baseline
command in native PowerShell and hit a crash the agent never saw:

```
[Sauron] Sauron: page changed and contains 'slot available'
...
FileNotFoundError: [Errno 2] No such file or directory: '\\tmp\\demo-state.txt'
```

`/tmp/...` only resolves as a real directory in Git Bash/MSYS, which is
what the agent used to verify every command in this repo's docs. In
native Windows PowerShell, `/tmp/...` resolves to a nonexistent
directory off the current drive root, and `Path.write_text()` doesn't
create missing parent directories — so the notification fired correctly
(that line runs first), then the very next line, persisting state,
crashed. Every documented example command using `/tmp/...` had this
same latent bug; it happened not to be caught earlier because the agent
verified them all from a shell where the bug is invisible.

**Change:** Two fixes, not one — a doc fix alone would have left the
underlying fragility in place for the next person who supplies any path
with a missing parent directory:

1. `baseline/watcher.py` and `advanced/watcher.py`'s `run()` now
   `state_file.parent.mkdir(parents=True, exist_ok=True)` before ever
   writing state — matching the pattern `advanced/memory.py`'s
   `WatcherMemory.save()` already had. Added
   `test_run_creates_missing_parent_directory_for_state_path` (baseline)
   and `test_run_creates_missing_parent_directories_for_state_and_memory`
   (advanced) — both use a `tmp_path` subdirectory that doesn't exist
   yet, since every prior test used `tmp_path` directly (which already
   exists) and so couldn't have caught this.
2. Replaced every `/tmp/...` reference across `docs/REPRODUCTION.md`,
   `DEMO_SCRIPT.md`, and `VIDEO_GUIDE.md` with a relative `sauron-run/`
   scratch directory (gitignored), which resolves identically in both
   Git Bash and native PowerShell — no shell-specific path logic needed
   anywhere.

**Result:** 72/72 tests pass (70 → 72). Reproduced the exact original
crash, then confirmed the fix resolves it, via PowerShell directly (not
just the agent's own Bash-tool testing this time) — ran the corrected
`sauron-run/`-based command, confirmed it creates the directory and
writes the file with no error. This is the second time in this project
that testing exclusively through one execution path (unit tests against
fakes; here, the agent's own Bash-tool shell) missed something the
user's actual environment caught immediately — see the entry below for
the first. Worth remembering for the Hot Take.

### [2026-08-29] Real advanced numbers: precision 1.00, recall 1.00 — plus three bugs the first real run surfaced

**Evidence:** The previous entry's `--fake` numbers were explicitly
flagged as not the measured result. User provided a real
`ANTHROPIC_API_KEY` (via `deploy/secrets.ps1`, dot-sourced directly into
a single command that also ran the eval — the key never entered this
conversation or got read/printed by the agent). First real run
(`python -m eval.run_eval --solution advanced`) surfaced three genuine
bugs in quick succession, each fixed and verified before moving to the
next:

1. `anthropic.BadRequestError: ... anthropic-workspace-id is required
   when authenticating with an identity-linked API key`. Not a bug in
   the request logic — this API key type needs an extra header the base
   SDK client doesn't attach automatically. User switched to a standard
   (non-identity-linked) key instead, sidestepping it.
2. `JSONDecodeError: Unexpected UTF-8 BOM` — `advanced/criteria.py`'s
   `load_config()` used strict `utf-8`, and a config file written by
   PowerShell's own `Set-Content -Encoding utf8` (or Notepad) carries a
   BOM by default. Fixed with `encoding="utf-8-sig"`, which strips a BOM
   when present and is identical to `utf-8` otherwise — a real
   Windows-deployment robustness gap, not just a test-harness artifact,
   so it got a real test (`test_load_config_handles_utf8_bom`).
3. During a live end-to-end CLI run: the interactive approval prompt
   printed the full drafted action twice (once via the notifier, again
   inside the `input()` prompt string) and crashed with an uncaught
   `EOFError` when stdin had no data to read. Fixed `advanced/approval.py`'s
   `_default_approve()` to prompt with just the short question (the
   notifier already showed the full action) and to catch `EOFError` as
   a safe decline, consistent with the "never auto-approve, never crash,
   decline when unsure" pattern already used everywhere else in this
   project.

**Change:** The three fixes above, plus a real end-to-end verification
pass: ran `python -m eval.run_eval --solution advanced` for real, then
manually ran `python -m advanced.watcher` twice more against a live
match — once confirming the interactive prompt now shows clean, correct
reasoning and declines safely on EOF; once with piped `"y"` input,
confirming `sys.stdin.isatty()` correctly treats a pipe as non-interactive
(no live human answering in real time) and declines rather than guessing,
exactly as designed.

**Result:** Real, measured `advanced` numbers, replacing the `--fake`
placeholder in the entry below:

```
TP=3  FP=0  TN=9  FN=0
Precision:            1.00
Recall:               1.00
False-positive rate:  0.00
classify() calls:     15 (~2 per confirmed match: detect + verify)
```

Perfect score across all 12 content-diff cases — including every case
baseline (precision 0.38) and the `--fake` stub (precision 0.60) got
wrong: negation (06), all three criteria near-misses (07-09), and the
ambiguous FAQ mention (10). Sample reasoning from the real model on case
05: *"The page shows 'Saturday 9:00-11:00 AM Slot available - up to 4
players,' which exactly matches all stated criteria: Saturday, 9-11am
time slot, and 4-person capacity."* — genuinely reading the criteria
compositionally rather than pattern-matching a phrase, which is exactly
the gap both baseline and the hand-written stub had (see the entry
below). 70/70 tests still pass after all three fixes.

### [2026-08-29] Advanced implemented: LLM-agent pipeline (Stage 3)

**Evidence:** Baseline's measured failure shape (precision 0.38, recall
1.00 — see the entry below) on negation, criteria near-misses, and the
FAQ mention, plus `eval/CASES.md`'s full case list, defined exactly what
advanced needed to fix while holding recall at 1.00.

**Change:** Implemented all six `advanced/` modules for real (no more
`NotImplementedError`): `criteria.py` (`WatchConfig` JSON loading),
`memory.py` (JSON-persisted decoy/already-surfaced tracking),
`detector.py` (`detect()`/`verify()`, with a real default classifier —
an Anthropic `claude-haiku-4-5` tool-use call for structured
`is_match`/`reasoning` output), `action_drafter.py`, `approval.py`
(notifies via `notifications.py`, then a synchronous approval prompt
when interactive, an honest automatic decline when not — see its module
docstring), and `watcher.py` (the orchestrator: `auto_expire` failsafe,
`release_date`-driven adaptive polling via `next_poll_interval()`, and
the full detect → verify → draft → approve → submit flow). Extracted
`fetch_page_state` out of `baseline/watcher.py` into a shared
`fetching.py` so both solutions use identical fetch semantics. 51 new
tests across 5 files (`test_criteria.py`, `test_memory.py`,
`test_detector.py`, `test_action_drafter.py`, `test_approval.py`,
`test_watcher.py`), all against injected fakes — zero network, zero API
key, zero cost, per CLAUDE.md's testing rule. Extended `eval/run_eval.py`
with `score_advanced()`, real by default (calls the actual API) with a
`--fake` flag for a $0 pipeline-correctness check against a
deliberately-not-perfected stubbed classifier.

**Result:** 51/51 new tests pass; 69/69 across the whole repo. Verified
the real CLI end-to-end up to the live API call itself — config loading,
fixture fetch, state/memory persistence, and a clean, actionable error
when `ANTHROPIC_API_KEY` is missing (both from the Python CLI and from
`deploy/run_watcher.ps1`'s pre-check) all confirmed correct; this
sandbox had no Anthropic API key available at the time this entry was
written, so the live call itself was unverified here — **see the entry
above this one for the real run**, done immediately afterward once a key
was provided, including three more real bugs it surfaced and fixed.

`--fake` pipeline sanity check (NOT the measured result — a
hand-written stub, not the real agent):

```
TP=3  FP=2  TN=7  FN=0
Precision:            0.60
Recall:               1.00
False-positive rate:  0.22
```

This is itself a useful, honest finding: the stub correctly catches
negation (case 06) and the party-size near-miss (case 09) via targeted
checks, but still misclassifies the date and time near-misses (cases
07-08) as matches, because it checks for "Saturday" / "9:00-11:00 AM" /
"4 players" as whole-page substrings rather than confirming they occur
*in the same table row*. A real LLM reading the page holistically
should associate those fields contextually and get this right — but
that's exactly the point: a hand-rolled heuristic, even one written with
the fixtures in hand, still falls short of genuine contextual
understanding. The stub was deliberately left as-is rather than patched
to hide this — see PROBLEM_STATEMENT.md's hot take.

**Case 12 (the challenging case), resolved:** `verify()` correctly
declines when the opening closes between detection and the re-fetch
(`advanced/test_detector.py::test_verify_catches_the_flappy_slot_closing`,
`advanced/test_watcher.py::test_flappy_slot_is_declined_after_verification`)
— see `eval/CASES.md`'s design note for the trade-off this surfaces.

**Update:** the real run happened — see the entry above this one.
Precision went 0.60 (`--fake`) → 1.00 (real), confirming the guess above
that the real model would beat the stub's whole-page-substring
heuristic on cases 07-08. Don't cite the `--fake` numbers in this entry
as the submission's headline result; they're preserved here only as the
honest record of what pipeline verification looked like before a key
was available.

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
