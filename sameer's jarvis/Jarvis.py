# Jarvis.py (structure)
from Mouth import opening_command, closing_command, speak
from Hand import handle_command, open_website
from Ear import listen
from Brain import ask_jarvis

def question_mode():
    while True:
        speak("Ask your question, or say exit.")
        q = listen()
        if not q:
            continue
        if "exit" in q.lower():
            return
        answer = ask_jarvis(q)
        print("Jarvis:", answer)
        speak(answer)

def application_mode():
    while True:
        speak("what would you like to do? Application, website, or exit?")
        choice = listen().lower()
        if "exit" in choice:
            return
        elif "application" in choice:
            speak("Which application?")
            handle_command(listen())
        elif "website" in choice:
            speak("Which website?")
            open_website(listen())

def main():
    while "jarvis" not in listen().lower():
        pass
    opening_command()
    while True:
        speak("what would you like to do? Question, application, or exit?")
        choice = listen().lower()
        if "question" in choice:
            question_mode()
        elif "application" in choice:
            application_mode()
        elif "exit" in choice:
            closing_command()
            break

if __name__ == "__main__":
    main()