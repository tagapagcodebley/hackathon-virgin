"""Tests for advanced/criteria.py. No network, no LLM calls -- pure
config parsing.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta

import pytest

from advanced.criteria import default_auto_expire, load_config


def write_config(tmp_path, **overrides):
    data = {
        "source": "eval/fixtures/00-baseline.html",
        "watch_for": "a Saturday 9-11am court booking for 4 people",
        "release_date": None,
        "auto_expire": "2026-09-28T00:00:00",
        "poll_interval_minutes": 15,
    }
    data.update(overrides)
    path = tmp_path / "config.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


def test_load_config_reads_fields(tmp_path):
    path = write_config(tmp_path)
    config = load_config(path)
    assert config.source == "eval/fixtures/00-baseline.html"
    assert config.watch_for == "a Saturday 9-11am court booking for 4 people"
    assert config.release_date is None
    assert config.auto_expire == datetime(2026, 9, 28)
    assert config.poll_interval == timedelta(minutes=15)


def test_load_config_parses_release_date(tmp_path):
    path = write_config(tmp_path, release_date="2026-09-05T12:00:00")
    config = load_config(path)
    assert config.release_date == datetime(2026, 9, 5, 12, 0, 0)


def test_load_config_defaults_auto_expire_from_release_date(tmp_path):
    path = write_config(tmp_path, release_date="2026-09-05T00:00:00", auto_expire=None)
    config = load_config(path)
    assert config.auto_expire == datetime(2026, 9, 6)  # +24h buffer


def test_load_config_requires_auto_expire_without_release_date(tmp_path):
    path = write_config(tmp_path, release_date=None, auto_expire=None)
    with pytest.raises(ValueError, match="auto_expire is required"):
        load_config(path)


def test_default_auto_expire_none_without_release_date():
    assert default_auto_expire(None) is None


def test_default_auto_expire_adds_buffer():
    release = datetime(2026, 9, 5)
    assert default_auto_expire(release) == release + timedelta(hours=24)
    assert default_auto_expire(release, buffer=timedelta(hours=2)) == release + timedelta(hours=2)


def test_load_config_handles_utf8_bom(tmp_path):
    """Windows editors (Notepad, PowerShell's own Set-Content) commonly
    write a UTF-8 BOM -- a real config file a user saves could easily
    have one.
    """
    data = {
        "source": "eval/fixtures/00-baseline.html",
        "watch_for": "a Saturday 9-11am court booking for 4 people",
        "auto_expire": "2026-09-28T00:00:00",
    }
    path = tmp_path / "config.json"
    path.write_bytes(b"\xef\xbb\xbf" + json.dumps(data).encode("utf-8"))
    config = load_config(str(path))
    assert config.source == "eval/fixtures/00-baseline.html"
