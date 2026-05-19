param(
    [string]$RemoteDevCoreDir = "",
    [string]$SmokeDir = ".tmp-smoke-remote-devcore-input-routes"
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
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $vault = Join-Path $smokePath "vault"
    $inbox = Join-Path $smokePath "inbox"
    New-Item -ItemType Directory -Path $vault | Out-Null
    New-Item -ItemType Directory -Path $inbox | Out-Null

    $config = Join-Path $smokePath "config.yaml"
    $configLines = @(
        "obsidian_vault_path: `"$($vault.Replace('\','/'))`"",
        "output_folder: `"00_Inbox/TodayPlus`"",
        "input_folder: `"$($inbox.Replace('\','/'))`"",
        "index_file: `".today_plus_index.json`"",
        "default_tags:",
        "  - today-plus",
        "  - remote-devcore",
        "  - input-routes-smoke",
        "related_links:",
        "  - `"ChatGPT`"",
        "  - `"Discord`"",
        "duplicate_similarity_threshold: 0.92"
    )
    [System.IO.File]::WriteAllText($config, ($configLines -join [Environment]::NewLine), $utf8NoBom)

    $discordMessage = Join-Path $smokePath "discord-message.json"
    $discordJson = @{
        id = "today-plus-smoke-message"
        channel_id = "today-plus-smoke-channel"
        author = @{
            id = "today-plus-smoke-user"
            bot = $false
        }
        content = "!jh today plus`n`nDiscord text local smoke payload for Today Plus archiver."
    } | ConvertTo-Json -Depth 5
    [System.IO.File]::WriteAllText($discordMessage, $discordJson, $utf8NoBom)

    $voiceTranscript = Join-Path $smokePath "voice-transcript.txt"
    [System.IO.File]::WriteAllText(
        $voiceTranscript,
        "today plus`n`nWhisper text local smoke payload for Today Plus archiver.",
        $utf8NoBom
    )

    $previousInbox = $env:TODAY_PLUS_INBOX
    $previousSource = $env:TODAY_PLUS_SOURCE
    $previousAgentRoom = $env:AGENT_ROOM_ENABLED
    $env:TODAY_PLUS_INBOX = $inbox
    $env:AGENT_ROOM_ENABLED = "false"

    Push-Location $RemoteDevCoreDir
    try {
        $env:TODAY_PLUS_SOURCE = "discord-text-local-smoke"
        & node src/cli.js --discord-message $discordMessage | Out-Host
        if ($LASTEXITCODE -ne 0) {
            throw "Remote DevCore Discord message route failed with exit code $LASTEXITCODE"
        }
        $discordDroppedFiles = @(Get-ChildItem -Path $inbox -File -Force | ForEach-Object { $_.Name })
        Write-Output "DISCORD_ROUTE_DROPPED_FILES=$($discordDroppedFiles -join ',')"
        if (-not ($discordDroppedFiles | Where-Object { $_ -like "today-plus-*.md" })) {
            throw "Discord text route did not drop a Today Plus markdown file"
        }

        Start-Sleep -Milliseconds 1100

        $env:TODAY_PLUS_SOURCE = "whisper-text-local-smoke"
        & node src/cli.js --file $voiceTranscript | Out-Host
        if ($LASTEXITCODE -ne 0) {
            throw "Remote DevCore Whisper text route failed with exit code $LASTEXITCODE"
        }
        $whisperDroppedFiles = @(Get-ChildItem -Path $inbox -File -Force | ForEach-Object { $_.Name })
        Write-Output "WHISPER_ROUTE_DROPPED_FILES=$($whisperDroppedFiles -join ',')"
        if (@($whisperDroppedFiles | Where-Object { $_ -like "today-plus-*.md" }).Count -lt 2) {
            throw "Whisper text route did not drop a second Today Plus markdown file"
        }
    } finally {
        Pop-Location
        $env:TODAY_PLUS_INBOX = $previousInbox
        $env:TODAY_PLUS_SOURCE = $previousSource
        $env:AGENT_ROOM_ENABLED = $previousAgentRoom
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

    $processedFiles = @(Get-ChildItem -Path (Join-Path $inbox "processed") -File -Force | ForEach-Object { $_.Name })
    $vaultFiles = @(Get-ChildItem -Path (Join-Path $vault "00_Inbox/TodayPlus") -File -Force | ForEach-Object { $_.Name })
    $vaultNoteCount = @($vaultFiles | Where-Object { $_ -like "*.md" }).Count
    $notePath = Get-ChildItem -Path (Join-Path $vault "00_Inbox/TodayPlus") -File -Filter "*.md" |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1 -ExpandProperty FullName
    $noteContent = Get-Content -Encoding UTF8 -Raw -Path $notePath

    Write-Output "PROCESSED_FILES=$($processedFiles -join ',')"
    Write-Output "VAULT_FILES=$($vaultFiles -join ',')"
    Write-Output "VAULT_NOTE_COUNT=$vaultNoteCount"

    if ($processedFiles.Count -lt 2) {
        throw "Processed route files missing"
    }
    if ($vaultNoteCount -lt 1) {
        throw "Vault markdown note missing"
    }
    if ($noteContent -notlike "*Discord text local smoke payload*" -or
        $noteContent -notlike "*Whisper text local smoke payload*") {
        throw "Vault note does not contain both route payloads"
    }
} finally {
    if (Test-Path $smokePath) {
        $resolvedSmoke = (Resolve-Path $smokePath).Path
        if ($resolvedSmoke.StartsWith($resolvedRoot)) {
            Remove-Item -LiteralPath $resolvedSmoke -Recurse -Force
        }
    }
}
