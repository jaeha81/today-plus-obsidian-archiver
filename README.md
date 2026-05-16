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

## 파일 입력

HTML, TXT, MD 파일을 직접 지정할 수 있습니다.

```powershell
python main.py --file "C:/Users/YOUR_NAME/Downloads/today_plus.html"
```

HTML은 `script`, `style`, `nav`, `footer`를 제거하고 본문 텍스트와 Markdown 링크를 추출합니다.

## 파일 감시 모드

`config.yaml`의 `input_folder`에 파일이 생기면 자동 저장합니다.

```powershell
python main.py --watch
```

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
