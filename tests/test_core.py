import json
import os
import tempfile
import unittest

from jarvis.core import Jarvis


class TestJarvis(unittest.TestCase):
    def setUp(self):
        fd, self.log = tempfile.mkstemp(suffix=".jsonl")
        os.close(fd)
        self.j = Jarvis(dry_run=True, log_file=self.log)

    def tearDown(self):
        os.remove(self.log)

    def test_open_allowed_app(self):
        r = self.j.handle("Jarvis, open VS Code")
        self.assertTrue(r.ok)

    def test_open_app_with_polite_words(self):
        self.assertTrue(self.j.handle("open my browser").ok)

    def test_time_date_help(self):
        for cmd in ["what time is it", "what's the date", "help"]:
            self.assertTrue(self.j.handle(cmd).ok, cmd)

    def test_unknown_command_rejected(self):
        r = self.j.handle("delete all my files")
        self.assertFalse(r.ok)
        self.assertEqual(r.error, "unknown_command")

    def test_app_not_on_allow_list_rejected(self):
        r = self.j.handle("open rm -rf /")
        self.assertFalse(r.ok)
        self.assertEqual(r.error, "app_not_allowed")

    def test_every_command_is_logged(self):
        self.j.handle("open vscode")
        self.j.handle("gibberish")
        with open(self.log) as f:
            rows = [json.loads(line) for line in f]
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["skill"], "open_app")
        self.assertEqual(rows[1]["error"], "unknown_command")


if __name__ == "__main__":
    unittest.main()
