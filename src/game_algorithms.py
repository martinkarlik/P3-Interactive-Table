from src._ip_algorithms import *

MOVED_BEER_THRESHOLD = 0.05

TABLE_SHAPE = (800, 400)


GREEN_COLOR_HSI = (115, 0.75, 0.5)

RED_COLOR_HSI = (350, 0.85, 0.5)

BLUE_COLOR_HSI = (350, 0.9, 0.5)

WAND_COLOR_HSI = (216, 0.8, 0.5)

GREEN_COLOR_BGR = (14, 94, 1)
RED_COLOR_BGR = (20, 9, 165)
BLUE_COLOR_BGR = (110, 58, 21)
WAND_COLOR_BGR = (110, 58, 21)

BALL_COLOR_OFFSET_HSI = (10, 0.3, 0.4)
WAND_COLOR_OFFSET_HSI = (20, 0.2, 0.3)

# Different liquid:
BEER_COLOR_HSI = (50, 0.6, 0.6)
BEER_OFFSET_HSI = (10, 0.3, 0.5)

DARK_BROWN_ALE = (40, 0.37, 0.115)
DARK_BROWN_ALE_OFFSET = (10, 0.11, 0.025)

MILK = (49.5, 0.403, 0.6145)
MILK_OFFSET = (0.5, 0.003, 0.0265)

COLA = (10, 0.45, 0.06)
COLA_OFFSET = (10, 0.45, 0.06)


class Beer:

    ball_colors = [RED_COLOR_HSI, GREEN_COLOR_HSI, BLUE_COLOR_HSI]
    balls_num = 2
    max_lifetime = 100

    def __init__(self, center):
        self.center = center
        self.is_present = True
        self.lifetime = self.max_lifetime

        self.wand_here = False
        self.meter = 0
        self.counter = 100
        self.yellow = False
        self.red = False
        self.balls = [False for i in range(0, self.balls_num)]


def extract_beers(source, template, beers_left, beers_right):

    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    match = match_template(binary, template)
    binary_centers = threshold(match, 0.35, 1)

    full_binary_centers = np.zeros([source.shape[0], source.shape[1]])
    tpl_radius = int(template.shape[0] / 2)
    full_binary_centers[tpl_radius:source.shape[0] - tpl_radius + 1, tpl_radius:source.shape[1] - tpl_radius + 1] = binary_centers

    cv2.imshow("bin", binary_centers)
    cv2.imshow("full bin", full_binary_centers)

    blobs = extract_blobs(full_binary_centers)

    for blob in blobs:
        relative_center = [blob.center[0] / source.shape[0], blob.center[1] / source.shape[1]]
        if relative_center[1] < 0.5:
            beers_left.append(Beer(relative_center))
        else:
            beers_right.append(Beer(relative_center))


def inform_beers(beers_left, beers_right, current_beers_left, current_beers_right):

    current_sides = [current_beers_left, current_beers_right]
    sides = [beers_left, beers_right]

    for i in range(0, len(sides)):
        for current_beer in current_sides[i]:
            existing_beer_found = False
            for beer in sides[i]:
                distance = abs(beer.center[0] - current_beer.center[0]) + abs(beer.center[1] - current_beer.center[1])
                if distance < MOVED_BEER_THRESHOLD:
                    beer.is_present = True
                    existing_beer_found = True
                    break

            if not existing_beer_found:
                sides[i].append(Beer(current_beer.center))

        for beer in sides[i]:
            if beer.is_present or any(beer.balls) or beer.wand_here:
                beer.lifetime = min(beer.max_lifetime, beer.lifetime + 1)
            else:
                beer.lifetime -= 1

        beers_len_init = len(sides[i])
        for j in range(0, beers_len_init):
            if sides[i][beers_len_init - j - 1].lifetime <= 0:
                sides[i].pop(beers_len_init - j - 1)


