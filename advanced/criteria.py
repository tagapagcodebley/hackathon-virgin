"""WatchConfig -- the generic, user-supplied config given to the detector
agent on every poll: what page, what to watch for (plain language), and
two distinct dates that must not be conflated (see
PROBLEM_STATEMENT.md's "Auto-expire vs. release date"):

- `release_date` drives urgency/adaptive polling.
- `auto_expire` is a failsafe unregister date, unrelated to timing.

Not baked into a booking-specific schema -- the tennis-court demo is one
instance of this, not the shape itself.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

DEFAULT_AUTO_EXPIRE_BUFFER = timedelta(hours=24)


@dataclass
class WatchConfig:
    source: str
    watch_for: str
    auto_expire: datetime
    poll_interval: timedelta = timedelta(minutes=15)
    release_date: Optional[datetime] = None


def load_config(path: str) -> WatchConfig:
    """Load a WatchConfig from a JSON file.

    Expected shape (see advanced/watch_config.example.json):
        {
          "source": "...",
          "watch_for": "...",
          "release_date": "2026-09-05T00:00:00" | null,
          "auto_expire": "2026-09-06T00:00:00" | null,
          "poll_interval_minutes": 15
        }

    `auto_expire` may be omitted/null when `release_date` is set, in
    which case it defaults via default_auto_expire(). It's an error to
    omit both -- there's no safe default without a reference date.
    """
    # utf-8-sig transparently strips a UTF-8 BOM if present (common in
    # JSON files saved by Windows editors/PowerShell's own Set-Content)
    # and behaves identically to plain utf-8 otherwise.
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)

    release_date = (
        datetime.fromisoformat(data["release_date"]) if data.get("release_date") else None
    )
    raw_auto_expire = data.get("auto_expire")
    if raw_auto_expire:
        auto_expire = datetime.fromisoformat(raw_auto_expire)
    else:
        auto_expire = default_auto_expire(release_date)
        if auto_expire is None:
            raise ValueError(
                f"{path}: auto_expire is required when release_date is not set -- "
                "there's no safe default without a reference date."
            )

    poll_interval = timedelta(minutes=data.get("poll_interval_minutes", 15))

    return WatchConfig(
        source=data["source"],
        watch_for=data["watch_for"],
        auto_expire=auto_expire,
        poll_interval=poll_interval,
        release_date=release_date,
    )


def default_auto_expire(
    release_date: Optional[datetime],
    buffer: timedelta = DEFAULT_AUTO_EXPIRE_BUFFER,
) -> Optional[datetime]:
    """Return `release_date + buffer` as a suggested failsafe default
    when `release_date` is known. Returns None when release_date is
    None, in which case the caller must supply auto_expire explicitly --
    there's no safe default without a reference date.
    """
    if release_date is None:
        return None
    return release_date + buffer
