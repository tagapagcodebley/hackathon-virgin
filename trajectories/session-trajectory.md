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
