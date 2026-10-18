# Hand.py
import subprocess, webbrowser
from Mouth import speak
from logger import log

APPS = {
    "calculator": "Calculator",
    "whatsapp": "WhatsApp",
    "vs code": "Visual Studio Code",
    "visual studio code": "Visual Studio Code",
    "browser": "Safari",
    "safari": "Safari",
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