import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, -5)

template = cv2.imread('images/testImages/templates/red_cup.jpg', 1)

while True:
    _, frame = cap.read()
    blurred_frame = cv2.GaussianBlur(frame, (9, 9), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([20, 80, 30])
    upper_red = np.array([0, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 2000:
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)



    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)


    # Feature matching
    # grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # orb = cv2.ORB_create()
    # kp1, dest = orb.detectAndCompute(template, None)
    # kp2, dest2 = orb.detectAndCompute(grey_frame, None)
    # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # matches = bf.match(dest, dest2)
    # matches = sorted(matches, key= lambda x:x.distance)
    # img3 = cv2.drawMatches(template, kp1, grey_frame, kp2, matches[:10], None, flags=2)
    # plt.imshow(img3)
    # plt.show()

    # Background removal!!
    # mask = np.zeros(frame.shape[:2], np.uint8)
    #
    # bgModel = np.zeros((1,65), np.float64)
    # fgModel = np.zeros((1, 65), np.float64)
    #
    # rect = (50, 100, frame.shape[1]-100, frame.shape[0]-200)
    #
    # cv2.grabCut(frame, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
    # mask2 = np.where((mask == 2) | (mask==0), 0, 1).astype('uint8')
    # frame = frame*mask2[:,:,np.newaxis]
    # plt.imshow(frame)
    # plt.colorbar()
    # plt.show()

    # cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
