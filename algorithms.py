import cv2
import random
from blob import Blob
import numpy as np
from scipy import signal
from scipy import misc


def matchTemplate(source, template):
    return cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)


def getImgKernel(x, y):
    imgKernel = np.array([
        [x - 1, y - 1, x, y - 1, x + 1, y - 1],
        [x - 1, y, x, y, x + 1, y],
        [x - 1, y + 1, x, y + 1, x + 1, y + 1]])
    return imgKernel


def matchTemplateSelf(source, template):
    tempImg = np.copy(source)
    templateArray = [[]]
    height = template.shape[1]
    width = template.shape[0]
    for x in range(0, width):
        for y in range(0, height):
            templateArray = x, y

    for x in range(0, source.shape[0]):
        for y in range(0, source.shape[1]):
            image = getImgKernel(x, y)

            # # TODO make the comparision work between the template and the source
            # if templateArray == image:
            #     tempImg[x, y] = 255, 255, 255
            # else:
            #     tempImg[x, y] = 0, 0, 0
            corr = signal.correlate2d(image, templateArray, boundary='symm', mode='same')
            i, j = np.unravel_index(np.argmax(corr), corr.shape)
            tempImg[x, y] = i, j
    return tempImg



def threshold(source, value, max_value):
    _, thresh = cv2.threshold(source, value, max_value, cv2.THRESH_BINARY)
    return thresh


def extractBlobs(binary_image):
    blobs = []
    for y in range(0, binary_image.shape[0]):
        for x in range(0, binary_image.shape[1]):
            if binary_image[y, x] > 0:
                binary_image[y, x] = 0
                blob = Blob()
                queue = [[y, x]]

                while len(queue) > 0:

                    y_temp = queue[0][0]
                    x_temp = queue[0][1]

                    if x_temp + 1 < binary_image.shape[1] and binary_image[y_temp, x_temp + 1] > 0:
                        binary_image[y_temp, x_temp + 1] = 0
                        queue.append([y_temp, x_temp + 1])
                    if y_temp + 1 < binary_image.shape[0] and binary_image[y_temp + 1, x_temp] > 0:
                        binary_image[y_temp + 1, x_temp] = 0
                        queue.append([y_temp + 1, x_temp])
                    if x_temp - 1 > 0 and binary_image[y_temp, x_temp - 1] > 0:
                        binary_image[y_temp, x_temp - 1] = 0
                        queue.append([y_temp, x_temp - 1])
                    if y_temp - 1 > 0 and binary_image[y_temp - 1, x_temp] > 0:
                        binary_image[y_temp - 1, x_temp] = 0
                        queue.append([y_temp - 1, x_temp])

                    blob.pixels.append(queue.pop(0))
                blobs.append(blob)
    return blobs


def associateBlobs():
    pass


def findCrop(web_cam):
    B = 116
    G = 77
    R = 157
    global finalMinX, finalMinY, finalMaxX, finalMaxY
    # Check if the web_cam is detected, if not this is not run
    if cv2.VideoCapture(web_cam).isOpened():
        cap = cv2.VideoCapture(web_cam)
        _, frame = cap.read()

        blurred_frame = cv2.GaussianBlur(frame, (9, 9), cv2.BORDER_DEFAULT)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        # Input BGR color to get HSV
        colorBGR = np.uint8([[[B, G, R]]])
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
                    blurred_frame[pixel[0], pixel[1], 0] = blue
                    blurred_frame[pixel[0], pixel[1], 1] = green
                    blurred_frame[pixel[0], pixel[1], 2] = red
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
                    blob.centerX = int(round(((blob.maxX - blob.minX) / 2) + blob.minX))
                    blob.centerY = int(round(((blob.maxY - blob.minY) / 2) + blob.minY))
                    print(blob.centerX, "Center X")
                    print(blob.centerY, "Center Y")
                    print(blob)
                else:
                    # Remove all other elements that aren't markers
                    blobs.remove(blob)
            print(len(blobs))

            # TODO Here calculate the different positions of the markers and use pythagoras to crops this shit
            errorScale = 0
            finalMinX = blobs[1].centerX + errorScale
            finalMinY = blobs[1].centerY + errorScale
            finalMaxX = blobs[0].centerX - errorScale
            finalMaxY = blobs[2].centerY - errorScale
            return finalMinY, finalMaxY, finalMinX, finalMaxX

        # If no markers are found, handle the error
        except IndexError:
            print("Error, no markers found")
            pass
    # No web cam detected, handle it
    else:
        print("No camera found")
