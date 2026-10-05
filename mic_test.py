import pyaudio
import audioop
import subprocess
import time

# Change this if normal sounds trigger Jarvis or your clap isn't detected.
VOLUME_THRESHOLD = 2500

# Prevent one clap from triggering Jarvis many times.
COOLDOWN_SECONDS = 3

audio = pyaudio.PyAudio()

stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=1024
)

print("Clap near the microphone. Press Ctrl+C to stop.")

last_trigger_time = 0

try:
    while True:
        data = stream.read(1024, exception_on_overflow=False)
        volume = audioop.rms(data, 2)
        current_time = time.monotonic()
        if (
            volume > VOLUME_THRESHOLD
            and current_time - last_trigger_time > COOLDOWN_SECONDS
        ):
            print("Clap detected!")
            subprocess.run([
                "say",
                "-v", "Daniel",
                "-r", "200",
                "I heard your clap"
            ])
            from speak_test import speak
            speak()
            break

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()