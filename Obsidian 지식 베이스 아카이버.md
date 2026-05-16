너는 내 로컬 PC에서 실행되는 “오늘의 플러스 → Obsidian 지식 베이스 아카이버”를 만들어야 한다.

목표:
ChatGPT의 ‘오늘의 플러스’ 내용을 사용자가 직접 복사하거나 로컬 파일로 저장하면, 해당 내용을 자동으로 정리해서 Obsidian Vault 안에 날짜별 Markdown 노트로 저장하고, 중복 내용을 제거하며, 태그/메타데이터/요약/액션아이템까지 생성하는 로컬 자동화 도구를 만들어라.

중요한 제약:
1. ChatGPT 웹페이지를 자동 로그인, 세션 탈취, 우회, CAPTCHA 우회, 무단 크롤링 방식으로 스크래핑하지 마라.
2. 사용자가 직접 복사한 클립보드 텍스트, 직접 저장한 HTML/PDF/TXT/MD 파일, 또는 직접 캡처한 스크린샷 OCR 입력만 처리하라.
3. 계정 비밀번호, 세션 쿠키, 토큰을 코드에 저장하지 마라.
4. 모든 데이터는 로컬 PC 안에서만 처리되도록 설계하라.
5. Obsidian Vault 경로는 .env 또는 config.yaml에서 설정할 수 있게 하라.

개발 환경:
- OS: Windows 기준으로 작성하되, macOS/Linux에서도 동작 가능하게 경로 처리를 pathlib로 구현
- 언어: Python 3.11 이상
- 저장 위치: Obsidian Vault 내부의 폴더
- 기본 저장 폴더 예시: 00_Inbox/TodayPlus
- 설정 파일: config.yaml
- 로그 파일: logs/today_plus_archiver.log

필수 기능:

1. 입력 방식 3가지 지원
   A. 클립보드 모드
      - 사용자가 오늘의 플러스 내용을 복사한 뒤 프로그램을 실행하면 클립보드 텍스트를 읽는다.
      - pyperclip을 사용한다.
   
   B. 파일 감시 모드
      - 사용자가 특정 폴더에 HTML, TXT, MD 파일을 저장하면 자동으로 감지한다.
      - watchdog을 사용한다.
      - 감시 폴더 예시: ~/TodayPlus_Input
   
   C. 수동 파일 입력 모드
      - python main.py --file "파일경로"
      - 해당 파일을 읽어서 Markdown으로 변환한다.

2. Markdown 저장 규칙
   - Obsidian Vault 안에 날짜별 노트를 만든다.
   - 파일명 형식:
     YYYY-MM-DD_오늘의-플러스.md
   - 예시:
     2026-05-16_오늘의-플러스.md

3. 노트 구조
   Markdown 파일은 아래 구조로 저장한다.

   ---
   title: 오늘의 플러스
   date: YYYY-MM-DD
   source: ChatGPT Today Plus
   type: daily-archive
   tags:
     - today-plus
     - chatgpt
     - ai-trend
     - knowledge-base
   created: ISO_DATETIME
   updated: ISO_DATETIME
   ---

   # YYYY-MM-DD 오늘의 플러스

   ## 원문 저장
   사용자가 복사하거나 저장한 원문 내용을 이곳에 정리해서 넣는다.

   ## 핵심 요약
   - 핵심 내용 3~7개를 bullet로 요약한다.

   ## 사업 아이디어 연결
   - 이 내용을 AI 자동화 사업, 콘텐츠 수익화, 인테리어 업무 자동화, Make.com 자동화 관점에서 어떻게 활용할 수 있는지 정리한다.

   ## 실행 액션
   - 오늘 바로 할 수 있는 작업
   - 이번 주 안에 할 수 있는 작업
   - 장기적으로 지식 베이스에 연결할 작업

   ## 관련 키워드
   - 키워드 목록

   ## 중복 체크
   - 이미 저장된 유사 내용이 있으면 관련 노트 링크를 추가한다.

4. 중복 제거 기능
   - 같은 날짜 파일이 이미 있으면 덮어쓰지 말고 내용을 비교한다.
   - 완전히 같은 내용이면 저장하지 않는다.
   - 일부만 다르면 기존 파일 하단에 “추가 수집분” 섹션으로 붙인다.
   - 텍스트 해시는 SHA256으로 생성한다.
   - 저장된 해시는 .today_plus_index.json 파일에 기록한다.

5. Obsidian 내부 링크 생성
   - 저장된 노트에는 아래 링크를 자동 삽입한다.
   - [[AI 자동화]]
   - [[ChatGPT]]
   - [[콘텐츠 수익화]]
   - [[Make.com]]
   - [[지식 베이스]]
   - 내용에 따라 자동으로 관련 링크를 추가한다.

