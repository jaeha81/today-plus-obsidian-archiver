from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path


class _TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._link_href: str | None = None
        self._link_parts: list[str] = []
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "nav", "footer"}:
            self._skip_depth += 1
        if tag == "a" and not self._skip_depth:
            href = dict(attrs).get("href")
            if href:
                self._link_href = href
                self._link_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._link_href and not self._skip_depth:
            label = clean_text(" ".join(self._link_parts))
            if label:
                self.parts.append(f"[{label}]({self._link_href})")
            else:
                self.parts.append(self._link_href)
            self._link_href = None
            self._link_parts = []
        if tag in {"script", "style", "nav", "footer"} and self._skip_depth:
            self._skip_depth -= 1
        if tag in {"p", "div", "br", "li", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            if self._link_href:
                self._link_parts.append(data)
            else:
                self.parts.append(data)


def read_input_file(path: Path) -> str:
    file_path = Path(path).expanduser()
    if not file_path.exists():
        raise FileNotFoundError(f"입력 파일이 없습니다: {file_path}")
    suffix = file_path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return clean_text(file_path.read_text(encoding="utf-8"))
    if suffix in {".html", ".htm"}:
        return html_to_text(file_path.read_text(encoding="utf-8"))
    raise ValueError(f"지원하지 않는 파일 형식입니다: {suffix}")


def html_to_text(html: str) -> str:
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        parser = _TextHTMLParser()
        parser.feed(html)
        return clean_text(" ".join(parser.parts))

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    for link in soup.find_all("a"):
        href = link.get("href")
        label = link.get_text(" ", strip=True)
        if href and label:
            link.replace_with(f"[{label}]({href})")
    return clean_text(soup.get_text("\n"))


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
