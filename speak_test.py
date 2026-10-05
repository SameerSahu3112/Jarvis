import subprocess

def speak():
    subprocess.run(["say", "-v", "Daniel", "-r", "250", "Hello, I am Jarvis, your personal assistant."])
    subprocess.run(["say", "-v", "Daniel", "-r", "250", "I Am Ready"])
    subprocess.run(["say", "-v", "Daniel", "-r", "250", "Show The Palm To Activate Me"])


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
                    "Shutting down Jarvis. Goodbye!"
                    ])

def opening_website():
    subprocess.run([
                    "say",
                    "-v", "Daniel",
                    "-r", "250",
                    "Tell Me What To Open"
                    ])
                    