def opening_command():
    import pyaudio
    import audioop
    import time

    # Raise this if small sounds still trigger Jarvis; lower it if claps are missed.
    VOLUME_THRESHOLD = 4000
    # A clap is loud briefly, then quickly becomes quiet. Longer sounds are ignored.
    MAX_CLAP_FRAMES = 4
    QUIET_THRESHOLD = VOLUME_THRESHOLD * 0.5
    STARTUP_IGNORE_SECONDS = 0.75

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024
    )

    print("Starting microphone. Wait for the ready message before clapping.")
    listening_started = time.monotonic()
    loud_candidate_frames = None
    ignoring_long_sound = False
    ready_message_shown = False

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            volume = audioop.rms(data, 2)
            elapsed = time.monotonic() - listening_started

            # Ignore the first few frames while the microphone settles.
            if elapsed < STARTUP_IGNORE_SECONDS:
                continue

            if not ready_message_shown:
                print("Ready. Clap once to start Jarvis.")
                ready_message_shown = True

            is_clap = False

            # Once a long sound is rejected, wait for quiet before looking again.
            if ignoring_long_sound:
                if volume < QUIET_THRESHOLD:
                    ignoring_long_sound = False
                continue

            # First detect a loud sound, then check that it quickly becomes quiet.
            if loud_candidate_frames is None:
                if volume > VOLUME_THRESHOLD:
                    loud_candidate_frames = 0
            else:
                loud_candidate_frames += 1

                if volume < QUIET_THRESHOLD:
                    is_clap = loud_candidate_frames <= MAX_CLAP_FRAMES
                    loud_candidate_frames = None
                elif loud_candidate_frames > MAX_CLAP_FRAMES:
                    # Ongoing sound such as speech is not treated as a clap.
                    loud_candidate_frames = None
                    ignoring_long_sound = True
                    continue
                else:
                    continue

            if is_clap:
                print("Clap detected!")
                from speak_test import speak, intro
                intro()
                speak()
                break

    except KeyboardInterrupt:
        print("\nStopped.")

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def closing_command():
    import pyaudio
    import audioop
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
                from speak_test import outro
                outro()
                break

    except KeyboardInterrupt:
        print("\nStopped.")

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
