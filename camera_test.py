# Step 1: check that Python can see your camera
import cv2

cap = cv2.VideoCapture(0)   # 0 = default webcam. If it fails, try 1 or 2.
if not cap.isOpened():
    raise SystemExit("Camera not found. Close other apps using it, or try index 1.")

while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)          # mirror view, feels natural
    cv2.imshow("Camera test (press Esc to quit)", frame)
    if cv2.waitKey(1) & 0xFF == 27:     # 27 = Esc key
        break

cap.release()
cv2.destroyAllWindows()