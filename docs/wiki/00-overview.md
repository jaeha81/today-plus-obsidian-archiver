# LLM Wiki Overview

이 위키는 `today-plus-obsidian-archiver` 개발 기준과 작업 맥락을 보존한다.

## 목적

ChatGPT `오늘의 플러스` 내용을 사용자가 직접 복사하거나 저장한 뒤, 로컬 PC에서 Obsidian Vault 날짜별 Markdown 노트로 정리한다.

## 핵심 원칙

- ChatGPT 웹 자동 로그인, 세션 탈취, CAPTCHA 우회, 무단 크롤링 금지
- 사용자 입력만 처리: 클립보드, 직접 저장 파일, 감시 폴더 파일
- 모든 처리 로컬 PC 내부 수행
- 계정 비밀번호, 세션 쿠키, API 토큰 저장 금지
- Obsidian Vault 경로는 `config.yaml` 또는 `--config`로 외부 설정

## 현재 상태

- Python CLI MVP 구현 완료
- `jH Remote DevCore` 파일 드롭 연동 규약 문서화
- GitHub 원격: `https://github.com/jaeha81/today-plus-obsidian-archiver.git`
- 기본 브랜치: `main`
- 테스트: `python -m unittest discover -s tests`

## 주요 명령

```powershell
python main.py --clipboard
python main.py --file "C:/path/today_plus.html"
python main.py --watch
python main.py --rebuild-index
python main.py --config "C:/path/config.yaml" --clipboard
```
