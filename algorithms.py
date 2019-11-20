import cv2

import constants
from blob import Blob
from beer import Beer
import numpy as np
from scipy import signal

TABLE_SIDE_LEFT = 0
TABLE_SIDE_RIGHT = 1
MOVED_BEER_THRESHOLD = 0.05


def match_template(source, template):
    return cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)


def threshold(source, threshold_value, max_value):
    thresh = np.zeros([source.shape[0], source.shape[1]])
    thresh[source >= threshold_value] = max_value
    return thresh


def extract_blobs(binary_image):
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









def inform_beers(beers, source, templates, target_color, table_side):

    beers_binary = np.zeros([source.shape[0], source.shape[1]])

    if templates:
        beers_likelihood_samples = []
        for template in templates:
            beers_likelihood_samples.append(match_template(source, template))

        beers_binary_samples = []
        for sample in beers_likelihood_samples:
            beers_binary_samples.append(threshold(sample, 0.4, 1))

        beers_binary = beers_binary_samples[0]

        for i in range(1, len(beers_binary_samples)):
            temp = np.zeros([beers_binary.shape[0], beers_binary.shape[1]])
            temp[beers_binary == beers_binary_samples[i]] = 1
            beers_binary = temp
            # logical AND operation performed on every binary image received from every passed template

    elif target_color:
        beers_binary = color_threshold(source, target_color[0], target_color[1])
        kernel = np.ones((10, 10), np.uint8)
        beers_binary = cv2.morphologyEx(beers_binary, cv2.MORPH_CLOSE, kernel)

    blobs = extract_blobs(beers_binary)

    for beer in beers:
        beer.is_present = False

    for blob in blobs:
        if blob.is_beer:
            blob_relative_center = [blob.center[0] / source.shape[0], table_side * 0.6 + 0.4 * blob.center[1] / source.shape[1]]
            existing_beer_found = False

            for beer in beers:
                distance = abs(blob_relative_center[0] - beer.center[0]) + abs(blob_relative_center[1] - beer.center[1])

                if distance < MOVED_BEER_THRESHOLD:
                    beer.is_present = True
                    existing_beer_found = True
                    break

            if not existing_beer_found:
                beer_center = [blob.center[0] / source.shape[0], table_side * 0.6 + 0.4 * blob.center[1] / source.shape[1]]
                beers.append(Beer(beer_center))

    beers_len_init = len(beers)
    for i in range(0, beers_len_init):
        if not beers[beers_len_init - i - 1].is_present:
            beers.pop(beers_len_init - i - 1)


