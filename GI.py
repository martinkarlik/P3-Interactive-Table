# This script is the one that will control the things that are projected on to the table

import cv2

cap = cv2.VideoCapture(0)
for i in range(0, 16):
    print(cap.get(i))

cap.set(5, 24)


while True:

    _, frame = cap.read()
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
