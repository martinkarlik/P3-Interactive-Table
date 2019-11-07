import cv2
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_EXPOSURE, -5)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('lo-fi_test1.avi', fourcc, 20.0, (640, 480))

while True:
    _, frame = cap.read()
    cv2.imshow("frame", frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    out.write(frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
