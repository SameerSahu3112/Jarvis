import webbrowser
import subprocess

def open_app(app_name):
    try:
        #* -a specifies the application to open 
        subprocess.Popen(["open", "-a", app_name])
        print(f"Opening {app_name}...")

    except Exception as e:
        print(f"Couldn't open {app_name}: {e}")

def handle_command(command):
    command = command.lower().strip()
    if "open calculator" in command:
        open_app("Calculator")
    elif "open whatsapp" in command:
        open_app("WhatsApp")
    elif "open vs code" in command or "open visual studio code" in command:
        open_app("Visual Studio Code")
    elif "open browser" in command or "open safari" in command:
        open_app("Safari")
    else:
        print("Sorry, I don't know that command yet.")

def open_website(url):
    try:
        webbrowser.open(url)
        print(f"Opening {url}...")
    except Exception as e:
        print(f"Couldn't open {url}: {e}")
