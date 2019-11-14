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
    tempImg = np.copy(source)
    templateArray = [[]]
    templateBlue = template[:, :, 0]
    templateGreen = template[:, :, 1]
    templateRed = template[:, :, 2]

    height = template.shape[1]
    width = template.shape[0]
    for x in range(0, width):
        for y in range(0, height):
            templateArray = x, y

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

def threshold(source, threshold_value, max_value):

    thresh = np.zeros([source.shape[0], source.shape[1]])
    thresh[source >= threshold_value] = max_value
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


def extractBeers(source, templates, target_color=None, locked_position=False):

    beers_likelihood_samples = []
    for template in templates:
        beers_likelihood_samples.append(matchTemplate(source, template))

    beers_binary_samples = []
    for sample in beers_likelihood_samples:
        beers_binary_samples = threshold(sample, 0.4, 1)

    beers_binary = beers_binary_samples[0]
    for i in range(1, len(beers_binary_samples)):
        beers_binary = beers_binary & beers_binary_samples[i]  # logical AND operation performed on every binary image received from every passed template

    blobs = extractBlobs(beers_binary)
    # filterBlobs(blobs)

    beers = []
    for blob in blobs:
        beers.append(Beer(blob.center))

    return beers


def informBeers(beers, blobs,  beer_area):

    for beer in beers:
        beer.is_present = False

        for blob in blobs:

            if blob.area > 0:  # some threshold to eliminate noise
                distance = abs(blob.center[0] - beer.center[0]) + abs(blob.center[1] - beer.center[1])

                if distance < 30:  # some other threshold
                    beer.is_present = True

                    end_point_y = beer.center[0] + 40 if beer.center[0] + 40 < beer_area.shape[0] else beer_area.shape[0]
                    end_point_x = beer.center[1] + 40 if beer.center[1] + 40 < beer_area.shape[1] else beer_area.shape[1]

                    current_beer_area = beer_area[beer.center[0]:end_point_y, beer.center[1]:end_point_x]

                    beer.green_ball = checkColor(current_beer_area, (120, 0.7, 0.5), (10, 0.3, 0.5))
                    beer.red_ball = checkColor(current_beer_area, (350, 0.9, 0.5), (10, 0.3, 0.5))


def checkColor(source, target_color, target_offset):

    hsv = bgrToHsi(source)

    hue_match = abs(hsv[:, :, 0] - target_color[0]) < target_offset[0]
    saturation_match = abs(hsv[:, :, 1] - target_color[1]) < target_offset[1]
    intensity_match = abs(hsv[:, :, 2] - target_color[2]) < target_offset[2]

    #  abs([7, 4, 1] - 3) results into [3, 1, -2].. [3, 1, -2] > 0 results into [True, True, False]
    # it might look confusing but these element-wise matrix operations are necessary for our code to run in real time

    result = hue_match & saturation_match & intensity_match
    # example: [False, True] & [True, False] -> [False, False]

    # ... the above does the same as the below, just faster
    # ...
    # for y in range(0, hsv.shape[0]):
    #     for x in range(0, hsv.shape[1]):
    #         if abs(hsv[y, x][0] - target_color[0]) < 10 and abs(hsv[y, x][1] - target_color[1]) < 0.3 and abs(hsv[y, x][2] - target_color[2]) < 0.5:
    #             return True

    return result.any()


def colorThreshold(source, target_color, target_offset):

    hsi = bgrToHsi(source)

    hue_match = abs(hsi[:, :, 0] - target_color[0]) < target_offset[0]
    saturation_match = abs(hsi[:, :, 1] - target_color[1]) < target_offset[1]
    intensity_match = abs(hsi[:, :, 2] - target_color[2]) < target_offset[2]

    match = hue_match & saturation_match & intensity_match

    result = np.zeros([source.shape[0], source.shape[1]])
    result[match] = 255

    # ... the above does the same as the below, just faster
    # for y in range(0, hsv.shape[0]):
    #     for x in range(0, hsv.shape[1]):
    #         if abs(hsv[y, x][0] - target_color[0]) < 10 and abs(hsv[y, x][1] - target_color[1]) < 0.3 and abs(hsv[y, x][2] - target_color[2]) < 0.5:
    #             return True

    return result

def detectBalls(source):
    return [checkColor(source, (105, 0.13, 0.58), (10, 0.07, 0.07)), checkColor(source, (0, 0.13, 0.58), (10, 0.08, 0.08))]


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

def findCrop(source):
    markers_binary = colorThreshold(source, (331, 0.5, 0.5), (10, 0.2, 0.5))


    markers = extractBlobs(markers_binary)

    # right now taking only the two markers in two opposing the corners.. cropping based on that
    # would not work if you angle the camera or the table
    # need to look into camera callibration, extrinsic parameters

    start_y = markers[0].bounding_box[0]
    start_x = markers[0].bounding_box[1]
    end_y = markers[1].bounding_box[2]
    end_x = markers[1].bounding_box[3]
    print(start_y, end_y, start_x, end_x)
    return [start_y, end_y, start_x, end_x]

