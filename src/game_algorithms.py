from src._ip_algorithms import *
import cv2


TABLE_SHAPE = (800, 400)

GREEN_COLOR = (120, 0.7, 0.5)
RED_COLOR = (350, 0.9, 0.5)
BLUE_COLOR = (350, 0.9, 0.5)

BEER_COLOR = (50, 0.6, 0.6)
WAND_COLOR = (216, 0.6, 0.5)
FINGER_COLOR = (37, 0.9, 0.5)

BALL_COLOR_OFFSET = (10, 0.2, 0.3)
WAND_COLOR_OFFSET = (20, 0.2, 0.3)

BALL_COLORS = [RED_COLOR, GREEN_COLOR, BLUE_COLOR]


class Beer:
    def __init__(self, center):
        self.center = center
        self.is_present = True
        self.highlighted = False
        self.balls = [False for i in range(0, 2)]


def inform_beers(source, beers_left, beers_right):

    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)

    # (ret, thresh) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                   cv2.THRESH_BINARY_INV, 11, 2)


    # kernel = np.ones((4, 4), np.uint8)
    # closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)
        arclength = cv2.arcLength(contour, True)
        circularity = 4 * np.pi * area / (arclength * arclength) if arclength != 0 else 0
        if circularity > 0.83 and area > 1000:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                relative_center = [cY / source.shape[0], cX / source.shape[1]]
                if relative_center[1] < 0.5:
                    beers_left.append(Beer(relative_center))
                else:
                    beers_right.append(Beer(relative_center))


# def inform_beers(beers, source, templates, target_color, table_side):
#
#     beers_binary = np.zeros([source.shape[0], source.shape[1]])
#
#     if templates:
#         beers_likelihood_samples = []
#         for template in templates:
#             beers_likelihood_samples.append(match_template(source, template))
#
#         beers_binary_samples = []
#         for sample in beers_likelihood_samples:
#             beers_binary_samples.append(threshold(sample, 0.4, 1))
#
#         beers_binary = beers_binary_samples[0]
#
#         for i in range(1, len(beers_binary_samples)):
#             temp = np.zeros([beers_binary.shape[0], beers_binary.shape[1]])
#             temp[beers_binary == beers_binary_samples[i]] = 1
#             beers_binary = temp
#             # logical AND operation performed on every binary image received from every passed template
#
#     elif target_color:
#         beers_binary = color_threshold(source, target_color[0], target_color[1])
#         kernel = np.ones((10, 10), np.uint8)
#         beers_binary = cv2.morphologyEx(beers_binary, cv2.MORPH_CLOSE, kernel)
#
#     blobs = extract_blobs(beers_binary)
#
#     for beer in beers:
#         beer.is_present = False
#
#     for blob in blobs:
#         if blob.is_beer:
#             blob_relative_center = [blob.center[0] / source.shape[0], table_side * 0.6 + 0.4 * blob.center[1] / source.shape[1]]
#             existing_beer_found = False
#
#             for beer in beers:
#                 distance = abs(blob_relative_center[0] - beer.center[0]) + abs(blob_relative_center[1] - beer.center[1])
#
#                 if distance < MOVED_BEER_THRESHOLD:
#                     beer.is_present = True
#                     existing_beer_found = True
#                     break
#
#             if not existing_beer_found:
#                 beer_center = [blob.center[0] / source.shape[0], table_side * 0.6 + 0.4 * blob.center[1] / source.shape[1]]
#                 beers.append(Beer(beer_center))
#
#     beers_len_init = len(beers)
#     for i in range(0, beers_len_init):
#         if not beers[beers_len_init - i - 1].is_present:
#             beers.pop(beers_len_init - i - 1)
def check_for_balls(source, beers_left, beers_right):
    for beer in beers_left:

        start_point_y = int(source.shape[0] * beer.center[0] - 20) if int(source.shape[0] * beer.center[0] - 20) > 0 else 0
        start_point_x = int(source.shape[1] * beer.center[1] - 20) if int(source.shape[1] * beer.center[1] - 20) > 0 else 0
        end_point_y = int(start_point_y + 40) if start_point_y + 40 < source.shape[0] else source.shape[0]
        end_point_x = int(start_point_x + 40) if start_point_x + 40 < source.shape[1] else source.shape[1]

        current_beer_area = source[start_point_y:end_point_y, start_point_x:end_point_x]
        for i in range(0, 2):
            beer.balls[i] = color_check_presence(current_beer_area, BALL_COLORS[i], BALL_COLOR_OFFSET)

    for beer in beers_right:

        start_point_y = int(source.shape[0] * beer.center[0] - 20) if int(source.shape[0] * beer.center[0] - 20) > 0 else 0
        start_point_x = int(source.shape[1] * beer.center[1] - 20) if int(source.shape[1] * beer.center[1] - 20) > 0 else 0
        end_point_y = int(start_point_y + 40) if start_point_y + 40 < source.shape[0] else source.shape[0]
        end_point_x = int(start_point_x + 40) if start_point_x + 40 < source.shape[1] else source.shape[1]

        current_beer_area = source[start_point_y:end_point_y, start_point_x:end_point_x]
        for i in range(0, 2):
            beer.balls[i] = color_check_presence(current_beer_area, BALL_COLORS[i], BALL_COLOR_OFFSET)


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


