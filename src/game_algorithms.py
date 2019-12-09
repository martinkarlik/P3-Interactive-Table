from src._ip_algorithms import *

TABLE_SHAPE = (800, 400)
CUP_RADIUS = 20
MOVED_CUP_THRESHOLD = 0.01

GREEN_COLOR_HSI = (115, 0.75, 0.5)
RED_COLOR_HSI = (350, 0.85, 0.5)
BLUE_COLOR_HSI = (350, 0.9, 0.5)
WAND_COLOR_HSI = (216, 0.7, 0.6)

GREEN_COLOR_RGB = (1, 94, 14)
RED_COLOR_RGB = (165, 9, 20)
BLUE_COLOR_RGB = (21, 58, 110)


BALL_COLOR_OFFSET_HSI = (10, 0.3, 0.4)
WAND_COLOR_OFFSET_HSI = (20, 0.2, 0.4)

DEFAULT_SRC_POINTS = np.float32([(1, 55), (619, 61), (610, 383), (7, 379)])


class Player:
    # static fields... python is weird about it, you don't have to declare anything, it's just static
    # "static" = variable same for every object of this class, "field" = instance variable

    team_colors = [RED_COLOR_RGB, GREEN_COLOR_RGB, BLUE_COLOR_RGB]
    team_names = ["Red", "Green", "Blue"]
    game_score = [0, 0]
    players_num = 2

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 0
        self.drinks = False
        self.hit = False


class Cup:

    ball_colors = [RED_COLOR_HSI, GREEN_COLOR_HSI, BLUE_COLOR_HSI]
    balls_num = 2
    max_lifetime = 10
    max_ball_lifetime = 10
    max_selected_time = 100

    def __init__(self, center):
        self.center = center
        self.is_present = True
        self.lifetime = self.max_lifetime

        self.selection_meter = 0
        self.selected_time = self.max_selected_time

        self.is_yellow = False
        self.is_red = False

        self.has_wand = False
        self.has_balls = [0 for i in range(0, self.balls_num)]


def get_current_cups(source, template, current_cups):

    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    match = match_template(binary, template)
    binary_centers = threshold(match, 0.35, 1)

    # cv2.imshow("binary", binary)
    # cv2.imshow("match", match)
    # cv2.imshow("bin centers", binary_centers)
    # cv2.waitKey(0)

    full_binary_centers = np.zeros([source.shape[0], source.shape[1]])
    tpl_radius = int(template.shape[0] / 2)
    full_binary_centers[tpl_radius:source.shape[0] - tpl_radius + 1, tpl_radius:source.shape[1] - tpl_radius + 1] = binary_centers

    blobs = extract_blobs(full_binary_centers)

    for blob in blobs:
        relative_center = [blob.center[0] / source.shape[0], blob.center[1] / source.shape[1]]
        if relative_center[1] < 0.5:
            current_cups[0].append(Cup(relative_center))
        else:
            current_cups[1].append(Cup(relative_center))


def update_cups(current_cups, cups):

    for i in range(0, len(cups)):

        for cup in cups[i]:
            cup.is_present = False

        for current_cup in current_cups[i]:
            existing_cup_found = False
            for cup in cups[i]:
                distance = abs(cup.center[0] - current_cup.center[0]) + abs(cup.center[1] - current_cup.center[1])
                if distance < MOVED_CUP_THRESHOLD:
                    cup.is_present = True
                    cup.center = current_cup.center
                    existing_cup_found = True
                    break

            if not existing_cup_found:
                cups[i].append(Cup(current_cup.center))

        for cup in cups[i]:
            if cup.is_present:
                cup.lifetime = min(cup.lifetime + 1, cup.max_lifetime)
            else:
                cup.lifetime -= 1

        cups_len_init = len(cups[i])
        for j in range(0, cups_len_init):
            if cups[i][cups_len_init - j - 1].lifetime <= 0:
                cups[i].pop(cups_len_init - j - 1)


def check_for_objects(source, cups):

    for side in cups:
        for cup in side:

            start_point_y = int(source.shape[0] * cup.center[0] - CUP_RADIUS) if int(source.shape[0] * cup.center[0] - CUP_RADIUS) > 0 else 0
            start_point_x = int(source.shape[1] * cup.center[1] - CUP_RADIUS) if int(source.shape[1] * cup.center[1] - CUP_RADIUS) > 0 else 0
            end_point_y = int(start_point_y + CUP_RADIUS * 2) if start_point_y + CUP_RADIUS * 2 < source.shape[0] else source.shape[0]
            end_point_x = int(start_point_x + CUP_RADIUS * 2) if start_point_x + CUP_RADIUS * 2 < source.shape[1] else source.shape[1]

            current_beer_area = source[start_point_y:end_point_y, start_point_x:end_point_x]
            for j in range(0, Cup.balls_num):
                if color_check_presence(current_beer_area, Cup.ball_colors[j], BALL_COLOR_OFFSET_HSI):
                    if cup.has_balls[j] == 0:
                        cup.has_balls[j] = Cup.max_ball_lifetime
                    else:
                        cup.has_balls[j] = min(cup.has_balls[j] + 1, Cup.max_ball_lifetime)
                else:
                    cup.has_balls[j] = max(cup.has_balls[j] - 1, 0)
            cup.has_wand = color_check_presence(current_beer_area, WAND_COLOR_HSI, WAND_COLOR_OFFSET_HSI)


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
    _, binary_inv = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
    open = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, kernel=(15, 15))
    close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel=(18, 18))

    blobs = extract_blobs(close)

    markers = []
    for blob in blobs:
        if blob.area in range(700, 1200) and blob.compactness > 0.8:
            print("Blob: ", blob.area, blob.compactness)
            markers.append(blob)

    src_points = DEFAULT_SRC_POINTS

    if len(markers) == 4 and False:
        ordered_markers = [pop_closest(markers, [0, 0]), pop_closest(markers, [0, source.shape[1]]),
                           pop_closest(markers, [source.shape[0], source.shape[1]]) , pop_closest(markers, [source.shape[0], 0])]

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



ar = [0, 0, 4, ]