def check_for_objects(source, beers_left, beers_right):

    sides = [beers_left, beers_right]

    for side in sides:
        for beer in side:

            start_point_y = int(source.shape[0] * beer.center[0] - 25) if int(source.shape[0] * beer.center[0] - 25) > 0 else 0
            start_point_x = int(source.shape[1] * beer.center[1] - 25) if int(source.shape[1] * beer.center[1] - 25) > 0 else 0
            end_point_y = int(start_point_y + 50) if start_point_y + 50 < source.shape[0] else source.shape[0]
            end_point_x = int(start_point_x + 50) if start_point_x + 50 < source.shape[1] else source.shape[1]

            # source[start_point_y:end_point_y, start_point_x:end_point_x] = 0

            current_beer_area = source[start_point_y:end_point_y, start_point_x:end_point_x]
            for i in range(0, Beer.balls_num):
                beer.balls[i] = color_check_presence(current_beer_area, Beer.ball_colors[i], BALL_COLOR_OFFSET_HSI)
            beer.wand_here = color_check_presence(current_beer_area, WAND_COLOR_HSI, WAND_COLOR_OFFSET_HSI)


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

    # gray = bgr_to_gray(source)
    # binary_inv = 1 - threshold(gray, 0.12, 1)
    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    _, binary_inv = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY_INV)
    open = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, kernel=(15, 15))
    close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel=(18, 18))

    cv2.imshow("bin markers", close)
    cv2.imshow("source", source)
    cv2.waitKey(1)
    blobs = extract_blobs(close)

    markers = []
    for blob in blobs:
        if blob.area in range(700, 1200) and blob.compactness > 0.7:
            print("Blob: ", blob.area, blob.compactness)
            markers.append(blob)

    print(len(markers))
    if len(markers) != 4:
        print("Could not find the correct markers. Instead found ", len(markers), " markers.")

        for marker in markers:
            print(marker.compactness, marker.area, marker.center)

        return np.ones([3, 3])

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


def choose_option(source, options):
    for option in options:
        if option.working:
            option.chosen = color_check_presence(get_roi(source, option.pos), WAND_COLOR_HSI, WAND_COLOR_OFFSET_HSI)


def detect_liquid(source, beers_left, beers_right):
    return
    # if color_check_presence(source,DARK_BROWN_ALE, DARK_BROWN_ALE_OFFSET):
    #
    #     DarkBrownAleDetected = color_threshold(source, DARK_BROWN_ALE, DARK_BROWN_ALE_OFFSET)
    #     kernelForClosingDarkAle = np.ones((9, 9), np.uint8)
    #     kernelForOpenningDarkAle = np.ones((5, 5), np.uint8)
    #
    #     # opening = cv2.morphologyEx(BeerDetected, cv2.MORPH_OPEN, kernelForOpeningDarkAle)
    #     # closing = cv2.morphologyEx(DarkBrownAleDetected, cv2.MORPH_CLOSE, kernelForClosingDarkAle)
    #     closing = DarkBrownAleDetected
    #
    # if color_check_presence(source, BEER_COLOR, BEER_OFFSET):
    #
    #     BeerDetected = color_threshold(source, BEER_COLOR, BEER_OFFSET)
    #     kernel = np.ones((9, 9), np.uint8)
    #     kernelOpening = np.ones((5, 5), np.uint8)
    #
    #     # opening = cv2.morphologyEx(BeerDetected, cv2.MORPH_OPEN, kernelOpening)
    #     # closing = cv2.morphologyEx(BeerDetected, cv2.MORPH_CLOSE, kernel)
    #     closing = BeerDetected
    #
    # if color_check_presence(source, MILK, MILK_OFFSET):
    #     MilkDetected = color_threshold(source, MILK, MILK_OFFSET)
    #     kernel = np.ones((7, 7), np.uint8)
    #     kernelOpening = np.ones((5, 5), np.uint8)
    #     kernelSmall = np.ones((10, 10), np.uint8)
    #
    #     # opening = cv2.morphologyEx(MilkDetected, cv2.MORPH_OPEN, kernelOpening)
    #     # closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    #     closing = MilkDetected
    #
    #
    # if color_check_presence(source, COLA, COLA_OFFSET):
    #     ColaDetected = color_threshold(source, COLA, COLA_OFFSET)
    #     kernelForClosingCola = np.ones((20, 20), np.uint8)
    #     kernelForOpenningCola = np.ones((10, 10), np.uint8)
    #
    #     # opening = cv2.morphologyEx(ColaDetected, cv2.MORPH_OPEN, kernelForOpenningScotch)
    #     # closing = cv2.morphologyEx(ColaDetected, cv2.MORPH_CLOSE, kernelForClosingCola)
    #     closing = ColaDetected
    #
    #
    #
    #
    # if color_check_presence (source,DARK_BROWN_ALE, DARK_BROWN_ALE_OFFSET) == False and color_check_presence(source,BEER_COLOR, BEER_OFFSET) == False and color_check_presence(source,MILK, MILK_OFFSET) == False and color_check_presence(source,COLA, COLA_OFFSET) == False :
    #     print("There is neither Brown ale, Beer, Milk or Cola in the cup ")
