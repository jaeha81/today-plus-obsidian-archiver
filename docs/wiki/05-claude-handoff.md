# Claude Handoff

## 역할

Codex가 본 개발을 주도한다. Claude는 필요 시 보조 구현, 검수 대응, 문서 정리, 운영 자동화 작업을 수행한다.

## Claude에게 맡기기 좋은 작업

- Windows 작업 스케줄러 등록 스크립트 작성
- `.bat` 또는 `.ps1` 원클릭 실행 파일 작성
- README 사용자 친화 문구 보강
- Obsidian Vault 실제 경로 자동 탐색 후보 조사
- 테스트 케이스 추가 작성
- GitHub Issues/Release notes 정리

## Claude가 건드리면 안 되는 것

- ChatGPT 세션 쿠키/토큰 저장 기능
- 웹 자동 로그인/무단 크롤링 기능
- `config.yaml`에 실제 개인 Vault 경로 하드코딩 후 커밋
- API key, 비밀번호, 세션 정보 커밋

## 다음 추천 작업

1. `scripts/run-clipboard.bat` 추가
2. `scripts/run-watch.bat` 추가
3. `scripts/install-task-scheduler.ps1` 추가
4. `tests/test_file_reader.py`로 HTML 링크 변환 검증 강화
5. 실제 Vault 경로에서 수동 smoke test

## 세션 전환 시 Claude 보조 가능 작업

- `docs/wiki/04-work-log.md`에 작업 요약 append
- 새 세션 시작 명령문을 사용자에게 전달할 수 있게 정리
- Codex가 개발 주도권을 유지하도록 구현 변경 전 요구사항 재확인
