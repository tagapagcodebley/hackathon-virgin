# Registers a Windows Scheduled Task that runs run_watcher.ps1 every 15
# minutes, indefinitely. Run this once (elevation not required for a
# per-user task).
#
# -Solution controls HOW the task runs, not just what it runs:
#   baseline  -> invokes PowerShell directly, so a console window
#                visibly flashes on every poll (see baseline/README.md).
#   advanced  -> routes through ..\advanced\deploy\run_hidden.vbs, so it
#                polls with zero visible window (see
#                advanced/deploy/README.md for why this is one of
#                advanced's own engineering-quality improvements).
#
# -Source/-Notify/-Keyword are deliberately left unresolved here unless
# you pass them explicitly. Leave them out and run_watcher.ps1 resolves
# them itself from config.ps1 on every poll -- so pointing the task at
# your own real page (and match phrase, for baseline) is just filling in
# config.ps1 once (see config.example.ps1), and editing it later takes
# effect on the task's next run without re-registering. Pass them here
# only to force a specific value for this one registration.
#
# -IntervalMinutes is different: it's baked into the Scheduled Task
# trigger itself, so it has to be decided now. Falls back to
# config.ps1's $env:SAURON_INTERVAL_MINUTES if not given explicitly.

param(
    [ValidateSet("baseline", "advanced")]
    [string]$Solution = "baseline",
    [string]$Source,
    [ValidateSet("console", "email")]
    [string]$Notify,
    [string]$Keyword,
    [int]$IntervalMinutes = 15
)

$ErrorActionPreference = "Stop"
$scriptDir = $PSScriptRoot
$repoRoot = Split-Path -Parent $scriptDir
$taskName = "SauronWatcher-$Solution"

if (-not $PSBoundParameters.ContainsKey('IntervalMinutes')) {
    $configPath = Join-Path $scriptDir "config.ps1"
    if (Test-Path $configPath) {
        . $configPath
    }
    if ($env:SAURON_INTERVAL_MINUTES) {
        $IntervalMinutes = [int]$env:SAURON_INTERVAL_MINUTES
    }
}

$watcherArgs = "-Solution $Solution"
if ($PSBoundParameters.ContainsKey('Source')) {
    $watcherArgs += " -Source `"$Source`""
}
if ($PSBoundParameters.ContainsKey('Notify')) {
    $watcherArgs += " -Notify $Notify"
}
if ($PSBoundParameters.ContainsKey('Keyword')) {
    $watcherArgs += " -Keyword `"$Keyword`""
}

if ($Solution -eq "advanced") {
    $vbsPath = Join-Path $repoRoot "advanced\deploy\run_hidden.vbs"
    $action = New-ScheduledTaskAction `
        -Execute "wscript.exe" `
        -Argument "`"$vbsPath`" $watcherArgs" `
        -WorkingDirectory $scriptDir
} else {
    $action = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptDir\run_watcher.ps1`" $watcherArgs" `
        -WorkingDirectory $scriptDir
}

$trigger = New-ScheduledTaskTrigger `
    -Once -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes)
# Leaving Repetition.Duration unset (rather than [TimeSpan]::MaxValue, which
# Register-ScheduledTask fails to serialize) means "repeat indefinitely".
$trigger.Repetition.Duration = ""
$trigger.Repetition.StopAtDurationEnd = $false

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

$sourceDescription = if ($PSBoundParameters.ContainsKey('Source')) { $Source } else { "its config.ps1-configured source" }

try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
        -Settings $settings -Description "Sauron ($Solution): polls $sourceDescription every $IntervalMinutes min." `
        -Force -ErrorAction Stop | Out-Null
} catch {
    Write-Error "Failed to register scheduled task: $_"
    exit 1
}

Write-Host "Registered scheduled task '$taskName'. It will run every $IntervalMinutes minutes."
Write-Host "View/manage it with: Get-ScheduledTask -TaskName $taskName"
Write-Host "Run it immediately with: Start-ScheduledTask -TaskName $taskName"
Write-Host "Remove it with: Unregister-ScheduledTask -TaskName $taskName -Confirm:`$false"
