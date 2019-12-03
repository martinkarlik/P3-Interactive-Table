import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cap.set(cv2.CAP_PROP_EXPOSURE, -3)


while True:
    _, frame = cap.read()

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# free up memory
cap.release()
cv2.destroyAllWindows()
