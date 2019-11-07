# This script will handle the two different GUI's that we will have, just to make it easier.

import cv2
cap = cv2.VideoCapture(0)


while cap.isOpened():
    _, frame = cap.read()

    cv2.imshow("frame", frame)

    if cv2.waitKey(20) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
