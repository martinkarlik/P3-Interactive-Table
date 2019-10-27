import cv2
cap = cv2.VideoCapture("output.avi")

while cap.isOpened():
    _, frame = cap.read()

    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("frame", frame)

    for i in range(0, 200000):
        a = 5*5
        # we can afford around 200 000 "5 times 5" computations without too much lag

    if cv2.waitKey(20) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
