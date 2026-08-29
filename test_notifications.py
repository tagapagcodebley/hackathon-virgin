"""Tests for notifications.py. Never touches real SMTP or the live
network (see CLAUDE.md's testing rule) — email_notify's SMTP client is
monkeypatched.
"""

from __future__ import annotations

import pytest

import notifications


def test_console_notify_prints(capsys):
    notifications.console_notify("Subject", "Body text")
    captured = capsys.readouterr()
    assert "Subject" in captured.out
    assert "Body text" in captured.out


def test_email_notify_raises_clear_error_without_credentials(monkeypatch):
    monkeypatch.delenv("SAURON_GMAIL_USER", raising=False)
    monkeypatch.delenv("SAURON_GMAIL_APP_PASSWORD", raising=False)
    with pytest.raises(RuntimeError, match="SAURON_GMAIL_USER"):
        notifications.email_notify("Subject", "Body")


def test_email_notify_sends_via_smtp(monkeypatch):
    monkeypatch.setenv("SAURON_GMAIL_USER", "sauron@example.com")
    monkeypatch.setenv("SAURON_GMAIL_APP_PASSWORD", "fake-app-password")
    monkeypatch.setenv("SAURON_NOTIFY_TO", "user@example.com, second@example.com")

    sent = {}

    class FakeSMTP:
        def __init__(self, host, port):
            sent["host"] = host
            sent["port"] = port

        def __enter__(self):
            return self

        def __exit__(self, *exc_info):
            return False

        def login(self, user, password):
            sent["login"] = (user, password)

        def sendmail(self, from_addr, to_addrs, message_string):
            sent["from_addr"] = from_addr
            sent["to_addrs"] = to_addrs
            sent["message_string"] = message_string

    monkeypatch.setattr(notifications.smtplib, "SMTP_SSL", FakeSMTP)

    notifications.email_notify("A real opening", "Saturday 9-11am is open")

    assert sent["host"] == "smtp.gmail.com"
    assert sent["login"] == ("sauron@example.com", "fake-app-password")
    assert sent["from_addr"] == "sauron@example.com"
    assert sent["to_addrs"] == ["user@example.com", "second@example.com"]
    assert "A real opening" in sent["message_string"]
    assert "Saturday 9-11am is open" in sent["message_string"]
