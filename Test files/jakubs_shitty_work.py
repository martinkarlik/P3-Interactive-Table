import cv2
import numpy as np

# hello, I need help with tresholding the pink ergo detecting the corners :(
# and overall the code is quite stupid but sometimes works!
# I'll try to work on it more

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_EXPOSURE, -5)
_, img = cap.read()


cv2.imshow('img', img)
bImage = img.copy()
contouredImg = img.copy()

# boundariesLow = [50, 0, 20]
# boundariesHigh = [150, 90, 80]

# pink image rotated
# boundariesLow = [120, 70, 165]
# boundariesHigh = [220, 150, 255]

# setting boundaries for thresholding
boundariesLow = [95, 60, 140]
boundariesHigh = [220, 150, 255]

lower = np.array(boundariesLow, dtype= "uint8")
upper = np.array(boundariesHigh, dtype= "uint8")
mask = cv2.inRange(img, lower, upper)
colorThresh = cv2.bitwise_and(img, img, mask = mask)

gray = cv2.cvtColor(colorThresh, cv2.COLOR_BGR2GRAY)

_, ColorThresh = cv2.threshold(gray, 0, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)

cv2.imshow('ColorThresh', colorThresh)

# closing holes, might not be necessary
kernel = np.ones((5, 5), np.uint8)
closing = cv2.morphologyEx(ColorThresh, cv2.MORPH_CLOSE, kernel)
cv2.imshow('closed', closing)

# finding contours
_, contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(contouredImg, contours, -1, (0, 255, 0), 2)

# area = cv2.contourArea(contours[0])
cv2.imshow('contouredImage', contouredImg)
boxesArray = []

# finding the boxes of the pink rect size
for i in range(0, len(contours)):
    x, y, w, h = cv2.boundingRect(contours[i])
    if 2000 > w*h > 400:
        bImage = cv2.rectangle(bImage, (x, y), (x + w, y + h), (0, 0, 0), 2)
        boxesArray.append(cv2.boundingRect(contours[i]))

cv2.imshow('boundingBoxes', bImage)
print(boxesArray)

# ordering the points A________B
#                     |        |
#                     |        |
#                     |        |
#                     D________C


for i in range(0, len(boxesArray)):
    if boxesArray[i][0] < 800 and boxesArray[i][1] > 400:
        Dx = boxesArray[i][0]
        Dy = boxesArray[i][1] + boxesArray[i][3]
    if boxesArray[i][0] < 800 and boxesArray[i][1] < 400:
        Ax = boxesArray[i][0]
        Ay = boxesArray[i][1]
    if boxesArray[i][0] > 800 and boxesArray[i][1] < 400:
        Bx = boxesArray[i][0] + boxesArray[i][2]
        By = boxesArray[i][1]
    if boxesArray[i][0] > 800 and boxesArray[i][1] > 400:
        Cx = boxesArray[i][0] + boxesArray[i][2]
        Cy = boxesArray[i][1] + boxesArray[i][3]

# setting the source points for the warping
src = np.float32([(Ax, Ay),
                 (Bx, By),
                 (Cx, Cy),
                 (Dx, Dy)])

#setting the points to which the imgage should be translated
dst = np.float32([(0, 0),
                  (1280, 0),
                  (1280, 720),
                  (0, 720)])


# warping
M = cv2.getPerspectiveTransform(src, dst)
warped = cv2.warpPerspective(bImage, M, (1280, 720))

cv2.imshow('unwarped', warped)

cv2.waitKey(0)
cv2.destroyAllWindows()