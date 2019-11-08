import cv2
import numpy
import algorithms
from blob import Blob

cap = cv2.VideoCapture("recordings/test2_gameplay.mp4")
beer_template = cv2.imread("images/beer_classic.jpg")

# _, frame = cap.read()
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# mid_area = gray[0:480, 220:420]

# to access our image processing algos:
# algorithms.matchTemplate()
# algorithms.findCrop() etc.

frame_count = 0

while cap.isOpened():

    frame_count += 1

    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = algorithms.findCrop()

    beer_area = frame[130:350, 0:220]

    beers_expected_center = [[21, 20], [18, 70], [15, 118], [12, 170], [64, 43], [61, 93], [56, 142], [107, 67], [102, 118], [147, 92]]

    beers_grayscale = algorithms.matchTemplate(beer_area, beer_template)
    beers_binary = algorithms.threshold(beers_grayscale, 0.4, 1)


    beers_blobs = algorithms.extractBlobs(beers_binary)  # might want to do this only once per x frames
    beers = algorithms.associateBlobs(beers_blobs, beers_expected_center)
    print(beers)
    print(len(beers_blobs))


    # for i in range(0, len(beers_blobs)):
    #     if beers[i]:
    #         cv2.circle(beer_area, (beers_blobs[i].center[0], beers_blobs[i].center[1]), 5, (255, 0, 0), -1)

    cv2.imshow("beer area", beer_area)
    cv2.imshow("beers binary", beers_binary)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
