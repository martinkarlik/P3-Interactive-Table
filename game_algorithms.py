from _ip_algorithms import *

TABLE_SIDE_LEFT = 0
TABLE_SIDE_RIGHT = 1

MOVED_BEER_THRESHOLD = 0.05

GREEN_COLOR = (120, 0.7, 0.5)
RED_COLOR = (350, 0.9, 0.5)
BEER_COLOR = (50, 0.6, 0.6)
WAND_COLOR = (168, 0.68, 0.5)

COLOR_OFFSET = (10, 0.3, 0.5)


class Beer:

    def __init__(self, center):
        self.center = center
        self.is_present = True

        self.highlighted = False
        self.green_ball = False
        self.red_ball = False

        self.green_buffer = []
        self.red_buffer = []


def inform_beers(beers, source):
    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    (ret, thresh) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        arclength = cv2.arcLength(contour, True)
        circularity = 4 * np.pi * area / (arclength * arclength) if arclength != 0 else 0
        # print('c: ', circularity)
        # print('a: ', area)
        if circularity > 0.83 and area > 1000:
            # print(circularity)
            # print(area)
            beers.append(contour)
            beers.Beer.area = area
            beers.Beer.circular = circularity
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                print(cX, cY)
                beers.Beer.position = cX, cY
            cv2.drawContours(source, contour, -1, (0, 255, 0), 3)

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


def check_for_balls(beers_left, beers_right, source):

    for beer in beers_left:
        start_point_y = int(source.shape[0] * beer.center[0] - 20) if int(source.shape[0] * beer.center[0] - 20) > 0 else 0
        start_point_x = int(source.shape[1] * beer.center[1] - 20) if int(source.shape[1] * beer.center[1] - 20) > 0 else 0
        end_point_y = int(start_point_y + 40) if start_point_y + 40 < source.shape[0] else source.shape[0]
        end_point_x = int(start_point_x + 40) if start_point_x + 40 < source.shape[1] else source.shape[1]

        current_beer_area = source[start_point_y:end_point_y, start_point_x:end_point_x]

        beer.green_ball = color_check_presence(current_beer_area, RED_COLOR, COLOR_OFFSET)
        beer.green_ball = color_check_presence(current_beer_area, GREEN_COLOR, COLOR_OFFSET)

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
        beer.green_ball = color_check_presence(current_beer_area, RED_COLOR, COLOR_OFFSET)
        beer.green_ball = color_check_presence(current_beer_area, GREEN_COLOR, COLOR_OFFSET)

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


def detect_balls(source):
    return [color_check_presence(source, (105, 0.13, 0.58), (10, 0.07, 0.07)),
            color_check_presence(source, (0, 0.13, 0.58), (10, 0.08, 0.08))]


def choose_mode(source):
    return color_check_presence(source, WAND_COLOR, COLOR_OFFSET)


def get_roi(source, y1, y2, x1, x2):
    return source[int(y1*source.shape[0]):int(y2*source.shape[0]), int(x1*source.shape[1]):int(x2*source.shape[1])]
