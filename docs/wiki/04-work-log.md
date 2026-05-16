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
