"""The pipeline: text -> intent -> permission check -> skill -> response + log."""
import json
from datetime import datetime

from . import intent, permissions, skills
from .config import LOG_FILE


class Jarvis:
    def __init__(self, dry_run: bool = False, log_file: str = LOG_FILE):
        self.dry_run = dry_run
        self.log_file = log_file

    def _log(self, command, skill, result):
        entry = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "command": command,
            "skill": skill,
            "ok": result.ok,
            "error": result.error,
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def handle(self, text: str) -> skills.Result:
        parsed = intent.parse(text)
        if parsed is None:
            result = skills.Result(False, "Sorry, I don't know that command. Say 'help'.",
                                   error="unknown_command")
            self._log(text, None, result)
            return result

        verdict = permissions.check(parsed.skill)
        if verdict == "deny":
            result = skills.Result(False, "That action isn't allowed.", error="denied")
        elif verdict == "confirm":
            result = skills.Result(False, "That needs confirmation (not built yet).",
                                   error="needs_confirmation")
        else:
            result = skills.run(parsed.skill, parsed.args, dry_run=self.dry_run)

        self._log(text, parsed.skill, result)
        return result
