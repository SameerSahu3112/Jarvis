import subprocess


def speak_text(text):
    """Speak text returned by the AI or a laptop-control action."""
    if text:
        subprocess.run(["say", "-v", "Daniel", "-r", "250", str(text)])


def speak():
    subprocess.run(["say", "-v", "Daniel", "-r", "250", "Hello, I am Jarvis, your personal assistant."])
    subprocess.run(["say", "-v", "Daniel", "-r", "250", "I Am Ready"])
    subprocess.run([
        "say", "-v", "Daniel", "-r", "250",
        "Open palm to ask a question. Closed fist to end the session. "
        "Thumbs change volume. Victory toggles Apple Music."
    ])


def intro():
    subprocess.run([
                    "say",
                    "-v", "Daniel",
                    "-r", "250",
                    "I heard your clap"
                    ])

def outro():
    subprocess.run([
                    "say",
                    "-v", "Daniel",
                    "-r", "250",
                    "Session ended. Clap when you want me again."
                    ])

def opening_website():
    subprocess.run([
                    "say",
                    "-v", "Daniel",
                    "-r", "250",
                    "Tell me what to open, or ask me a question."
                    ])
                    
