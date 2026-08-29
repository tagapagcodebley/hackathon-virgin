# Copy this file to secrets.ps1 (same deploy/ folder) and fill in your
# values. secrets.ps1 is loaded by deploy/run_watcher.ps1 and is NOT
# meant to be shared/committed — see deploy/README.md and CLAUDE.md's
# credentials pattern.

# Only needed for real email delivery (-Notify email); console
# notifications need no credentials at all.
$env:SAURON_GMAIL_USER = "your.gmail.address@gmail.com"
$env:SAURON_GMAIL_APP_PASSWORD = "xxxxxxxxxxxxxxxx"   # 16-char Gmail App Password, no spaces
$env:SAURON_NOTIFY_TO = "example@gmail.com, example2@gmail.com"  # comma-separated list of email addresses to notify

# Only needed for -Solution advanced (its semantic detection is a real
# Anthropic API call — this is the one dependency advanced has that
# baseline doesn't, see docs/REPRODUCTION.md's "Approx cost").
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# Only needed if the key above is "identity-linked" (issued against a
# specific workspace/account rather than a standalone developer key) --
# such keys are rejected with a 400 error asking for this. A standard
# API key works fine without it; only uncomment if you hit that error.
# Find it in the Anthropic Console under your workspace's settings.
# $env:ANTHROPIC_WORKSPACE_ID = "..."
