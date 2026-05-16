param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$PythonCommand = "python",
    [string]$TaskPrefix = "TodayPlusArchive",
    [string]$ClipboardTime = "09:00"
)

$ErrorActionPreference = "Stop"

$mainPath = Join-Path $ProjectRoot "main.py"
if (-not (Test-Path $mainPath)) {
    throw "main.py not found under ProjectRoot: $ProjectRoot"
}

$venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $PythonCommand = $venvPython
}

$clipboardTaskName = "${TaskPrefix}Clipboard"
$watchTaskName = "${TaskPrefix}Watch"

$clipboardAction = New-ScheduledTaskAction `
    -Execute $PythonCommand `
    -Argument "`"$mainPath`" --clipboard" `
    -WorkingDirectory $ProjectRoot
$clipboardTrigger = New-ScheduledTaskTrigger -Daily -At $ClipboardTime

Register-ScheduledTask `
    -TaskName $clipboardTaskName `
    -Action $clipboardAction `
    -Trigger $clipboardTrigger `
    -Description "Archive user-copied Today Plus text from the local clipboard." `
    -Force | Out-Null

$watchAction = New-ScheduledTaskAction `
    -Execute $PythonCommand `
    -Argument "`"$mainPath`" --watch" `
    -WorkingDirectory $ProjectRoot
$watchTrigger = New-ScheduledTaskTrigger -AtLogOn

Register-ScheduledTask `
    -TaskName $watchTaskName `
    -Action $watchAction `
    -Trigger $watchTrigger `
    -Description "Watch the configured local input folder for user-saved Today Plus files." `
    -Force | Out-Null

Write-Host "Registered scheduled tasks:"
Write-Host " - $clipboardTaskName daily at $ClipboardTime"
Write-Host " - $watchTaskName at logon"
