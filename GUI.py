# This script will handle the two different GUI's that we will have, just to make it easier.


import cv2

beer = cv2.imread("images/beer_reg_left.jpg")
cv2.imshow("beer", beer)

cv2.waitKey(0)
cv2.destroyAllWindows()