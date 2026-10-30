import re
from Mouth import speak
from Ear import listen
from logger import log
from Brain import ask_lyra
from Hand import APPS, SITES, handle_command, open_website
from Stomach import (
    memorize_app, memorize_website, memorize_text,
    show_memorized_apps, show_memorized_websites, show_memorized_texts,
)
from Hand import APPS, SITES, handle_command, open_website, search_command
from Fingers import type_command, send_it, new_line, delete_that, paste_it, whatsapp_chat
from Muscles import (
    battery_info, cpu_info, ram_info, disk_info,
    volume_command, mute, unmute, brightness_command,
    take_screenshot, list_files, open_folder, create_folder, find_file,
    set_reminder,
)
from Fingers import type_command, send_it, new_line, delete_that, paste_it
from Tongue import translate_command
from Brain import think
from Stomach import remember, recall

def route_signal(message):
    message = message.lower()
    
    # Vessel decides: Is this for the Stomach?
    if "memorise" in message:
        return remember(message)
    
    if "what did i" in message or "recall" in message:
        return recall(message)
    
    # Otherwise, the Vessel carries it to the Brain
    return think(message)

# ---------- small helpers for the memory commands ----------

def save_app(text=""):
    speak("Which app?")
    name = listen()
    if name:
        memorize_app(name, name.title())


def save_website(text=""):
    speak("What name?")
    name = listen()
    speak("Say the address, like spotify dot com.")
    address = listen().lower().replace(" dot ", ".").replace(" ", "")
    if "." not in address:
        address = address + ".com"
    if name and address:
        memorize_website(name, "https://" + address)


def save_note(text=""):
    speak("What should I remember?")
    note = listen()
    if note:
        memorize_text(note)


def show_apps(text=""):
    show_memorized_apps()


def show_websites(text=""):
    show_memorized_websites()


def show_notes(text=""):
    show_memorized_texts()


def open_anything(text):
    # Opens a saved app or website. Returns False if it knows neither,
    # so the AI can handle the sentence instead.
    for key in APPS:
        if key in text:
            handle_command(text)
            return
    for key in SITES:
        if key in text.replace(" ", ""):
            open_website(text)
            return
    return False


# ---------- the routes ----------
# (phrases a sentence can START with, function to run)
# The first match wins, so specific phrases go before general ones.

ROUTES = [
    # teach Lyra
    (["save app", "save an app"], save_app),
    (["save website", "save web site", "save a website"], save_website),
    (["save note", "save a note"], save_note),
    (["show apps", "show my apps"], show_apps),
    (["show websites", "show my websites"], show_websites),
    (["show notes", "show my notes", "read my notes"], show_notes),

    # system info
    (["battery level", "battery status", "battery percentage"], battery_info),
    (["cpu usage", "cpu load"], cpu_info),
    (["ram usage", "memory usage"], ram_info),
    (["disk space", "free space", "storage space"], disk_info),

    # sound and screen
    (["unmute"], unmute),
    (["mute"], mute),
    (["volume up", "volume down", "volume to", "set volume"], volume_command),
    (["brightness up", "brightness down"], brightness_command),
    (["screenshot", "take a screenshot", "take screenshot"], take_screenshot),

    # files
    (["new folder", "create folder", "create a folder"], create_folder),
    (["list files", "list my files"], list_files),
    (["open folder", "open downloads", "open desktop", "open documents"], open_folder),
    (["find file", "find my file"], find_file),

    # reminders
    (["remind me"], set_reminder),

    # keyboard (Fingers)
    (["type", "write"], type_command),
    (["send it", "send message", "press enter"], send_it),
    (["new line"], new_line),
    (["delete that", "undo typing"], delete_that),
    (["paste it", "paste that"], paste_it),

    # translation (Tongue)
    (["translate"], translate_command),
    (["type", "write", "dictate"], type_command),

    # search and WhatsApp
    (["search"], search_command),
    (["whatsapp"], whatsapp_chat),

    # apps and websites (last, because "open" is a general word)
    (["open"], open_anything),
]

# these functions need your original capital letters, the others get lowercase
KEEP_CASE = (type_command, translate_command)

# polite words that are allowed before the command
START = r"^(?:(?:hey|ok|okay|please|lyra|can you|could you)\s+)*"


def route(text):
    """Run the first matching route. Returns True if a route handled it."""
    lowered = text.lower().strip()
    for phrases, function in ROUTES:
        for phrase in phrases:
            if re.match(START + re.escape(phrase) + r"\b", lowered):
                log(f"VESSEL | '{lowered}' -> {function.__name__}")
                argument = text.strip() if function in KEEP_CASE else lowered
                if function(argument) is False:
                    return False
                return True
    return False


def send(text):
    """The main entry point. Sends one sentence to the right organ."""
    lowered = text.lower().strip()
    keeps_and = re.match(START + r"(type|write|dictate|translate)\b", lowered)

    # a sentence with "and" usually has two jobs, so the AI plans the steps,
    # except typing and translating, where "and" is part of your message
    keeps_and = re.match(START + r"(type|write|translate)\b", lowered)
    if (keeps_and or " and " not in lowered) and route(text):
        return

    log(f"VESSEL | '{lowered}' -> brain (agent)")
    answer = ask_lyra(text)
    print("Lyra:", answer)
    speak(answer)