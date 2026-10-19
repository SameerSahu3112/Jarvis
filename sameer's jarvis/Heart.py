import sys
from Mouth import opening_command, closing_command, speak
from Hand import handle_command, open_website
from Ear import listen
from Brain import ask_jarvis
from logger import log
from Stomach import (
    memorize_app, memorize_website, memorize_text,
    show_memorized_apps, show_memorized_websites, show_memorized_texts,
    load_memorized,
)

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
        elif "application" in choice:
            speak("Which application?")
            handle_command(listen())
        elif "website" in choice:
            speak("Which website?")
            open_website(listen())

def memory_mode():
    while True:
        speak("Say save application, save website, save note, show applications, show websites, show notes, or exit.")
        choice = listen().lower()

        if "exit" in choice:
            return

        elif "save application" in choice:
            speak("Which application?")
            name = listen()
            if name:
                #* title() capitalizes the first letter of each word, which is how apps are usually named
                memorize_app(name, name.title())

        elif "save web" in choice:
            speak("What name?")
            name = listen()
            speak("Say the address, like spotify dot com.")
            #* replace " dot " with "." and remove spaces to form a valid URL
            address = listen().lower().replace(" dot ", ".").replace(" ", "")
            if "." not in address:
                address = address + ".com"
            if name and address:
                memorize_website(name, "https://" + address)

        elif "save note" in choice:
            speak("What should I remember?")
            note = listen()
            if note:
                memorize_text(note)

        elif "show app" in choice:
            show_memorized_apps()
        elif "show web" in choice:
            show_memorized_websites()
        elif "show note" in choice:
            show_memorized_texts()

def main():
    while "jarvis" not in listen().lower():
        pass
    log("START | Jarvis woke up")
    load_memorized()
    opening_command()
    while True:
        speak("What would you like to do? Question, application, memory, or exit?")
        choice = listen().lower()
        if "question" in choice:
            question_mode()
        elif "application" in choice:
            application_mode()
        elif "memory" in choice:
            memory_mode()
        elif "exit" in choice:
            log("EXIT | user said exit")
            closing_command()
            sys.exit()

if __name__ == "__main__":
    main()