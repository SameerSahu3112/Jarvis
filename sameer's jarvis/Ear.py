import speech_recognition as sr
from Mouth import speak

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Speak now!")
        try:
            audio = recognizer.listen(
                source,
                #* timeout specifies how long to wait for a phrase to start
                #* phrase_time_limit specifies how long to wait for a phrase to end
                timeout=5,
                phrase_time_limit=5
            )
        except sr.WaitTimeoutError:
            speak("No voice detected.")
            return ""
    try:
        text = getattr(recognizer, "recognize_google")(audio)
        print("Recognized:", text)
        speak(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        speak("Voice captured, but words weren't understood.")
    except sr.RequestError as e:
        print("Google service error:", e)
    return ""

