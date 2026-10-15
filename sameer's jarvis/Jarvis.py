from Mouth import mouth, opening_command, closing_command

def main():
    command = input("Do You Want To Start Jarvis:  ")
    if command.lower() == "yes":
        opening_command()
        question = input("Do You Want To Ask Question:  ")
        if question.lower() == "yes":
            mouth()
        elif question.lower() == "no":
            closing_command()


if __name__ == "__main__":
    main()
