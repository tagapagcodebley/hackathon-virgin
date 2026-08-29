# Copy this file to secrets.ps1 (same deploy/ folder) and fill in your
# values. secrets.ps1 is loaded by deploy/run_watcher.ps1 and is NOT
# meant to be shared/committed — see deploy/README.md and CLAUDE.md's
# credentials pattern. Only needed if you want real email delivery
# (-Notify email); console notifications need no credentials at all.

$env:SAURON_GMAIL_USER = "your.gmail.address@gmail.com"
$env:SAURON_GMAIL_APP_PASSWORD = "xxxxxxxxxxxxxxxx"   # 16-char Gmail App Password, no spaces
$env:SAURON_NOTIFY_TO = "example@gmail.com, example2@gmail.com"  # comma-separated list of email addresses to notify