def check_for_balls(beers_left, beers_right, source):

    for beer in beers_left:
        start_point_y = int(source.shape[0] * beer.center[0] - 20) if int(source.shape[0] * beer.center[0] - 20) > 0 else 0
        start_point_x = int(source.shape[1] * beer.center[1] - 20) if int(source.shape[1] * beer.center[1] - 20) > 0 else 0
        end_point_y = int(start_point_y + 40) if start_point_y + 40 < source.shape[0] else source.shape[0]
        end_point_x = int(start_point_x + 40) if start_point_x + 40 < source.shape[1] else source.shape[1]

        current_beer_area = source[start_point_y:end_point_y, start_point_x:end_point_x]

        beer.green_ball = color_check(current_beer_area, constants.red_color, constants.color_offset)
        beer.green_ball = color_check(current_beer_area, constants.green_color, constants.color_offset)

        # if len(beer.green_buffer) < 10:
        #     beer.green_buffer.append(color_check(current_beer_area, constants.green_color, constants.color_offset))
        # else:
        #     beer.green_buffer.pop(0)
        # np_green_buffer = np.array(beer.green_buffer)
        # beer.green_ball = np_green_buffer.all()
        #
        # if len(beer.red_buffer) < 10:
        #     beer.red_buffer.append(color_check(current_beer_area, constants.red_color, constants.color_offset))
        # else:
        #     beer.red_buffer.pop(0)
        #     beer.red_buffer.append(color_check(current_beer_area, constants.red_color, constants.color_offset))
        # np_red_buffer = np.array(beer.red_buffer)
        # beer.red_ball = np_red_buffer.all()

    for beer in beers_right:
        start_point_x = int(source.shape[1] * beer.center[1])
        start_point_y = int(source.shape[0] * beer.center[0])
        end_point_y = int(start_point_y + 40) if start_point_y + 40 < source.shape[0] else source.shape[0]
        end_point_x = int(start_point_x + 40) if start_point_x + 40 < source.shape[1] else source.shape[1]

        current_beer_area = source[start_point_y:end_point_y, start_point_x:end_point_x]
        beer.green_ball = color_check(current_beer_area, constants.red_color, constants.color_offset)
        beer.green_ball = color_check(current_beer_area, constants.green_color, constants.color_offset)

        # # check if the ball has been spotted for more than 10 frames
        # if len(beer.green_buffer) < 10:
        #     beer.green_buffer.append(color_check(current_beer_area, constants.green_color, constants.color_offset))
        # else:
        #     beer.green_buffer.pop(0)
        #     beer.green_buffer.append(color_check(current_beer_area, constants.green_color, constants.color_offset))
        # np_green_buffer = np.array(beer.green_buffer)
        # beer.green_ball = np_green_buffer.all()
        #
        # if len(beer.red_buffer) < 10:
        #     beer.red_buffer.append(color_check(current_beer_area, constants.red_color, constants.color_offset))
        # else:
        #     beer.red_buffer.pop(0)
        #     beer.red_buffer.append(color_check(current_beer_area, constants.red_color, constants.color_offset))
        # np_red_buffer = np.array(beer.red_buffer)
        # beer.red_ball = np_red_buffer.all()


def color_check(source, target_color, target_offset):
    hsi = bgr_to_hsi(source)

    hue_match = abs(hsi[:, :, 0] - target_color[0]) < target_offset[0]
    saturation_match = abs(hsi[:, :, 1] - target_color[1]) < target_offset[1]
    intensity_match = abs(hsi[:, :, 2] - target_color[2]) < target_offset[2]

    #  abs([7, 4, 1] - 3) results into [3, 1, -2].. [3, 1, -2] > 0 results into [True, True, False]
    # it might look confusing but these element-wise matrix operations are necessary for our code to run in real time

    result = hue_match & saturation_match & intensity_match

    return result.any()


def color_threshold(source, target_color, target_offset):
    hsi = bgr_to_hsi(source)

    hue_match = abs(hsi[:, :, 0] - target_color[0]) < target_offset[0]
    saturation_match = abs(hsi[:, :, 1] - target_color[1]) < target_offset[1]
    intensity_match = abs(hsi[:, :, 2] - target_color[2]) < target_offset[2]

    match = hue_match & saturation_match & intensity_match

    result = np.zeros([source.shape[0], source.shape[1]])
    result[match] = 1

    return result


def detect_balls(source):
    return [color_check(source, (105, 0.13, 0.58), (10, 0.07, 0.07)),
            color_check(source, (0, 0.13, 0.58), (10, 0.08, 0.08))]


def bgr_to_hsi(image_bgr):
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


def find_crop(source):
    markers_binary = color_threshold(source, (331, 0.5, 0.5), (30, 0.4, 0.5))
    kernel = np.ones((10, 10), np.uint8)
    markers_binary = cv2.morphologyEx(markers_binary, cv2.MORPH_CLOSE, kernel)

    markers = extract_blobs(markers_binary)
    print(len(markers))

    # right now taking only the two markers in two opposing the corners.. cropping based on that
    # would not work if you angle the camera or the table
    # need to look into camera calibration, extrinsic parameters

    start_y = markers[0].bounding_box[0]
    start_x = markers[0].bounding_box[1]
    end_y = markers[1].bounding_box[2]
    end_x = markers[1].bounding_box[3]

    return [start_y, end_y, start_x, end_x]
