from pathlib import Path
import time

import cv2
import mediapipe as mp


def palm_test(target_gestures):
    """Wait for one requested gesture, without showing the camera preview.

    target_gestures may be one gesture name or a collection of names.
    Returns the detected gesture, or None if the camera could not read a frame.
    """
    if isinstance(target_gestures, str):
        target_gestures = {target_gestures}
    else:
        target_gestures = set(target_gestures)

    model_path = Path(__file__).resolve().parent / "gesture_recognizer.task"
    if not model_path.exists():
        raise SystemExit(f"Gesture model not found: {model_path}")

    options = mp.tasks.vision.GestureRecognizerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=1,
    )

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not camera.isOpened():
        raise SystemExit("Could not open the camera.")

    detected_gesture = None
    candidate_gesture = None
    candidate_frames = 0
    release_frames = 0
    stable_frames_required = 4
    release_frames_required = 3

    try:
        with mp.tasks.vision.GestureRecognizer.create_from_options(options) as recognizer:
            start_time = time.monotonic()

            while True:
                ok, frame = camera.read()
                if not ok:
                    print("Could not read a camera frame.")
                    break

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb_frame,
                )
                timestamp_ms = int((time.monotonic() - start_time) * 1000)
                result = recognizer.recognize_for_video(mp_image, timestamp_ms)

                gesture = "No hand detected"
                if result.gestures and result.gestures[0]:
                    gesture = result.gestures[0][0].category_name

                # Require several matching frames so a one-frame mistake won't act.
                if detected_gesture is None:
                    if gesture in target_gestures:
                        if gesture == candidate_gesture:
                            candidate_frames += 1
                        else:
                            candidate_gesture = gesture
                            candidate_frames = 1

                        if candidate_frames >= stable_frames_required:
                            detected_gesture = gesture
                            # A fist ends the session immediately; no release is needed.
                            if gesture == "Closed_Fist":
                                print("Closed fist detected. Ending this Jarvis session.")
                                break
                            print(f"{gesture} detected. Release your hand to continue.")
                    else:
                        candidate_gesture = None
                        candidate_frames = 0

                # Wait for the hand to leave the selected pose before returning.
                # This prevents a held gesture from repeating the action.
                elif gesture not in target_gestures:
                    release_frames += 1
                    if release_frames >= release_frames_required:
                        break
                else:
                    release_frames = 0

    finally:
        camera.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

    return detected_gesture
