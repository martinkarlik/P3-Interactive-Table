import cv2
import numpy as np
import matplotlib.pyplot as plt


def nothing(x):
    pass


cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_EXPOSURE, -5)

cv2.namedWindow('mask')

cv2.createTrackbar('L - H', 'mask', 0, 179, nothing)
cv2.createTrackbar('L - S', 'mask', 0, 255, nothing)
cv2.createTrackbar('L - V', 'mask', 0, 255, nothing)
cv2.createTrackbar('U - H', 'mask', 179, 179, nothing)
cv2.createTrackbar('U - S', 'mask', 255, 255, nothing)
cv2.createTrackbar('U - V', 'mask', 255, 255, nothing)

# template = cv2.imread('images/testImages/templates/red_cup.jpg', 1)
running = True
while running:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (ret, thresh) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # blurred_frame = cv2.GaussianBlur(frame, (3, 3), 0)
    # hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos('L - H', 'mask')
    l_S = cv2.getTrackbarPos('L - S', 'mask')
    l_V = cv2.getTrackbarPos('L - V', 'mask')
    u_h = cv2.getTrackbarPos('U - H', 'mask')
    u_s = cv2.getTrackbarPos('U - S', 'mask')
    u_v = cv2.getTrackbarPos('U - V', 'mask')

    # lower_color = np.array([l_h, l_S, l_V])
    # upper_color = np.array([u_h, u_s, u_v])
    # mask = cv2.inRange(hsv, lower_color, upper_color)
    #
    # result = cv2.bitwise_and(frame, frame, mask=mask)
    #
    # kernel = np.ones((5, 5), np.uint8)
    # closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    # opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations=2)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        arclength = cv2.arcLength(contour, True)
        circularity = 4 * np.pi * area / (arclength * arclength) if arclength != 0 else 0
        # print('c: ', circularity)
        # print('a: ', area)
        if circularity > 0.83 and area > 1000:
            # print(circularity)
            # print(area)
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                print (cX,cY)
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
    # cv2.imshow('mask', mask)
    # cv2.imshow('Opening', opening)
    # cv2.imshow('Closing', closing)

    cv2.imshow('thresh', thresh)
    cv2.imshow('frame', frame)

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
