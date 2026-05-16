from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DuplicateResult:
    is_duplicate: bool
    is_similar: bool
    match_path: str | None = None
    similarity: float = 0.0


class Deduplicator:
    """Manage SHA256 content hashes and lightweight similarity checks."""

    def __init__(self, index_path: Path, similarity_threshold: float = 0.92) -> None:
        self.index_path = Path(index_path)
        self.similarity_threshold = similarity_threshold

    def check(self, content: str) -> DuplicateResult:
        normalized = self._normalize(content)
        content_hash = self.hash_content(normalized)
        index = self._load()

        for item in index.get("items", []):
            if item.get("hash") == content_hash:
                return DuplicateResult(
                    is_duplicate=True,
                    is_similar=True,
                    match_path=item.get("path"),
                    similarity=1.0,
                )

        best_path: str | None = None
        best_score = 0.0
        for item in index.get("items", []):
            previous = item.get("content", "")
            score = SequenceMatcher(None, normalized, previous).ratio()
            if score > best_score:
                best_score = score
                best_path = item.get("path")

        return DuplicateResult(
            is_duplicate=False,
            is_similar=best_score >= self.similarity_threshold,
            match_path=best_path if best_score >= self.similarity_threshold else None,
            similarity=best_score,
        )

    def record(self, content: str, note_path: Path) -> None:
        normalized = self._normalize(content)
        index = self._load()
        content_hash = self.hash_content(normalized)
        items = [item for item in index.get("items", []) if item.get("hash") != content_hash]
        items.append(
            {
                "hash": content_hash,
                "path": str(note_path),
                "content": normalized,
            }
        )
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(
            json.dumps({"items": items}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def rebuild(self, folder: Path) -> int:
        items: list[dict[str, str]] = []
        for note in sorted(Path(folder).glob("*.md")):
            content = self._normalize(note.read_text(encoding="utf-8"))
            items.append(
                {
                    "hash": self.hash_content(content),
                    "path": str(note),
                    "content": content,
                }
            )
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(
            json.dumps({"items": items}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return len(items)

    @staticmethod
    def hash_content(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _load(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return {"items": []}
        try:
            return json.loads(self.index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"items": []}

    @staticmethod
    def _normalize(content: str) -> str:
        return "\n".join(line.strip() for line in content.splitlines() if line.strip())
