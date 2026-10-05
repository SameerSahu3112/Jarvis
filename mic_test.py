import pyaudio
import audioop

audio = pyaudio.PyAudio()
stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=1024
)

print("Clap near the microphone. Press Ctrl+C to stop.")

try:
    while True:
        data = stream.read(1024, exception_on_overflow=False)
        volume = audioop.rms(data, 2)  # measure sound volume
        if volume > 2500:              # adjust this if needed
            print("Loud sound detected!")
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()