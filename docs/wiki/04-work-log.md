# Work Log

## 2026-05-16

### 초기 구현

- Markdown 요구사항 3개 읽음
- Python CLI 프로젝트 생성
- `clipboard`, `file`, `watch`, `rebuild-index` 구현
- Obsidian Markdown writer 구현
- SHA256 중복 인덱스 구현
- 규칙 기반 요약/키워드/사업 적용/콘텐츠 아이디어 구현
- README, requirements, config 작성
- Git 초기화, origin 연결, GitHub push

커밋:

```text
d78ebe2 Initial Today Plus Obsidian archiver
```

### 운영 보강

- `--config` 옵션 추가
- 임시 Vault에 실제 저장하는 workflow smoke test 추가
- README에 `--config` 사용법 추가

커밋:

```text
5e36ef8 Add config override and workflow smoke test
```

### 위키 적용

- `docs/wiki` 생성
- 요구사항, 아키텍처, 결정사항, 작업로그, Claude 인계 문서화

커밋:

```text
3347a82 Add LLM wiki documentation
```

### 세션 연속성 프로토콜

- Goal Mode 컨텍스트 압축 전 사용자 고지 절차 정의
- 세션 종료 전 Wiki 반영 절차 정의
- 새 세션에서 이어갈 시작 명령문 템플릿 추가

검증 명령:

```powershell
python -m unittest discover -s tests
python -m compileall main.py src tests
git diff --check
```

### Windows 실행 편의 보강

- `scripts/run-clipboard.bat` 추가
- `scripts/run-watch.bat` 추가
- `scripts/install-task-scheduler.ps1` 추가
- HTML fallback 파서의 링크 Markdown 변환 검증 강화
- README에 배치 파일과 작업 스케줄러 등록 방법 추가

검증 명령:

```powershell
python -m unittest tests.test_scripts
python -m unittest tests.test_file_reader
```

### 작업 스케줄러 설정 경로 보강

- `scripts/install-task-scheduler.ps1`에 선택적 `-ConfigPath` 추가
- 작업 스케줄러 등록 시 운영용 config 파일을 명시할 수 있도록 README 갱신

검증 명령:

```powershell
python -m unittest tests.test_scripts
```

### 파일 입력 실행 스크립트 추가

- `scripts/run-file.bat` 추가
- HTML/TXT/MD 직접 파일 입력을 Windows 배치 파일로 실행 가능하게 README 갱신

검증 명령:

```powershell
python -m unittest tests.test_scripts
```

### Windows 스크립트 문서화

- `scripts/README.md` 추가
- 클립보드, 파일 입력, 폴더 감시, 작업 스케줄러 등록 사용법을 스크립트 폴더에 정리
- 최상위 README에서 스크립트 문서 위치 안내

검증 명령:

```powershell
git diff --check
```

### Daily capture 흐름 추가

- `scripts/run-daily-capture.bat` 추가
- ChatGPT를 열고 사용자가 직접 복사한 클립보드 내용을 저장하는 안전한 daily capture 흐름 문서화
- 앱/웹 세션 자동 읽기, 쿠키 접근, 크롤링 금지 결정을 `docs/wiki/03-decisions.md`에 명시

검증 명령:

```powershell
python -m unittest tests.test_scripts
```

### Remote DevCore 연동 규약 문서화

- `docs/wiki/07-remote-devcore-integration.md` 추가
- Discord/Whisper/Local Control Agent가 사용자 입력을 로컬 inbox 파일로 드롭하는 계약 정의
- ChatGPT 세션 자동화 없이 `--watch` 감시 폴더로 연동하는 구조 명시

검증 명령:

```powershell
git diff --check
```

### Remote DevCore 파일 드롭 처리 보강

- watch 모드 처리 로직을 `handle_watch_path`로 분리
- `.tmp` 파일 생성 이벤트는 무시하고 최종 지원 확장자만 처리하도록 테스트 추가
- Local Control Agent의 `.tmp` 쓰기 후 `.md` rename 흐름을 위해 watchdog `on_moved` 이벤트 처리 추가

검증 명령:

