import os
import subprocess
import tempfile
import ollama
from Mouth import speak
from logger import log

#* expanduser completes the rest name 
HOME = os.path.expanduser("~")
VISION_MODEL = "gemma3:4b"          # must be a model that can see images
client = ollama.Client()

TEXT_TYPES = (".txt", ".md", ".py", ".csv", ".json", ".log", ".tex", ".c", ".cpp", ".html")
BLOCKED_WORDS = ("password", "secret", "token", "nerves", "credential")


def is_safe(path):
    """Lyra may only read inside your home folder, and never private things."""
    if not path.startswith(HOME):
        return False
    #* relpath makes the path start from your home folder.
    relative = os.path.relpath(path, HOME)
    parts = relative.split(os.sep)
    if any(part.startswith(".") for part in parts):     # hidden files and folders
        return False
    if parts[0] == "Library":
        return False
    return not any(word in relative.lower() for word in BLOCKED_WORDS)


def find_folder_path(text):
    """Find a folder in your home folder from spoken words."""
    text = text.lower()
    candidates = []
    try:
        for name in os.listdir(HOME):
            path = os.path.join(HOME, name)
            if os.path.isdir(path) and not name.startswith(".") and name != "Library":
                candidates.append((name, path))
                for sub in os.listdir(path):
                    sub_path = os.path.join(path, sub)
                    if os.path.isdir(sub_path) and not sub.startswith("."):
                        candidates.append((sub, sub_path))
    except OSError:
        pass

    best = None
    for name, path in candidates:
        if len(name) >= 3 and name.lower() in text:
            if best is None or len(name) > len(best[0]):
                best = (name, path)
    return best[1] if best else None


# ---------- information tools (they RETURN text for the AI to read) ----------

def list_folders(text=""):
    base = find_folder_path(text) or HOME
    try:
        names = sorted(
            n for n in os.listdir(base)
            if os.path.isdir(os.path.join(base, n)) and not n.startswith(".") and n != "Library"
        )
    except OSError:
        return "I am not allowed to open that folder. Check the Files and Folders permission."
    if not names:
        return "There are no folders there."
    return f"Folders in {os.path.basename(base)}: " + ", ".join(names[:60])


def look_in_folder(text=""):
    path = find_folder_path(text)
    if not path:
        return "I could not find that folder."
    try:
        items = [n for n in os.listdir(path) if not n.startswith(".")]
        items.sort(key=lambda n: os.path.getmtime(os.path.join(path, n)), reverse=True)
    except OSError:
        return "I am not allowed to open that folder. Check the Files and Folders permission."
    lines = []
    for n in items[:40]:
        kind = "folder" if os.path.isdir(os.path.join(path, n)) else "file"
        lines.append(f"{n} ({kind})")
    return f"{len(items)} items in {os.path.basename(path)}. Newest first: " + ", ".join(lines)


def read_file(text=""):
    name = text.strip()
    if not name:
        return "Which file?"
    result = subprocess.run(["mdfind", "-name", name], capture_output=True, text=True)
    for path in result.stdout.splitlines():
        if is_safe(path) and path.lower().endswith(TEXT_TYPES) and os.path.isfile(path):
            try:
                with open(path, "r", errors="ignore") as f:
                    content = f.read(2000)
            except OSError:
                continue
            log(f"EYES | read file {os.path.basename(path)}")
            return f"File {os.path.basename(path)}:\n{content}"
    return "I could not find a readable text file with that name."


def look_at_screen(text=""):
    path = os.path.join(tempfile.gettempdir(), "lyra_screen.png")
    result = subprocess.run(["screencapture", "-x", path])
    if result.returncode != 0 or not os.path.exists(path):
        return "I could not capture the screen. Screen recording permission may be missing."

    question = text or "Describe what is on this screen."
    try:
        response = client.chat(
            model=VISION_MODEL,
            messages=[{
                "role": "user",
                "content": question + " Answer in two or three short sentences.",
                "images": [path],
            }],
        )
        answer = response["message"]["content"]
    except Exception as e:
        log(f"EYES | vision FAILED: {e}")
        return "The vision model did not respond. Is it downloaded?"
    finally:
        if os.path.exists(path):
            os.remove(path)                 # do not keep screenshots of your screen
    log("EYES | looked at the screen")
    return "Screen: " + answer


# ---------- action tool (it speaks for itself) ----------

def show_folder(text=""):
    path = find_folder_path(text) or HOME
    subprocess.run(["open", path])
    speak(f"Opening {os.path.basename(path)}.")