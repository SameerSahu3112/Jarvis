import os
import re
import subprocess
import threading
from datetime import datetime

import psutil

from Mouth import speak
from logger import log

HOME = os.path.expanduser("~")

FOLDERS = {
    "downloads": os.path.join(HOME, "Downloads"),
    "desktop": os.path.join(HOME, "Desktop"),
    "documents": os.path.join(HOME, "Documents"),
}


# ---------- system info ----------

def battery_info(text=""):
    #* sensors_battery() returns None if battery info is not available
    battery = psutil.sensors_battery()
    if battery is None:
        speak("I can't read the battery.")
        return
    state = "charging" if battery.power_plugged else "not charging"
    speak(f"Battery is at {int(battery.percent)} percent and {state}.")


def cpu_info(text=""):
    #* cpu_percent(interval=1) returns the CPU usage over a 1-second interval
    speak(f"CPU usage is {int(psutil.cpu_percent(interval=1))} percent.")


def ram_info(text=""):
    #* virtual_memory().percent returns the percentage of memory usage
    speak(f"Memory usage is {int(psutil.virtual_memory().percent)} percent.")


def disk_info(text=""):
    #* disk_usage("/") returns the total, used, and free space on the root filesystem
    free_gb = psutil.disk_usage("/").free // (1024 ** 3)
    speak(f"You have about {free_gb} gigabytes free on your disk.")


# ---------- volume ----------

def get_volume():
    result = subprocess.run(
        #* -e specifies the AppleScript command to run
        #* output volume of (get volume settings) returns the current output volume as an integer between 0 and 100
        ["osascript", "-e", "output volume of (get volume settings)"],
        capture_output=True, text=True,
    )
    try:
        #* result.stdout is the text output printed by a command-line program when it runs successfully
        return int(result.stdout.strip())
    except ValueError:
        return 50


def set_volume(level):
    level = max(0, min(100, level))
    subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
    log(f"TOOL | volume set to {level}")
    speak(f"Volume {level} percent.")


def volume_command(text):
    #* re.findall is a Python function that finds all matches of a pattern in a piece of text and returns them as a list.
    numbers = re.findall(r"\d+", text)
    if numbers:
        set_volume(int(numbers[0]))
    elif "up" in text or "increase" in text:
        set_volume(get_volume() + 10)
    elif "down" in text or "decrease" in text or "lower" in text:
        set_volume(get_volume() - 10)
    else:
        speak("Say volume up, volume down, or volume and a number.")


def mute(text=""):
    subprocess.run(["osascript", "-e", "set volume with output muted"])
    log("TOOL | muted")


def unmute(text=""):
    subprocess.run(["osascript", "-e", "set volume without output muted"])
    speak("Unmuted.")


# ---------- brightness ----------

def brightness_command(text):
    if "down" in text or "lower" in text or "decrease" in text:
        key, word = 145, "down"
    else:
        key, word = 144, "up"
    for _ in range(4):
        result = subprocess.run(
            ["osascript", "-e", f'tell application "System Events" to key code {key}'],
            capture_output=True,
        )
        if result.returncode != 0:
            speak("I need accessibility permission to change brightness.")
            return
    log(f"TOOL | brightness {word}")
    speak(f"Brightness {word}.")


# ---------- screenshot ----------

def take_screenshot(text=""):
    #* strftime string format time
    name = datetime.now().strftime("lyra_screenshot_%Y%m%d_%H%M%S.png")
    path = os.path.join(FOLDERS["desktop"], name)
    #* -x  tells it to take the screenshot without the camera shutter sound.
    result = subprocess.run(["screencapture", "-x", path])
    if result.returncode == 0:
        log(f"TOOL | screenshot saved {path}")
        speak("Screenshot saved on your desktop.")
    else:
        speak("I could not take the screenshot.")


# ---------- files ----------

def find_folder(text):
    for name, path in FOLDERS.items():
        if name in text.lower():
            return name, path
    return None, None


def list_files(text):
    name, path = find_folder(text)
    if not path:
        speak("Say downloads, desktop, or documents.")
        return
    files = [f for f in os.listdir(path) if not f.startswith(".")]
    files.sort(key=lambda f: os.path.getmtime(os.path.join(path, f)), reverse=True)
    speak(f"You have {len(files)} items in {name}. The newest are:")
    for f in files[:5]:
        speak(f)


def open_folder(text):
    name, path = find_folder(text)
    if not path:
        speak("Say downloads, desktop, or documents.")
        return
    subprocess.run(["open", path])
    speak(f"Opening {name}.")


def create_folder(text):
    text = text.lower()
    if "called" in text:
        name = text.split("called", 1)[1]
    elif "named" in text:
        name = text.split("named", 1)[1]
    else:
        name = text.split("folder", 1)[-1]
    name = name.replace("/", " ").strip()
    if not name:
        speak("I didn't catch the folder name.")
        return
    os.makedirs(os.path.join(FOLDERS["desktop"], name), exist_ok=True)
    log(f"TOOL | folder created: {name}")
    speak(f"Folder {name} created on your desktop.")


def find_file(text):
    words = text.lower().split("find", 1)[-1].split()
    words = [w for w in words if w not in ("file", "the", "my", "a")]
    name = " ".join(words)
    if not name:
        speak("I didn't catch the file name.")
        return
    result = subprocess.run(["mdfind", "-name", name], capture_output=True, text=True)
    matches = [p for p in result.stdout.splitlines() if p.startswith(HOME)]
    if not matches:
        speak("I couldn't find it.")
        return
    speak(f"I found {len(matches)} matches. Showing the first one.")
    subprocess.run(["open", "-R", matches[0]])


# ---------- reminders ----------

def fire_reminder(task):
    clean = task.replace('"', "").replace("\\", "")
    subprocess.run(["osascript", "-e", f'display notification "{clean}" with title "Lyra reminder"'])
    speak(f"Reminder. {clean}")


def set_reminder(text):
    text = text.lower()
    match = re.search(r"in (\d+) (second|minute|hour)s?", text)
    if not match:
        speak("Say it like: remind me in 10 minutes to drink water.")
        return
    amount = int(match.group(1))
    unit = match.group(2)
    seconds = amount * {"second": 1, "minute": 60, "hour": 3600}[unit]

    task = text.replace(match.group(0), "")
    if " to " in task:
        task = task.split(" to ", 1)[1].strip()
    else:
        task = "do your task"

    timer = threading.Timer(seconds, fire_reminder, args=[task])
    timer.daemon = True
    timer.start()
    log(f"TOOL | reminder in {seconds} seconds: {task}")
    plural = "s" if amount != 1 else ""
    speak(f"Okay, I will remind you in {amount} {unit}{plural} to {task}.")