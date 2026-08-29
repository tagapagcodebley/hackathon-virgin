"""Tests for advanced/memory.py. No network -- pure local persistence."""

from __future__ import annotations

from advanced.memory import WatcherMemory


def test_decoy_round_trip(tmp_path):
    path = str(tmp_path / "memory.json")
    memory = WatcherMemory(path)
    assert memory.is_known_decoy("some text") is False
    memory.record_decoy("some text")
    assert memory.is_known_decoy("some text") is True


def test_surfaced_match_round_trip(tmp_path):
    path = str(tmp_path / "memory.json")
    memory = WatcherMemory(path)
    assert memory.is_already_surfaced("a real match") is False
    memory.record_surfaced_match("a real match")
    assert memory.is_already_surfaced("a real match") is True


def test_persists_across_instances(tmp_path):
    path = str(tmp_path / "memory.json")
    first = WatcherMemory(path)
    first.record_decoy("decoy text")
    first.record_surfaced_match("match text")
    first.save()

    second = WatcherMemory(path)
    assert second.is_known_decoy("decoy text") is True
    assert second.is_already_surfaced("match text") is True


def test_missing_file_starts_empty(tmp_path):
    path = str(tmp_path / "does-not-exist.json")
    memory = WatcherMemory(path)
    assert memory.is_known_decoy("anything") is False
    assert memory.is_already_surfaced("anything") is False
