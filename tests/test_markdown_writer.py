import tempfile
import unittest
from pathlib import Path

from src.markdown_writer import MarkdownWriter


class MarkdownWriterTest(unittest.TestCase):
    def test_writes_daily_note_with_frontmatter_and_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            writer = MarkdownWriter(vault_path=vault, output_folder="00_Inbox/TodayPlus")

            path = writer.write_new_note(
                date="2026-05-16",
                original_text="Original body",
                summary=["First point"],
                business_points=["Business point"],
                content_ideas=["Blog title"],
                actions=["Do today"],
                keywords=["AI"],
                related_links=["ChatGPT"],
                tags=["today-plus"],
            )

            self.assertEqual(path.name, "2026-05-16_오늘의-플러스.md")
            content = path.read_text(encoding="utf-8")
            self.assertIn("title: 오늘의 플러스", content)
            self.assertIn("## 원문 저장", content)
            self.assertIn("[[ChatGPT]]", content)
            self.assertIn("## 내 사업에 적용할 포인트", content)

    def test_appends_additional_collection_without_overwriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            writer = MarkdownWriter(vault_path=vault, output_folder="00_Inbox/TodayPlus")
            note = writer.write_new_note(
                date="2026-05-16",
                original_text="First",
                summary=[],
                business_points=[],
                content_ideas=[],
                actions=[],
                keywords=[],
                related_links=[],
                tags=[],
            )

            writer.append_collection(note, "Second")

            content = note.read_text(encoding="utf-8")
            self.assertIn("First", content)
            self.assertIn("## 추가 수집분", content)
            self.assertIn("Second", content)


if __name__ == "__main__":
    unittest.main()
