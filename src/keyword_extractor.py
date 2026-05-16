from __future__ import annotations

from src.summarizer import RuleBasedSummarizer


def extract_keywords(text: str, limit: int = 12) -> list[str]:
    return RuleBasedSummarizer(max_keywords=limit).extract_keywords(text)
