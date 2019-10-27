import random
from BlobClass import Blob
import cv2
import numpy as np


def findCrop(web_cam):
    # Check if the web_cam is detected, if not this is not run
    global finalMinX, finalMinY, finalMaxX, finalMaxY
    if cv2.VideoCapture(web_cam).isOpened():
        cap = cv2.VideoCapture(web_cam)
        _, frame = cap.read()
        cv2.imshow('Frame', frame)
        cv2.waitKey(0)
        # For testing purposes
        # frame = cv2.imread('Images/Marker.jpg', 1)
        # frame = cv2.imread('Images/Marker2.jpg', 1)

        blurred_frame = cv2.GaussianBlur(frame, (5, 5), cv2.BORDER_DEFAULT)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        # Input BGR color to get HSV
        colorBGR = np.uint8([[[147, 117, 252]]])
        hsv_color = cv2.cvtColor(colorBGR, cv2.COLOR_BGR2HSV)

        hue = hsv_color[0, 0, 0]
        # print(hue)

        lowerValue = np.array([hue, 80, 0])
        upperValue = np.array([hue, 255, 255])

        lowerValue[0] -= 15
        # print("Lower", lowerValue)
        upperValue[0] += 15
        # print("Upper: ", upperValue)

        mask = cv2.inRange(hsv, lowerValue, upperValue)
        # res = cv2.bitwise_and(hsv, hsv, mask=mask)

        kernel = np.ones((9, 9), np.uint8)

        # Opening removes false positives from the background
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        opening2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # In a try block we see if there are any markers, if not handle them later
        try:
            blobs = []
            for y in range(0, opening.shape[0]):
                for x in range(0, opening.shape[1]):
                    if opening[y, x] > 0:
                        opening[y, x] = 0
                        tempBlob = Blob()
                        queue = [[y, x]]
                        while len(queue) > 0:
                            y_temp = queue[0][0]
                            x_temp = queue[0][1]
                            if x_temp + 1 < opening.shape[1] and opening[y_temp, x_temp + 1] > 0:
                                opening[y_temp, x_temp + 1] = 0
                                queue.append([y_temp, x_temp + 1])
                            if y_temp + 1 < opening.shape[0] and opening[y_temp + 1, x_temp] > 0:
                                opening[y_temp + 1, x_temp] = 0
                                queue.append([y_temp + 1, x_temp])
                            if x_temp - 1 > 0 and opening[y_temp, x_temp - 1] > 0:
                                opening[y_temp, x_temp - 1] = 0
                                queue.append([y_temp, x_temp - 1])
                            if y_temp - 1 > 0 and opening[y_temp - 1, x_temp] > 0:
                                opening[y_temp - 1, x_temp] = 0
                                queue.append([y_temp - 1, x_temp])
                            tempBlob.pixels.append(queue.pop(0))
                        blobs.append(tempBlob)

            for blob in blobs:
                blue = random.randint(0, 255)
                green = random.randint(0, 255)
                red = random.randint(0, 255)

                blob.area = len(blob.pixels)
                blob.minX = blob.pixels[0][1]
                blob.maxX = blob.pixels[0][1]
                blob.minY = blob.pixels[0][0]
                blob.maxY = blob.pixels[0][0]

                for pixel in blob.pixels:
                    frame[pixel[0], pixel[1], 0] = blue
                    frame[pixel[0], pixel[1], 1] = green
                    frame[pixel[0], pixel[1], 2] = red
                    if pixel[0] < blob.minY:
                        blob.minY = pixel[0]
                    if pixel[0] > blob.maxY:
                        blob.maxY = pixel[0]
                    if pixel[1] < blob.minX:
                        blob.minX = pixel[1]
                    if pixel[1] > blob.maxX:
                        blob.maxX = pixel[1]
                blob.compactness = blob.calcCompactness(blob.area)

            # Check if the blob has a compactness that matches a square and set it to be a marker
            for blob in blobs:
                if blob.isMarker(0.89):
                    blob.marker = True
                    print(blob)
                else:
                    # Remove all other elements that aren't markers
                    blobs.remove(blob)
            print(len(blobs))

            errorScale = 8
            finalMinX = blobs[0].minX + errorScale
            finalMinY = blobs[0].minY + errorScale
            finalMaxX = blobs[1].minX - errorScale
            finalMaxY = blobs[1].maxY - errorScale
            return finalMinY, finalMaxY, finalMinX, finalMaxX

        # If no markers are found, handle the error
        except IndexError:
            print("Error, no markers found")
            pass
    # No web cam detected, handle it
    else:
        print("No camera found")

# Used for testing purposes
# if __name__ == '__main__':
#     #The number here defines the web cam that is used
#     findCrop(1)
