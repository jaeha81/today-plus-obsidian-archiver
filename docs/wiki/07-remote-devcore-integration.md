# Remote DevCore Integration

이 문서는 `jH Remote DevCore`와 `today-plus-obsidian-archiver`를 연결하는 파일 드롭 규약을 정의한다.

## 목적

모바일에서 ChatGPT 오늘의 플러스 내용을 수동으로 파일 저장 후 PC로 옮기는 절차를 줄인다.

`jH Remote DevCore`는 Discord, Whisper Agent Bot, Local Control Agent를 통해 사용자가 보낸 내용을 로컬 PC의 inbox 폴더에 파일로 내려준다. 이 아카이버는 해당 폴더를 `--watch`로 감시하고 Obsidian 노트로 정리한다.

## 데이터 흐름

```text
모바일 ChatGPT
  -> 사용자가 Discord/Whisper/Remote DevCore 채널에 오늘의 플러스 내용 전달
  -> jH Remote DevCore 수신
  -> Local Control Agent가 로컬 inbox 폴더에 .md 또는 .txt 파일 생성
  -> today-plus-obsidian-archiver --watch 감지
  -> Obsidian TodayPlus 노트 저장
```

## 폴더 규약

`config.yaml`의 `input_folder`는 Local Control Agent가 파일을 쓰는 폴더와 같아야 한다.

권장 예:

```yaml
input_folder: "D:/ai프로젝트/today-plus-obsidian-archiver/inbox"
```

샘플 운영 config:

```text
config.example.remote-devcore.yaml
```

사용 전 `obsidian_vault_path`를 실제 Obsidian Vault 경로로 바꾼 사본을 만든다.

```powershell
copy config.example.remote-devcore.yaml config.remote-devcore.yaml
python main.py --config config.remote-devcore.yaml --watch
```

지원 확장자:

- `.md`
- `.txt`
- `.html`
- `.htm`

## 파일명 규약

권장 파일명:

```text
today-plus-YYYYMMDD-HHMMSS.md
```

예:

```text
today-plus-20260516-213000.md
```

동시 쓰기나 미완성 파일 감지를 줄이기 위해 Local Control Agent는 임시 파일로 먼저 쓰고 최종 확장자로 rename한다.

```text
today-plus-20260516-213000.tmp
today-plus-20260516-213000.md
```

아카이버 watch 모드는 `.tmp` 생성 이벤트를 무시하고, 최종 `.md`, `.txt`, `.html`, `.htm` 파일 생성 또는 rename 이벤트를 처리한다.

## 파일 내용 권장 형식

```markdown
# Today Plus

source: discord
received_at: 2026-05-16T21:30:00+09:00
sender: user

---

오늘의 플러스 원문 내용...
```

현재 아카이버는 파일 전체를 원문으로 처리한다. 위 metadata는 사람이 추적하기 위한 참고 정보이며, 별도 파싱 계약은 아직 없다.

## Remote DevCore sample payload

Discord slash command 예:

```text
/todayplus 오늘의 플러스 원문 내용...
```

Discord 태그 라우팅 예:

```text
#todayplus
오늘의 플러스 원문 내용...
```

Whisper Agent Bot 텍스트 라우팅 예:

```text
오늘의 플러스 저장:
오늘의 플러스 원문 내용...
```

Remote DevCore가 Local Control Agent로 넘기는 내부 payload 권장 형식:

```json
{
  "type": "today_plus",
  "source": "discord",
  "sender": "user",
  "received_at": "2026-05-16T21:30:00+09:00",
  "content": "오늘의 플러스 원문 내용..."
}
```

Local Control Agent 출력 파일 예:

```markdown
# Today Plus

source: discord
received_at: 2026-05-16T21:30:00+09:00
sender: user

---

오늘의 플러스 원문 내용...
```

성공 응답 예:

```text
Today Plus queued: today-plus-20260516-213000.md
```

실패 응답 예:

```text
Today Plus queue failed: inbox path is not writable
```

## Remote DevCore 구현 요구

1. Today Plus 전용 명령 또는 라우팅 태그를 제공한다.
   예: `/todayplus`, `#todayplus`, Discord slash command
2. 수신한 사용자 메시지를 Local Control Agent로 전달한다.
3. Local Control Agent는 지정 inbox 폴더에 파일을 쓴다.
4. 파일명은 timestamp 기반으로 충돌을 피한다.
5. 파일 쓰기는 `.tmp` 생성 후 `.md` rename 방식을 권장한다.
6. 실패 시 Discord/Whisper 채널에 에러를 보고한다.

## 금지 사항

- ChatGPT 웹 자동 로그인
- 세션 쿠키, 토큰, 비밀번호 접근
- ChatGPT 화면 DOM 또는 앱 UI 자동 크롤링
- CAPTCHA 또는 접근제어 우회
- 사용자가 직접 전달하지 않은 계정 데이터 수집

## 연동 테스트

1. `config.yaml`의 `input_folder`를 Local Control Agent 파일 드롭 폴더로 맞춘다.
2. 아카이버를 감시 모드로 실행한다.

```powershell
python main.py --watch
```

또는 장시간 감시 없이 inbox를 한 번만 처리한다.

```powershell
python main.py --config config.remote-devcore.yaml --process-inbox-once
```

기본 동작은 원본 inbox 파일을 그대로 둔다. 처리 완료 원본을 보관 폴더로 이동하려면 명시적으로 옵션을 추가한다.

```powershell
python main.py --config config.remote-devcore.yaml --process-inbox-once --archive-processed
```

이 옵션은 처리 성공한 지원 확장자 파일만 `inbox/processed/`로 이동한다. 같은 파일명이 이미 있으면 덮어쓰지 않고 `-1`, `-2` 같은 suffix를 붙인다.

3. Remote DevCore에서 테스트 메시지를 보낸다.
4. Local Control Agent가 inbox 폴더에 `.md` 파일을 생성하는지 확인한다.
5. 아카이버가 Obsidian TodayPlus 노트로 저장하는지 확인한다.

## 다음 구현 후보

- Remote DevCore와 실제 end-to-end smoke test
