# Copy this file to config.ps1 (same deploy/ folder) and fill in your
# real watch target. Optional — everything already has a safe,
# fixture-based default, so Sauron runs out of the box without this
# file. This is what lets a *registered scheduled task* point at your
# own real page without typing it as a command-line argument every
# time — and without ever committing a real, personal target URL into a
# tracked file. config.ps1 is gitignored, same as secrets.ps1, but it's
# a separate file: secrets.ps1 is credentials, this is just your
# personal deployment target — keeping them apart means a reader of
# secrets.ps1 doesn't have to wonder whether a URL in there is sensitive.

$env:SAURON_SOURCE = "https://example.com/your-real-booking-page"   # baseline only
$env:SAURON_NOTIFY = "email"          # "console" or "email"
$env:SAURON_KEYWORD = "in stock"      # baseline only -- the short phrase it substring-matches on (advanced reasons over watch_for instead, see PROBLEM_STATEMENT.md)
$env:SAURON_CONFIG_PATH = "advanced\my_watch_config.json"   # advanced only -- your own WatchConfig JSON (copy advanced\watch_config.example.json and edit source/watch_for/release_date/auto_expire)
$env:SAURON_INTERVAL_MINUTES = "15"   # only used by register_task.ps1
