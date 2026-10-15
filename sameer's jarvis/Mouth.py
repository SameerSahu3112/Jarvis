import subprocess
def mouth():
    # * -v = specifies the voice and -r = specifies the rate of speech
    while True:
        command = input("What Your Question:  ")
        subprocess.run(["say","-v", "Daniel", "-r", "250", command])
        if command.lower() == "exit":
            break

def opening_command():
    subprocess.run(["say","-v", "Daniel", "-r", "250", "Hey, I Am Jarvis, I Am Ready To Assist You."])

def closing_command():
    subprocess.run(["say","-v", "Daniel", "-r", "250", "Jarvis Is Shutting Down."])

