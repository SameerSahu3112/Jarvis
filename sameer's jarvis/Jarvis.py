from Mouth import opening_command, closing_command
from Hand import handle_command, open_website

def main():
    command = input("Do You Want To Start Jarvis:  ")
    if command.lower() == "jarvis":
        opening_command()
        while True:
            question = input("Do You Want To Ask Question(1) Or Want To Open Application(2) Or Want To Exit(3):  ")
            if question.lower() == "1":
                from Brain import ask_jarvis
                while True:
                    question = input("What Your Question:  ")
                    if question.lower() == "exit":
                        break
                    else:
                        answer = ask_jarvis(question)
                        print("Jarvis: ", answer)
            elif question.lower() == "2":
                while True:
                    choice = input("What Application You Want To Open (1) or Website (2) or Exit (3):  ")
                    if choice.lower() == "1":
                        command = input("What Application You Want To Open:  ") 
                        if command.lower() == "exit":
                            break
                        else:
                            handle_command(command)
                    elif choice.lower() == "2":
                        command = input("What Website You Want To Open:  ")
                        if command.lower() == "exit":
                            break
                        else:
                            if command.lower() == "google":
                                open_website("https://www.google.com")
                            elif command.lower() == "youtube":
                                open_website("https://www.youtube.com")
                            elif command.lower() == "facebook":
                                open_website("https://www.facebook.com")
                            elif command.lower() == "twitter":
                                open_website("https://www.twitter.com")
                            elif command.lower() == "instagram":
                                open_website("https://www.instagram.com")
                            elif command.lower() == "linkedin":
                                open_website("https://www.linkedin.com")
                            elif command.lower() == "gmail":
                                open_website("https://mail.google.com")
                            else:
                                print("Sorry, I don't know that website yet.")
                    elif choice.lower() == "3":
                        break
                    else:
                        print("Invalid Input. Please enter '1', '2' or '3'.")
                        continue
            elif question.lower() == "3":
                closing_command()
                break
            else:
                print("Invalid Input. Please enter '1', '2' or '3'.")

if __name__ == "__main__":
    main()
