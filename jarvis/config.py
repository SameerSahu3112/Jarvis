"""Everything Jarvis is allowed to launch lives here. Nothing else can run."""

# App allow-list: friendly name -> command (as a list, never a shell string) per OS.
# sys.platform values: "win32", "darwin", "linux"
APPS = {
    "vscode": {
        "win32": ["code"],
        "darwin": ["open", "-a", "Visual Studio Code"],
        "linux": ["code"],
    },
    "browser": {
        "win32": ["cmd", "/c", "start", "", "https://www.google.com"],
        "darwin": ["open", "https://www.google.com"],
        "linux": ["xdg-open", "https://www.google.com"],
    },
    "calculator": {
        "win32": ["calc"],
        "darwin": ["open", "-a", "Calculator"],
        "linux": ["gnome-calculator"],
    },
}

# Spoken/typed names -> allow-list key
APP_ALIASES = {
    "vs code": "vscode",
    "visual studio code": "vscode",
    "code": "vscode",
    "vscode": "vscode",
    "browser": "browser",
    "web browser": "browser",
    "chrome": "browser",
    "calculator": "calculator",
    "calc": "calculator",
}

LOG_FILE = "jarvis_log.jsonl"
