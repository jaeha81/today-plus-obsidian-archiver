# Mobile/Discord -> Remote DevCore -> Obsidian Runbook

This runbook describes the safe operating flow where the user sends Today Plus content from mobile or Discord, Remote DevCore writes a local inbox file, and this archiver stores it in Obsidian.

## Scope

Allowed:

- User-provided Discord text routed by Remote DevCore.
- User-provided voice transcript routed by Remote DevCore after Whisper transcription.
- Local files dropped into `inbox`.
- One-shot inbox processing with `--process-inbox-once`.
- Watch mode only after explicit approval.

Not allowed:

- ChatGPT web auto-login.
- Session cookie or token access.
- Unauthorized crawling of ChatGPT UI or DOM.
- Discord live bot startup without user approval.
- Whisper/OpenAI API use without user approval and key setup.

## Prerequisites

1. Confirm `config.remote-devcore.yaml` exists or copy it from `config.example.remote-devcore.yaml`.
2. Set `obsidian_vault_path` to the real Obsidian vault.
3. Confirm `input_folder` points to the same inbox used by Remote DevCore.
4. Confirm Remote DevCore is available beside this repo as `D:\ai프로젝트\jH Remote DevCore`.
5. Keep `inbox\processed\` ignored by Git.

## Discord text

Manual local verification, no live bot:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-input-routes.ps1
```

Operational live Discord text requires approval:

```powershell
cd "D:\ai프로젝트\jH Remote DevCore"
$env:TODAY_PLUS_INBOX="D:\ai프로젝트\today-plus-obsidian-archiver\inbox"
$env:TODAY_PLUS_SOURCE="discord-live"
$env:DISCORD_BOT_TOKEN="..."
node src/cli.js --discord-live
```

Expected user message:

```text
!jh today plus

Original Today Plus content...
```

Remote DevCore should create `today-plus-YYYYMMDD-HHMMSS.md` in the archiver inbox.

## Whisper voice

Local transcript verification, no OpenAI API:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-input-routes.ps1
```

Real voice verification requires approval and API key setup:

```powershell
cd "D:\ai프로젝트\jH Remote DevCore"
$env:TODAY_PLUS_INBOX="D:\ai프로젝트\today-plus-obsidian-archiver\inbox"
$env:TODAY_PLUS_SOURCE="discord-voice-live"
$env:WHISPER_PROVIDER="openai"
$env:OPENAI_API_KEY="..."
$env:DISCORD_BOT_TOKEN="..."
$env:DISCORD_VOICE_GUILD_ID="..."
$env:DISCORD_VOICE_CHANNEL_ID="..."
node src/cli.js --discord-voice-live
```

The spoken command should include a clear Today Plus trigger, for example:

```text
today plus. Original Today Plus content...
```

## Archiver processing

One-shot processing:

```powershell
scripts\run-process-inbox-once.bat --config config.remote-devcore.yaml --archive-processed
```

Direct Python equivalent:

```powershell
python main.py --config config.remote-devcore.yaml --process-inbox-once --archive-processed
```

Expected result:

- Source file moves to `inbox\processed\`.
- Today's Obsidian note is created or appended.
- Existing same-day note is not overwritten.
- Additional captures appear under `## 추가 수집분`.

## Watch mode

Approval required before starting a long-running watch process:

```powershell
python main.py --config config.remote-devcore.yaml --watch
```

Approval required before registering or changing Windows Task Scheduler:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-task-scheduler.ps1 -ConfigPath "D:\ai프로젝트\today-plus-obsidian-archiver\config.remote-devcore.yaml"
```

## Operational checklist

- Run `git status --short --branch`.
- Run `python -m unittest discover -s tests`.
- Run `powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-input-routes.ps1`.
- For operational vault verification, run `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-remote-devcore-operational-e2e.ps1`.
- Open Obsidian and confirm today's note under `000-Inbox/TodayPlus` or the configured output folder.
- Confirm `inbox\processed\` contains the processed source file.

## Approval required

- Discord bot live execution.
- Whisper/OpenAI API key based voice verification.
- Windows Task Scheduler registration or changes.
- Long-running watch process setup.
