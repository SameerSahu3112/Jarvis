# Hand.py
import subprocess, webbrowser
from Mouth import speak
from logger import log
import re
from urllib.parse import quote_plus

APPS = {
    "calculator": "Calculator",
    "whatsapp": "WhatsApp",
    "vs code": "Visual Studio Code",
    "visual studio code": "Visual Studio Code",
    "browser": "Safari",
    "safari": "Safari",
    "claude": "Claude",
    "codex": "ChatGPT ",
    "devin": "Devin"
}

SITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
}

def open_app(name):
    #* -a specifies the application to open
    result = subprocess.run(["open", "-a", name], capture_output=True)
    if result.returncode == 0:
        speak(f"Opening {name}")
        log(f"APP | opened {name} | success")
    else:
        speak(f"I couldn't find {name}")
        log(f"APP | {name} | FAILED: app not found")


def handle_command(command):
    command = command.lower()
    for key, app in APPS.items():
        if key in command:
            open_app(app)
            return
    log(f"APP | heard '{command}' | FAILED: unknown application")
    speak("Sorry, I don't know that application yet.")

def open_website(name):
    name = name.lower().strip()
    print("Website heard:", name)          # debug line, remove later
    for key, url in SITES.items():
        if key in name.replace(" ", ""):   # "you tube" becomes "youtube"
            webbrowser.open(url)
            speak(f"Opening {key}")
            log(f"WEBSITE | opened {key} | success")
            return
    log(f"WEBSITE | heard '{name}' | FAILED: unknown website")
    speak("Sorry, I don't know that website yet.")

def extract_query(text):
    """Pulls the search words out of a sentence like 'search code with harry in youtube'."""
    query = text.lower().strip().replace("you tube", "youtube")
    query = re.sub(r"^\W*(?:(?:hey|ok|okay|please|jarvis|lyra|can you|could you)\s+)*", "", query)
    query = re.sub(r"^(?:search for|search|look up|find)\s+", "", query)
    query = re.sub(r"^(?:on|in)\s+(?:youtube|google)\s+(?:for\s+)?", "", query)
    query = re.sub(r"\s+(?:on|in)\s+(?:youtube|google)\W*$", "", query)
    query = re.sub(r"^(?:youtube|google)\s+(?:for\s+)?", "", query)
    return query.strip(" .?!")


def search_youtube(text):
    query = extract_query(text)
    if not query:
        speak("What should I search for?")
        return
    webbrowser.open("https://www.youtube.com/results?search_query=" + quote_plus(query))
    log(f"SEARCH | youtube: {query}")
    speak(f"Searching YouTube for {query}.")


def search_web(text):
    query = extract_query(text)
    if not query:
        speak("What should I search for?")
        return
    webbrowser.open("https://www.google.com/search?q=" + quote_plus(query))
    log(f"SEARCH | google: {query}")
    speak(f"Searching Google for {query}.")


def search_command(text):
    lowered = text.lower().replace("you tube", "youtube")
    if "youtube" in lowered:
        search_youtube(text)
    elif "google" in lowered:
        search_web(text)
    else:
        return False        # no site named, so let the AI decide
