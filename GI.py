# This script is the one that will control the things that are projected on to the table
import algorithms
import cv2
import numpy as np


# beer_frame = cv2.imread("images/test2_nonhighlighted.png")

green_ball = cv2.imread("images/green_ball_thrown2.jpg")

cv2.imshow("green ball", green_ball)


# beer = beer_frame[200:240, 100:140]
# cv2.imshow("beer", beer)
# cv2.imwrite("images/beer_reg_left.jpg", beer)

cv2.waitKey(0)
cv2.destroyAllWindows()
