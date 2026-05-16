param(
    [string]$SmokeDir = ".tmp-smoke-process-inbox-once"
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

    Set-Content -Encoding UTF8 -Path (Join-Path $inbox "today-plus-smoke.tmp") -Value "partial content"
    Set-Content -Encoding UTF8 -Path (Join-Path $inbox "today-plus-smoke.md") -Value "ChatGPT today plus smoke content."

    Push-Location $projectRoot
    try {
        python main.py --config $config --process-inbox-once --archive-processed | Out-Host
    } finally {
        Pop-Location
    }

    $inboxFileCount = @(Get-ChildItem -Path $inbox -File -Force).Count
    $processedFiles = @(Get-ChildItem -Path (Join-Path $inbox "processed") -File -Force | ForEach-Object { $_.Name })
    $vaultFiles = @(Get-ChildItem -Path (Join-Path $vault "00_Inbox/TodayPlus") -File -Force | ForEach-Object { $_.Name })

    Write-Output "INBOX_FILE_COUNT=$inboxFileCount"
    Write-Output "PROCESSED_FILES=$($processedFiles -join ',')"
    Write-Output "VAULT_FILES=$($vaultFiles -join ',')"

    if ($inboxFileCount -ne 1) {
        throw "Expected only tmp to remain in inbox root"
    }
    if ($processedFiles -notcontains "today-plus-smoke.md") {
        throw "Processed markdown file missing"
    }
    if (-not ($vaultFiles | Where-Object { $_ -like "*.md" })) {
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
