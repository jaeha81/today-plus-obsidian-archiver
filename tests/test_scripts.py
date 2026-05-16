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


if __name__ == "__main__":
    unittest.main()
