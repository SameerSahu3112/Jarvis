# Hand.py
import subprocess, webbrowser
from Mouth import speak

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
    else:
        speak(f"I couldn't find {name}")

def handle_command(command):
    command = command.lower()
    for key, app in APPS.items():
        if key in command:
            open_app(app)
            return
    speak("Sorry, I don't know that application yet.")

def open_website(name):
    url = SITES.get(name.lower())
    if url:
        webbrowser.open(url)
        speak(f"Opening {name}")
    else:
        speak("Sorry, I don't know that website yet.")