import subprocess
#* -r specifies the rate of speech and -v specifies the voice to use

def opening_command():
    subprocess.run(["say","-v", "Samantha", "-r", "250", "Hey, I Am Lyra, I Am Ready To Assist You."])

def closing_command():
    subprocess.run(["say","-v", "Samantha", "-r", "250", "Lyra Is Shutting Down."])

def speak(text):
    subprocess.run(["say","-v", "Samantha", "-r", "250", text])