param(
    [string]$RemoteDevCoreDir = "",
    [string]$VaultPath = "",
    [string]$OutputFolder = "000-Inbox/TodayPlus",
    [string]$InboxPath = "",
    [string]$SmokeDir = ".tmp-operational-remote-devcore-e2e"
)

$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$resolvedRoot = (Resolve-Path $projectRoot).Path
$projectParent = Split-Path $projectRoot -Parent

if (-not $RemoteDevCoreDir) {
    $RemoteDevCoreDir = Join-Path $projectParent "jH Remote DevCore"
}
if (-not $VaultPath) {
    $VaultPath = Join-Path $projectParent "jh-obsidian"
}
if (-not $InboxPath) {
    $InboxPath = Join-Path $projectRoot "inbox"
}

if (-not (Test-Path $RemoteDevCoreDir)) {
    throw "Remote DevCore directory not found: $RemoteDevCoreDir"
}
if (-not (Test-Path $VaultPath)) {
    throw "Obsidian Vault path not found: $VaultPath"
}

$workPath = Join-Path $projectRoot $SmokeDir
if (Test-Path $workPath) {
    $resolvedWork = (Resolve-Path $workPath).Path
    if (-not $resolvedWork.StartsWith($resolvedRoot)) {
        throw "Unsafe operational work path: $resolvedWork"
    }
    Remove-Item -LiteralPath $resolvedWork -Recurse -Force
}
New-Item -ItemType Directory -Path $workPath | Out-Null
New-Item -ItemType Directory -Path $InboxPath -Force | Out-Null

try {
    $config = Join-Path $workPath "config.yaml"
    $configContent = @"
obsidian_vault_path: "$($VaultPath.Replace('\','/'))"
output_folder: "$OutputFolder"
input_folder: "$($InboxPath.Replace('\','/'))"
index_file: ".today_plus_index.json"
default_tags:
  - today-plus
  - remote-devcore
  - operational-e2e
related_links:
  - "ChatGPT"
  - "AI automation"
duplicate_similarity_threshold: 0.92
"@
    Set-Content -Encoding UTF8 -Path $config -Value $configContent

    $beforeFiles = @(Get-ChildItem -Path $InboxPath -File -Force | ForEach-Object { $_.FullName })
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss K"
    $payload = "today plus`n`nOperational Remote DevCore E2E verification at $timestamp. This confirms CLI file drop, archiver inbox processing, processed archival, and Obsidian vault write."

    $previousInbox = $env:TODAY_PLUS_INBOX
    $previousSource = $env:TODAY_PLUS_SOURCE
    $env:TODAY_PLUS_INBOX = $InboxPath
    $env:TODAY_PLUS_SOURCE = "remote-devcore-operational-e2e"

    Push-Location $RemoteDevCoreDir
    try {
        & node src/cli.js --text $payload | Out-Host
        if ($LASTEXITCODE -ne 0) {
            throw "Remote DevCore CLI failed with exit code $LASTEXITCODE"
        }
    } finally {
        Pop-Location
        $env:TODAY_PLUS_INBOX = $previousInbox
        $env:TODAY_PLUS_SOURCE = $previousSource
    }

    $afterFiles = @(Get-ChildItem -Path $InboxPath -File -Force | ForEach-Object { $_.FullName })
    $newFiles = @($afterFiles | Where-Object { $beforeFiles -notcontains $_ })
    Write-Output "OPERATIONAL_DROPPED_FILES=$($newFiles -join ',')"

    if (-not ($newFiles | Where-Object { $_ -like "*today-plus-*.md" })) {
        throw "Remote DevCore did not create a new Today Plus markdown file in the operational inbox"
    }

    Push-Location $projectRoot
    try {
        & python main.py --config $config --process-inbox-once --archive-processed | Out-Host
        if ($LASTEXITCODE -ne 0) {
            throw "Archiver processing failed with exit code $LASTEXITCODE"
        }
    } finally {
        Pop-Location
    }

    $outputPath = Join-Path $VaultPath $OutputFolder
    $noteDate = Get-Date -Format "yyyy-MM-dd"
    $notePath = Get-ChildItem -Path $outputPath -File -Filter "$noteDate*.md" |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1 -ExpandProperty FullName
    $processedFiles = @(Get-ChildItem -Path (Join-Path $InboxPath "processed") -File -Force | Sort-Object LastWriteTime -Descending | Select-Object -First 5 -ExpandProperty Name)

    Write-Output "OPERATIONAL_PROCESSED_RECENT=$($processedFiles -join ',')"
    Write-Output "OPERATIONAL_NOTE_PATH=$notePath"

    if (-not $notePath -or -not (Test-Path $notePath)) {
        throw "Operational Obsidian note was not created in: $outputPath"
    }

    $noteContent = Get-Content -Encoding UTF8 -Raw -Path $notePath
    if ($noteContent -notlike "*Operational Remote DevCore E2E verification*") {
        throw "Operational Obsidian note does not contain the E2E verification payload"
    }
} finally {
    if (Test-Path $workPath) {
        $resolvedWork = (Resolve-Path $workPath).Path
        if ($resolvedWork.StartsWith($resolvedRoot)) {
            Remove-Item -LiteralPath $resolvedWork -Recurse -Force
        }
    }
}
