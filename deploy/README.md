# Deployment

Everything under `baseline/`, `advanced/`, and `eval/` is enough to
reproduce the *measured result* (the eval comparison) from a clean
environment — that path stays offline against fixtures, per `CLAUDE.md`'s
testing rule and the rulebook's ground rule 07 (advanced's real,
non-`--fake` eval run is the one exception — see
[`../docs/REPRODUCTION.md`](../docs/REPRODUCTION.md)'s "Approx cost").
This folder is the separate, opt-in piece that makes Sauron an
actually-deployable, standalone tool: a real poll loop and real
unattended notification delivery, not just a detection function.

The core scheduling/notification machinery here (`run_watcher.ps1`,
`secrets.example.ps1`, credential handling) is shared by both
`baseline/` and `advanced/`. One piece is *not* shared —
[`../advanced/deploy/`](../advanced/deploy/)'s hidden-window execution
wrapper is advanced-only by design; see "Running unattended" below and
[`../advanced/deploy/README.md`](../advanced/deploy/README.md).

## baseline and advanced take different config shapes

`run_watcher.ps1` branches on `-Solution` rather than pretending
they're the same:

- `baseline` — `-Source` (a page) + `-Keyword` (a short literal phrase).
- `advanced` — `-ConfigPath` (a `WatchConfig` JSON: source, watch_for,
  release_date, auto_expire, poll_interval — see
  [`../advanced/watch_config.example.json`](../advanced/watch_config.example.json))
  + `-MemoryPath` (its cross-poll memory file).

## Two notification channels

- `console` (default): `print()`s. No credentials, no network — this is
  what the tests and `eval/run_eval.py` use.
- `email`: real Gmail SMTP delivery, via
  [`../notifications.py`](../notifications.py)'s `email_notify`. Needs
  credentials (see below).

Advanced additionally needs `ANTHROPIC_API_KEY` regardless of the
notify channel — its semantic detection is a real LLM call, the one
dependency it has that baseline doesn't (see
[`../docs/REPRODUCTION.md`](../docs/REPRODUCTION.md)'s "Approx cost").

## One-off run

```powershell
.\deploy\run_watcher.ps1 -Solution baseline -Source "eval\fixtures\05-real-match.html" -Notify console
.\deploy\run_watcher.ps1 -Solution advanced -ConfigPath "advanced\watch_config.example.json" -Notify console
```

Runs a single poll and exits — this is what a Scheduled Task actually
invokes on each trigger (see below), not a long-running loop, so state
persists to `deploy\state.txt` (and, for advanced, `deploy\advanced_memory.json`
— both gitignored) between invocations rather than in memory.

## Real (email) notifications, and advanced's API key

