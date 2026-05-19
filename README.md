# Today Plus Obsidian Archiver

ChatGPT `오늘의 플러스` 내용을 사용자가 직접 복사하거나 로컬 파일로 저장하면, 로컬 PC에서 정리해 Obsidian Vault 안 날짜별 Markdown 노트로 저장하는 도구입니다.

웹 자동 로그인, 세션 탈취, CAPTCHA 우회, 무단 크롤링은 하지 않습니다. 입력은 클립보드, 사용자가 저장한 파일, 감시 폴더에 생성된 파일만 처리합니다.

## 설치

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 설정

`config.yaml`에서 Obsidian Vault 경로를 본인 환경에 맞게 바꿉니다.

```yaml
obsidian_vault_path: "C:/Users/YOUR_NAME/Documents/ObsidianVault"
output_folder: "00_Inbox/TodayPlus"
input_folder: "C:/Users/YOUR_NAME/TodayPlus_Input"
```

저장 파일명은 `YYYY-MM-DD_오늘의-플러스.md` 형식입니다.

## 클립보드 저장

1. ChatGPT 오늘의 플러스 화면에서 필요한 내용을 직접 복사합니다.
2. 아래 명령을 실행합니다.

```powershell
python main.py --clipboard
```

다른 설정 파일을 쓰려면 `--config`를 추가합니다.

```powershell
python main.py --config "C:/Users/YOUR_NAME/today-plus-config.yaml" --clipboard
```

Windows에서는 배치 파일로도 실행할 수 있습니다.

```powershell
scripts\run-clipboard.bat
scripts\run-clipboard.bat --config "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

매일 PC에서 ChatGPT를 열고, 복사 후 바로 저장하는 흐름은 아래 스크립트를 씁니다.

```powershell
scripts\run-daily-capture.bat
scripts\run-daily-capture.bat --config "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

이 스크립트는 ChatGPT를 열어 주고 사용자가 직접 복사한 클립보드 내용만 저장합니다. 로그인 세션, 쿠키, 화면 내용을 자동으로 읽지 않습니다.

## 파일 입력

HTML, TXT, MD 파일을 직접 지정할 수 있습니다.

```powershell
python main.py --file "C:/Users/YOUR_NAME/Downloads/today_plus.html"
```

HTML은 `script`, `style`, `nav`, `footer`를 제거하고 본문 텍스트와 Markdown 링크를 추출합니다.

Windows에서는 배치 파일로도 실행할 수 있습니다.

```powershell
scripts\run-file.bat "C:/Users/YOUR_NAME/Downloads/today_plus.html"
scripts\run-file.bat "C:/Users/YOUR_NAME/Downloads/today_plus.html" --config "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

## 파일 감시 모드

`config.yaml`의 `input_folder`에 파일이 생기면 자동 저장합니다.

```powershell
python main.py --watch
```

Windows에서는 배치 파일로도 실행할 수 있습니다.

```powershell
scripts\run-watch.bat
scripts\run-watch.bat --config "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

`jH Remote DevCore`와 연동할 때는 샘플 config를 복사해 Vault 경로만 수정해서 사용할 수 있습니다.

```powershell
copy config.example.remote-devcore.yaml config.remote-devcore.yaml
python main.py --config config.remote-devcore.yaml --watch
```

장시간 감시 없이 현재 inbox 파일만 한 번 처리하려면 아래 명령을 씁니다.

```powershell
python main.py --config config.remote-devcore.yaml --process-inbox-once
```

Windows에서는 배치 파일로도 실행할 수 있습니다.

```powershell
scripts\run-process-inbox-once.bat --config config.remote-devcore.yaml
```

처리 완료된 원본 파일을 `inbox/processed/`로 옮기려면 명시적으로 옵션을 추가합니다.

```powershell
python main.py --config config.remote-devcore.yaml --process-inbox-once --archive-processed
scripts\run-process-inbox-once.bat --config config.remote-devcore.yaml --archive-processed
```

기본 동작은 원본 파일을 inbox에 그대로 두는 것입니다.

Remote DevCore 파일 드롭 end-to-end 준비 상태는 임시 inbox/vault에서 `.tmp` 작성 후 `.md` rename을 재현하는 smoke 스크립트로 확인할 수 있습니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-file-drop.ps1
```

Remote DevCore CLI까지 포함한 교차 프로젝트 E2E는 아래 명령으로 확인합니다. 이 smoke는 임시 inbox/vault만 사용합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-cli-e2e.ps1
```

Discord text input and Whisper transcript input can be verified locally without live bot startup or OpenAI API use:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-input-routes.ps1
```

The operational user flow is documented in `docs/mobile-discord-to-obsidian-runbook.md`.

실제 로컬 inbox와 `D:\ai프로젝트\jh-obsidian` Vault를 대상으로 운영 E2E를 확인하려면 아래 명령을 사용합니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-remote-devcore-operational-e2e.ps1
```

운영 E2E는 `000-Inbox/TodayPlus`에 오늘 날짜 노트를 만들거나 기존 오늘 노트에 `추가 수집분`으로 붙입니다. 같은 날짜에 여러 번 수집해도 기존 노트를 덮어쓰지 않습니다.

## 중복 인덱스 재생성

기존 TodayPlus 폴더의 Markdown 파일을 다시 읽어 `.today_plus_index.json`을 재생성합니다.

```powershell
python main.py --rebuild-index
```

## Obsidian 확인

Obsidian에서 `00_Inbox/TodayPlus` 폴더를 열고 `YYYY-MM-DD_오늘의-플러스.md` 파일을 확인합니다. 노트에는 원문, 핵심 요약, 사업 적용 포인트, 콘텐츠 아이디어, 실행 액션, 키워드, 내부 링크가 포함됩니다.

## Windows 작업 스케줄러 예시

매일 오전 9시에 클립보드 저장:

```powershell
python D:\ai프로젝트\today-plus-obsidian-archiver\main.py --clipboard
```

로그인 시 감시 모드 실행:

```powershell
python D:\ai프로젝트\today-plus-obsidian-archiver\main.py --watch
```

작업 스케줄러에서는 시작 위치를 프로젝트 폴더로 지정하세요.

매일 확인 시간을 알림처럼 쓰고 싶으면 작업 스케줄러에서 `scripts\run-daily-capture.bat`를 실행 대상으로 등록합니다. 이 방식은 사용자가 직접 복사한 내용만 저장합니다.

등록 스크립트를 쓰려면 PowerShell에서 프로젝트 폴더 기준으로 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-task-scheduler.ps1
```

운영용 설정 파일을 따로 쓰려면 `-ConfigPath`를 지정합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-task-scheduler.ps1 -ConfigPath "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

기본으로 `TodayPlusArchiveClipboard`는 매일 09:00, `TodayPlusArchiveWatch`는 로그인 시 실행되도록 등록합니다.

Windows 보조 스크립트 전체 사용법은 `scripts/README.md`에 정리되어 있습니다.

## 테스트

```powershell
python -m unittest discover -s tests
```

## LLM Wiki

개발 맥락, 요구사항, 아키텍처, 결정사항은 `docs/wiki`에 기록합니다.

- `docs/wiki/00-overview.md`
- `docs/wiki/01-requirements.md`
- `docs/wiki/02-architecture.md`
- `docs/wiki/03-decisions.md`
- `docs/wiki/04-work-log.md`
- `docs/wiki/05-claude-handoff.md`
- `docs/wiki/06-session-continuity.md`
- `docs/wiki/07-remote-devcore-integration.md`
