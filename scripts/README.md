# Windows Scripts

이 폴더는 Windows에서 `today-plus-obsidian-archiver`를 빠르게 실행하기 위한 보조 스크립트를 담고 있다.

모든 배치 파일은 프로젝트 루트로 이동한 뒤 실행된다. `.venv\Scripts\python.exe`가 있으면 그 Python을 우선 사용하고, 없으면 시스템 `python`을 사용한다.

## 클립보드 저장

ChatGPT 오늘의 플러스 내용을 직접 복사한 뒤 실행한다.

```powershell
scripts\run-clipboard.bat
scripts\run-clipboard.bat --config "C:/Users/YOUR_NAME/today-plus-config.yaml"
```

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
