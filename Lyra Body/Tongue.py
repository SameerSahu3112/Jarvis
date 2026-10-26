import re
import subprocess
from deep_translator import GoogleTranslator
from Mouth import speak
from logger import log

ALIASES = {"chinese": "chinese (simplified)"}

# macOS voices for a few languages. See what you have with:  say -v '?'
VOICES = {
    "hindi": "Lekha",
    "spanish": "Monica",
    "french": "Thomas",
    "german": "Anna",
    "japanese": "Kyoko",
    "italian": "Alice",
    "korean": "Yuna",
}


def translate(text, language):
    language = ALIASES.get(language.lower(), language.lower())
    return GoogleTranslator(source="auto", target=language).translate(text)


def to_english(text):
    """Any language to English. Returns the text unchanged if it fails."""
    try:
        return GoogleTranslator(source="auto", target="en").translate(text) or text
    except Exception as e:
        log(f"TONGUE | to_english skipped: {e}")
        return text


def speak_in(text, language):
    voice = VOICES.get(language)
    if voice:
        result = subprocess.run(["say", "-v", voice, text])
        if result.returncode == 0:
            return True
    return False


def translate_command(text=""):
    match = re.match(
        r"\s*translate\s+(.+)\s+(?:to|into|in)\s+([a-zA-Z]+)\s*[.!?]*$",
        text,
        re.IGNORECASE,
    )
    if not match:
        speak("Say it like: translate good morning to hindi.")
        return

    phrase = match.group(1).strip()
    language = match.group(2).lower()

    try:
        result = translate(phrase, language)
    except Exception as e:
        log(f"TONGUE | translate FAILED: {e}")
        speak("I couldn't translate that. Check the language name and your internet.")
        return

    print(f"{phrase} -> {language}: {result}")
    subprocess.run(["pbcopy"], input=result.encode("utf-8"))   # copied, so you can paste it
    log(f"TONGUE | '{phrase}' -> {language}: {result}")

    speak(f"In {language}:")
    if not speak_in(result, language):
        speak("It is on your screen and copied, so you can paste it.")