"""WatchConfig — the generic, user-supplied config given to the detector
agent on every poll: what page, what to watch for (plain language), and
two distinct dates that must not be conflated (see
PROBLEM_STATEMENT.md's "Auto-expire vs. release date"):

- `release_date` drives urgency/adaptive polling.
- `auto_expire` is a failsafe unregister date, unrelated to timing.

Not baked into a booking-specific schema — the tennis-court demo is one
instance of this, not the shape itself.

Stage 1 scaffolding only.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

DEFAULT_AUTO_EXPIRE_BUFFER = timedelta(hours=24)


@dataclass
class WatchConfig:
    """TODO: fields —

    - source: str — URL in production, fixture path in tests/eval.
    - watch_for: str — plain-language description of the condition to
      detect, e.g. "a Saturday 9-11am court booking for 4 people". This
      is what the advanced detector reasons over semantically, and what
      the baseline reduces to a keyword substring match.
    - release_date: datetime | None — the user's best guess of when the
      watched-for condition is expected to become true (e.g. an expected
      ticket on-sale date, NOT the concert date itself — tickets go on
      sale well before the event). Optional: unknown for something like
      a permit portal with no announced opening. Drives adaptive polling
      (see watcher.next_poll_interval) — has no bearing on auto_expire.
    - auto_expire: datetime — a failsafe unregister date. Purely a
      safety net so a forgotten watcher doesn't poll forever; carries no
      timing signal of its own. Required. Defaults to
      `release_date + DEFAULT_AUTO_EXPIRE_BUFFER` when release_date is
      set (see default_auto_expire below); must be set explicitly
      otherwise.
    - poll_interval: timedelta — base polling rate, used unmodified when
      release_date is unset or far away. Baseline always uses this value
      unmodified regardless of release_date.
    """

    # TODO: source: str
    # TODO: watch_for: str
    # TODO: release_date: datetime | None
    # TODO: auto_expire: datetime
    # TODO: poll_interval: timedelta


def load_config(path: str) -> WatchConfig:
    """TODO: load a WatchConfig from a config file (JSON/YAML)."""
    raise NotImplementedError


def default_auto_expire(
    release_date: datetime | None,
    buffer: timedelta = DEFAULT_AUTO_EXPIRE_BUFFER,
) -> datetime | None:
    """TODO: return `release_date + buffer` as a suggested failsafe
    default when `release_date` is known. Returns None when
    release_date is None, in which case the caller must supply
    auto_expire explicitly — there's no safe default without a
    reference date.
    """
    raise NotImplementedError
