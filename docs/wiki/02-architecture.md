# Architecture

## 진입점

`main.py`

- CLI 인자 파싱
- config 로딩
- 입력 모드 분기
- archive workflow 실행
- 로그 기록

## 모듈

```text
src/
  clipboard_reader.py   # 클립보드 입력
  file_reader.py        # HTML/TXT/MD 읽기 및 정리
  markdown_writer.py    # Obsidian Markdown 작성
  deduplicator.py       # SHA256/유사도 중복 체크
  summarizer.py         # 규칙 기반 요약/키워드/사업 아이디어
  keyword_extractor.py  # 키워드 추출 facade
  obsidian_linker.py    # 내부 링크 생성
  logger.py             # 파일 로그 설정
```

## 데이터 흐름

```text
clipboard/file/watch
  -> text cleanup
  -> duplicate check
  -> summary/keywords/business mapping
  -> related Obsidian links
  -> markdown note write or append
  -> index update
```

## 저장 위치

`config.yaml`

```yaml
obsidian_vault_path: "C:/Users/YOUR_NAME/Documents/ObsidianVault"
output_folder: "00_Inbox/TodayPlus"
input_folder: "C:/Users/YOUR_NAME/TodayPlus_Input"
index_file: ".today_plus_index.json"
```

## 오류 처리

- Vault 경로 없음: 명확한 오류 출력
- 클립보드 비어 있음: 저장하지 않음
- 미지원 확장자: 안내 메시지
- 저장 실패: `logs/today_plus_archiver.log` 기록
