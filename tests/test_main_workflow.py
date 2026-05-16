import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import archive_text, handle_watch_path, load_config, parse_args, process_inbox_once


class MainWorkflowTest(unittest.TestCase):
    def test_archives_text_to_configured_vault(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            vault.mkdir()
            config = {
                "obsidian_vault_path": str(vault),
                "output_folder": "00_Inbox/TodayPlus",
                "index_file": ".today_plus_index.json",
                "default_tags": ["today-plus", "chatgpt"],
                "related_links": ["AI 자동화", "ChatGPT"],
                "duplicate_similarity_threshold": 0.92,
            }

            note_path = archive_text(
                "AI automation with ChatGPT and Make.com for Obsidian knowledge base.",
                config,
            )

            self.assertIsNotNone(note_path)
            self.assertTrue(note_path.exists())
            self.assertTrue((vault / "00_Inbox/TodayPlus/.today_plus_index.json").exists())

    def test_archiving_second_distinct_capture_preserves_existing_daily_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            vault.mkdir()
            config = {
                "obsidian_vault_path": str(vault),
                "output_folder": "00_Inbox/TodayPlus",
                "index_file": ".today_plus_index.json",
                "default_tags": ["today-plus", "chatgpt"],
                "related_links": [],
                "duplicate_similarity_threshold": 0.92,
            }

            note_path = archive_text(
                "First distinct capture about AI automation workflows and operational notes.",
                config,
            )
            first_content = note_path.read_text(encoding="utf-8")

            second_note_path = archive_text(
                "Second unrelated capture about interior business planning and sales scripts.",
                config,
            )
            second_content = second_note_path.read_text(encoding="utf-8")

            self.assertEqual(second_note_path, note_path)
            self.assertIn("First distinct capture", second_content)
            self.assertIn("Second unrelated capture", second_content)
            self.assertIn("## 추가 수집분", second_content)
            self.assertGreater(len(second_content), len(first_content))

    def test_loads_explicit_config_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "custom.yaml"
            config_path.write_text(
                'obsidian_vault_path: "C:/Vault"\noutput_folder: "Inbox"\n',
                encoding="utf-8",
            )

            config = load_config(config_path)

            self.assertEqual(config["output_folder"], "Inbox")

    def test_remote_devcore_example_config_loads(self):
        config = load_config(Path("config.example.remote-devcore.yaml"))

        self.assertEqual(
            config["input_folder"],
            "D:/ai프로젝트/today-plus-obsidian-archiver/inbox",
        )
        self.assertIn("today-plus", config["default_tags"])
        self.assertIn("ChatGPT", config["related_links"])

    def test_parse_args_accepts_explicit_config_path(self):
        args = parse_args(["--config", "custom.yaml", "--file", "input.md"])

        self.assertEqual(args.config, "custom.yaml")
        self.assertEqual(args.file, "input.md")

    def test_parse_args_accepts_process_inbox_once(self):
        args = parse_args(["--process-inbox-once"])

        self.assertTrue(args.process_inbox_once)

    def test_watch_path_ignores_temp_files(self):
        config = {"obsidian_vault_path": "unused"}

        with patch("main.read_input_file") as read_input_file:
            handled = handle_watch_path(Path("today-plus.tmp"), config)

        self.assertFalse(handled)
        read_input_file.assert_not_called()

    def test_watch_path_archives_supported_files(self):
        config = {"obsidian_vault_path": "unused"}

        with (
            patch("main.read_input_file", return_value="Today Plus content") as read_input_file,
            patch("main.archive_text") as archive_text_mock,
        ):
            handled = handle_watch_path(Path("today-plus.md"), config)

        self.assertTrue(handled)
        read_input_file.assert_called_once_with(Path("today-plus.md"))
        archive_text_mock.assert_called_once_with("Today Plus content", config)

    def test_process_inbox_once_handles_supported_files_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_folder = Path(tmp) / "inbox"
            input_folder.mkdir()
            (input_folder / "a.tmp").write_text("partial", encoding="utf-8")
            (input_folder / "b.md").write_text("Today Plus markdown", encoding="utf-8")
            (input_folder / "c.txt").write_text("Today Plus text", encoding="utf-8")
            config = {"input_folder": str(input_folder), "obsidian_vault_path": "unused"}

            with patch("main.handle_watch_path", return_value=True) as handle_watch_path_mock:
                count = process_inbox_once(config)

        self.assertEqual(count, 2)
        handled_paths = [call.args[0] for call in handle_watch_path_mock.call_args_list]
        self.assertEqual(
            handled_paths,
            [input_folder / "b.md", input_folder / "c.txt"],
        )

    def test_process_inbox_once_can_move_processed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_folder = Path(tmp) / "inbox"
            input_folder.mkdir()
            markdown_path = input_folder / "today-plus.md"
            markdown_path.write_text("Today Plus markdown", encoding="utf-8")
            config = {"input_folder": str(input_folder), "obsidian_vault_path": "unused"}

            with patch("main.handle_watch_path", return_value=True):
                count = process_inbox_once(config, archive_processed=True)

            processed_path = input_folder / "processed" / "today-plus.md"
            self.assertEqual(count, 1)
            self.assertFalse(markdown_path.exists())
            self.assertTrue(processed_path.exists())

    def test_process_inbox_once_does_not_overwrite_processed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_folder = Path(tmp) / "inbox"
            processed_folder = input_folder / "processed"
            processed_folder.mkdir(parents=True)
            markdown_path = input_folder / "today-plus.md"
            existing_processed_path = processed_folder / "today-plus.md"
            markdown_path.write_text("new content", encoding="utf-8")
            existing_processed_path.write_text("existing content", encoding="utf-8")
            config = {"input_folder": str(input_folder), "obsidian_vault_path": "unused"}

            with patch("main.handle_watch_path", return_value=True):
                count = process_inbox_once(config, archive_processed=True)

            self.assertEqual(count, 1)
            self.assertEqual(existing_processed_path.read_text(encoding="utf-8"), "existing content")
            self.assertTrue((processed_folder / "today-plus-1.md").exists())


if __name__ == "__main__":
    unittest.main()
