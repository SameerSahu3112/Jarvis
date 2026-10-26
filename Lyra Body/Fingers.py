import re
import subprocess
import time

import pyautogui

from Mouth import speak
from logger import log

pyautogui.PAUSE = 0.05      # tiny pause between key presses

# Lyra will refuse to type into these apps (she runs in one of them)
# If you run Lyra inside VS Code's terminal, add "Code" to this list
BLOCKED_APPS = ("Terminal", "iTerm2")

# If the typing command is followed by one of these words, it is a request
# to the AI ("write a poem"), not a message to type
ASK_WORDS = ("a", "an", "the", "me", "us", "some", "of", "is", "are", "was",
             "code", "program", "essay", "email", "letter", "poem", "story",
             "function", "script", "report", "paragraph", "summary", "answer")

last_typed = ""


def frontmost_app():
    result = subprocess.run(
        ["osascript", "-e",
         'tell application "System Events" to get name of first application process whose frontmost is true'],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def split_command(text):
    """Returns (command word, the message after it), keeping capital letters."""
    pattern = r"^\W*(?:(?:hey|ok|okay|please|jarvis|lyra|can you|could you)\s+)*(write|type)\s+(.*)$"
    match = re.match(pattern, text.strip(), re.IGNORECASE | re.DOTALL)
    if not match:
        return None, ""
    return match.group(1).lower(), match.group(2).strip()


def paste_text(message):
    # paste instead of typing key by key: it handles any character and is faster
    old_clipboard = subprocess.run(["pbpaste"], capture_output=True).stdout
    subprocess.run(["pbcopy"], input=message.encode("utf-8"))
    time.sleep(0.1)
    pyautogui.hotkey("command", "v")
    time.sleep(0.3)
    subprocess.run(["pbcopy"], input=old_clipboard)       # give your clipboard back


def type_command(text=""):
    global last_typed

    word, message = split_command(text)
    message = message.rstrip(".")           # chat messages rarely end with a full stop
    if not message:
        speak("What should I type?")
        return

    if message.split()[0].lower().strip(",.") in ASK_WORDS:
        return False                        # let the AI handle it

    app = frontmost_app()
    if app in BLOCKED_APPS:
        speak(f"I won't type into {app}. Open the app you want first.")
        return

    paste_text(message)
    last_typed = message
    log(f"FINGERS | typed {len(message)} characters into {app or 'unknown app'}")
    speak("Typed.")


def send_it(text=""):
    global last_typed
    pyautogui.press("enter")
    last_typed = ""
    log("FINGERS | pressed enter")
    speak("Sent.")


def new_line(text=""):
    pyautogui.hotkey("shift", "enter")
    log("FINGERS | new line")


def delete_that(text=""):
    global last_typed
    if not last_typed:
        speak("I haven't typed anything to delete.")
        return
    pyautogui.press("backspace", presses=len(last_typed))
    log(f"FINGERS | deleted {len(last_typed)} characters")
    last_typed = ""


def paste_it(text=""):
    pyautogui.hotkey("command", "v")
    log("FINGERS | pasted")