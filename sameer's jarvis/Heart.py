import sys
from Mouth import opening_command, closing_command, speak
from Hand import handle_command, open_website
from Ear import listen
from Brain import ask_jarvis
from logger import log

def question_mode():
    while True:
        speak("Ask your question, or say exit.")
        q = listen()
        if not q:
            continue
        if "exit" in q.lower():
            return
        answer = ask_jarvis(q)
        log(f"QUESTION | {q} | answered")
        print("Jarvis:", answer)
        speak(answer)

def application_mode():
    while True:
        speak("What would you like to do? App, website, or exit?")
        choice = listen().lower()
        if "exit" in choice:
            return
        elif "app" in choice:
            speak("Which application?")
            handle_command(listen())
        elif "web" in choice:              # matches "website" and "web site"
            speak("Which website?")
            open_website(listen())

def main():
    while "jarvis" not in listen().lower():
        pass
    log("START | Jarvis woke up")
    opening_command()
    while True:
        speak("What would you like to do? Question, application, or exit?")
        choice = listen().lower()
        if "question" in choice:
            question_mode()
        elif "application" in choice:
            application_mode()
        elif "exit" in choice:
            log("EXIT | user said exit")
            closing_command()
            sys.exit()

if __name__ == "__main__":
    main()