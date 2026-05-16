from __future__ import annotations

import re
from collections import Counter


class RuleBasedSummarizer:
    """Extract summaries and keywords without external paid APIs."""

    STOPWORDS = {
        "the",
        "and",
        "for",
        "with",
        "that",
        "this",
        "from",
        "into",
        "can",
        "how",
        "are",
        "오늘",
        "내용",
        "통해",
        "대한",
        "있는",
        "으로",
        "에서",
        "하다",
        "된다",
    }

    def __init__(self, max_items: int = 7, max_keywords: int = 12) -> None:
        self.max_items = max_items
        self.max_keywords = max_keywords

    def summarize(self, text: str) -> list[str]:
        candidates = self._candidate_lines(text)
        if not candidates:
            return []
        scored = sorted(
            candidates,
            key=lambda line: (self._score_line(line), -candidates.index(line)),
            reverse=True,
        )
        result: list[str] = []
        for line in scored:
            clean = line.strip(" -\t")
            if clean and clean not in result:
                result.append(clean)
            if len(result) >= self.max_items:
                break
        return result

    def extract_keywords(self, text: str) -> list[str]:
        words = re.findall(r"[A-Za-z0-9가-힣.]{2,}", text.lower())
        filtered = [word for word in words if word not in self.STOPWORDS and not word.isdigit()]
        counts = Counter(filtered)
        return [word for word, _count in counts.most_common(self.max_keywords)]

    def business_points(self, text: str) -> list[str]:
        keywords = ", ".join(self.extract_keywords(text)[:5]) or "핵심 주제"
        return [
            f"AI 자동화 사업 관점에서 '{keywords}' 흐름을 반복 업무 자동화 소재로 검토",
            "Make.com 시나리오로 수집, 분류, 요약, Obsidian 저장 과정을 자동화 가능",
            "인테리어 업무에서는 상담 기록, 현장 이슈, 감리 체크리스트 지식화에 응용 가능",
            "블로그, 유튜브 쇼츠, 애드센스 콘텐츠 주제로 재가공 가능",
            "반복 수요가 확인되면 유료 템플릿 또는 자동화 패키지로 발전 가능",
        ]

    def content_ideas(self, text: str) -> list[str]:
        keywords = self.extract_keywords(text)
        topic = keywords[0] if keywords else "AI 자동화"
        return [
            f"블로그: {topic}를 업무 자동화에 연결하는 방법",
            f"블로그: 오늘의 AI 트렌드에서 찾은 {topic} 기회",
            f"블로그: Obsidian 지식 베이스로 {topic} 관리하기",
            f"블로그: Make.com으로 {topic} 수집 자동화하기",
            f"블로그: 소상공인을 위한 {topic} 활용 전략",
            f"유튜브 쇼츠: {topic} 핵심만 30초 요약",
            "유튜브 쇼츠: 오늘 바로 써먹는 AI 자동화 아이디어",
            "유튜브 쇼츠: Obsidian에 쌓으면 돈 되는 지식",
            "유튜브 쇼츠: Make.com 자동화 전후 비교",
            "유튜브 쇼츠: 인테리어 업무에 붙이는 AI 팁",
            "자동화 템플릿: Today Plus 수집 후 Obsidian 저장",
            "자동화 템플릿: 키워드별 콘텐츠 아이디어 생성",
            "자동화 템플릿: 주간 지식 베이스 리포트",
        ]

    def actions(self) -> list[str]:
        return [
            "오늘: 핵심 내용 1개를 기존 사업 아이디어 노트와 연결",
            "이번 주: 반복 등장 키워드를 기준으로 콘텐츠 초안 1개 작성",
            "장기: 유사 주제를 묶어 자동화 템플릿 또는 유료 서비스 후보로 관리",
        ]

    def priorities(self) -> dict[str, int]:
        return {
            "수익화 가능성": 4,
            "자동화 가능성": 5,
            "실행 난이도": 3,
            "기존 업무 연관성": 4,
            "장기 지식 자산 가치": 5,
        }

    def _candidate_lines(self, text: str) -> list[str]:
        lines = []
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith(("#", "-", "*")) or 30 <= len(line) <= 220:
                lines.append(line.strip("#-* "))
        if lines:
            return lines
        return [part.strip() for part in re.split(r"(?<=[.!?。])\s+", text) if part.strip()]

    def _score_line(self, line: str) -> int:
        lowered = line.lower()
        score = min(len(line), 160)
        for marker in ("ai", "자동화", "make.com", "obsidian", "수익", "콘텐츠", "업무"):
            if marker in lowered:
                score += 40
        return score
