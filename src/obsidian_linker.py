from __future__ import annotations


def build_related_links(text: str, configured_links: list[str]) -> list[str]:
    lowered = text.lower()
    links = list(dict.fromkeys(configured_links))
    auto_rules = {
        "AI 자동화": ("ai", "자동화", "automation"),
        "ChatGPT": ("chatgpt", "gpt"),
        "Make.com": ("make.com", "make"),
        "콘텐츠 수익화": ("콘텐츠", "수익", "adsense", "유튜브", "블로그"),
        "지식 베이스": ("obsidian", "지식", "knowledge"),
        "인테리어 자동화": ("인테리어", "시공", "감리", "디자인"),
    }
    for link, markers in auto_rules.items():
        if any(marker in lowered for marker in markers) and link not in links:
            links.append(link)
    return links
