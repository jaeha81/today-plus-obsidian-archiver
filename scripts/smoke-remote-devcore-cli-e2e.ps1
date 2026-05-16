param(
    [string]$RemoteDevCoreDir = "",
    [string]$SmokeDir = ".tmp-smoke-remote-devcore-cli-e2e"
)

$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$resolvedRoot = (Resolve-Path $projectRoot).Path
$smokePath = Join-Path $projectRoot $SmokeDir

if (-not $RemoteDevCoreDir) {
    $RemoteDevCoreDir = Join-Path (Split-Path $projectRoot -Parent) "jH Remote DevCore"
}

if (-not (Test-Path $RemoteDevCoreDir)) {
    throw "Remote DevCore directory not found: $RemoteDevCoreDir"
}

if (Test-Path $smokePath) {
    $resolvedSmoke = (Resolve-Path $smokePath).Path
    if (-not $resolvedSmoke.StartsWith($resolvedRoot)) {
        throw "Unsafe smoke path: $resolvedSmoke"
    }
    Remove-Item -LiteralPath $resolvedSmoke -Recurse -Force
}

New-Item -ItemType Directory -Path $smokePath | Out-Null

try {
    $vault = Join-Path $smokePath "vault"
    $inbox = Join-Path $smokePath "inbox"
    New-Item -ItemType Directory -Path $vault | Out-Null
    New-Item -ItemType Directory -Path $inbox | Out-Null

    $config = Join-Path $smokePath "config.yaml"
    @(
        "obsidian_vault_path: `"$($vault.Replace('\','/'))`"",
        "output_folder: `"00_Inbox/TodayPlus`"",
        "input_folder: `"$($inbox.Replace('\','/'))`"",
        "index_file: `".today_plus_index.json`"",
        "default_tags:",
        "  - today-plus",
        "  - remote-devcore",
        "related_links:",
        "  - `"ChatGPT`"",
        "duplicate_similarity_threshold: 0.92"
    ) | Set-Content -Encoding UTF8 -Path $config

    $previousInbox = $env:TODAY_PLUS_INBOX
    $previousSource = $env:TODAY_PLUS_SOURCE
    $env:TODAY_PLUS_INBOX = $inbox
    $env:TODAY_PLUS_SOURCE = "remote-devcore-cli-e2e"

    Push-Location $RemoteDevCoreDir
    try {
        node src/cli.js --text "today plus`n`nRemote DevCore CLI to Today Plus archiver E2E smoke content." | Out-Host
    } finally {
        Pop-Location
        $env:TODAY_PLUS_INBOX = $previousInbox
        $env:TODAY_PLUS_SOURCE = $previousSource
    }

    $droppedFiles = @(Get-ChildItem -Path $inbox -File -Force | ForEach-Object { $_.Name })
    Write-Output "DEVCORE_DROPPED_FILES=$($droppedFiles -join ',')"

    if (-not ($droppedFiles | Where-Object { $_ -like "today-plus-*.md" })) {
        throw "Remote DevCore did not drop a Today Plus markdown file"
    }

    Push-Location $projectRoot
    try {
        python main.py --config $config --process-inbox-once --archive-processed | Out-Host
    } finally {
        Pop-Location
    }

    $processedFiles = @(Get-ChildItem -Path (Join-Path $inbox "processed") -File -Force | ForEach-Object { $_.Name })
    $vaultFiles = @(Get-ChildItem -Path (Join-Path $vault "00_Inbox/TodayPlus") -File -Force | ForEach-Object { $_.Name })
    $vaultNoteCount = @($vaultFiles | Where-Object { $_ -like "*.md" }).Count

    Write-Output "PROCESSED_FILES=$($processedFiles -join ',')"
    Write-Output "VAULT_FILES=$($vaultFiles -join ',')"
    Write-Output "VAULT_NOTE_COUNT=$vaultNoteCount"

    if ($processedFiles.Count -lt 1) {
        throw "Processed Remote DevCore file missing"
    }
    if ($vaultNoteCount -lt 1) {
        throw "Vault markdown note missing"
    }
} finally {
    if (Test-Path $smokePath) {
        $resolvedSmoke = (Resolve-Path $smokePath).Path
        if ($resolvedSmoke.StartsWith($resolvedRoot)) {
            Remove-Item -LiteralPath $resolvedSmoke -Recurse -Force
        }
    }
}