```powershell
python -m unittest tests.test_main_workflow
```

### Remote DevCore inbox 설정 정리

- `config.yaml`의 `input_folder`를 로컬 `inbox` 폴더로 확정
- 깨진 한글 `related_links` 문자열을 UTF-8 기준으로 복구
- `inbox/.gitkeep` 추가로 Local Control Agent 파일 드롭 대상 폴더를 저장소에 명시

검증 명령:

```powershell
python -m unittest discover -s tests
```

### Remote DevCore sample payload 문서화

- Discord slash command, 태그 라우팅, Whisper 텍스트 라우팅 예시 추가
- Remote DevCore 내부 payload 권장 JSON 형식 추가
- Local Control Agent 출력 파일, 성공 응답, 실패 응답 예시 추가

검증 명령:

```powershell
git diff --check
```

### Remote DevCore 샘플 config 추가

- `config.example.remote-devcore.yaml` 추가
- Remote DevCore 파일 드롭용 `input_folder`와 관련 태그 기본값 제공
- README와 연동 문서에 샘플 config 복사/실행 방법 추가

검증 명령:

```powershell
python -m unittest tests.test_main_workflow
```

### Inbox 1회 처리 모드 추가

- `--process-inbox-once` CLI 옵션 추가
- Remote DevCore 파일 드롭 테스트를 장시간 watch 프로세스 없이 처리 가능하게 함
- README와 Remote DevCore 연동 문서에 실행 예시 추가

검증 명령:

```powershell
python -m unittest tests.test_main_workflow
```

### 처리 완료 파일 보관 옵션 추가

- `--archive-processed` CLI 옵션 추가
- `--process-inbox-once`에서 처리 성공한 원본 파일을 `inbox/processed/`로 이동 가능
- 기본 동작은 원본 유지이며, 동일 파일명 충돌 시 suffix를 붙여 덮어쓰지 않도록 구현

검증 명령:

```powershell
python -m unittest tests.test_main_workflow
```

### Inbox 1회 처리 Windows 스크립트 추가

- `scripts/run-process-inbox-once.bat` 추가
- Remote DevCore 파일 드롭 후 1회 처리와 `--archive-processed` 옵션을 배치 파일로 실행 가능하게 문서화

검증 명령:

```powershell
python -m unittest tests.test_scripts
```

### Inbox 1회 처리 smoke 스크립트 추가

- `scripts/smoke-process-inbox-once.ps1` 추가
- 임시 Vault/inbox로 `--process-inbox-once --archive-processed` 검증 자동화
- smoke test 실행법을 `scripts/README.md`에 문서화

검증 명령:

```powershell
python -m unittest tests.test_scripts
```

### Remote DevCore 파일 드롭 E2E smoke 준비

- `scripts/smoke-remote-devcore-file-drop.ps1` 추가
- Local Control Agent 방식처럼 `today-plus-e2e.tmp` 작성 후 `today-plus-e2e.md` rename을 재현
- 임시 Vault/inbox에서 `--process-inbox-once --archive-processed`를 실행해 processed 이동과 Vault 노트 생성을 검증
- README와 `scripts/README.md`에 실행법 문서화

검증 명령:

```powershell
python -m unittest tests.test_scripts
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-file-drop.ps1
```

### Remote DevCore CLI 교차 프로젝트 E2E smoke 준비

- `scripts/smoke-remote-devcore-cli-e2e.ps1` 추가
- sibling 폴더 `jH Remote DevCore`의 `node src/cli.js --text ...`를 실행해 실제 DevCore writer가 임시 inbox에 `today-plus-*.md`를 쓰는지 검증
- 같은 임시 inbox를 archiver `--process-inbox-once --archive-processed`로 처리해 processed 이동과 Vault 노트 생성을 검증
- 한글 경로 리터럴 인코딩 문제를 피하기 위해 프로젝트 부모 경로에서 Remote DevCore 경로를 조합하도록 구현
- README와 `scripts/README.md`에 실행법 문서화

검증 명령:

```powershell
python -m unittest tests.test_scripts
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-remote-devcore-cli-e2e.ps1
```
