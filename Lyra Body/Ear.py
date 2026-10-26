import time

import speech_recognition as sr

from logger import log

# Languages Google should try, in order. Examples:
#   "en-US"  English
#   "en-IN"  Indian English
#   "hi-IN"  Hindi
# Each extra language is only tried if the one before it understood nothing.
LANGUAGES = ["en-US"]

# Your routes and tools understand English, so other languages get translated
TRANSLATE_TO_ENGLISH = True

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.6

print("Calibrating the microphone...")
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
print("Ready.")


def english(text):
    try:
        from Tongue import to_english
        return to_english(text)
    except Exception as e:
        log(f"EAR | translation skipped: {e}")
        return text


def listen():
    with sr.Microphone() as source:
        print("Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("No voice detected.")
            return ""

    started = time.time()
    text, language = "", ""

    for code in LANGUAGES:
        try:
            text = getattr(recognizer, "recognize_google")(audio, language=code)
            language = code
            break
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print("Google service error:", e)
            return ""

    if not text:
        print("Voice captured, but words weren't understood.")
        return ""

    original = text
    if TRANSLATE_TO_ENGLISH and not language.startswith("en"):
        text = english(text)

    log(f"EAR | google ({language}) took {time.time() - started:.1f}s: {original} -> {text}")
    print(f"Recognized ({language}):", text)
    return text