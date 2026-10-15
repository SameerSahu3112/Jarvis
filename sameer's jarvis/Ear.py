import speech_recognition as sr

recognizer = sr.Recognizer()

def listen(command):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Speak now!")
        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )
            print("Audio captured!")
        except sr.WaitTimeoutError:
            print("No voice detected.")
            return ""
    try:
        text = getattr(recognizer, "recognize_google")(audio)
        print("Recognized:", text)
        return text
    except sr.UnknownValueError:
        print("Voice captured, but words weren't understood.")
    except sr.RequestError as e:
        print("Google service error:", e)
    return ""

