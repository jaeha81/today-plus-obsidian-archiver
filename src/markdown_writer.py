from __future__ import annotations

from datetime import datetime
from pathlib import Path


class MarkdownWriter:
    """Write Today Plus notes into an Obsidian vault."""

    def __init__(self, vault_path: Path, output_folder: str) -> None:
        self.vault_path = Path(vault_path).expanduser()
        self.output_dir = self.vault_path / output_folder

    def ensure_ready(self) -> None:
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Obsidian Vault 경로가 없습니다: {self.vault_path}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def note_path(self, date: str) -> Path:
        return self.output_dir / f"{date}_오늘의-플러스.md"

    def write_new_note(
        self,
        date: str,
        original_text: str,
        summary: list[str],
        business_points: list[str],
        content_ideas: list[str],
        actions: list[str],
        keywords: list[str],
        related_links: list[str],
        tags: list[str],
        priorities: dict[str, int] | None = None,
    ) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        now = datetime.now().isoformat(timespec="seconds")
        path = self.note_path(date)
        content = self._render(
            date=date,
            original_text=original_text,
            summary=summary,
            business_points=business_points,
            content_ideas=content_ideas,
            actions=actions,
            keywords=keywords,
            related_links=related_links,
            tags=tags,
            created=now,
            updated=now,
            priorities=priorities or {},
        )
        path.write_text(content, encoding="utf-8")
        return path

    def append_collection(self, note_path: Path, text: str) -> None:
        timestamp = datetime.now().isoformat(timespec="seconds")
        addition = f"\n\n## 추가 수집분\n\n수집 시각: {timestamp}\n\n{text.strip()}\n"
        with Path(note_path).open("a", encoding="utf-8") as handle:
            handle.write(addition)

    def _render(
        self,
        date: str,
        original_text: str,
        summary: list[str],
        business_points: list[str],
        content_ideas: list[str],
        actions: list[str],
        keywords: list[str],
        related_links: list[str],
        tags: list[str],
        created: str,
        updated: str,
        priorities: dict[str, int],
    ) -> str:
        tag_lines = "\n".join(f"  - {tag}" for tag in tags)
        link_lines = "\n".join(f"- [[{link}]]" for link in related_links)
        priority_lines = "\n".join(f"- {name}: {score}/5" for name, score in priorities.items())
        return f"""---
title: 오늘의 플러스
date: {date}
source: ChatGPT Today Plus
type: daily-archive
tags:
{tag_lines}
created: {created}
updated: {updated}
---

# {date} 오늘의 플러스

## 원문 저장
{original_text.strip()}

## 핵심 요약
{self._bullets(summary)}

## 사업 아이디어 연결
{self._bullets(business_points)}

## 내 사업에 적용할 포인트
{self._bullets(business_points)}

## 콘텐츠화 아이디어
{self._bullets(content_ideas)}

## 실행 액션
{self._bullets(actions)}

## 우선순위
{priority_lines or "- 평가 항목 없음"}

## 관련 키워드
{self._bullets(keywords)}

## Obsidian 내부 링크
{link_lines}

## 중복 체크
- SHA256 인덱스 기준으로 저장 여부 확인
"""

    @staticmethod
    def _bullets(items: list[str]) -> str:
        if not items:
            return "- 없음"
        return "\n".join(f"- {item}" for item in items)
