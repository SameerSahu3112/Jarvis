def speak():
    import subprocess

    subprocess.run(["say", "-v", "Daniel", "-r", "250", "Hello, I am Jarvis, your personal assistant."])
    subprocess.run(["say", "-v", "Daniel", "-r", "250", "I Am Ready"])