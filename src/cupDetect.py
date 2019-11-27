import cv2
import numpy as np
import matplotlib.pyplot as plt
#
#
# import cv2
# cap = cv2.VideoCapture(0)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('../recordings/cups.avi', fourcc, 20.0, (640, 480))
# while True:
#     _, frame = cap.read()
#     cv2.imshow("frame", frame)
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     out.write(frame)
#     if cv2.waitKey(1) & 0xff == ord('q'):
#         break
# cap.release()
# out.release()
# cv2.destroyAllWindows()

team_a = [1, 2, 3, 4]

team_a[1 if True else 2] = 0

