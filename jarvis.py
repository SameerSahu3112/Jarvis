from laptop_controls import toggle_music_playback, volume_down, volume_up
from llm_brain import ask_ai
from mic_test import opening_command
from palm_test import palm_test
from speak_test import opening_website, outro, speak_text
from voice_test import voice_test


GESTURES = {
    "Open_Palm",
    "Closed_Fist",
    "Thumb_Up",
    "Thumb_Down",
    "Victory",
}


def main():
    while True:
        # A clap starts a new Jarvis session.
        opening_command()
        print("Clap heard. Camera gesture detection is running without a preview.")

        while True:
            # Wait for any gesture Jarvis knows how to handle.
            gesture = palm_test(GESTURES)

            if gesture == "Closed_Fist":
                # End this session; the outer loop will wait for another clap.
                outro()
                print("Jarvis is waiting for a clap.")
                break

            elif gesture == "Open_Palm":
                # Open palm asks for one website command or question.
                opening_website()
                question = voice_test()
                if question:
                    answer = ask_ai(question)
                    print("Jarvis:", answer)
                    speak_text(answer)

            elif gesture == "Thumb_Up":
                speak_text(volume_up())

            elif gesture == "Thumb_Down":
                speak_text(volume_down())

            elif gesture == "Victory":
                speak_text(toggle_music_playback())


if __name__ == "__main__":
    main()
