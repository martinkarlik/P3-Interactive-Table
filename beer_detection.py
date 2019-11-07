from algorithms import findCrop
from blob import Blob
import cv2
import numpy as np
import random

if __name__ == '__main__':
    # This controls which web cam is being used
    web_cam = 1
    finalMinY, finalMaxY, finalMinX, finalMaxX = findCrop(web_cam)
    # Check if the web_cam is detected, if not this is not run
    if cv2.VideoCapture(web_cam).isOpened():
        cap = cv2.VideoCapture(web_cam)
        while True:
            _, frame = cap.read()

            crop_frame = frame[finalMinY:finalMaxY, finalMinX:finalMaxX]
            # For testing purposes
            # frame = cv2.imread('Images/Marker.jpg', 1)
            # frame = cv2.imread('Images/Marker2.jpg', 1)

            blurred_frame = cv2.GaussianBlur(crop_frame, (5, 5), cv2.BORDER_DEFAULT)
            hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

            # Input BGR color to get HSV
            colorBGR = np.uint8([[[24, 56, 99]]])
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
                        crop_frame[pixel[0], pixel[1], 0] = blue
                        crop_frame[pixel[0], pixel[1], 1] = green
                        crop_frame[pixel[0], pixel[1], 2] = red
                        if pixel[0] < blob.minY:
                            blob.minY = pixel[0]
                        if pixel[0] > blob.maxY:
                            blob.maxY = pixel[0]
                        if pixel[1] < blob.minX:
                            blob.minX = pixel[1]
                        if pixel[1] > blob.maxX:
                            blob.maxX = pixel[1]
                    blob.compactness = blob.calcCompactness(blob.area)
                # print(blobs)

                for blob in blobs:
                    x = (blob.maxX - blob.minX)*(blob.maxX - blob.minX)
                    y = (blob.maxY - blob.minY)*(blob.maxY - blob.minY)
                    perimeter = np.sqrt(x + y)
                    # print(perimeter, " perimiter")
                    blob.circular = perimeter/(2*(np.sqrt(np.pi * blob.area)))
                    # print(perimeter / (2 * (np.sqrt(np.pi * blob.area))), "Circularity")
                    if blob.isBeer(0.42):
                        blob.beer = True
                        # print(blob)
                    else:
                        blobs.remove(blob)

                print(len(blobs), " beer blobs")
                cv2.imshow('opening2', opening2)
                cv2.imshow('frame', frame)

            # If no markers are found, handle the error
            except IndexError:
                print("Error, no markers found")
                pass
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    # No web cam detected, handle it
    else:
        print("No camera found")
