"""Skills are small, ordinary Python functions. The LLM never writes shell text."""
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime

from .config import APPS, APP_ALIASES


@dataclass
class Result:
    ok: bool
    message: str
    error: str = ""


def open_app(app: str, dry_run: bool = False) -> Result:
    key = APP_ALIASES.get(app.strip().lower())
    if key is None:
        return Result(False, f"I'm not allowed to open '{app}'.", error="app_not_allowed")

    cmd = APPS[key].get(sys.platform) or APPS[key].get("linux")
    if dry_run:
        return Result(True, f"(dry run) Would open {key}.")

    exe = shutil.which(cmd[0])
    if exe is None:
        return Result(False, f"I couldn't find {key} on this computer.", error="executable_not_found")
    try:
        subprocess.Popen([exe, *cmd[1:]])  # list args, no shell=True
    except OSError as e:
        return Result(False, f"Opening {key} failed.", error=str(e))
    return Result(True, f"Opening {key}.")


def get_time() -> Result:
    return Result(True, datetime.now().strftime("It is %I:%M %p."))


def get_date() -> Result:
    return Result(True, datetime.now().strftime("Today is %A, %d %B %Y."))


def list_commands() -> Result:
    return Result(True, "Try: open vscode, open browser, open calculator, "
                        "what time is it, what's the date.")


def run(skill: str, args: dict, dry_run: bool = False) -> Result:
    if skill == "open_app":
        return open_app(dry_run=dry_run, **args)
    if skill == "get_time":
        return get_time()
    if skill == "get_date":
        return get_date()
    if skill == "list_commands":
        return list_commands()
    return Result(False, "That skill isn't implemented.", error="no_such_skill")
