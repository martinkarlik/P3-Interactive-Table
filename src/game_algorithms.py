from src._ip_algorithms import *
import cv2
import math

TABLE_SHAPE = (800, 400)

GREEN_COLOR = (120, 0.7, 0.5)
RED_COLOR = (350, 0.9, 0.5)

WAND_COLOR = (168, 0.68, 0.5)
BLUE_COLOR = (350, 0.9, 0.5)

BEER_COLOR = (50, 0.6, 0.6)
# WAND_COLOR = (216, 0.6, 0.5)
FINGER_COLOR = (37, 0.9, 0.5)

BALL_COLOR_OFFSET = (10, 0.2, 0.3)
WAND_COLOR_OFFSET = (20, 0.2, 0.3)

BALL_COLORS = [RED_COLOR, GREEN_COLOR, BLUE_COLOR]

# Different liquid:
BEER_COLOR = (50, 0.6, 0.6)
BEER_OFFSET = (10, 0.3, 0.5)

DARK_BROWN_ALE = (40, 0.37, 0.115)
DARK_BROWN_ALE_OFFSET = (10, 0.11, 0.025)

MILK = (49.5, 0.403, 0.6145)
MILK_OFFSET = (0.5, 0.003, 0.0265)

COLA = (10, 0.45, 0.06)
COLA_OFFSET = (10, 0.45, 0.06)


class Beer:
    def __init__(self, center):
        self.center = center
        self.is_present = True
        self.wand_here = False
        self.meter = 0
        self.counter = 1200
        self.highlighted = False
        self.yellow = False
        self.red = False
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


def check_for_wand(source, beers_left, beers_right):
    for beer in beers_left:

        start_point_y = int(source.shape[0] * beer.center[0] - 20) if int(source.shape[0] * beer.center[0] - 20) > 0 else 0
        start_point_x = int(source.shape[1] * beer.center[1] - 20) if int(source.shape[1] * beer.center[1] - 20) > 0 else 0
        end_point_y = int(start_point_y + 40) if start_point_y + 40 < source.shape[0] else source.shape[0]
        end_point_x = int(start_point_x + 40) if start_point_x + 40 < source.shape[1] else source.shape[1]

        current_beer_area = source[start_point_y:end_point_y, start_point_x:end_point_x]
        beer.wand_here = color_check_presence(current_beer_area, WAND_COLOR, WAND_COLOR_OFFSET)

    for beer in beers_right:

        start_point_y = int(source.shape[0] * beer.center[0] - 20) if int(source.shape[0] * beer.center[0] - 20) > 0 else 0
        start_point_x = int(source.shape[1] * beer.center[1] - 20) if int(source.shape[1] * beer.center[1] - 20) > 0 else 0
        end_point_y = int(start_point_y + 40) if start_point_y + 40 < source.shape[0] else source.shape[0]
        end_point_x = int(start_point_x + 40) if start_point_x + 40 < source.shape[1] else source.shape[1]

        current_beer_area = source[start_point_y:end_point_y, start_point_x:end_point_x]
        beer.wand_here = color_check_presence(current_beer_area, WAND_COLOR, WAND_COLOR_OFFSET)


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
# def turn_to_drink_left():
#     global player_1_drinks
#     if player_1_drinks:
#         player_1_drinks = False
#         return constants.red_display_color
#     else:
#         player_1_drinks = True
#         return constants.green_display_color
#
#
# def turn_to_drink_right():
#     global player_3_drinks
#     if player_3_drinks:
#         player_3_drinks = False
#         return constants.red_display_color
#     else:
#         player_3_drinks = True
#         return constants.green_display_color