6. 요약 생성 방식
   - 외부 유료 API를 사용하지 않는 기본 버전을 먼저 만든다.
   - 기본 버전은 규칙 기반 요약으로 작성한다.
   - 문장 분리, 키워드 빈도, 제목/목록 패턴을 기준으로 핵심 내용을 추출한다.
   - 추후 OpenAI API 또는 로컬 LLM을 붙일 수 있도록 summarizer.py를 모듈화한다.

7. 프로젝트 구조
   아래 구조로 파일을 생성하라.

   today-plus-obsidian-archiver/
   ├─ main.py
   ├─ config.yaml
   ├─ requirements.txt
   ├─ README.md
   ├─ src/
   │  ├─ clipboard_reader.py
   │  ├─ file_reader.py
   │  ├─ markdown_writer.py
   │  ├─ deduplicator.py
   │  ├─ summarizer.py
   │  ├─ keyword_extractor.py
   │  ├─ obsidian_linker.py
   │  └─ logger.py
   ├─ logs/
   │  └─ .gitkeep
   └─ tests/
      ├─ test_deduplicator.py
      ├─ test_markdown_writer.py
      └─ test_summarizer.py

8. CLI 명령어
   아래 명령이 동작하게 만들어라.

   python main.py --clipboard
   - 현재 클립보드 내용을 읽어서 오늘 날짜의 Obsidian 노트로 저장한다.

   python main.py --file "C:/Users/사용자/Downloads/today_plus.html"
   - 지정한 파일을 읽어서 저장한다.

   python main.py --watch
   - config.yaml에 지정한 input_folder를 감시하고 새 파일이 생기면 자동 저장한다.

   python main.py --rebuild-index
   - 기존 TodayPlus 폴더의 Markdown 파일들을 다시 읽어서 중복 인덱스를 재생성한다.

9. config.yaml 예시
   아래 기본 설정 파일을 만들어라.

   obsidian_vault_path: "C:/Users/YOUR_NAME/Documents/ObsidianVault"
   output_folder: "00_Inbox/TodayPlus"
   input_folder: "C:/Users/YOUR_NAME/TodayPlus_Input"
   index_file: ".today_plus_index.json"
   language: "ko"
   default_tags:
     - today-plus
     - chatgpt
     - ai-trend
     - knowledge-base
   related_links:
     - "AI 자동화"
     - "ChatGPT"
     - "콘텐츠 수익화"
     - "Make.com"
     - "지식 베이스"
     - "인테리어 자동화"
   duplicate_similarity_threshold: 0.92

10. requirements.txt
   필요한 라이브러리를 작성하라.
   최소 포함:
   - pyperclip
   - pyyaml
   - watchdog
   - beautifulsoup4
   - python-dateutil

11. HTML 처리
   - HTML 파일이 입력되면 BeautifulSoup으로 script, style, nav, footer를 제거한다.
   - 본문 텍스트만 추출한다.
   - 링크가 있으면 Markdown 링크 형식으로 변환한다.
   - 너무 긴 공백은 정리한다.

12. TXT/MD 처리
   - 그대로 읽되, 불필요한 공백과 반복 줄바꿈을 정리한다.

13. 예외 처리
   - Obsidian Vault 경로가 없으면 명확한 에러 메시지를 출력한다.
   - 클립보드가 비어 있으면 저장하지 않는다.
   - 파일 확장자가 지원되지 않으면 안내 메시지를 출력한다.
   - 저장 실패 시 logs/today_plus_archiver.log에 기록한다.

14. README.md 작성
   README에는 아래 내용을 포함하라.
   - 설치 방법
   - config.yaml 설정 방법
   - 클립보드 저장 방법
   - 파일 감시 모드 사용 방법
   - Obsidian에서 확인하는 방법
   - 자동 실행 등록 방법

15. Windows 자동 실행 방법
   README에 Windows 작업 스케줄러 등록 예시를 추가하라.
   예:
   - 매일 오전 9시 python main.py --clipboard 실행
   - 또는 로그인 시 python main.py --watch 실행

16. 품질 기준
   - 모든 코드는 함수 단위로 분리한다.
   - pathlib를 사용한다.
   - 타입 힌트를 넣는다.
   - 주요 함수에는 docstring을 작성한다.
   - 테스트 코드를 포함한다.
   - 처음 실행하는 사용자가 README만 보고 설치할 수 있어야 한다.

최종 산출물:
1. 전체 프로젝트 코드
2. requirements.txt
3. config.yaml
4. README.md
5. 테스트 코드
6. 실행 예시

추가 요청:
코드 작성이 끝나면 아래 순서로 사용법을 설명하라.

1. 가상환경 생성
2. 패키지 설치
3. config.yaml에서 Obsidian Vault 경로 수정
4. 오늘의 플러스 내용을 직접 복사
5. python main.py --clipboard 실행
6. Obsidian에서 YYYY-MM-DD_오늘의-플러스.md 파일 확인