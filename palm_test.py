from pathlib import Path
import time

import cv2
import mediapipe as mp


def palm_test(target_gesture):
    # Find the gesture model beside this Python file.
    model_path = Path(__file__).resolve().parent / "gesture_recognizer.task"

    if not model_path.exists():
        raise SystemExit(f"Gesture model not found: {model_path}")

    # Configure MediaPipe for video frames so it can track the hand between frames.
    options = mp.tasks.vision.GestureRecognizerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path=str(model_path)
        ),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=1,
    )

    # Open the default camera.
    camera = cv2.VideoCapture(0)

    # Request a smaller frame to reduce the amount of work per detection.
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not camera.isOpened():
        raise SystemExit("Could not open the camera.")

    detected_gesture = None

    try:
        # Create the gesture recognizer.
        with mp.tasks.vision.GestureRecognizer.create_from_options(options) as recognizer:
            # Video mode requires an increasing timestamp for each camera frame.
            start_time = time.monotonic()

            while True:
                # Read one image from the camera.
                ok, frame = camera.read()

                if not ok:
                    print("Could not read a camera frame.")
                    break

                # Mirror the image, like a mirror view.
                frame = cv2.flip(frame, 1)

                # OpenCV uses BGR colors; MediaPipe expects RGB.
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Wrap the image in the format MediaPipe expects.
                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb_frame
                )

                # Ask MediaPipe to identify the gesture in this video frame.
                timestamp_ms = int((time.monotonic() - start_time) * 1000)
                result = recognizer.recognize_for_video(mp_image, timestamp_ms)

                gesture = "No hand detected"

                if result.gestures and result.gestures[0]:
                    gesture = result.gestures[0][0].category_name

                # Display the gesture name on the camera image.
                cv2.putText(
                    frame,
                    f"Gesture: {gesture}",
                    (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                cv2.imshow("Jarvis gesture detection", frame)
                # Let OpenCV process window events before we possibly exit this loop.
                key = cv2.waitKey(1) & 0xFF

                # Stop when the requested gesture is recognized.
                if gesture == target_gesture:
                    detected_gesture = gesture
                    print(gesture, "detected.")
                    break

                # Press Esc to stop without detecting the requested gesture.
                if key == 27:
                    break

    finally:
        # Always release the camera and close its window.
        camera.release()
        cv2.destroyAllWindows()
        # Give the window system one event cycle to finish closing the window.
        cv2.waitKey(1)

    # Send the result back to the file that called this function.
    return detected_gesture
