from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from src.clipboard_reader import read_clipboard
from src.deduplicator import Deduplicator
from src.file_reader import read_input_file
from src.logger import setup_logger
from src.markdown_writer import MarkdownWriter
from src.obsidian_linker import build_related_links
from src.summarizer import RuleBasedSummarizer


def load_config(path: Path = Path("config.yaml")) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError("config.yaml 파일이 없습니다.")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def archive_text(text: str, config: dict[str, Any]) -> Path | None:
    vault_path = Path(config["obsidian_vault_path"]).expanduser()
    output_folder = config.get("output_folder", "00_Inbox/TodayPlus")
    index_file = config.get("index_file", ".today_plus_index.json")
    today = date.today().isoformat()

    writer = MarkdownWriter(vault_path=vault_path, output_folder=output_folder)
    writer.ensure_ready()
    output_dir = writer.output_dir
    dedup = Deduplicator(
        index_path=output_dir / index_file,
        similarity_threshold=float(config.get("duplicate_similarity_threshold", 0.92)),
    )
    duplicate = dedup.check(text)
    if duplicate.is_duplicate:
        print(f"이미 저장된 동일 내용입니다: {duplicate.match_path}")
        return None

    summarizer = RuleBasedSummarizer()
    related_links = build_related_links(text, config.get("related_links", []))
    note_path = writer.note_path(today)

    if duplicate.is_similar and note_path.exists():
        writer.append_collection(note_path, text)
        dedup.record(text, note_path)
        print(f"유사 내용 추가 수집분으로 저장: {note_path}")
        return note_path

    note_path = writer.write_new_note(
        date=today,
        original_text=text,
        summary=summarizer.summarize(text),
        business_points=summarizer.business_points(text),
        content_ideas=summarizer.content_ideas(text),
        actions=summarizer.actions(),
        keywords=summarizer.extract_keywords(text),
        related_links=related_links,
        tags=config.get("default_tags", []),
        priorities=summarizer.priorities(),
    )
    dedup.record(text, note_path)
    print(f"저장 완료: {note_path}")
    return note_path


def handle_watch_path(path: Path, config: dict[str, Any]) -> bool:
    file_path = Path(path)
    if file_path.suffix.lower() not in {".html", ".htm", ".txt", ".md"}:
        print(f"지원하지 않는 파일 무시: {file_path}")
        return False
    archive_text(read_input_file(file_path), config)
    return True


def watch_folder(config: dict[str, Any]) -> None:
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError as exc:
        raise RuntimeError("watchdog가 설치되어 있지 않습니다. requirements.txt를 설치하세요.") from exc

    input_folder = Path(config["input_folder"]).expanduser()
    input_folder.mkdir(parents=True, exist_ok=True)

    class Handler(FileSystemEventHandler):
        def on_created(self, event: Any) -> None:
            if event.is_directory:
                return
            handle_watch_path(Path(event.src_path), config)

        def on_moved(self, event: Any) -> None:
            if event.is_directory:
                return
            handle_watch_path(Path(event.dest_path), config)

    observer = Observer()
    observer.schedule(Handler(), str(input_folder), recursive=False)
    observer.start()
    print(f"감시 시작: {input_folder}")
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def rebuild_index(config: dict[str, Any]) -> int:
    vault_path = Path(config["obsidian_vault_path"]).expanduser()
    output_dir = vault_path / config.get("output_folder", "00_Inbox/TodayPlus")
    dedup = Deduplicator(output_dir / config.get("index_file", ".today_plus_index.json"))
    count = dedup.rebuild(output_dir)
    print(f"인덱스 재생성 완료: {count}개")
    return count


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ChatGPT 오늘의 플러스를 Obsidian 노트로 저장합니다.")
    parser.add_argument("--config", default="config.yaml", help="설정 파일 경로")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--clipboard", action="store_true", help="클립보드 텍스트 저장")
    mode.add_argument("--file", type=str, help="HTML/TXT/MD 파일 저장")
    mode.add_argument("--watch", action="store_true", help="입력 폴더 감시")
    mode.add_argument("--rebuild-index", action="store_true", help="중복 인덱스 재생성")
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    config = load_config(Path(args.config))
    logger = setup_logger(Path("logs/today_plus_archiver.log"))
    try:
        if args.clipboard:
            archive_text(read_clipboard(), config)
        elif args.file:
            archive_text(read_input_file(Path(args.file)), config)
        elif args.watch:
            watch_folder(config)
        elif args.rebuild_index:
            rebuild_index(config)
        return 0
    except Exception as exc:
        logger.exception("실행 실패")
        print(f"오류: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
