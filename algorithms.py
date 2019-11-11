import cv2
import random
from blob import Blob
from beer import Beer
import numpy as np
from scipy import signal


def matchTemplate(source, template):
    return cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)


def getImgKernel(x, y):
    imgKernel = np.array([
        [x - 1, y - 1, x, y - 1, x + 1, y - 1],
        [x - 1, y, x, y, x + 1, y],
        [x - 1, y + 1, x, y + 1, x + 1, y + 1]])
    return imgKernel


def matchTemplateSelf(source, template):
    tempImg = source
    sourceArr = [source[0], source[1], source[2]]

    templateBlue = template[0]
    templateGreen = template[1]
    templateRed = template[2]

    for x in range(0, source.shape[0]):
        for y in range(0, source.shape[1]):
            sourceBlueKernel = getImgKernel(x, y)
            sourceGreenKernel = getImgKernel(x, y)
            sourceRedKernel = getImgKernel(x, y)

            corrBlue = signal.correlate2d(sourceBlueKernel, templateBlue, boundary='symm', mode='same')
            corrGreen = signal.correlate2d(sourceGreenKernel, templateGreen, boundary='symm', mode='same')
            corrRed = signal.correlate2d(sourceRedKernel, templateRed, boundary='symm', mode='same')
            i, j = np.unravel_index(np.argmax(corrBlue), corrBlue.shape)
            tempImg = corrBlue

    return tempImg

def threshold(source, threhsold_value, max_value):

    thresh = np.zeros([source.shape[0], source.shape[1]])
    thresh[source >= threhsold_value] = max_value
    return thresh


def extractBlobs(binary_image):
    blobs = []
    for y in range(0, binary_image.shape[0]):
        for x in range(0, binary_image.shape[1]):
            if binary_image[y, x] > 0:
                binary_image[y, x] = 0
                blob_pixels = []
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

                    blob_pixels.append(queue.pop(0))
                blobs.append(Blob(blob_pixels))
    return blobs


def informBeers(beers, blobs,  beer_area):

    for beer in beers:
        beer.is_present = False

        for blob in blobs:

            if blob.area > 0:  # some threshold to eliminate noise
                distance = abs(blob.center[0] - beer.ideal_center[0]) + abs(blob.center[1] - beer.ideal_center[1])

                if distance < 30:  # some other threshold
                    beer.is_present = True

                    end_point_y = beer.ideal_center[0] + 40 if beer.ideal_center[0] + 40 < beer_area.shape[0] else beer_area.shape[0]
                    end_point_x = beer.ideal_center[1] + 40 if beer.ideal_center[1] + 40 < beer_area.shape[1] else beer_area.shape[1]

                    current_beer_area = beer_area[beer.ideal_center[0]:end_point_y, beer.ideal_center[1]:end_point_x]

                    beer.green_ball = checkColor(current_beer_area, (120, 0.7, 0.5))
                    beer.red_ball = checkColor(current_beer_area, (350, 0.9, 0.5))


def checkColor(source, target_color):

    hsv = bgrToHsi(source)

    hue = hsv[:, :, 0]
    saturation = hsv[:, :, 1]
    intensity = hsv[:, :, 2]

    hue_match = abs(hue - target_color[0]) < 10
    saturation_match = abs(saturation - target_color[1]) < 0.3
    intensity_match = abs(intensity - target_color[2]) < 0.5

    result = hue_match & saturation_match & intensity_match

    # for y in range(0, hsv.shape[0]):
    #     for x in range(0, hsv.shape[1]):
    #         if abs(hsv[y, x][0] - target_color[0]) < 10 and abs(hsv[y, x][1] - target_color[1]) < 0.3 and abs(hsv[y, x][2] - target_color[2]) < 0.5:
    #             return True

    return result.any()


def bgrToHsi(image_bgr):

    blue = image_bgr[:, :, 0] / 255
    green = image_bgr[:, :, 1] / 255
    red = image_bgr[:, :, 2] / 255

    # following code implements the formulas for calculating hue, saturation and intensity from a BGR image
    # since these are point processing operations, they can be implemented using element-wise matrix operations with numpy

    nominator = (red - green) + (red - blue)
    denominator = 2 * np.sqrt((red - green) * (red - green) + (red - blue) * (green - blue))

    theta = np.zeros([image_bgr.shape[0], image_bgr.shape[1]])

    # get indices where denominator is non-zero
    non_zeros = denominator > 0
    theta[non_zeros] = np.degrees(np.arccos(nominator[non_zeros] / denominator[non_zeros]))

    hue = np.zeros([image_bgr.shape[0], image_bgr.shape[1]])
    hue[blue <= green] = theta[blue <= green]
    hue[blue > green] = (360 - theta[blue > green])

    saturation = np.zeros([image_bgr.shape[0], image_bgr.shape[1]])
    non_zeros = (red + green + blue) > 0
    saturation[non_zeros] = 1 - (3 / (red[non_zeros] + green[non_zeros] + blue[non_zeros]) *
                                 np.minimum(np.minimum(red[non_zeros], green[non_zeros]), blue[non_zeros]))

    intensity = (red + green + blue) / 3

    image_hsi = np.zeros([image_bgr.shape[0], image_bgr.shape[1], image_bgr.shape[2]])
    image_hsi[:, :, 0] = hue
    image_hsi[:, :, 1] = saturation
    image_hsi[:, :, 2] = intensity

    return image_hsi

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
