# This script is the one that will control the things that are projected on to the table
# import algorithms
# import cv2
import numpy as np

a = np.array([5, 7, 10, 4])
target = 6

c = abs(a - target) <= 1

b = np.array([True, False, False, False])
d = np.array([False, False, False, False])

print(d.any())






# beer_frame = cv2.imread("images/test2_nonhighlighted.png")
#
# hsi = algorithms.bgrToHsi(beer_frame)
#
# cv2.imshow("beers", beer_frame)
# cv2.imshow("beers h", hsi[:, :, 0] / 360)
# cv2.imshow("beers s", hsi[:, :, 1])
# cv2.imshow("beers i", hsi[:, :, 2])
#
#
#
# # beer = beer_frame[200:240, 100:140]
# # cv2.imshow("beer", beer)
# # cv2.imwrite("images/beer_reg_left.jpg", beer)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
