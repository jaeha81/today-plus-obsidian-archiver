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
