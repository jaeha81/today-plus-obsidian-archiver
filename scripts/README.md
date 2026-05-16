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
