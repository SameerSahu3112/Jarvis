from mic_test import opening_command
from palm_test import palm_test
from speak_test import opening_website, outro
from voice_test import voice_test


def main():
    while True:
        # Wait for a clap to start a session.
        opening_command()

        # Wait for an open palm.
        gesture = palm_test("Open_Palm")
        if gesture != "Open_Palm":
            continue

        # Ask for a website and open the spoken request.
        print("Open palm detected. Listening for a website command now.")
        opening_website()
        voice_test()

        # Wait for a closed fist to end this session.
        print("Website command finished. Waiting for a closed fist.")
        gesture = palm_test("Closed_Fist")
        if gesture == "Closed_Fist":
            outro()
            print("Jarvis is waiting. Clap to start again.")


if __name__ == "__main__":
    main()
