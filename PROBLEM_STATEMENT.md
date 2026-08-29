# Problem Statement — Sauron

Chosen from the [micro1 Agentic Workflows Hackathon](micro1%20-%20First%20Hackathon97ce7c5.pdf)
rulebook, which is intentionally open-ended: "Pick a specific and
meaningful problem you understand." This file is the answer to that
prompt, following the rulebook's four framing questions.

**Sauron** — the eye that watches so you don't have to. Point it at a
page, tell it in plain language what you're watching for, say how long
to keep watching and how often to check, and it drafts your next move
the moment a real match shows up — then waits for you to say go.

## 01 — Who has this problem?

Anyone waiting on a rare, unpredictable change on a page that offers no
alert of its own: a slot opening on a public tennis-court reservation
portal, a DMV/visa appointment, a campsite permit, concert tickets going
on sale, a restock. Demoed here against a synthetic public tennis-court
reservation portal — a domain the author has direct, lived experience
with, so the failure modes below are drawn from a real pain point, not
guessed at. The engine itself is generic: `source` (what page),
`watch_for` (a plain-language description of the condition), `auto_expire`
(how long to keep watching), and `poll_interval` (how often) are all
user-supplied config, not hardcoded to booking.

## 02 — What bottleneck makes it worth solving?

The user can't watch the page continuously. Manually checking means
either wasting hours refreshing or missing the window entirely — these
openings are typically claimed within minutes.

### Prior art — why not just use an existing watcher?

