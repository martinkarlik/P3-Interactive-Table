from src._ip_algorithms import *
import cv2

MOVED_BEER_THRESHOLD = 0.05

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

    MAX_LIFETIME = 100

    def __init__(self, center):
        self.center = center
        self.lifetime = 5
        self.highlighted = False
        self.balls = [False for i in range(0, 2)]


def extract_beers(source, template, beers_left, beers_right):

    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    match = match_template(binary, template)
    # kernel = np.ones((10, 10), np.uint8)
    # dst = cv2.filter2D(thresh, -1, tpl)

    binary_centers = threshold(match, 0.5, 1)

    cv2.imshow("sth", match)
    cv2.imshow("bin", binary_centers)
    cv2.waitKey(1)

    blobs = extract_blobs(binary_centers)

    for blob in blobs:
        if blob.center[1] / source.shape[1] < 0.5:
            beers_left.append(Beer(blob.center))
        else:
            beers_right.append(Beer(blob.center))

    # closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("closed", closing)

    # contours, _ = cv2.findContours(binary.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #
    # for contour in contours:
    #     area = cv2.contourArea(contour)
    #     arclength = cv2.arcLength(contour, True)
    #     circularity = 4 * np.pi * area / (arclength * arclength) if arclength != 0 else 0
    #     if circularity > 0.75 and area > 1000:
    #         M = cv2.moments(contour)
    #         if M["m00"] != 0:
    #             cX = int((M["m10"] / M["m00"]))
    #             cY = int((M["m01"] / M["m00"]))
    #             relative_center = [cY / source.shape[0], cX / source.shape[1]]
    #             # print(cX, cY, area)
    #
    #             if relative_center[1] < 0.5:
    #                 beers_left.append(Beer(relative_center))
    #             else:
    #                 beers_right.append(Beer(relative_center))


def inform_beers(beers_left, beers_right, current_beers_left, current_beers_right):

    for current_beer in current_beers_left:
        existing_beer_found = False
        for beer in beers_left:
            distance = abs(beer.center[0] - current_beer.center[0]) + abs(beer.center[1] - current_beer.center[1])
            if distance < MOVED_BEER_THRESHOLD:
                beer.is_present = True
                existing_beer_found = True
                break

        if not existing_beer_found:
            beers_left.append(Beer(current_beer.center))

    for beer in beers_left:
        if beer.is_present or any(beer.balls):
            beer.lifetime = min(beer.MAX_LIFETIME, beer.lifetime + 1)
        else:
            beer.lifetime -= 1

    beers_len_init = len(beers_left)
    for i in range(0, beers_len_init):
        if beers_left[beers_len_init - i - 1].lifetime <= 0:
            beers_left.pop(beers_len_init - i - 1)


    for current_beer in current_beers_right:
        existing_beer_found = False
        for beer in beers_right:
            distance = abs(beer.center[0] - current_beer.center[0]) + abs(beer.center[1] - current_beer.center[1])
            if distance < MOVED_BEER_THRESHOLD:
                beer.is_present = True
                existing_beer_found = True
                break

        if not existing_beer_found:
            beers_right.append(Beer(current_beer.center))




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
    binary_inv = 1 - threshold(gray, 0.1, 1)

    cv2.imshow("binary", binary_inv)
    blobs = extract_blobs(binary_inv)

    markers = []
    for blob in blobs:
        if blob.area in range(200, 800) and blob.compactness > 0.7:
            markers.append(blob)

    print(len(markers))

    ordered_markers = [pop_closest(markers, [0, 0]), pop_closest(markers, [0, source.shape[1]]),
                       pop_closest(markers, [source.shape[0], source.shape[1]]), pop_closest(markers, [source.shape[0], 0])]

    src_points = np.float32([(ordered_markers[0].bounding_box[1], ordered_markers[0].bounding_box[0]),
                            (ordered_markers[1].bounding_box[3], ordered_markers[1].bounding_box[0]),
                            (ordered_markers[2].bounding_box[3], ordered_markers[2].bounding_box[2]),
                            (ordered_markers[3].bounding_box[1], ordered_markers[3].bounding_box[2])])

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