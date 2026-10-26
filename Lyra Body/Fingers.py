import re
import subprocess
import time

import pyautogui

from Ear import listen
from Mouth import speak
from logger import log

pyautogui.PAUSE = 0.05      # tiny pause between key presses

# Lyra will refuse to type into these apps (she runs in one of them)
# If you run Lyra inside VS Code's terminal, add "Code" to this list
BLOCKED_APPS = ("Terminal", "iTerm2")

# Warn out loud if macOS has not given the keyboard permission
CHECK_ACCESSIBILITY = True

# If the typing command is followed by one of these words, it is a request
# to the AI ("write a poem"), not a message to type
ASK_WORDS = ("a", "an", "the", "me", "us", "some", "of", "is", "are", "was",
             "code", "program", "essay", "email", "letter", "poem", "story",
             "function", "script", "report", "paragraph", "summary", "answer")

# Keys pressed after the name is typed in WhatsApp's search box (opens the first result)
WHATSAPP_AFTER_SEARCH = ["down", "enter"]

last_typed = ""


def accessibility_ok():
    """True or False if macOS says this app may press keys, None if unknown."""
    try:
        from ApplicationServices import AXIsProcessTrusted
        return bool(AXIsProcessTrusted())
    except Exception:
        return None


def frontmost_app():
    result = subprocess.run(
        ["osascript", "-e",
         'tell application "System Events" to get name of first application process whose frontmost is true'],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def ready_to_type(check_app=True):
    """Returns the front app's name, or None (after explaining why) if Lyra should not type."""
    if CHECK_ACCESSIBILITY and accessibility_ok() is False:
        speak("I need accessibility permission to press keys. Open System Settings, "
              "Privacy and Security, Accessibility, and allow your terminal.")
        return None
    app = frontmost_app()
    if check_app and app in BLOCKED_APPS:
        speak(f"I won't type into {app}. Open the app you want first.")
        return None
    return app or "unknown app"


def split_command(text):
    """Returns (command word, the message after it), keeping capital letters."""
    pattern = r"^\W*(?:(?:hey|ok|okay|please|jarvis|lyra|can you|could you)\s+)*(write|type|dictate)(?:\s+(.*))?$"
    match = re.match(pattern, text.strip(), re.IGNORECASE | re.DOTALL)
    if not match:
        return None, ""
    return match.group(1).lower(), (match.group(2) or "").strip()


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
    message = message.rstrip(".").strip()

    # "write a poem about rain" is a request for the AI, not a message to type
    if message and message.split()[0].lower().strip(",.") in ASK_WORDS:
        return False

    app = ready_to_type()
    if not app:
        return

    if not message:
        # you only said "write" or "type": ask for the message, then type it
        speak("Go ahead.")
        message = listen().strip().rstrip(".")
        if not message:
            speak("I didn't hear anything to type.")
            return

    paste_text(message)
    last_typed = message
    log(f"FINGERS | typed {len(message)} characters into {app}")
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


def whatsapp_chat(text=""):
    """'whatsapp rahul' opens WhatsApp and searches for that chat."""
    rest = re.sub(r"^\W*(?:(?:hey|ok|okay|please|jarvis|lyra)\s+)*whatsapp\b", "", text.lower().strip())
    name = re.sub(r"^\W*(?:(?:search|message|chat|with|for|to|call|on)\s+)+", "", rest).strip(" .")

    if not name:
        speak("Whose chat?")
        name = listen().strip(" .")
    if not name:
        return

    if not ready_to_type(check_app=False):
        return

    subprocess.run(["open", "-a", "WhatsApp"])
    time.sleep(2)                                   # wait for the app to come forward
    pyautogui.hotkey("command", "f")                # WhatsApp's search box
    time.sleep(0.5)
    paste_text(name)
    time.sleep(1.2)                                 # wait for the results to appear
    for key in WHATSAPP_AFTER_SEARCH:
        pyautogui.press(key)
        time.sleep(0.3)

    log(f"FINGERS | whatsapp search for {name}")
    speak(f"I searched WhatsApp for {name}. Check the chat, then say type and your message.")