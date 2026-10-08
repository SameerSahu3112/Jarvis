"""A small, fixed set of macOS actions triggered by hand gestures."""

import subprocess


def _run_applescript(script, success_message):
    """Run one built-in macOS AppleScript and return a message for Jarvis."""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return "I could not find the macOS AppleScript command."

    if result.returncode != 0:
        return "The Mac did not allow that action. Check its Automation permission."
    return success_message


def volume_up():
    script = """
    set currentVolume to output volume of (get volume settings)
    set newVolume to currentVolume + 10
    if newVolume > 100 then set newVolume to 100
    set volume output volume newVolume
    """
    return _run_applescript(script, "Volume up.")


def volume_down():
    script = """
    set currentVolume to output volume of (get volume settings)
    set newVolume to currentVolume - 10
    if newVolume < 0 then set newVolume to 0
    set volume output volume newVolume
    """
    return _run_applescript(script, "Volume down.")


def toggle_music_playback():
    script = 'tell application "Music" to playpause'
    return _run_applescript(script, "Toggled Apple Music playback.")
