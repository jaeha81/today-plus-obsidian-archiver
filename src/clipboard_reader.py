from __future__ import annotations


def read_clipboard() -> str:
    try:
        import pyperclip
    except ImportError as exc:
        raise RuntimeError("pyperclip이 설치되어 있지 않습니다. requirements.txt를 설치하세요.") from exc

    text = pyperclip.paste()
    if not text or not text.strip():
        raise ValueError("클립보드가 비어 있습니다.")
    return text.strip()
