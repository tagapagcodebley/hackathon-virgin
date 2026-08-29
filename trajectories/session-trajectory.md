# Session Trajectory — Real Submission

> Per [`CLAUDE.md`](../CLAUDE.md): one running trajectory file for this
> activity (the actual competition submission), delineated by stage-gate
> headers, superseding the numbered-per-file convention described in
> [`trajectories/README.md`](README.md) — that file documents an
> alternative pattern this repo no longer defaults to.

**Agent / model:** Claude Code, claude-sonnet-5
**Repo:** `C:\Users\bley\micro1-hackathon` (repo root — the real submission,
not `practice/` or `practice2/`, both gitignored dry runs of this same
process)

## Stage-gate model (see `CLAUDE.md` for full definition)

1. **Stage 1 — Scaffolding.**
2. **Stage 2 — Basic/baseline solution.**
3. **Stage 3 — Advanced solution.**
4. **Stage 4 — Finalize.**

Each stage ends with an explicit human checkpoint before the next begins.

---

## Stage 1 — Scaffolding (pre-kickoff prep)

### Context

The real problem statement is unknown until the pre-event orientation and
kickoff, both at 1AM local time (not yet happened as of this entry). This
repo's scaffold (`README.md`, `CHANGELOG.md`, `docs/REPRODUCTION.md`,
`baseline/README.md`, `advanced/README.md`, `trajectories/README.md`) was
created in an earlier session (commit `c0f72b3`, "Scaffold repo for micro1
Frontier Engineering Challenge 2026") and is still accurate — it correctly
defers problem-specific content with "fill in once the problem is known."

Two full dry runs of the whole stage-gated process happened first, to
rehearse it before the real, unknown problem arrives: `practice/`
(fabricated rate-limiter problem) and `practice2/` (a real, useful
page-watcher + email-notifier tool, now deployed as a genuine Windows
Scheduled Task — see `practice2/trajectories/session-trajectory.md` for
its full log). Both are gitignored and are not part of this submission.

### Instructions given (verbatim, user message)

> yep, i like what we've established with our practice sessions. all we
> have to do now is wait for orientation and then actual start. to
> finalize this conversation, you can update our main scaffolding to prep
> for stage 1 of actual competition. you dont have to log anything on
> practice2 anymore. lets keep that folder as it is. good night claude!

### What the agent did

1. Read the existing top-level scaffold (`README.md`, `CHANGELOG.md`,
   `docs/REPRODUCTION.md`, `baseline/README.md`, `advanced/README.md`,
   `trajectories/README.md`) to confirm what already exists vs. what
   tonight's prep should add. Left the problem-specific placeholders
   (`baseline/README.md`, `advanced/README.md`, `docs/REPRODUCTION.md`,
   `CHANGELOG.md`) untouched — there's nothing concrete to fill in before
   the real problem is known, and pre-guessing its shape (e.g. stubbing
   out code, picking a language/framework) would be building for a
   hypothetical requirement rather than a real one.
2. Created this file (`trajectories/session-trajectory.md`) — the real
   submission didn't have its running trajectory file yet, only
   `trajectories/README.md`'s now-superseded numbered-file convention doc.
3. Added a short pointer note at the top of `trajectories/README.md`
   clarifying that `CLAUDE.md`'s single-file convention is what this repo
   actually uses now, so a future reader doesn't follow the stale
   numbered-file instructions.
4. Updated top-level `README.md`'s status to reflect: scaffold ready,
   both practice runs complete, awaiting kickoff.
5. Did **not** touch `practice2/` at all, per explicit instruction — its
   trajectory log stays exactly as Stage 4 left it.
6. Updated the agent's own cross-session memory (outside this repo, at
   `C:\Users\bley\.claude\projects\C--Users-bley-micro1-hackathon\memory\`)
   so a fresh conversation opened once orientation/kickoff happens picks
   up: the stage-gate process, this file as where the real trajectory
   continues, and that both practice runs are finished rehearsals, not
   further context to dig through.

### Human checkpoint

No further action expected tonight — user is signing off ("good night")
ahead of the 1AM orientation/kickoff. Next real step is Stage 1 continuing
once the actual problem statement is available: fill in `README.md`'s "The
problem" section for real, decide the baseline/advanced split for the
actual requirements, and place problem-specific TODOs in `baseline/` and
`advanced/` — logged as the next entry in this same file, under this same
Stage 1 header (or a new one, if scaffolding turns out to need real
placeholder files at that point).

### Outcome

Repo-root scaffold confirmed still accurate and now has its own running
trajectory file, consistent with the process established across both
practice runs. Nothing implemented yet — correctly so, since the problem
is still unknown. Ready for kickoff.

---

## Stage 1 — Scaffolding (continued, post-kickoff)

### Instructions given (verbatim, user message)

> real problem has dropped. initiate stage 1.

### What the agent did

1. Ran `ls` on the repo root and found a new untracked file,
   `micro1 - First Hackathon97ce7c5.pdf` (timestamped this morning) —
   read it in full via the `Read` tool.
2. **Finding:** the PDF is the hackathon's rulebook, not a fixed problem
   assignment. It's explicitly open-ended — "Pick a specific and
   meaningful problem you understand" — and includes the four framing
   questions, judging rubric (100 pts: Problem & User Value 15, Agent
   Solution & Engineering 30, End-to-End Quality 20, Measured Improvement
   15, Reproducibility 15, Hot Take/Insights 5), ground rules (notably
   #04: sandbox/simulate consequential actions with human approval
   before they happen; #07: use synthetic/public/approved data; #08: no
   credentials in the submission), the four required deliverables, and
   three worked examples in an appendix (repo quality assessment,
   candidate hiring evaluation, podcast translation consistency).
3. Confirmed via `README.md` and `docs/`/`baseline/`/`advanced/` reads
   that no problem had been chosen yet — this repo's existing scaffold
   was still all placeholders.
4. Peeked at `practice/` and `practice2/`'s file listings (not their
   content) to recall what domains those dry runs covered, since the
   user's own memory (`project_micro1_hackathon.md`) flagged them as
   relevant prior context.
5. Since picking the actual problem is a decision only the user can make
   (per the harness's guidance: ask when genuinely blocked on something
   only the user can decide), asked three rounds of `AskUserQuestion`
   rather than guessing:
   - Round 1 — user chose **"Brainstorm from things you already have"**
     over "I have a specific problem in mind" / "Adapt one of the PDF's
     three examples."
   - Round 2 — offered three candidate directions grounded in the user's
     existing `tennis-booker` and `practice2` page-watcher patterns; user
     chose **"Generalized watch-and-act agent"** over "Tennis court
     booking assistant" / "Hackathon submission rubric auditor."
   - Round 3 — offered three concrete scenarios to anchor the
     generalized engine's eval/demo; user chose **"Time-sensitive slot
     booking"** over "Narrow job/gig posting match" / "Price/inventory
     drop on a specific item."
6. Synthesized the three answers into a concrete problem: someone trying
   to grab a rare, unpredictably-released reservation slot (demoed
   against a synthetic tennis-court portal) that a naive diff-watcher
   handles badly — false positives on decoy changes, no criteria
   matching, no drafted action beyond a notification.
7. Wrote the Stage 1 scaffold (folders/files with TODOs and
   `NotImplementedError` placeholders only, per `CLAUDE.md` — no real
   logic):
   - `README.md` — filled in "The problem" section for real.
   - `PROBLEM_STATEMENT.md` (new, root) — full who/bottleneck/why,
     baseline vs. advanced approach, and evaluation plan, following the
     rulebook's four framing questions.
   - `baseline/` — `README.md` (filled in), `watcher.py`,
     `test_watcher.py`, `requirements.txt` — all placeholder stubs for a
     dumb hash/text-diff watcher with no semantic judgment.
   - `advanced/` — `README.md` (filled in), plus five placeholder
     modules reflecting the intended architecture: `criteria.py`
     (context), `memory.py` (decoy memory across polls), `detector.py`
     (semantic detection + verification pass), `action_drafter.py`
     (drafts a structured reservation request), `approval.py` (human
     approval gate + simulated-only submit), `watcher.py` (orchestrator),
     `test_watcher.py`, `requirements.txt`, `__init__.py`.
   - `eval/CASES.md` (new) — 12 evaluation cases (steady state, three
     decoy variants, exact match, three criteria-near-miss variants,
     ambiguous FAQ mention, duplicate-detection/memory case, the
     "challenging case" — a slot that opens and closes within one poll
     interval — and a fetch-error robustness case), with expected
     baseline vs. advanced behavior spelled out per case, and the
     primary/secondary metrics defined.
   - `eval/fixtures/README.md` (new) — placeholder noting fixture files
     land in Stage 2/3.
   - `eval/run_eval.py` (new) — placeholder scoring/comparison-table
     runner.
   - `docs/REPRODUCTION.md` — filled in structure (deps, synthetic-only
     data, command shapes) while leaving exact commands as TODOs.

### Human checkpoint

Per `CLAUDE.md`: **stopping here for explicit validation before Stage 2**
(baseline implementation). Have not written any real logic — every new
`.py` file raises `NotImplementedError` or has TODO-only bodies. Asking
the user to confirm: the chosen problem framing in
`PROBLEM_STATEMENT.md`, the baseline/advanced split, and the `eval/CASES.md`
case list, before implementing the baseline in Stage 2.

### Outcome

Full Stage 1 scaffold in place for the real problem: problem statement
written, baseline and advanced folder structures created with
placeholder-only code reflecting the intended design (dumb diff-watcher
vs. context+memory+verification+drafting+approval-gated agent), and a
12-case evaluation plan defined. Nothing executable yet — correctly so
per the stage-gate process. Awaiting user validation to start Stage 2.

---

## Stage 1 — Scaffolding (refinement: naming, generalization, prior art)

### Instructions given (verbatim, user message 1)

> let's refine the problem statement some more and brainstorm with me. i
> like the idea of a generic page watcher. let's call this project
> sauron. the user can simply input what page or site to watch, what to
> watch out for, for how long, and how often. could it be a browser
> plugin? is there anything similar to this now?

### What the agent did (in response to message 1)

This was an exploratory/brainstorming ask, not an implementation
request, so answered in chat without editing files first: named real
prior art (changedetection.io, Distill.io, Wachete, Visualping, Follow
That Page, CamelCamelCamel, community slot-sniping scripts) and the
common gap across all of them (keyword/CSS-diff matching only, stops at
a notification, no semantic judgment, no drafted next step); recommended
generalizing the rigid booking-criteria schema to a plain-language
`watch_for` field plus `source`/`auto_expire`/`poll_interval`;
recommended against a browser extension as the core deliverable
(install/permission overhead hurts the rubric's Reproducibility
criterion) in favor of noting it as future work. Asked whether to fold
this in now, and asked two follow-up design questions (should `duration`
auto-expire, should poll frequency adapt).

### Instructions given (verbatim, user message 2)

> yes, fold these ideas in. and yes, i like the auto-expire option
> because i actually needed the hackathon page watcher to expire after
> the rules have been released. so for example, when watching for
> concert tickets, the default auto-expire date should be when the
> concert happens. and also yes, i like the polling frequency idea. some
> booking sites allow users to hold the booking. would this break the
> rules if the agent initiates the hold? is that even possible to do
> automatically? or does it always require user intervention?

### What the agent did (in response to message 2)

1. Answered the hold-automation question directly in chat before editing
   anything: concluded a hold is still "consequential" under ground rule
   04 even though it's typically reversible/time-boxed, because it's a
   real action against a real system affecting real availability for
   other real people — a standing "always hold for me" setting wouldn't
   satisfy "approval before the action happens" read as approval in the
   moment. Separately flagged that most booking/ticketing sites' ToS
   prohibit automated interaction and increasingly CAPTCHA-gate it
   (ground rule 03), and that the agent's own operating rules prohibit
   building CAPTCHA-bypass tooling regardless of legitimacy of the use
   case. Landed on: Sauron always stops at detect → draft → prompt; the
   submit/hold step is simulated-only in this submission, never a live
   call.
2. Rewrote `PROBLEM_STATEMENT.md` in full: renamed the project to
   Sauron with a tagline; added a "Prior art" subsection under Q02 naming
   the tools above and the three-part gap (no negation/semantic
   understanding, no criteria disambiguation, no drafted follow-through);
   added an "Auto-expire and adaptive polling" subsection tying
   auto-expire's default to a known target date (concert date; the
   hackathon kickoff-page precedent from `practice2/`) and adaptive
   polling to tightening near that date; generalized the baseline/advanced
   description from "booking criteria" to `WatchConfig`
   (source/watch_for/auto_expire/poll_interval); added an "On automated
   holds (ground rule 04)" subsection recording the decision above; added
   a "Future work" section documenting the browser-extension option as
   explicitly out of scope, per ground rule 02.
3. Rewrote `eval/CASES.md`: reframed the baseline from "any diff" to
   "keyword-substring diff" (a fairer, more realistic baseline matching
   the prior-art tools) and added a **negation case** (case 06 — "no
   Saturday slots available" contains the watch_for substring but means
   the opposite) as the sharpest baseline-failure showcase, sharper than
   raw-diff false positives on decoys. Restructured decoy cases (02-04)
   to correctly *not* fire for a keyword baseline (since decoys don't
   contain the keyword), keeping the baseline credible rather than a
   strawman. Added two new orchestration cases (13: expired watch stops
   polling/acting; 14: poll interval tightens near auto_expire) tested
   via an injected fake clock rather than fixture content, and a design
   note flagging that case 12 (the flappy-slot race) may reveal that
   adaptive polling, not smarter detection, is the real fix — earmarked
   as the project's eventual Hot Take.
4. Updated code scaffolds to match (still placeholder-only, no real
   logic): `advanced/criteria.py` — `BookingCriteria` → `WatchConfig`
   (source/watch_for/auto_expire/poll_interval) plus a
   `default_expiry_from_watch_for()` stub; `advanced/memory.py` —
   broadened to also track already-surfaced matches, not just decoys;
   `advanced/detector.py` and `action_drafter.py` — updated to the new
   `WatchConfig` type and generalized docstrings; `advanced/watcher.py` —
   added a `next_poll_interval()` stub and expiry-aware `run()`;
   `baseline/watcher.py` — replaced `notify`-on-any-change with a
   `matches_watch_for()` naive-substring-check stub, explicitly
   documented as the negation-blind limitation. Rewrote both
   `test_watcher.py` files' TODO cases to match the new case list
   (including the negation, expiry, and adaptive-interval tests).
   Updated `baseline/README.md`, `advanced/README.md`, root `README.md`
   (title → Sauron, "The problem" section, new "Future work" section),
   and `docs/REPRODUCTION.md` (command placeholder →
   `--config watch_config.example.json`) for consistency.
5. Syntax-checked every touched `.py` file via `ast.parse` — all clean.
6. Updating this trajectory entry and the cross-session project memory
   (`project_micro1_hackathon.md`) to record the Sauron name and the
   refined design before moving on.

### Human checkpoint

Still Stage 1 — no real logic written, only refined placeholders/specs.
Next step is starting Stage 2 (baseline implementation) once the user
confirms this refined framing, or continuing to brainstorm further.

### Outcome

Problem statement and full scaffold refined and renamed to Sauron:
generic `WatchConfig` (not booking-specific), prior-art/differentiation
section, auto-expire defaulting to a known target date, adaptive polling
near expiry, an explicit ground-rule-04 decision on automated holds
(never automated, always simulated-submit-only), browser extension moved
to documented future work, and the eval case list sharpened around a
fairer keyword baseline with a negation case as its headline failure.

---

## Stage 1 — Scaffolding (correction: auto_expire is not a timing signal)

### Instructions given (verbatim, user message)

> clarification: poll_interval shouldn't tighten around auto_expire.
> that date should just be a fail safe date for the script to get
> unregistered for when the user forgets to do it themselves. the
> tightening should be around another date, e.g. release_date because
> tickets normally go on sale way before the event happens. the user can
> set auto_expire to release_date + 24 hours, for example.

### What the agent did

Caught and fixed a real design error from the prior refinement pass: it
had conflated "when to give up" (a failsafe) with "when to lean in"
(urgency/adaptive polling) into a single `auto_expire` field, and had
even suggested defaulting expiry to the concert date itself — wrong,
since tickets go on sale well before the event.

1. `PROBLEM_STATEMENT.md` — rewrote "Auto-expire and adaptive polling"
   as "Auto-expire vs. release date — two different dates, not one":
   `auto_expire` is now framed purely as a failsafe unregister date with
   no timing signal; a new `release_date` (optional — the user's best
   guess of when the watched-for condition becomes true, e.g. an
   expected ticket on-sale date) is what adaptive polling actually keys
   off; documented that `auto_expire` can default to
   `release_date + 24h` as a suggested buffer while remaining a distinct
   concept the user can override.
2. `advanced/criteria.py` — rewrote `WatchConfig`'s field docs to add
   `release_date: datetime | None` and reframe `auto_expire` as
   failsafe-only; replaced the old (wrong) `default_expiry_from_watch_for`
   stub, which tried to infer an expiry from watch_for text, with
   `default_auto_expire(release_date, buffer=DEFAULT_AUTO_EXPIRE_BUFFER)`
   returning `release_date + buffer`.
3. `advanced/watcher.py` — fixed `next_poll_interval()`'s docstring to
   key off `release_date`, with an explicit "must NOT reference
   auto_expire" note so a future implementer doesn't reintroduce the
   same conflation; `run()`'s docstring now describes `auto_expire` as
   the failsafe stop condition, independent of `release_date`.
4. `advanced/README.md` — updated the `criteria.py`/`watcher.py` table
   rows and the "What's different from baseline" paragraph to describe
   both fields correctly and distinctly.
5. `advanced/test_watcher.py` — renamed/refined case 14's test
   (`test_poll_interval_tightens_near_release_date`) to assert
   tightening tracks `release_date` while `auto_expire` is held
   constant/far away, so a future implementation can't pass by
   accidentally keying off the wrong field.
6. `eval/CASES.md` — case 14 reworded to tighten around `release_date`
   with `auto_expire` set well past it; case 13 reworded to clarify it's
   testing the failsafe specifically, independent of `release_date`; the
   "Fixed watch config" sketch and the case-12 design note updated to
   match; added a note that the primary scenario's config leaves
   `release_date` unset (no announced court-opening date) and that case
   14 uses a separate config to exercise tightening.
7. Syntax-checked the three touched `.py` files — all clean.

### Human checkpoint

Still Stage 1, still placeholder-only. This correction is now folded in;
next step is either further brainstorming or the user confirming to
start Stage 2 (baseline implementation).

### Outcome

Fixed a real conflation bug in the design before any implementation
existed to inherit it: `auto_expire` (failsafe, no timing role) and
`release_date` (urgency signal, drives adaptive polling) are now
consistently distinct fields across `PROBLEM_STATEMENT.md`,
`eval/CASES.md`, and every touched code/test scaffold file.

---

## Stage 1 → Stage 2 (lock in, commit, implement baseline)

### Instructions given (verbatim, user message)

> let's lock in Stage 1, git commit, then start Stage 2

### What the agent did — locking in Stage 1

1. Ran `git status`, confirmed everything staged was Stage 1 scaffolding
   (plus one pre-existing uncommitted change to `trajectories/README.md`
   from the earlier pre-kickoff session, folded in as legitimate prior
   work) — no secrets, no build artifacts.
2. Committed as `ecc6b61`, "Stage 1: scaffold Sauron, a generic
   watch-and-act agent" (23 files, all placeholder/TODO code plus the
   problem statement, eval case list, and rulebook PDF). Did not push —
   not asked to.

### What the agent did — Stage 2 (real baseline implementation)

1. Designed the concrete fixture scenario: a synthetic "Riverside Park
   Tennis Courts" booking-calendar page. Fixed the actual watch config —
   `watch_for` (advanced, full sentence): "a Saturday 9-11am court
   booking for 4 people"; `keyword` (baseline, short literal phrase, a
   separate/narrower input than `watch_for` — see reasoning in
   `baseline/README.md`): "slot available".
2. Wrote 14 real HTML fixtures in `eval/fixtures/` covering content-diff
   cases 01–12 from `eval/CASES.md` (steady state, 3 decoys, real match,
   negation, 3 criteria near-misses, ambiguous FAQ mention, a duplicate
   pair, and a flappy open/closed pair).
3. Implemented `baseline/watcher.py` for real (no more
   `NotImplementedError`): `fetch_page_state` (local file or HTTP),
   `has_changed` (raw text compare), `matches_watch_for` (naive
   case-insensitive substring check against `keyword`), `notify`
   (prints a readable snippet — added `_visible_text()` to strip HTML
   tags after the first CLI run showed a wall of markup), and `run`
   (persists state to a file, catches fetch errors without crashing).
   Added a `--source`/`--state`/`--keyword` CLI entry point.
4. Rewrote `baseline/test_watcher.py` with real test bodies (no more
   skips) against the fixtures — one test per case, plus fetch-error and
   end-to-end state-persistence tests. Added `baseline/__init__.py` so
   `from baseline.watcher import ...` resolves under pytest.
5. Implemented `eval/run_eval.py`'s baseline path for real: an embedded
   case table (fixture pair + ground-truth label) covering cases 01–11,
   computing precision/recall/false-positive-rate; the advanced path
   still prints "not implemented yet" pending Stage 3.
6. Ran `pip install -r baseline/requirements.txt` then
   `python -m pytest baseline/ -v` — **14/14 passed**. Ran
   `python -m eval.run_eval --solution baseline` —
   `TP=3 FP=5 TN=4 FN=0`, precision 0.38, recall 1.00, false-positive
   rate 0.56, exactly matching the predicted failure shape (perfect
   recall, poor precision on negation/near-miss/FAQ cases).
7. Verified the exact documented CLI command
   (`python -m baseline.watcher --source ... --state ...`) end to end;
   caught a real (cosmetic) bug in the process — the notification dumped
   raw HTML markup and an em-dash garbled under the Windows console's
   default codepage — fixed with `sys.stdout.reconfigure(encoding="utf-8")`
   and a `_visible_text()` tag-stripping helper so notifications read as
   plain text.
8. Updated docs to match reality: `CHANGELOG.md` (new entry with the
   real eval numbers, evidence command, and the explicit target for
   Stage 3 — hold recall at 1.00 while raising precision well above
   0.38), `docs/REPRODUCTION.md` (real Python version, real commands,
   real expected output for baseline; advanced section still TODO),
   `baseline/README.md` (real numbers, and the `keyword`-vs-`watch_for`
   design rationale), `eval/CASES.md` ("Fixed watch config" section
   filled in with the real values; Status section updated), root
   `README.md` (status line, real Quickstart commands).

### Human checkpoint

Stopping here per `CLAUDE.md`'s stage-gate rule — not self-advancing to
Stage 3 even though the next step (advanced) is obvious. Presenting the
Stage 2 result to the user for validation, and confirming whether to
commit Stage 2 before starting Stage 3.

### Outcome

Stage 1 committed (`ecc6b61`). Stage 2 (baseline) fully implemented and
verified: 14/14 tests pass, the CLI runs end-to-end exactly as
documented, and the eval run produces the expected "perfect recall, poor
precision" failure shape that Stage 3's advanced solution is meant to
fix. Nothing about the advanced solution has been implemented yet.

---

## Stage 2 (continued): real deployment, not just an eval harness

### Instructions given (verbatim, user message)

> why doesn't baseline contain the notification parts? windows register
> task? readme deployment instructions? it should still be a deployable
> standalone solution right?

### What the agent did

Confirmed this was a genuine gap, not an intentional scope choice: what
Stage 2 had built so far was detection logic plus an eval harness — the
`notify()` function only ever `print()`ed to a console someone would
have to be actively watching, and there were no scripts or docs for
running it unattended. That doesn't actually solve the stated bottleneck
("they can't watch the page 24/7") even at the baseline tier.

1. Read `C:\Users\bley\tennis-booker`'s `secrets.example.ps1`,
   `run_watcher.ps1`, `register_task.ps1`, `.gitignore`, and the email
   section of `watch_courts.py` to confirm the exact established pattern
   (Gmail SMTP_SSL on port 465 with an App Password;
   `TENNIS_GMAIL_USER`/`TENNIS_GMAIL_APP_PASSWORD`/`TENNIS_NOTIFY_TO` env
   vars sourced from a gitignored `secrets.ps1`; a `run_hidden.vbs`
   wrapper so a Scheduled Task doesn't flash a console window) — CLAUDE.md
   requires reusing this exact pattern for anything needing credentials.
2. Added `notifications.py` (repo root, shared by baseline and, from
   Stage 3, advanced): `console_notify` (default, no credentials) and
   `email_notify` (real Gmail SMTP, `SAURON_`-prefixed env vars mirroring
   tennis-booker's naming convention), plus a `NOTIFIERS` lookup dict for
   the CLI. Added `test_notifications.py` — tests `email_notify`'s
   missing-credentials error path for real, and its SMTP call via a
   monkeypatched `smtplib.SMTP_SSL` (never real network/credentials).
3. Rewired `baseline/watcher.py`'s `notify()`/`run()` to take an
   injectable `notifier` callable (default `console_notify`), and added
   `--notify {console,email}` to the CLI. Added a test proving the
   notifier is genuinely pluggable (nothing hits stdout when a fake
   notifier is injected).
4. Built `deploy/` — `secrets.example.ps1`, `run_watcher.ps1` (loads
   secrets if present, resolves repo root, invokes
   `python -m {baseline|advanced}.watcher`, parameterized so it already
   supports switching to advanced once Stage 3 exists),
   `register_task.ps1` (Windows Scheduled Task registration, forwards
   params through `run_hidden.vbs`), `run_hidden.vbs` (adapted from
   tennis-booker's to forward CLI arguments, which the original didn't
   need), and `README.md` documenting one-off runs, real email setup,
   unattended registration, and the caveat about pointing `-Source` at a
   real site (ToS check, same reasoning already written for the
   automated-holds decision).
5. Updated `.gitignore` (`deploy/secrets.ps1`, `deploy/state.txt`,
   `*.log`) — none of the existing patterns matched `secrets.ps1`.
6. Verified everything for real rather than assuming: parse-checked both
   `.ps1` scripts via `[System.Management.Automation.Language.Parser]::ParseFile`
   (no execution); ran `deploy\run_watcher.ps1` end-to-end against a
   matching fixture with `-Notify console` — fired a real notification
   through the full wrapper (repo-root resolution, secrets-skip logic,
   python invocation) with exit code 0; ran it again with `-Notify email`
   and no `secrets.ps1` present — failed with the intended clear error
   message and exit code 1, not a stack trace.
7. Deliberately did **not** run `register_task.ps1` for real — that
   registers a standing background automation on the user's own machine,
   which the user has always done themselves (tennis-booker's task was
   "registered by the user" per prior memory). Left it ready to run, not
   auto-executed.
8. Updated docs to match: `baseline/README.md` (new "Deployment"
   section), `docs/REPRODUCTION.md` (corrected exact stdout text and test
   count — 14 → 18 — after the notifier rewrite changed the print format;
   added a "Deploy it for real (optional)" section), root `README.md`
   (status line, Quickstart command), `CHANGELOG.md` (new entry —
   evidence: the user's question; change: notifications.py + deploy/;
   result: verified end-to-end, 18/18 passing, detection numbers
   unchanged since this was a delivery-layer gap not a detection one),
   `advanced/approval.py` (one-line note that Stage 3's human-approval
   alert should reuse `notifications.py` rather than building a second
   notification path).

### Human checkpoint

Still Stage 2 — this was filling a real gap the user caught in what was
presented as "done," not starting Stage 3. Presenting the fix back to
the user; Stage 2 commit still pending their go-ahead (asked at the end
of the previous entry, not yet answered).

### Outcome

Baseline is now an actually-deployable standalone tool, not just a
detection-logic-plus-eval-harness: real email delivery, a working
Windows Scheduled Task path, and documentation a judge or the user could
follow from a clean environment — verified end-to-end, not just written.
18/18 tests pass. Detection numbers (precision 0.38 / recall 1.00 / FP
rate 0.56) unchanged, as expected, since this addition was entirely at
the delivery layer.

---

## Stage 2 (continued): hidden-window wrapper moved to advanced; doc scrub

### Instructions given (verbatim, user message)

> i actually want the vbs wrapper to be part of the advanced solution
> since that was a real quality-of-life improvement. also, READMEs
> messaging should be intended for users (and judges more importantly)
> who do not have context on what my projects have been. so referencing
> anything i've done in the past should be reworded. what do you think?

### What the agent did

Agreed with both points and implemented rather than just discussing:
the previous commit had made the hidden-window wrapper shared
infrastructure (`-Solution baseline|advanced` on one `deploy/run_hidden.vbs`),
which diluted a real, demonstrable engineering-quality difference into
something both solutions got for free — and several docs referenced the
author's unrelated local projects (`tennis-booker`, `practice2/`) in a
way that assumes context a judge or user wouldn't have.

1. **Restructuring:** created `advanced/deploy/` — moved
   `run_hidden.vbs` there (fixed its path resolution: now two levels
   deep, so it locates `../../deploy/run_watcher.ps1` via
   `GetParentFolderName` twice), and added `advanced/deploy/README.md`
   explaining why this specific piece is an advanced-only "meaningful
   improvement... in engineering quality" per the rulebook, not shared
   infra. Deleted the old shared `deploy/run_hidden.vbs`.
2. Rewrote `deploy/register_task.ps1` so `-Solution` changes *how* the
   task runs, not just what: `baseline` now invokes PowerShell directly
   (a console window visibly flashes every poll — an honest reflection
   of baseline's "no cleverness" positioning), `advanced` routes through
   `advanced/deploy/run_hidden.vbs` (silent). Task names now
   solution-suffixed (`SauronWatcher-baseline` / `-advanced`) so both
   could coexist.
3. Verified the new vbs path resolution for real: invoked it directly
   via `wscript.exe` (not through a registered task) against a matching
   fixture — resolved paths correctly from its new two-levels-deep
   location, ran the poll, wrote state, exit code 0. Parse-checked the
   rewritten `register_task.ps1`.
4. Noticed and documented a real consequence of the restructuring while
   writing it up: hidden execution only makes sense paired with
   `-Notify email`, since a hidden window's stdout is invisible — added
   that caveat to both `deploy/README.md` and
   `advanced/deploy/README.md` rather than leaving it as a silent trap.
5. **Doc scrub:** grepped the whole repo for `tennis-booker` and
   `practice2`/`practice/` across every `.md` file. Reworded every
   judge/user-facing hit — `README.md` (dropped the practice-folder
   mention entirely, since those folders are gitignored and invisible to
   a judge cloning the repo anyway), `PROBLEM_STATEMENT.md` (two spots —
   the tennis-court domain-familiarity aside, and the auto_expire
   motivating scenario, both reworded to stand on their own without
   naming another project), `baseline/README.md`, `deploy/README.md`,
   `docs/REPRODUCTION.md`, `CHANGELOG.md` (both entries). Deliberately
   left `CLAUDE.md` (agent process instructions, not product messaging)
   and `trajectories/session-trajectory.md` (the required agent-process
   deliverable, where naming a source project is honest transparency,
   not an assumed-context problem) unchanged — the user's ask was
   specifically about README-style messaging.
6. Added a new `CHANGELOG.md` entry for this restructuring (evidence:
   the user's feedback, quoted; change: what moved; result: verified
   path resolution, and why this is now a real demo-video-visible
   contrast rather than a hidden implementation detail).
7. Re-ran the full test suite — still 18/18 passing, confirming the
   restructuring didn't touch any tested code path (it was
   deployment-script-only).

### Human checkpoint

Still Stage 2. Presenting the restructuring and scrub back to the user;
the same two questions from before this detour remain open: does this
match what they wanted, and is Stage 2 ready to commit.

### Outcome

The hidden-window wrapper is now a real, attributable advanced-solution
improvement instead of shared infrastructure both solutions got for
free — and every judge/user-facing doc stands on its own without
requiring knowledge of the author's other projects, while the
process-transparency mentions in `trajectories/` (where that context is
actually appropriate) were left intact.

---

## Stage 2 (continued): config.ps1 for the user's real watch target

### Instructions given (verbatim, user message)

> shouldn't the editable args also be secrets so that the user can
> point it to whatever page they need watched when they register the
> task?

### What the agent did

Agreed this was a real gap: `-Source`/`-Notify`/`-IntervalMinutes` had
to be retyped as CLI args on every registration, easy to forget, not
persisted, and risked someone hardcoding a real personal target URL
into a tracked file out of impatience. Distinguished the ask from
literally merging into `secrets.ps1` — that file's name and existing
convention mean "credentials," so mixing in a non-sensitive personal
target would confuse a future reader — and instead added a sibling
gitignored file with the identical dot-sourced mechanism, kept
conceptually separate.

1. Added `deploy/config.example.ps1` (committed template) /
   `deploy/config.ps1` (gitignored, added to `.gitignore` alongside
   `secrets.ps1`) — `$env:SAURON_SOURCE`, `$env:SAURON_NOTIFY`,
   `$env:SAURON_INTERVAL_MINUTES`.
2. Updated `deploy/run_watcher.ps1`: dot-sources `config.ps1` if
   present, then resolves `$Source`/`$Notify` from it via
   `$PSBoundParameters.ContainsKey(...)` checks — an explicit CLI arg
   always wins, otherwise config.ps1's value, otherwise the original
   hardcoded fixture default. Moved this resolution *before* the
   secrets.ps1/email check so a `$Notify` value coming from config.ps1
   (not just from the CLI) still triggers the friendly
   missing-credentials error instead of failing deeper inside Python.
3. Redesigned `deploy/register_task.ps1` rather than just mirroring the
   same pattern: realized baking a resolved `-Source` into the
   registered task's action string at registration time would mean
   editing `config.ps1` later wouldn't take effect without
   re-registering. Changed so `-Source`/`-Notify` are only forwarded
   into the task's action if explicitly passed *to register_task.ps1
   itself*; left unset, the task's action omits them entirely and
   `run_watcher.ps1` resolves them fresh from `config.ps1` on every
   single poll. `-IntervalMinutes` is the one value still resolved at
   registration time (from config.ps1 if not overridden), since it's
   genuinely baked into the Scheduled Task trigger and can't be
   deferred.
4. Verified for real: wrote a temporary `deploy/config.ps1` pointing at
   a matching fixture, ran `.\deploy\run_watcher.ps1` with zero
   arguments — correctly resolved `Source`/`Notify` from config and
   fired a real notification; ran it again with an explicit `-Source`
   pointing at a non-matching fixture — confirmed the CLI value won
   over config.ps1 (stayed silent, as expected for that fixture).
   Removed the temporary config.ps1 afterward. Separately verified the
   `$PSBoundParameters` binding logic used in `register_task.ps1` with a
   throwaway scratch script covering all three call shapes (no args,
   `-Source` only, `-Solution`/`-IntervalMinutes` only) before trusting
   it in the real file — confirmed `BoundSource`/`BoundNotify` correctly
   read `False` when omitted rather than erroring on the unset,
   no-default `[ValidateSet]` string params.
5. Updated `deploy/README.md` with a new "Pointing it at your own real
   page (config.ps1)" section, and updated the "Running unattended"
   examples to show the now-possible bare `.\deploy\register_task.ps1
   -Solution baseline` form alongside the explicit-override form.
6. Re-ran the full test suite (still 18/18 — this was deployment-script
   only) and checked `git status` to confirm no test artifacts
   (`config.ps1`, `state.txt`) were left behind.

### Human checkpoint

Still Stage 2. Three rounds of user-caught gaps now folded in
(deployment/notifications, vbs-to-advanced attribution, config.ps1) —
presenting back to the user; commit still pending their go-ahead.

### Outcome

Registering a scheduled task (or running a one-off poll) against a real,
personal page no longer requires typing it as a command-line argument or
risking it landing in a tracked file: `config.ps1` holds it, gitignored,
separate from credentials, resolved fresh on every poll so it can be
edited without re-registering. Verified end-to-end, not just written.

---

## Stage 2 (continued): keyword was missing from the deploy layer entirely

### Instructions given (verbatim, user message)

> shouldn't keyword also be in the configs file?

### What the agent did

Checked `deploy/run_watcher.ps1` against `baseline/watcher.py`'s actual
CLI and found a real gap, not just a missing config option: the
PowerShell wrapper never exposed `--keyword` at all — it silently
fell back to Python's own hardcoded default (`"slot available"`) no
matter what, so there was no way to deploy against a real page with a
different match phrase except bypassing the wrapper scripts and calling
`python -m baseline.watcher` directly.

1. Added `-Keyword` to both `deploy/run_watcher.ps1` and
   `deploy/register_task.ps1`, following the exact precedence pattern
   already established for `Source`/`Notify`: explicit CLI arg > `config.ps1`'s
   `$env:SAURON_KEYWORD` > Python's own default.
2. One deliberate care point: `$Keyword` has no PowerShell-side default
   (stays unset/empty if neither CLI nor config.ps1 sets it), and
   `run_watcher.ps1` only appends `--keyword $Keyword` to the Python
   invocation when `$Keyword` is truthy — an empty string would've been
   passed straight through as `--keyword ""`, and an empty substring
   matches every page (`"" in text` is always `True`), which would have
   been a silent, serious false-positive bug. Switched the Python
   invocation from string interpolation to an args array
   (`$pythonArgs = @(...); & $python @pythonArgs`) to make the
   conditional-append clean.
3. Also scoped `Keyword` correctly to baseline only — advanced reasons
   over the full `watch_for` sentence, not a short keyword, so the flag
   is only appended when `$Solution -eq "baseline"`.
4. Verified all three precedence cases for real: (a) no config.ps1, no
   `-Keyword` → falls back to Python's default, fires on a matching
   fixture; (b) `config.ps1` sets `SAURON_KEYWORD="in stock"` (not
   present on the fixture) → correctly stays silent, proving the value
   actually reaches Python rather than being silently dropped; (c)
   explicit `-Keyword "slot available"` on the CLI overrides config.ps1's
   `"in stock"` → fires again. Cleaned up the temporary `config.ps1`
   afterward.
5. Updated `deploy/config.example.ps1` (added `SAURON_KEYWORD`, noted
   baseline-only) and `deploy/README.md`'s config section.
6. Re-ran the full test suite (still 18/18) and confirmed `git status`
   showed no leftover test artifacts.

### Human checkpoint

Still Stage 2. Four rounds of user-caught gaps now folded in
(deployment/notifications, vbs-to-advanced attribution, config.ps1,
keyword). Commit still pending the user's go-ahead.

### Outcome

`deploy/`'s config surface now matches what `baseline/watcher.py`'s CLI
actually supports — nothing silently unreachable through the wrapper
scripts. Caught and fixed a real would-be bug (empty-string keyword
matching everything) before it could ship, by testing the negative case
(a config'd keyword absent from the fixture) rather than only the happy
path.
