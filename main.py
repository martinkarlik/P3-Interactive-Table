import cv2
import numpy
import algorithms
from blob import Blob


cap = cv2.VideoCapture("recordings/7cups.avi")

beer_template = cv2.imread("images/beer2.jpg")

_, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# mid_area = gray[0:480, 220:420]

# to access our image processing algos:
# algorithms.matchTemplate()
# algorithms.findCrop() etc.

frame_count = 0

while cap.isOpened():

    # frame_count += 1

    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = algorithms.findCrop()

    beer_area = frame[130:350, 20:220]

    beers_expected_centre = [[10, 10], [20, 20], [30, 30], [40, 40], [50, 50], [60, 60], [70, 70], [80, 80], [90, 90], [100, 100]]

    beers_grayscale = algorithms.matchTemplate(beer_area, beer_template)
    beers_binary = algorithms.threshold(beers_grayscale, 0.4, 1)
    # beers_blobs = algorithms.extractBlobs(beers_binary)  # might want to do this only once per x frames

    # print(len(beers_blobs))
    # beers = algorithms.associateBlobs(beers_blobs, beers_expected_centre)


    cv2.imshow("beer area", beer_area)
    cv2.imshow("beers binary", beers_grayscale)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
