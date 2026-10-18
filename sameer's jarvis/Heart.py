import sys
from Mouth import opening_command, closing_command, speak
from Ear import listen
from Brain import ask_jarvis
from logger import log

def main():
    while "jarvis" not in listen().lower():
        pass
    log("START | Jarvis woke up")
    opening_command()

    while True:
        text = listen()
        if not text:
            continue
        lowered = text.lower()

        if "exit" in lowered or "goodbye" in lowered:
            log("EXIT | user said exit")
            closing_command()
            sys.exit()

        answer = ask_jarvis(text)
        print("Jarvis:", answer)
        speak(answer)

if __name__ == "__main__":
    main()