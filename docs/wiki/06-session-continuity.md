# Session Continuity Protocol

이 문서는 Goal Mode 작업 중 컨텍스트 압축, 세션 종료, 새 세션 재개가 필요할 때 따를 절차를 정의한다.

## 발동 조건

아래 상황이면 세션 연속성 절차를 발동한다.

- 대화 컨텍스트가 길어져 압축이 필요하다고 판단될 때
- 작업 범위가 커져 새 세션에서 이어가는 편이 안전할 때
- 사용자가 `세션 종료`, `종료 저장`, `오늘 세션 저장`, `새 세션으로 이어가자`라고 요청할 때
- 테스트, 커밋, 푸시 전후 상태를 다음 세션에 정확히 넘겨야 할 때

## 압축 전 사용자 고지

컨텍스트 압축이 필요하면 먼저 사용자에게 짧게 고지한다.

고지문:

```text
컨텍스트 압축 필요. 지금까지 작업을 LLM Wiki와 Git 상태 기준으로 정리한 뒤, 새 세션 시작 명령문까지 남기겠습니다.
```

사용자가 중단을 명시하지 않으면 아래 절차를 계속한다.

## 세션 종료 전 필수 기록

종료 전 다음 파일을 갱신한다.

- `docs/wiki/04-work-log.md`: 완료 작업, 검증 결과, 커밋 해시
- `docs/wiki/05-claude-handoff.md`: Claude에게 넘길 작업이 있으면 추가
- `docs/wiki/06-session-continuity.md`: 절차 변경이 있으면 갱신

필요하면 `README.md`에도 사용자 실행 절차를 반영한다.

## 종료 전 검증

가능한 경우 아래 명령을 실행한다.

```powershell
python -m unittest discover -s tests
python -m compileall main.py src tests
git diff --check
git status --short --branch
```

코드 변경이 없는 문서 작업이어도 `git status`는 확인한다.

## Git 처리

변경이 있으면 커밋하고 push한다.

커밋 메시지 예:

```text
Update session continuity wiki
```

push 후 `git status --short --branch`가 `main...origin/main`인지 확인한다.

## 사용자에게 전달할 새 세션 시작 명령문

세션 종료 또는 새 세션 전환 시 아래 명령문을 사용자에게 제공한다.

```text
이전 세션 이어서 진행.

프로젝트:
D:\ai프로젝트\today-plus-obsidian-archiver

먼저 아래 문서를 순서대로 읽어라:
1. docs/wiki/00-overview.md
2. docs/wiki/01-requirements.md
3. docs/wiki/02-architecture.md
4. docs/wiki/03-decisions.md
5. docs/wiki/04-work-log.md
6. docs/wiki/05-claude-handoff.md
7. docs/wiki/06-session-continuity.md

그 다음 실행:
- git status --short --branch
- python -m unittest discover -s tests

현재 운영 원칙:
- Codex가 본 개발 주도
- 필요 작업은 Claude에게 지시 가능
- ChatGPT 웹 자동 로그인/세션 탈취/무단 크롤링 금지
- 사용자 입력 기반 클립보드/파일/감시 폴더만 처리
- 변경 후 테스트, 커밋, GitHub push까지 진행

이어서 다음 개발 작업을 진행해라.
```

## 최종 보고 형식

세션 종료 보고는 짧게 한다.

```text
세션 종료 준비 완료.
- Wiki 반영: 완료
- 테스트: 결과
- Git: 커밋 해시 / push 여부
- 새 세션 시작 명령문: 아래 전달
```
