"""Notification channels for Sauron, shared by baseline/ and advanced/.

Injectable so a watch loop never hardcodes a transport: `console_notify`
is the safe default (used by tests and eval — no credentials, no
network). `email_notify` sends a real email and needs SMTP credentials
from the environment, following this repo's credentials pattern (see
CLAUDE.md): a committed secrets.example.ps1 template, a gitignored
secrets.ps1 that's dot-sourced into $env: vars, code reads only from
os.environ. Mirrors the exact mechanism already deployed for
`tennis-booker` (Gmail SMTP_SSL + an App Password), just with
SAURON_-prefixed variable names for this project.
"""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


def console_notify(subject: str, body: str) -> None:
    """Print the notification. Default — no credentials, no network,
    safe for tests and eval.
    """
    print(f"[Sauron] {subject}\n{body}")


def email_notify(subject: str, body: str) -> None:
    """Send the notification by email via Gmail SMTP.

    Reads SAURON_GMAIL_USER, SAURON_GMAIL_APP_PASSWORD, and
    SAURON_NOTIFY_TO from the environment (populate via secrets.ps1, see
    secrets.example.ps1). Raises a clear RuntimeError rather than
    silently failing to notify when credentials are missing.
    """
    email_from = os.environ.get("SAURON_GMAIL_USER")
    app_password = os.environ.get("SAURON_GMAIL_APP_PASSWORD")
    if not email_from or not app_password:
        raise RuntimeError(
            "SAURON_GMAIL_USER / SAURON_GMAIL_APP_PASSWORD environment "
            "variables are not set -- cannot send email. Copy "
            "secrets.example.ps1 to secrets.ps1, fill in your Gmail App "
            "Password, and dot-source it before running."
        )
    to_addrs = [
        addr.strip()
        for addr in os.environ.get("SAURON_NOTIFY_TO", email_from).split(",")
        if addr.strip()
    ]

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = email_from
    message["To"] = ", ".join(to_addrs)
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_from, app_password)
        server.sendmail(email_from, to_addrs, message.as_string())


NOTIFIERS = {
    "console": console_notify,
    "email": email_notify,
}
