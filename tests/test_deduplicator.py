import tempfile
import unittest
from pathlib import Path

from src.deduplicator import Deduplicator


class DeduplicatorTest(unittest.TestCase):
    def test_identifies_exact_duplicate_by_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / ".today_plus_index.json"
            dedup = Deduplicator(index_path=index_path, similarity_threshold=0.92)
            content = "same today plus content"

            result = dedup.check(content)
            self.assertFalse(result.is_duplicate)

            dedup.record(content, Path("2026-05-16_오늘의-플러스.md"))
            duplicate = dedup.check(content)

            self.assertTrue(duplicate.is_duplicate)
            self.assertEqual(duplicate.match_path, "2026-05-16_오늘의-플러스.md")

    def test_detects_similar_content_over_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / ".today_plus_index.json"
            dedup = Deduplicator(index_path=index_path, similarity_threshold=0.8)
            dedup.record(
                "AI automation content for Obsidian archive and Make.com workflow",
                Path("note.md"),
            )

            result = dedup.check(
                "AI automation content for Obsidian archive and Make.com workflow updated"
            )

            self.assertFalse(result.is_duplicate)
            self.assertTrue(result.is_similar)
            self.assertEqual(result.match_path, "note.md")


if __name__ == "__main__":
    unittest.main()
