# Wrapper invoked by the scheduled task (see register_task.ps1). Loads
# config.ps1 (your real watch target, if present) and secrets.ps1 (Gmail
# creds, if present) into the environment, then runs a single poll
# against the effective $Source, persisting state to $StatePath.
#
# Precedence for $Source/$Notify/$Keyword: an explicit CLI arg always
# wins; then config.ps1's $env:SAURON_SOURCE / $env:SAURON_NOTIFY /
# $env:SAURON_KEYWORD; then baseline/watcher.py's own built-in default
# for Keyword (Source/Notify still fall back to the fixture defaults
# below). This means a registered task can point at your own real page
# and its match phrase just by having config.ps1 filled in — no need to
# type either as a command-line argument every time.
#
# $Keyword only applies to -Solution baseline (advanced reasons over the
# full watch_for sentence, not a short keyword — see PROBLEM_STATEMENT.md).
# Left unset here on purpose: an empty string would be passed straight
# through to Python as --keyword "", and an empty substring matches
# every page, so "unset" has to mean "don't pass the flag at all," not
# "pass an empty one."
#
# Params can still be overridden at the call site for a one-off run, e.g.:
#   .\run_watcher.ps1 -Solution baseline -Source "https://example.com/booking" -Notify email -Keyword "in stock"

param(
    [ValidateSet("baseline", "advanced")]
    [string]$Solution = "baseline",
    [string]$Source = "eval\fixtures\00-baseline.html",
    [string]$StatePath = "deploy\state.txt",
    [ValidateSet("console", "email")]
    [string]$Notify = "console",
    [string]$Keyword
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -Path $repoRoot

$configPath = Join-Path $PSScriptRoot "config.ps1"
if (Test-Path $configPath) {
    . $configPath
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

$secretsPath = Join-Path $PSScriptRoot "secrets.ps1"
if (Test-Path $secretsPath) {
    . $secretsPath
} elseif ($Notify -eq "email") {
    Write-Error "secrets.ps1 not found. Copy deploy\secrets.example.ps1 to deploy\secrets.ps1 and fill in your Gmail App Password, or run with -Notify console."
    exit 1
}

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$python = if (Test-Path $venvPython) { $venvPython } else { "python" }

$pythonArgs = @("-m", "$Solution.watcher", "--source", $Source, "--state", $StatePath, "--notify", $Notify)
if ($Solution -eq "baseline" -and $Keyword) {
    $pythonArgs += @("--keyword", $Keyword)
}

& $python @pythonArgs