def detect_liquid(source, cupNum):


    if color_check_presence(source,DARK_BROWN_ALE, DARK_BROWN_ALE_OFFSET):

        DarkBrownAleDetected = color_threshold(source, DARK_BROWN_ALE, DARK_BROWN_ALE_OFFSET)
        kernelForClosingDarkAle = np.ones((9, 9), np.uint8)
        kernelForOpenningDarkAle = np.ones((5, 5), np.uint8)

        # opening = cv2.morphologyEx(BeerDetected, cv2.MORPH_OPEN, kernelForOpeningDarkAle)
        # closing = cv2.morphologyEx(DarkBrownAleDetected, cv2.MORPH_CLOSE, kernelForClosingDarkAle)
        closing = DarkBrownAleDetected

        if cupNum == 0:
            cv2.imshow("Cup 1 DA", closing)
        elif cupNum == 1:
            cv2.imshow("Cup 2 DA", closing)
        elif cupNum == 2:
            cv2.imshow("Cup 3 DA", closing)
        elif cupNum == 3:
            cv2.imshow("Cup 4 DA", closing)
        elif cupNum == 4:
            cv2.imshow("Cup 5 DA", closing)
        elif cupNum == 5:
            cv2.imshow("Cup 6 DA", closing)
        elif cupNum == 6:
            cv2.imshow("Cup 7 DA", closing)
        elif cupNum == 7:
            cv2.imshow("Cup 8 DA", closing)
        elif cupNum == 8:
            cv2.imshow("Cup 9 DA", closing)
        elif cupNum == 9:
            cv2.imshow("Cup 10 DA", closing)

        numOfDarkBrownAle = extract_blobs(closing)



        if len(numOfDarkBrownAle) > 0 and cupNum == 0:
            print("This is a Dark Brown Ale",  len(numOfDarkBrownAle), "Cup 1")

        elif len(numOfDarkBrownAle) > 0 and cupNum == 1:
            print("This is a Dark Brown Ale", len(numOfDarkBrownAle), "Cup 2")

        elif len(numOfDarkBrownAle) > 0 and cupNum == 2:
            print("This is a Dark Brown Ale", len(numOfDarkBrownAle), "Cup 3")

        elif len(numOfDarkBrownAle) > 0 and cupNum == 3:
            print("This is a Dark Brown Ale", len(numOfDarkBrownAle), "Cup 4")

        elif len(numOfDarkBrownAle) > 0 and cupNum == 4:
            print("This is a Dark Brown Ale", len(numOfDarkBrownAle), "Cup 5")

        elif len(numOfDarkBrownAle) > 0 and cupNum == 5:
            print("This is a Dark Brown Ale", len(numOfDarkBrownAle), "Cup 6")

        elif len(numOfDarkBrownAle) > 0 and cupNum == 6:
            print("This is a Dark Brown Ale", len(numOfDarkBrownAle), "Cup 7")

        elif len(numOfDarkBrownAle) > 0 and cupNum == 7:
            print("This is a Dark Brown Ale", len(numOfDarkBrownAle), "Cup 8")

        elif len(numOfDarkBrownAle) > 0 and cupNum == 8:
            print("This is a Dark Brown Ale", len(numOfDarkBrownAle), "Cup 9")

        elif len(numOfDarkBrownAle) > 0 and cupNum == 9:
            print("This is a Dark Brown Ale", len(numOfDarkBrownAle), "Cup 10")

    if color_check_presence(source, BEER_COLOR, BEER_OFFSET):

        BeerDetected = color_threshold(source, BEER_COLOR, BEER_OFFSET)
        kernel = np.ones((9, 9), np.uint8)
        kernelOpening = np.ones((5, 5), np.uint8)

        # opening = cv2.morphologyEx(BeerDetected, cv2.MORPH_OPEN, kernelOpening)
        # closing = cv2.morphologyEx(BeerDetected, cv2.MORPH_CLOSE, kernel)
        closing = BeerDetected
        if cupNum == 0:
            cv2.imshow("Cup 1 B", closing)
        elif cupNum == 1:
            cv2.imshow("Cup 2 B", closing)
        elif cupNum == 2:
            cv2.imshow("Cup 3 B", closing)
        elif cupNum == 3:
            cv2.imshow("Cup 4 B", closing)
        elif cupNum == 4:
            cv2.imshow("Cup 5 B", closing)
        elif cupNum == 5:
            cv2.imshow("Cup 6 B", closing)
        elif cupNum == 6:
            cv2.imshow("Cup 7 B", closing)
        elif cupNum == 7:
            cv2.imshow("Cup 8 B", closing)
        elif cupNum == 8:
            cv2.imshow("Cup 9 B", closing)
        elif cupNum == 9:
            cv2.imshow("Cup 10 B", closing)

        numOfBeer = extract_blobs(closing)



        if len(numOfBeer) > 0 and cupNum == 0:
            print("This is a beer",  len(numOfBeer), "Cup 1")

        elif len(numOfBeer) > 0 and cupNum == 1:
            print("This is a beer", len(numOfBeer), "Cup 2")

        elif len(numOfBeer) > 0 and cupNum == 2:
            print("This is a beer", len(numOfBeer), "Cup 3")

        elif len(numOfBeer) > 0 and cupNum == 3:
            print("This is a beer", len(numOfBeer), "Cup 4")

        elif len(numOfBeer) > 0 and cupNum == 4:
            print("This is a beer", len(numOfBeer), "Cup 5")

        elif len(numOfBeer) > 0 and cupNum == 5:
            print("This is a beer", len(numOfBeer), "Cup 6")

        elif len(numOfBeer) > 0 and cupNum == 6:
            print("This is a beer", len(numOfBeer), "Cup 7")

        elif len(numOfBeer) > 0 and cupNum == 7:
            print("This is a beer", len(numOfBeer), "Cup 8")

        elif len(numOfBeer) > 0 and cupNum == 8:
            print("This is a beer", len(numOfBeer), "Cup 9")

        elif len(numOfBeer) > 0 and cupNum == 9:
            print("This is a beer", len(numOfBeer), "Cup 10")


    if color_check_presence(source, MILK, MILK_OFFSET):
        MilkDetected = color_threshold(source, MILK, MILK_OFFSET)
        kernel = np.ones((7, 7), np.uint8)
        kernelOpening = np.ones((5, 5), np.uint8)
        kernelSmall = np.ones((10, 10), np.uint8)

        # opening = cv2.morphologyEx(MilkDetected, cv2.MORPH_OPEN, kernelOpening)
        # closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        closing = MilkDetected

        if cupNum == 0:
            cv2.imshow("Cup 1 Milk", closing)
        elif cupNum == 1:
            cv2.imshow("Cup 2 Milk", closing)
        elif cupNum == 2:
            cv2.imshow("Cup 3 Milk", closing)
        elif cupNum == 3:
            cv2.imshow("Cup 4 Milk", closing)
        elif cupNum == 4:
            cv2.imshow("Cup 5 Milk", closing)
        elif cupNum == 5:
            cv2.imshow("Cup 6 Milk", closing)
        elif cupNum == 6:
            cv2.imshow("Cup 7 Milk", closing)
        elif cupNum == 7:
            cv2.imshow("Cup 8 Milk", closing)
        elif cupNum == 8:
            cv2.imshow("Cup 9 Milk", closing)
        elif cupNum == 9:
            cv2.imshow("Cup 10 Milk", closing)

        numOfMilk = extract_blobs(closing)

        if len(numOfMilk) > 0 and cupNum == 0:
            print("This is a milk",  len(numOfMilk), "Cup 1")
        elif len(numOfMilk) > 0 and cupNum == 1:
            print("This is a milk", len(numOfMilk), "Cup 2")
        elif len(numOfMilk) > 0 and cupNum == 2:
            print("This is a milk", len(numOfMilk), "Cup 3")
        elif len(numOfMilk) > 0 and cupNum == 3:
            print("This is a milk", len(numOfMilk), "Cup 4")
        elif len(numOfMilk) > 0 and cupNum == 4:
            print("This is a milk", len(numOfMilk), "Cup 5")
        elif len(numOfMilk) > 0 and cupNum == 5:
            print("This is a milk", len(numOfMilk), "Cup 6")
        elif len(numOfMilk) > 0 and cupNum == 6:
            print("This is a milk", len(numOfMilk), "Cup 7")
        elif len(numOfMilk) > 0 and cupNum == 7:
            print("This is a milk", len(numOfMilk), "Cup 8")
        elif len(numOfMilk) > 0 and cupNum == 8:
            print("This is a milk", len(numOfMilk), "Cup 9")
        elif len(numOfMilk) > 0 and cupNum == 9:
            print("This is a milk", len(numOfMilk), "Cup 10")


    if color_check_presence(source, COLA, COLA_OFFSET):
        ColaDetected = color_threshold(source, COLA, COLA_OFFSET)
        kernelForClosingCola = np.ones((20, 20), np.uint8)
        kernelForOpenningCola = np.ones((10, 10), np.uint8)

        # opening = cv2.morphologyEx(ColaDetected, cv2.MORPH_OPEN, kernelForOpenningScotch)
        # closing = cv2.morphologyEx(ColaDetected, cv2.MORPH_CLOSE, kernelForClosingCola)
        closing = ColaDetected

        if cupNum == 0:
            cv2.imshow("Cup 1 C", closing)
        elif cupNum == 1:
            cv2.imshow("Cup 2 C", closing)
        elif cupNum == 2:
            cv2.imshow("Cup 3 C", closing)
        elif cupNum == 3:
            cv2.imshow("Cup 4 C", closing)
        elif cupNum == 4:
            cv2.imshow("Cup 5 C", closing)
        elif cupNum == 5:
            cv2.imshow("Cup 6 C", closing)
        elif cupNum == 6:
            cv2.imshow("Cup 7 C", closing)
        elif cupNum == 7:
            cv2.imshow("Cup 8 C", closing)
        elif cupNum == 8:
            cv2.imshow("Cup 9 C", closing)
        elif cupNum == 9:
            cv2.imshow("Cup 10 C", closing)

        numOfCola = extract_blobs(closing)



        if len(numOfCola) > 0 and cupNum == 0:
            print("This is a Cola",  len(numOfCola), "Cup 1")

        elif len(numOfCola) > 0 and cupNum == 1:
            print("This is a Cola", len(numOfCola), "Cup 2")

        elif len(numOfCola) > 0 and cupNum == 2:
            print("This is a Cola", len(numOfCola), "Cup 3")

        elif len(numOfCola) > 0 and cupNum == 3:
            print("This is a Cola", len(numOfCola), "Cup 4")

        elif len(numOfCola) > 0 and cupNum == 4:
            print("This is a Cola", len(numOfCola), "Cup 5")

        elif len(numOfCola) > 0 and cupNum == 5:
            print("This is a Cola", len(numOfCola), "Cup 6")

        elif len(numOfCola) > 0 and cupNum == 6:
            print("This is a Cola", len(numOfCola), "Cup 7")

        elif len(numOfCola) > 0 and cupNum == 7:
            print("This is a Cola", len(numOfCola), "Cup 8")

        elif len(numOfCola) > 0 and cupNum == 8:
            print("This is a Cola", len(numOfCola), "Cup 9")

        elif len(numOfCola) > 0 and cupNum == 9:
            print("This is a Cola", len(numOfCola), "Cup 10")



    if color_check_presence (source,DARK_BROWN_ALE, DARK_BROWN_ALE_OFFSET) == False and color_check_presence(source,BEER_COLOR, BEER_OFFSET) == False and color_check_presence(source,MILK, MILK_OFFSET) == False and color_check_presence(source,COLA, COLA_OFFSET) == False :
        print("There is neither Brown ale, Beer, Milk or Cola in the cup ")



def choose_option(source, modes):
    for i in range(0, len(modes)):
        modes[i].chosen = color_check_presence(get_roi(source, modes[i].pos), WAND_COLOR, WAND_COLOR_OFFSET)
