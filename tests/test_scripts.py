import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


class ScriptsTest(unittest.TestCase):
    def test_clipboard_runner_exists_and_uses_clipboard_mode(self):
        script = SCRIPTS_DIR / "run-clipboard.bat"

        self.assertTrue(script.exists())
        content = script.read_text(encoding="utf-8")
        self.assertIn("main.py", content)
        self.assertIn("--clipboard", content)

    def test_watch_runner_exists_and_uses_watch_mode(self):
        script = SCRIPTS_DIR / "run-watch.bat"

        self.assertTrue(script.exists())
        content = script.read_text(encoding="utf-8")
        self.assertIn("main.py", content)
        self.assertIn("--watch", content)

    def test_process_inbox_once_runner_exists_and_uses_one_shot_mode(self):
        script = SCRIPTS_DIR / "run-process-inbox-once.bat"

        self.assertTrue(script.exists())
        content = script.read_text(encoding="utf-8")
        self.assertIn("main.py", content)
        self.assertIn("--process-inbox-once", content)
        self.assertIn("--archive-processed", content)
        self.assertIn('"%~1"=="--help"', content)

    def test_smoke_process_inbox_once_script_uses_temp_workspace_and_archive_processed(self):
        script = SCRIPTS_DIR / "smoke-process-inbox-once.ps1"

        self.assertTrue(script.exists())
        content = script.read_text(encoding="utf-8")
        self.assertIn("--process-inbox-once", content)
        self.assertIn("--archive-processed", content)
        self.assertIn("Remove-Item", content)
        self.assertIn("StartsWith", content)
        self.assertIn("INBOX_FILE_COUNT", content)
        self.assertIn("PROCESSED_FILES", content)

    def test_remote_devcore_file_drop_smoke_script_simulates_tmp_rename_drop(self):
        script = SCRIPTS_DIR / "smoke-remote-devcore-file-drop.ps1"

        self.assertTrue(script.exists())
        content = script.read_text(encoding="utf-8")
        self.assertIn("today-plus-e2e.tmp", content)
        self.assertIn("today-plus-e2e.md", content)
        self.assertIn("Move-Item", content)
        self.assertIn("--process-inbox-once", content)
        self.assertIn("--archive-processed", content)
        self.assertIn("PROCESSED_FILES", content)
        self.assertIn("VAULT_NOTE_COUNT", content)

    def test_remote_devcore_cli_e2e_smoke_script_runs_devcore_then_archiver(self):
        script = SCRIPTS_DIR / "smoke-remote-devcore-cli-e2e.ps1"

        self.assertTrue(script.exists())
        content = script.read_text(encoding="utf-8")
        self.assertIn("jH Remote DevCore", content)
        self.assertIn("Split-Path $projectRoot -Parent", content)
        self.assertIn("TODAY_PLUS_INBOX", content)
        self.assertIn("node", content)
        self.assertIn("src/cli.js", content)
        self.assertIn("--text", content)
        self.assertIn("--process-inbox-once", content)
        self.assertIn("--archive-processed", content)
        self.assertIn("DEVCORE_DROPPED_FILES", content)
        self.assertIn("VAULT_NOTE_COUNT", content)

    def test_file_runner_exists_and_uses_file_mode(self):
        script = SCRIPTS_DIR / "run-file.bat"

        self.assertTrue(script.exists())
        content = script.read_text(encoding="utf-8")
        self.assertIn("main.py", content)
        self.assertIn("--file", content)
        self.assertIn("%~1", content)
        self.assertIn('"%~1"=="--help"', content)
        self.assertNotIn("--file \"%~1\" %*", content)

    def test_daily_capture_runner_opens_chatgpt_without_scraping(self):
        script = SCRIPTS_DIR / "run-daily-capture.bat"

        self.assertTrue(script.exists())
        content = script.read_text(encoding="utf-8")
        self.assertIn("https://chatgpt.com", content)
        self.assertIn("run-clipboard.bat", content)
        self.assertIn("pause", content.lower())
        self.assertIn('"%~1"=="--help"', content)
        self.assertNotIn("cookie", content.lower())
        self.assertNotIn("selenium", content.lower())
        self.assertNotIn("playwright", content.lower())
        self.assertNotIn("requests", content.lower())

    def test_task_scheduler_installer_registers_non_web_local_modes(self):
        script = SCRIPTS_DIR / "install-task-scheduler.ps1"

        self.assertTrue(script.exists())
        content = script.read_text(encoding="utf-8")
        self.assertIn("Register-ScheduledTask", content)
        self.assertIn('[string]$TaskPrefix = "TodayPlusArchive"', content)
        self.assertIn('${TaskPrefix}Clipboard', content)
        self.assertIn('${TaskPrefix}Watch', content)
        self.assertNotIn("chat.openai.com", content.lower())
        self.assertNotIn("cookie", content.lower())

    def test_task_scheduler_installer_accepts_config_path(self):
        script = SCRIPTS_DIR / "install-task-scheduler.ps1"

        content = script.read_text(encoding="utf-8")
        self.assertIn("[string]$ConfigPath", content)
        self.assertIn("--config", content)
        self.assertIn("Test-Path $ConfigPath", content)


if __name__ == "__main__":
    unittest.main()
