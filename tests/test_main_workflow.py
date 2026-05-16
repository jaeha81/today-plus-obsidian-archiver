import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import archive_text, handle_watch_path, load_config, parse_args


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


if __name__ == "__main__":
    unittest.main()
