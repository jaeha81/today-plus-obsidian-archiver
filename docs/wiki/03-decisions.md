# Decisions

## D001: 웹 스크래핑 금지

ChatGPT 웹페이지 직접 자동화는 하지 않는다.

이유:

- 세션/계정 보안 위험
- CAPTCHA/접근제어 우회 가능성
- 사용자 요구사항이 로컬 입력 처리로 제한

## D002: 유료 API 없는 규칙 기반 요약 우선

초기 버전은 외부 LLM API를 쓰지 않는다.

이유:

- 로컬 처리 원칙 유지
- 비용 없음
- 추후 `summarizer.py` 교체로 OpenAI API 또는 로컬 LLM 확장 가능

## D003: SHA256 + SequenceMatcher 조합

완전 중복은 SHA256, 유사 중복은 `difflib.SequenceMatcher`로 처리한다.

이유:

- 의존성 최소화
- 작은 개인 지식베이스 규모에서는 충분
- 향후 임베딩 기반 중복 탐지로 교체 가능

## D004: `--config` 옵션 추가

기본 `config.yaml` 외 다른 설정 파일을 CLI에서 지정 가능하게 했다.

이유:

- 테스트와 실제 운영 config 분리
- 여러 Obsidian Vault 운영 가능
- 사용자 환경 수정 부담 감소

## D005: 위키를 repo 내부 `docs/wiki`에 둠

작업 맥락과 결정 사항을 코드와 함께 버전 관리한다.

이유:

- 대화 맥락 소실 방지
- Claude/Codex 협업 기준 명확화
- GitHub에서 바로 확인 가능
