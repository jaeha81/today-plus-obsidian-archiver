param(
    [string]$SmokeDir = ".tmp-smoke-remote-devcore-file-drop"
)

$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$resolvedRoot = (Resolve-Path $projectRoot).Path
$smokePath = Join-Path $projectRoot $SmokeDir

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

    $tmpDrop = Join-Path $inbox "today-plus-e2e.tmp"
    $finalDrop = Join-Path $inbox "today-plus-e2e.md"
    @(
        "# Today Plus",
        "",
        "source: remote-devcore-smoke",
        "received_at: 2026-05-17T09:00:00+09:00",
        "sender: codex-smoke",
        "",
        "---",
        "",
        "ChatGPT today plus Remote DevCore file drop E2E smoke content."
    ) | Set-Content -Encoding UTF8 -Path $tmpDrop
    Move-Item -LiteralPath $tmpDrop -Destination $finalDrop

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

    if (Test-Path $tmpDrop) {
        throw "Temporary drop file should have been renamed before processing"
    }
    if ($processedFiles -notcontains "today-plus-e2e.md") {
        throw "Processed Remote DevCore markdown file missing"
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
