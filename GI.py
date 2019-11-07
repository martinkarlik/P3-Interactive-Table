# This script is the one that will control the things that are projected on to the table

import cv2
beer_frame = cv2.imread("images/beer_frame_bs.jpg")

# beer = beer_frame[255:275, 85:105]
beer = beer_frame[220:250, 440:470]

cv2.imshow("beer", beer)
cv2.imwrite("images/beer_highlighted.jpg", beer)

cv2.waitKey(0)
cv2.destroyAllWindows()