This space already has real tools: [changedetection.io](https://changedetection.io)
(open-source, self-hosted, CSS/xpath filters, restock/price detection,
notifies via ~80 channels), **Distill.io** and **Wachete** (browser
extensions that monitor pages and alert), **Visualping**, **Follow That
Page**, and single-purpose trackers like **CamelCamelCamel** for Amazon
prices — plus a long tail of community scripts built specifically for
slot-sniping (recreation.gov bots, Global Entry/visa appointment
finders).

Every one of these does **keyword/CSS-selector/price-threshold matching
on a diff, and stops at a notification.** That leaves three gaps a
plain-language, agentic watcher can close:

1. **No semantic understanding, only substring matching.** A page that
   says *"no slots available"* contains the substring *"slots
   available"* — a keyword-matching tool fires anyway. It can't tell a
   negation, a paraphrase, or an unrelated FAQ mention from a real match.
2. **No criteria disambiguation.** A real opening on the wrong date, at
   the wrong time, or for the wrong party size still trips a keyword
   match. None of these tools take a full description of what you
   actually want and check the specific opening against it.
3. **The user still does all the follow-through by hand**, under time
   pressure, after the alert lands. Nothing drafts the actual next step.

### Auto-expire vs. release date — two different dates, not one

A real watcher needs to eventually stop even if nobody remembers to
cancel it — otherwise it just polls forever once its purpose is clearly
over. That's `auto_expire`'s only job — a **failsafe unregister date**,
decoupled from any timing logic. It exists so a forgotten watcher
doesn't poll forever, not to signal anything about when the awaited
event is likely.

The field that actually drives urgency is a separate, optional
`release_date`: the user's best guess of when the watched-for condition
is expected to become true — e.g. tickets typically go on sale *well
before* the event itself, so `release_date` is the expected on-sale
date, not the concert date. `poll_interval` is a base rate that the
advanced solution can tighten as `release_date` approaches (checking
every 15 minutes for three weeks is wasteful; checking every 15 minutes
in the last hour before a known release is under-responsive) — `auto_expire`
plays no part in that tightening.

The two are related but distinct: `auto_expire` can default to
`release_date + a buffer` (e.g. release_date + 24 hours) when a
`release_date` is set, as a reasonable "shouldn't still be running past
this" upper bound — but the user can always override it, and when
`release_date` is unknown (e.g. a permit portal with no announced
opening) `auto_expire` must be set explicitly and polling stays at the
fixed base rate, since there's no target to tighten around.

## 03 — Does the agent solve it well?

**Baseline** (`baseline/`): a keyword-diff script — a realistic,
standard baseline (this is literally what most of the prior-art tools
above do). Fetches the page, diffs it against the last-seen snapshot,
and fires a plain notification if the diff's new text contains a
substring from `watch_for`. Reasonable and simple — and expected to
visibly fail exactly where the prior-art gap is: negation ("no slots
available"), unrelated mentions, and any real opening that doesn't
actually match the user's full criteria. It also never proposes a next
action and never suppresses a repeat notification for the same
already-seen match.

**Advanced** (`advanced/`): an LLM-agent pipeline —

- **Context:** the full `watch_for` description and structured
  `WatchConfig` (source, auto_expire, poll_interval) are given to the
  agent on every poll, not reduced to a keyword list.
- **Memory:** the agent tracks prior page states, confirmed decoy
  patterns, and matches it has already surfaced — so known noise and
  already-actioned openings stop generating repeat detections.
- **Verification:** before treating a detection as real, a second pass
  re-confirms it against the freshly-fetched page, cutting false
  positives from a transient glitch or stale fetch.
- **Action drafting:** on a confirmed, criteria-matching opening, the
  agent drafts the structured next step (e.g. a reservation request) —
  not just a notification.
- **Human approval gate:** the drafted action is held for explicit human
  approval before a *simulated* submit call ever runs.
- **Deployment quality:** running unattended, advanced polls with no
  visible window at all, versus baseline's plainly-flashing console —
  see `advanced/deploy/README.md`. A small thing, but a real,
  demonstrable engineering-quality difference, and one the rulebook
  explicitly counts as a valid axis for "meaningful improvement."

### On automated holds (ground rule 04)

Many booking sites let you place a temporary, non-final "hold" on a slot.
Sauron never initiates one automatically, even though it's often
technically possible: a hold is still a real action against a real
system affecting real availability for other real people, which makes it
"consequential" under ground rule 04 regardless of whether it's
reversible — and the rule reads as approval *at the moment*, not a
standing pre-authorization. Separately, most booking/ticketing sites'
ToS explicitly prohibit automated interaction and increasingly
CAPTCHA-gate it for exactly this reason (ground rule 03). So Sauron's
scope stops at detect → draft → prompt; `approval.py`'s submit step is
always simulated in this submission, never a live call.

## 04 — Can another person reproduce the result?

Yes, entirely offline. The evaluation runs against a fixed set of
synthetic HTML/text page-state fixtures (`eval/fixtures/`, see
`eval/CASES.md` for the full case list) — never the live network, per
`CLAUDE.md`'s testing rule and the rulebook's ground rule 07. The same
fixture sequence and the same `watch_for` config are given to the
baseline and the advanced solution. `docs/REPRODUCTION.md` gives exact
commands, expected output, and approximate runtime/cost for both, plus
the evaluation.

## Evaluation plan (sketch — full cases in `eval/CASES.md`)

- **Primary metric:** precision/recall over "correctly identified an
  actionable, criteria-matching opening and correctly gated it behind
  human approval," computed across the content-diff cases.
- **Secondary metrics:** false-positive rate (alert fatigue) and human
  time per task (time from a real opening appearing to a drafted action
  being ready for approval) — advanced solution only, since baseline
  never drafts an action.
- **≥10 cases**, including decoys, the negation case (baseline's
  sharpest failure mode), criteria near-misses, a duplicate/memory case,
  and one challenging race case (a slot that opens and closes within a
  single poll interval) — see `eval/CASES.md`. Two additional
  orchestration cases (expiry, adaptive interval) are tested against an
  injected fake clock rather than fixture content.

## Future work (explicitly out of scope for this submission)

- **Browser extension front-end.** Distill.io/Wachete ship this way, and
  it would solve watching pages behind a login for free — but a
  Manifest V3 extension is significant install/permission overhead for a
  judge trying to reproduce the main result from a clean environment
  (rubric criterion: Reproducibility). Kept as a CLI/service for this
  submission; noted here per ground rule 02 (what existed vs. what was
  added).
- **Live-site holds**, if ever pursued, would need a per-instance live
  human click (not a standing setting) and a per-site ToS check — see
  "On automated holds" above.
