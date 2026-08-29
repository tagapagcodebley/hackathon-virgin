# Wrapper invoked by the scheduled task (see register_task.ps1). Loads
# config.ps1 (your real watch target, if present) and secrets.ps1
# (credentials, if present) into the environment, then runs a single
# poll, persisting state to $StatePath.
#
# baseline and advanced take genuinely different config shapes -- this
# script branches on -Solution rather than pretending they're the same:
#   baseline  -> --source (a page) + --keyword (a short literal phrase)
#   advanced  -> --config (a WatchConfig JSON: source, watch_for,
#                release_date, auto_expire, poll_interval) + --memory
#                (its cross-poll memory file)
#
# Precedence for $Source/$Notify/$Keyword/$ConfigPath: an explicit CLI
# arg always wins; then config.ps1's matching $env:SAURON_* variable;
# then the built-in defaults below. This means a registered task can
# point at your own real page (and match phrase, or config file) just by
# having config.ps1 filled in -- no need to type it as a command-line
# argument every time.
#
# $Keyword only applies to -Solution baseline (advanced reasons over the
# full watch_for sentence in its config, not a short keyword). Left
# unset here on purpose: an empty string would be passed straight
# through to Python as --keyword "", and an empty substring matches
# every page, so "unset" has to mean "don't pass the flag at all," not
# "pass an empty one."
#
# Params can still be overridden at the call site for a one-off run, e.g.:
#   .\run_watcher.ps1 -Solution baseline -Source "https://example.com/booking" -Notify email -Keyword "in stock"
#   .\run_watcher.ps1 -Solution advanced -ConfigPath "advanced\watch_config.example.json" -Notify email

param(
    [ValidateSet("baseline", "advanced")]
    [string]$Solution = "baseline",
    [string]$Source = "eval\fixtures\00-baseline.html",
    [string]$StatePath = "deploy\state.txt",
    [ValidateSet("console", "email")]
    [string]$Notify = "console",
    [string]$Keyword,
    [string]$ConfigPath = "advanced\watch_config.example.json",
    [string]$MemoryPath = "deploy\advanced_memory.json"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -Path $repoRoot

$configPsPath = Join-Path $PSScriptRoot "config.ps1"
if (Test-Path $configPsPath) {
    . $configPsPath
}
if (-not $PSBoundParameters.ContainsKey('Source') -and $env:SAURON_SOURCE) {
    $Source = $env:SAURON_SOURCE
}
if (-not $PSBoundParameters.ContainsKey('Notify') -and $env:SAURON_NOTIFY) {
    $Notify = $env:SAURON_NOTIFY
}
if (-not $PSBoundParameters.ContainsKey('Keyword') -and $env:SAURON_KEYWORD) {
    $Keyword = $env:SAURON_KEYWORD
}
if (-not $PSBoundParameters.ContainsKey('ConfigPath') -and $env:SAURON_CONFIG_PATH) {
    $ConfigPath = $env:SAURON_CONFIG_PATH
}

$secretsPath = Join-Path $PSScriptRoot "secrets.ps1"
if (Test-Path $secretsPath) {
    . $secretsPath
} elseif ($Notify -eq "email") {
    Write-Error "secrets.ps1 not found. Copy deploy\secrets.example.ps1 to deploy\secrets.ps1 and fill in your Gmail App Password, or run with -Notify console."
    exit 1
}

if ($Solution -eq "advanced" -and -not $env:ANTHROPIC_API_KEY) {
    Write-Error "ANTHROPIC_API_KEY not set. Copy deploy\secrets.example.ps1 to deploy\secrets.ps1 and fill in your Anthropic API key -- advanced's semantic detection is a real LLM call and needs it."
    exit 1
}

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$python = if (Test-Path $venvPython) { $venvPython } else { "python" }

if ($Solution -eq "advanced") {
    $pythonArgs = @("-m", "advanced.watcher", "--config", $ConfigPath, "--state", $StatePath, "--memory", $MemoryPath, "--notify", $Notify)
} else {
    $pythonArgs = @("-m", "baseline.watcher", "--source", $Source, "--state", $StatePath, "--notify", $Notify)
    if ($Keyword) {
        $pythonArgs += @("--keyword", $Keyword)
    }
}

& $python @pythonArgs
