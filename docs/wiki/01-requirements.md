# Requirements

## 입력

- 클립보드 모드: `pyperclip`으로 사용자가 직접 복사한 텍스트를 읽음
- 파일 모드: HTML, TXT, MD 지원
- 감시 모드: `watchdog`으로 `input_folder` 신규 파일 감지

## 출력

Obsidian Vault 내부 `output_folder`에 날짜별 Markdown 생성.

파일명:

```text
YYYY-MM-DD_오늘의-플러스.md
```

## 노트 구조

- YAML frontmatter
- 원문 저장
- 핵심 요약
- 사업 아이디어 연결
- 내 사업에 적용할 포인트
- 콘텐츠화 아이디어
- 실행 액션
- 우선순위
- 관련 키워드
- Obsidian 내부 링크
- 중복 체크

## 중복 정책

- SHA256 해시를 `.today_plus_index.json`에 저장
- 완전 동일 내용은 저장하지 않음
- 유사 내용은 같은 날짜 노트가 있으면 `추가 수집분`으로 append
- 유사도 기준은 `duplicate_similarity_threshold`

## 비기능 요구

- Python 3.11 이상 기준
- `pathlib` 기반 경로 처리
- 외부 유료 API 없이 규칙 기반 요약 우선
- 테스트 코드 포함
- README만 보고 설치/실행 가능해야 함
