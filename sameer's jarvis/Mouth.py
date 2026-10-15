import subprocess
#* -r specifies the rate of speech and -v specifies the voice to use

def opening_command():
    subprocess.run(["say","-v", "Daniel", "-r", "250", "Hey, I Am Jarvis, I Am Ready To Assist You."])

def closing_command():
    subprocess.run(["say","-v", "Daniel", "-r", "250", "Jarvis Is Shutting Down."])

def speak(text):
    subprocess.run(["say","-v", "Daniel", "-r", "250", text])