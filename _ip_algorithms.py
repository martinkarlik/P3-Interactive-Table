import cv2
import numpy as np


class Blob:

    def __init__(self, pixels):
        self.pixels = pixels
        self.area = len(pixels)

        self.bounding_box = self.find_bounding_box()
        self.center = self.find_center()
        self.mean = self.find_mean()

        self.is_beer = self.is_beer()
        self.is_marker = self.is_marker()

    def find_bounding_box(self):
        min_y = self.pixels[0][0]
        min_x = self.pixels[0][1]
        max_y = self.pixels[0][0]
        max_x = self.pixels[0][1]

        for pixel in self.pixels:

            if pixel[0] < min_y:
                min_y = pixel[0]
            if pixel[0] > max_y:
                max_y = pixel[0]
            if pixel[1] < min_x:
                min_x = pixel[1]
            if pixel[1] > max_x:
                max_x = pixel[1]

        return [min_y, min_x, max_y, max_x]

    def find_center(self):
        return [int((self.bounding_box[0] + self.bounding_box[2]) / 2), int((self.bounding_box[1] + self.bounding_box[3]) / 2)]

    def find_mean(self):
        sum_x = 0
        sum_y = 0
        for p in self.pixels:
            sum_x += p[1]
            sum_y += p[0]

        return [int(sum_y / self.area), int(sum_x / self.area)]

    def get_compactness(self):
        return self.area / (self.bounding_box[3] - self.bounding_box[1] + 1) * (self.bounding_box[2] - self.bounding_box[0] + 1)

    def get_circularity(self):
        x = (self.bounding_box[3] - self.bounding_box[1]) * (self.bounding_box[3] - self.bounding_box[1])
        y = (self.bounding_box[2] - self.bounding_box[0]) * (self.bounding_box[2] - self.bounding_box[0])
        perimeter = np.sqrt(x + y)
        return perimeter / (2 * (np.sqrt(np.pi * self.area)))

    def is_beer(self):
        return self.area > 50 and self.get_circularity() > 0

    def is_marker(self):
        return self.area > 100 and self.get_compactness() > 0.7


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


def color_threshold(source, target_color, target_offset):
    hsi = bgr_to_hsi(source)

    hue_match = abs(hsi[:, :, 0] - target_color[0]) < target_offset[0]
    saturation_match = abs(hsi[:, :, 1] - target_color[1]) < target_offset[1]
    intensity_match = abs(hsi[:, :, 2] - target_color[2]) < target_offset[2]

    match = hue_match & saturation_match & intensity_match

    result = np.zeros([source.shape[0], source.shape[1]])
    result[match] = 1

    return result


def color_check_presence(source, target_color, target_offset):
    color_match = color_threshold(source, target_color, target_offset)
    return color_match.any()


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

