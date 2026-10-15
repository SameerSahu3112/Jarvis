import webbrowser
import subprocess
from Mouth import speak

def open_app(app_name):
    try:
        #* -a specifies the application to open 
        subprocess.Popen(["open", "-a", app_name])
        speak(f"Opening {app_name}...")

    except Exception as e:
        speak(f"Couldn't open {app_name}: {e}")

def handle_command(command):
    command = command.lower().strip()
    if "open calculator" in command:
        speak("Opening Calculator...")
        open_app("Calculator")
    elif "open whatsapp" in command:
        speak("Opening WhatsApp...")
        open_app("WhatsApp")
    elif "open vs code" in command or "open visual studio code" in command:
        speak("Opening Visual Studio Code...")
        open_app("Visual Studio Code")
    elif "open browser" in command or "open safari" in command:
        speak("Opening Safari...")
        open_app("Safari")
    else:
        print("Sorry, I don't know that command yet.")

def open_website(url):
    try:
        webbrowser.open(url)
        speak(f"Opening {url}...")
    except Exception as e:
        speak(f"Couldn't open {url}: {e}")
