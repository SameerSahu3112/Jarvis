import io
import time

import speech_recognition as sr

from logger import log
from Tongue import to_english

# Whisper runs on your laptop: free, no account, no API key
try:
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")   # "small" is more accurate but slower
except Exception as e:
    model = None
    log(f"EAR | Whisper not available, using Google: {e}")

# Your routes and tools understand English, so other languages get translated
TRANSLATE_TO_ENGLISH = True

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.6

# measure background noise once, at startup
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)


def whisper_transcribe(audio):
    wav = io.BytesIO(audio.get_wav_data(convert_rate=16000, convert_width=2))
    segments, info = model.transcribe(
        wav,
        beam_size=1,            # faster
        vad_filter=True,        # ignore silence and noise
        initial_prompt="Lyra",  # helps it spell the name
    )
    text = " ".join(segment.text.strip() for segment in segments).strip()
    return text, info.language


def google_transcribe(audio):
    return getattr(recognizer, "recognize_google")(audio), "en"


def listen():
    with sr.Microphone() as source:
        print("Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("No voice detected.")
            return ""

    started = time.time()
    text, language, engine = "", "en", ""

    if model is not None:
        try:
            text, language = whisper_transcribe(audio)
            engine = "whisper"
        except Exception as e:
            log(f"EAR | whisper FAILED, using google: {e}")

    if not engine:
        try:
            text, language = google_transcribe(audio)
            engine = "google"
        except sr.UnknownValueError:
            print("Voice captured, but words weren't understood.")
            return ""
        except sr.RequestError as e:
            print("Google service error:", e)
            return ""

    original = text
    if TRANSLATE_TO_ENGLISH and language != "en" and text:
        text = to_english(text)

    log(f"EAR | {engine} ({language}) took {time.time() - started:.1f}s: {original} -> {text}")
    print(f"Recognized ({language}):", text)
    return text