1. Copy `secrets.example.ps1` to `secrets.ps1` in this folder (gitignored,
   never committed — see `CLAUDE.md`'s credentials pattern).
2. For email: fill in a Gmail address and a 16-character
   [Gmail App Password](https://myaccount.google.com/apppasswords) (not
   your normal password).
3. For advanced: fill in `ANTHROPIC_API_KEY`.
4. Run with `-Notify email`:
   ```powershell
   .\deploy\run_watcher.ps1 -Solution baseline -Source "eval\fixtures\05-real-match.html" -Notify email
   ```
   Delete `deploy\state.txt` first if you want to force a fresh "first
   poll" (which always counts as changed) rather than needing the source
   to actually differ from last time.

Missing `secrets.ps1` while requesting `-Notify email`, or missing
`ANTHROPIC_API_KEY` while running `-Solution advanced`, both fail with a
clear message rather than crashing or silently not notifying.

## Pointing it at your own real page (config.ps1)

`-Source`/`-Notify`/`-Keyword` (baseline) and `-ConfigPath` (advanced)
don't have to be typed on the command line every time. Copy
`config.example.ps1` to `config.ps1` in this folder (gitignored,
separate from `secrets.ps1` — this holds your personal watch target, not
credentials) and fill in your real page:

```powershell
$env:SAURON_SOURCE = "https://your-real-target.example.com/booking"   # baseline only
$env:SAURON_NOTIFY = "email"
$env:SAURON_KEYWORD = "in stock"      # baseline only
$env:SAURON_CONFIG_PATH = "advanced\my_watch_config.json"   # advanced only -- copy watch_config.example.json and edit it
$env:SAURON_INTERVAL_MINUTES = "15"
```

With `config.ps1` in place:

```powershell
.\deploy\run_watcher.ps1 -Solution baseline    # resolves Source/Notify/Keyword from config.ps1
.\deploy\run_watcher.ps1 -Solution advanced    # resolves ConfigPath/Notify from config.ps1
.\deploy\register_task.ps1 -Solution baseline  # same resolution, at registration
.\deploy\register_task.ps1 -Solution advanced
```

An explicit CLI flag always overrides `config.ps1` for that one call
(e.g. `-Source "eval\fixtures\00-baseline.html" -Keyword "slot available"`
to run a one-off test against a fixture even with `config.ps1` filled
in) — and there's no ambiguity about "unset": an empty `-Keyword` is
never sent to Python as `--keyword ""`, since an empty substring would
match every page. `IntervalMinutes` is resolved once, at registration
time, since it's baked into the Scheduled Task trigger — everything
else is resolved fresh by `run_watcher.ps1` on *every* poll, so editing
`config.ps1` later takes effect on the task's next run without
re-registering it.

## Running unattended (Windows Scheduled Task)

With `config.ps1` filled in (see above), registering is just:

```powershell
.\deploy\register_task.ps1 -Solution baseline
.\deploy\register_task.ps1 -Solution advanced
```

Or override for this one registration without touching `config.ps1`:

```powershell
.\deploy\register_task.ps1 -Solution baseline -Source "eval\fixtures\00-baseline.html" -Notify console -IntervalMinutes 15
.\deploy\register_task.ps1 -Solution advanced -ConfigPath "advanced\watch_config.example.json" -Notify email -IntervalMinutes 15
```

`-Solution` changes *how* the task runs, not just what it runs:

- `baseline` invokes PowerShell directly, so a console window visibly
  flashes on-screen every poll — functional, if a little annoying; an
  honest reflection of baseline's "simplest correct solution, no
  cleverness" positioning (see `../baseline/README.md`).
- `advanced` routes through
  [`../advanced/deploy/run_hidden.vbs`](../advanced/deploy/run_hidden.vbs)
  instead, so it polls silently with no visible window at all — one of
  advanced's own engineering-quality improvements, not shared with
  baseline (see `../advanced/deploy/README.md`).

Pair `advanced` + hidden execution with `-Notify email`, not `console` —
a hidden window's stdout is invisible, so `-Notify console` in the
background is equivalent to notifying no one. `advanced` also needs
`ANTHROPIC_API_KEY` in `secrets.ps1` for the task to do anything on each
poll (see above).

Manage a registered task with `Get-ScheduledTask -TaskName
SauronWatcher-baseline` (or `-advanced`),
`Start-ScheduledTask -TaskName <name>`, or remove it with
`Unregister-ScheduledTask -TaskName <name> -Confirm:$false`.

**This repo doesn't register a live task itself** — that's a standing
background automation on *your* machine. Run the commands above when
you actually want one running.

## Pointing this at a real page instead of a fixture

Everything above defaults to a local fixture file, which never changes
on its own — fine for proving the loop and notification path genuinely
work end-to-end, but it'll never actually fire after the first poll. To
watch something real:

```powershell
.\deploy\run_watcher.ps1 -Solution baseline -Source "https://example.com/booking-page" -Notify email
```

For advanced, copy `advanced\watch_config.example.json` to your own
file and edit its `"source"` field to a real URL, then point
`-ConfigPath` (or `config.ps1`'s `SAURON_CONFIG_PATH`) at it.

Two things to check first, both already covered in
[`../PROBLEM_STATEMENT.md`](../PROBLEM_STATEMENT.md):

- The target site's terms of service — many booking/ticketing sites
  restrict automated polling, not just automated booking.
- This still only *detects and drafts*; baseline's keyword match has
  the documented false-positive problems in
  [`../eval/CASES.md`](../eval/CASES.md), and no solution in this repo
  ever submits or holds anything automatically (see
  PROBLEM_STATEMENT.md's "On automated holds").
