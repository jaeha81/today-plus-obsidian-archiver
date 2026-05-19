# Windows Scripts

이 폴더는 Windows에서 `today-plus-obsidian-archiver`를 빠르게 실행하기 위한 보조 스크립트를 담고 있다.

모든 배치 파일은 프로젝트 루트로 이동한 뒤 실행된다. `.venv\Scripts\python.exe`가 있으면 그 Python을 우선 사용하고, 없으면 시스템 `python`을 사용한다.

## 클립보드 저장

ChatGPT 오늘의 플러스 내용을 직접 복사한 뒤 실행한다.

```powershell
scripts\run-clipboard.bat
scripts\run-clipboard.bat --config "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

## 매일 캡처 흐름

PC에서 ChatGPT를 열고, 사용자가 직접 복사한 오늘의 플러스 내용을 바로 저장한다.

```powershell
scripts\run-daily-capture.bat
scripts\run-daily-capture.bat --config "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

이 스크립트는 ChatGPT URL을 열고 사용자가 복사할 때까지 대기한 뒤 `run-clipboard.bat`를 실행한다. 로그인 세션, 쿠키, 화면 내용을 자동으로 읽지 않는다.

## 파일 입력

사용자가 직접 저장한 HTML, TXT, MD 파일을 지정한다.

```powershell
scripts\run-file.bat "C:/Users/YOUR_NAME/Downloads/today_plus.html"
scripts\run-file.bat "C:/Users/YOUR_NAME/Downloads/today_plus.html" --config "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

## 폴더 감시

`config.yaml`의 `input_folder`에 새 파일이 생기면 자동 저장한다.

```powershell
scripts\run-watch.bat
scripts\run-watch.bat --config "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

## Inbox 1회 처리

Remote DevCore가 파일을 드롭한 뒤 장시간 감시 없이 현재 inbox 파일만 한 번 처리한다.

```powershell
scripts\run-process-inbox-once.bat --config config.remote-devcore.yaml
scripts\run-process-inbox-once.bat --config config.remote-devcore.yaml --archive-processed
```

`--archive-processed`를 추가하면 처리 성공한 원본 파일을 `inbox\processed\`로 이동한다. 기본 동작은 원본 유지다.

## Smoke test

임시 Vault와 임시 inbox로 1회 처리와 `processed` 이동을 검증한다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-process-inbox-once.ps1
```

스크립트는 `.tmp` 파일이 inbox에 남고, `.md` 파일이 처리 후 `processed`로 이동하며, 임시 Vault에 노트가 생성되는지 확인한 뒤 임시 폴더를 정리한다.

Remote DevCore 실제 파일 드롭 방식인 `.tmp` 작성 후 `.md` rename까지 재현하려면 아래 smoke 스크립트를 실행한다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-file-drop.ps1
```

스크립트는 `today-plus-e2e.tmp`를 만든 뒤 `today-plus-e2e.md`로 이동하고, `--process-inbox-once --archive-processed` 실행 결과 `processed` 이동과 Vault 노트 생성을 검증한다.

Remote DevCore CLI가 실제로 inbox 파일을 쓰고 archiver가 처리하는 교차 프로젝트 E2E는 아래 명령으로 확인한다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-cli-e2e.ps1
```

Discord text JSON route and Whisper transcript-file route can be verified without starting live Discord or using an OpenAI API key:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-input-routes.ps1
```

This smoke creates a local Discord `MESSAGE_CREATE` JSON file and a local voice transcript text file, runs Remote DevCore with `--discord-message` and `--file`, then processes the resulting inbox files with `--process-inbox-once --archive-processed`. It does not connect to Discord Gateway and does not call Whisper/OpenAI.

스크립트는 sibling 폴더 `jH Remote DevCore`를 찾아 `TODAY_PLUS_INBOX`를 임시 inbox로 지정하고, `node src/cli.js --text ...` 실행 후 archiver의 `--process-inbox-once --archive-processed`까지 검증한다.

실제 로컬 inbox와 sibling `jh-obsidian` Vault를 대상으로 운영 E2E를 확인하려면 아래 명령을 실행한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-remote-devcore-operational-e2e.ps1
```

기본 출력 폴더는 `000-Inbox/TodayPlus`이며, `-VaultPath`, `-OutputFolder`, `-InboxPath`, `-RemoteDevCoreDir`로 경로를 바꿀 수 있다.

## 작업 스케줄러 등록

기본 등록:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-task-scheduler.ps1
```

운영용 설정 파일 지정:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-task-scheduler.ps1 -ConfigPath "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

기본 작업 이름:

- `TodayPlusArchiveClipboard`: 매일 09:00 실행
- `TodayPlusArchiveWatch`: 로그인 시 실행

작업 스케줄러 등록은 Windows 시스템 설정을 변경한다. 실제 등록 전에는 config 경로와 Vault 경로를 먼저 확인한다.
