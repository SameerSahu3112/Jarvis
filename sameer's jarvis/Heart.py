import sys
from Mouth import opening_command, closing_command, speak
from Ear import listen
from logger import log
from Stomach import load_memorized
from vessels import send

#! add translate so that it can listen every voice language and translate it and still be working 

EXIT_WORDS = ("exit", "goodbye", "quit", "shut down")

def main():
    while "jarvis" not in listen().lower():
        pass
    log("START | Jarvis woke up")
    load_memorized()
    opening_command()

    while True:
        text = listen()
        if not text:
            continue
        if text.lower().strip(" .!?") in EXIT_WORDS:
            log("EXIT | user said exit")
            closing_command()
            sys.exit()
        send(text)

if __name__ == "__main__":
    main()