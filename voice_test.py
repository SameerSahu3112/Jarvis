def voice_test():
    import speech_recognition as sr
    import webbrowser

    recognizer = sr.Recognizer()
    words = None

    try:
        with sr.Microphone() as microphone:
            print("Calibrating for room noise—please wait.")
            recognizer.adjust_for_ambient_noise(microphone, duration=0.5)

            print("Say: open YouTube")
            print("Say: open Gmail")
            print("Say: open Google")
            print("Or ask Jarvis a question.")
            recording = recognizer.listen(
                microphone,
                timeout=8,
                phrase_time_limit=5,
            )
        words = recognizer.recognize_google(
            recording,
            language="en-IN"
        ).lower()
        print("Jarvis heard:", words)
    except sr.WaitTimeoutError:
        print("I didn't hear you start speaking.")
    except sr.UnknownValueError:
        print("I heard audio, but couldn't understand the words.")
    except sr.RequestError as error:
        print("Speech recognition service problem:", error)

    # Only check website commands if speech recognition returned text.
    if words is None:
        return

    # Require an explicit command so merely hearing a site name does not open it.
    if not words.startswith("open "):
        # A normal question should go to the AI instead of the website router.
        return words

    website_name = words.removeprefix("open ").strip()

    if "youtube" in website_name:
        print("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
        return None
    elif "gmail" in website_name:
        print("Opening Gmail.")
        webbrowser.open("https://mail.google.com")
        return None
    elif "google" in website_name:
        print("Opening Google.")
        webbrowser.open("https://www.google.com")
    else:
        # Return general questions, and unsupported commands, to the AI brain.
        return words

    return None
