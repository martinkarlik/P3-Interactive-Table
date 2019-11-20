import pygame
import cv2
import algorithms
import constants
import numpy as np

table_img = ""

left_drinks = False
player_1_drinks = True
right_drinks = False
player_3_drinks = True

drink_color_left = constants.white_display_color

game_mode_chosen = False
frame_count = 0


def projection_to_camera_pos(y1, y2, x1, x2):
    return table_roi[int((y1 / 1080) * table_roi.shape[0]): int((y2 / 1080) * table_roi.shape[0]),
           int((x1 / 1920) * table_roi.shape[1]): int(x2 / 1920 * table_roi.shape[1])]


def display_text(score, player):
    if player == 1:
        score = font.render(str(score), True, constants.red_display_color)
        return score
    if player == 2:
        score = font.render(str(score), True, constants.green_display_color)
        return score


# the function that is responsible for changing the table image
def change_table_img(path):
    global table_img
    table_img = "images/tableImages/" + path


# The function that shows the current table image
def display_table_img():
    global table_img
    img = pygame.image.load(table_img)
    img_scale = pygame.transform.scale(img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    screen.blit(img_scale, (0, 0))


# def display_circle(side, side_drinking, player_top, player_bottom):
#     for beer in side:
#         if not side_drinking and beer.red_ball:
#             side_drinking = True
#             drink_color = turn_to_drink_left() if side == beers_left else turn_to_drink_right()
#             player_top += 1
#         elif not side_drinking and beer.green_ball:
#             side_drinking = True
#             drink_color = turn_to_drink_left() if side == beers_left else turn_to_drink_right()
#             player_bottom += 1
#         else:
#             side_drinking = False
#             drink_color = constants.white_display_color
#         pygame.draw.circle(screen, drink_color,
#                            (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 20)


def play_audio(audio):
    pygame.mixer.music.load(audio)
    pygame.mixer.music.queue(audio)

    pygame.mixer.music.play()


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


if __name__ == '__main__':

    # cap = cv2.VideoCapture("recordings/test2_gameplay2.mp4")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_EXPOSURE, -5)
    beer_template_left = cv2.imread("images/testImages/templates/beer_reg_left.jpg")
    beer_template_right = cv2.imread("images/testImages/templates/beer_reg_right.jpg")

    pygame.init()

    DISPLAY_WIDTH = 960
    DISPLAY_HEIGHT = 540

    # DISPLAY_WIDTH = 1280
    # DISPLAY_HEIGHT = 720

    # Create the screen
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)

    # Setup the frame
    pygame.display.set_caption("BeerPong")
    icon = pygame.image.load("images/cheers.png")
    pygame.display.set_icon(icon)

    # change_table_img(("images/tableImages/GameStarted.png"))
    # circle_white = pygame.image.load("images/tableImages/circle_white.png")

    # Setup general things
    font = pygame.font.Font('freesansbold.ttf', 15)

    # player variables
    players_scores = np.zeros(4)

    beers_left = []
    beers_right = []

    _, frame = cap.read()
    cropped_dimensions = algorithms.find_crop(frame)

    app_running = True
    while app_running and cap.isOpened():
        _, frame = cap.read()

        table_roi = frame[cropped_dimensions[0]:cropped_dimensions[1], cropped_dimensions[2]:cropped_dimensions[3]]

        beer_area_left = table_roi[0:table_roi.shape[0], 0:int(table_roi.shape[1] * 0.4)]
        algorithms.inform_beers(beers_left, beer_area_left, None, [(50, 0.6, 0.5), (15, 0.3, 0.5)],
                                algorithms.TABLE_SIDE_LEFT)

        beer_area_right = table_roi[0:table_roi.shape[0], int(table_roi.shape[1] * 0.6):table_roi.shape[1]]
        algorithms.inform_beers(beers_right, beer_area_right, None, [(50, 0.6, 0.5), (15, 0.3, 0.5)],
                                algorithms.TABLE_SIDE_RIGHT)

        algorithms.check_for_balls(beers_left, beers_right, table_roi)

        cv2.imshow("table", table_roi)

        # turns = algorithms.detectTurns()

        # The exit conditions, both pressing x and esc works so far
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app_running = False

        screen.fill(0)

        # Conditionals controlling the projected table image
        if not game_mode_chosen:
            change_table_img("choose_game_mode.png")
            if not algorithms.color_check(table_roi, (172, 0.68, 0.5), constants.color_offset):
                frame_count = 0
            # Casual
            if algorithms.color_check(projection_to_camera_pos(320, 540, 125, 785), (172, 0.68, 0.5), constants.color_offset):
                frame_count += 1
                print(frame_count)
                if frame_count == 5:
                    print("Casual chosen")
                    game_mode_chosen = True
            # HardCore
            if algorithms.color_check(projection_to_camera_pos(320, 540, 1140, 1800), (172, 0.68, 0.5), constants.color_offset):
                frame_count += 1
                print(frame_count)
                if frame_count == 5:
                    print("Hardcore chosen")
                    game_mode_chosen = True
            # Competitive
            if algorithms.color_check(projection_to_camera_pos(710, 930, 125, 785), (172, 0.68, 0.5), constants.color_offset):
                frame_count += 1
                print(frame_count)
                if frame_count == 5:
                    print("Competitive chosen")
            # Custom
            if algorithms.color_check(projection_to_camera_pos(710, 930, 1140, 1800), (172, 0.68, 0.5), constants.color_offset):
                frame_count += 1
                print(frame_count)
                if frame_count == 5:
                    print("Custom chosen")

        elif game_mode_chosen:
            change_table_img("PlaceCups.png")

        elif beers_left != 10 and beers_right != 10:
            change_table_img("GameStarted.png")

        # displays that current path to the image, change image with change_table_img()
        display_table_img()

        # Everything that needs to run after names are input
        if game_mode_chosen:
            screen.blit(pygame.transform.rotate(display_text(int(players_scores[0]), 1), -90),
                        (92 / 1920 * DISPLAY_WIDTH, 160 / 1080 * DISPLAY_HEIGHT))
            screen.blit(pygame.transform.rotate(display_text(int(players_scores[1]), 2), -90),
                        (92 / 1920 * DISPLAY_WIDTH, 870 / 1080 * DISPLAY_HEIGHT))
            screen.blit(pygame.transform.rotate(display_text(int(players_scores[2]), 1), 90),
                        (1725 / 1920 * DISPLAY_WIDTH, 160 / 1080 * DISPLAY_HEIGHT))
            screen.blit(pygame.transform.rotate(display_text(int(players_scores[3]), 2), 90),
                        (1725 / 1920 * DISPLAY_WIDTH, 870 / 1080 * DISPLAY_HEIGHT))

            for beer in beers_left:
                if beer.red_ball:
                    if not left_drinks:
                        left_drinks = True
                        players_scores[0] += 1
                        if left_drinks and player_1_drinks:
                            drink_color_left = constants.red_display_color
                            player_1_drinks = False
                        elif left_drinks and not player_1_drinks:
                            drink_color_left = constants.green_display_color
                            player_1_drinks = True
                elif beer.green_ball:
                    if not left_drinks:
                        left_drinks = True
                        players_scores[1] += 1
                        if left_drinks and player_1_drinks:
                            drink_color_left = constants.red_display_color
                            player_1_drinks = False
                        elif left_drinks and not player_1_drinks:
                            drink_color_left = constants.green_display_color
                            player_1_drinks = True
                else:
                    left_drinks = False
                    drink_color_left = constants.white_display_color

                pygame.draw.circle(screen, drink_color_left,
                                   (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 20)

            for beer in beers_right:
                # if beer.red_ball and not right_drinks:
                #     right_drinks = True
                #     drink_color_right = turn_to_drink_right()
                #     players_scores[2] += 1
                # elif beer.green_ball and right_drinks:
                #     right_drinks = True
                #     drink_color_right = turn_to_drink_right()
                #     players_scores[3] += 1
                # else:
                right_drinks = False
                drink_color_right = constants.white_display_color
                pygame.draw.circle(screen, drink_color_right,
                                   (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 20)

            # display_circle(beers_left, left_drinks, players_scores[0], players_scores[1])
            # display_circle(beers_right, right_drinks, players_scores[2], players_scores[3])

        pygame.display.update()

    cap.release()
    cv2.destroyAllWindows()