def find_table_transform(source, dims):

    def pop_closest(blobs, pos):
        min_distance = abs(blobs[0].center[0] - pos[0]) + abs(blobs[0].center[1] - pos[1])
        closest_index = 0
        for i in range(1, len(blobs)):
            distance = abs(blobs[i].center[0] - pos[0]) + abs(blobs[i].center[1] - pos[1])
            if distance < min_distance:
                min_distance = distance
                closest_index = i

        return blobs.pop(closest_index)

    gray = bgr_to_gray(source)

    binary_inv = 1 - threshold(gray, 0.03, 1)

    blobs = extract_blobs(binary_inv)

    markers = []
    for blob in blobs:
        if blob.area in range(200, 500) and blob.get_compactness() > 0.8:
            markers.append(blob)

    # if len(markers) != 4:
    #     return None

    ordered_markers = [pop_closest(markers, [0, 0]), pop_closest(markers, [0, source.shape[1]]),
                       pop_closest(markers, [source.shape[0], source.shape[1]]), pop_closest(markers, [source.shape[0], 0])]

    src_points = np.float32([(ordered_markers[0].bounding_box[1], ordered_markers[0].bounding_box[0]),
                            (ordered_markers[1].bounding_box[3], ordered_markers[1].bounding_box[0]),
                            (ordered_markers[2].bounding_box[3], ordered_markers[2].bounding_box[2]),
                            (ordered_markers[3].bounding_box[1], ordered_markers[3].bounding_box[2])])

    # src_points = np.float32([(ordered_markers[0].center[1], ordered_markers[0].center[0]),
    #                          (ordered_markers[1].center[1], ordered_markers[1].center[0]),
    #                          (ordered_markers[2].center[1], ordered_markers[2].center[0]),
    #                          (ordered_markers[3].center[1], ordered_markers[3].center[0])])

    # src_points = np.float32([(0, 0),
    #                          (50, 0),
    #                          (50, 50),
    #                          (0, 50)])

    dst_points = np.float32([(0, 0),
                  (dims[0], 0),
                  (dims[0], dims[1]),
                  (0, dims[1])])

    return get_perspective_transform(src_points, dst_points)


def apply_transform(source, matrix, dims):
    return warp_perspective(source, matrix, dims)


def get_roi(source, pos):
    return source[int(pos[0]*source.shape[0]):int(pos[1]*source.shape[0]), int(pos[2]*source.shape[1]):int(pos[3]*source.shape[1])]


def choose_option(source, modes):
    for i in range(0, len(modes)):
        modes[i].chosen = color_check_presence(get_roi(source, modes[i].pos), WAND_COLOR, WAND_COLOR_OFFSET)