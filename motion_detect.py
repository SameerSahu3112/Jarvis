# Step 2: detect your movement by comparing each frame with the previous one
import cv2

MIN_AREA = 1500      # ignore changes smaller than this (noise). Raise it if too sensitive.
THRESHOLD = 25       # how different a pixel must be to count as "changed" (0-255)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise SystemExit("Camera not found. Close other apps using it, or try index 1.")

prev_gray = None

while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)

    # 1. Simplify: grayscale + blur removes colour and tiny camera noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_gray is None:               # first frame: nothing to compare with yet
        prev_gray = gray
        continue

    # 2. Difference between this frame and the previous one
    diff = cv2.absdiff(prev_gray, gray)
    mask = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)[1]
    mask = cv2.dilate(mask, None, iterations=2)     # fill small gaps

    # 3. Find the moving regions and draw boxes around the big ones
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    moving = False
    for cnt in contours:
        if cv2.contourArea(cnt) < MIN_AREA:
            continue
        moving = True
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    status = "MOVEMENT DETECTED" if moving else "NO MOVEMENT"
    color = (0, 0, 255) if moving else (0, 200, 0)
    cv2.putText(frame, status, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    prev_gray = gray                    # current frame becomes the "previous" one

    cv2.imshow("Jarvis - motion detection (Esc to quit)", frame)
    #cv2.imshow("What the computer sees", mask)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
