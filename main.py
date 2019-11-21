import pygame
import cv2
import game_algorithms
import numpy as np

table_img = ""

GREEN_DISPLAY_COLOR = 7, 129, 30
RED_DISPLAY_COLOR = 242, 81, 87
WHITE_DISPLAY_COLOR = 255, 255, 255


def display_text(score, player):
    if player == 1:
        score = font.render(str(score), True, RED_DISPLAY_COLOR)
        return score
    if player == 2:
        score = font.render(str(score), True, GREEN_DISPLAY_COLOR)
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


DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080

if __name__ == '__main__':

    # CAPTURE SETUP
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_EXPOSURE, -5)
    beer_template_left = cv2.imread("images/testImages/templates/beer_reg_left.jpg")
    beer_template_right = cv2.imread("images/testImages/templates/beer_reg_right.jpg")

    # PYGAME SETUP
    pygame.init()

    pygame.display.set_caption("BeerPong")
    icon = pygame.image.load("images/cheers.png")
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    font = pygame.font.Font('freesansbold.ttf', 15)

    # GAME SETUP
    players_scores = np.zeros(4)
    game_phase = "game_play"

    beers_left = []
    beers_right = []

    drink_color_left = WHITE_DISPLAY_COLOR

    left_drinks = False
    player_1_drinks = True
    right_drinks = False
    player_3_drinks = True
    game_mode_chosen = False

    _, frame = cap.read()
    # cropped_dimensions = game_algorithms.find_crop(frame)
    # TODO cropping, camera calibration (extrinsic parameters)
    cropped_dimensions = [65, 378, 21, 620]



    app_running = True
    while app_running and cap.isOpened():

        _, frame = cap.read()
        table_roi = frame[cropped_dimensions[0]:cropped_dimensions[1], cropped_dimensions[2]:cropped_dimensions[3]]

        cv2.imshow("frame", frame)

        # IMAGE PROCESSING

        if game_phase == "game_mode":

            mode = 0
            if not game_algorithms.choose_mode(table_roi):
                frame_count = 0
                # Casual

            if game_algorithms.choose_mode(game_algorithms.get_roi(table_roi, 0.49, 0.71, 0.56, 0.9)):
                frame_count += 1
                mode = 1
                print(frame_count, "Custom")
                if frame_count == 10:
                    print("Custom chosen")
                    game_phase = "game_play"
                # HardCore
            if game_algorithms.choose_mode(game_algorithms.get_roi(table_roi, 0.5, 0.72, 0.06, 0.4)):
                frame_count += 1
                print(frame_count, "competitive")
                mode = 2
                if frame_count == 10:
                    print("Competitive chosen")
                    game_phase = "game_play"
                # Competitive
            if game_algorithms.choose_mode(game_algorithms.get_roi(table_roi, 0.14, 0.36, 0.56, 0.9)):
                frame_count += 1
                mode = 3
                print(frame_count, "Hardcore")
                if frame_count == 10:
                    print("HardCore chosen")
                    game_phase = "game_play"
                # Custom
            if game_algorithms.choose_mode(game_algorithms.get_roi(table_roi, 0.14, 0.36, 0.06, 0.4)):
                frame_count += 1
                mode = 4
                print(frame_count, "Casual")
                if frame_count == 10:
                    print("Casual chosen")
                    game_phase = "game_play"

        elif game_phase == "game_play":
            table_roi = frame[cropped_dimensions[0]:cropped_dimensions[1], cropped_dimensions[2]:cropped_dimensions[3]]

            beer_area_left = table_roi[0:table_roi.shape[0], 0:int(table_roi.shape[1] * 0.4)]
            game_algorithms.inform_beers(beers_left, beer_area_left, None, [(50, 0.6, 0.5), (20, 0.4, 0.5)], game_algorithms.TABLE_SIDE_LEFT)

            beer_area_right = table_roi[0:table_roi.shape[0], int(table_roi.shape[1] * 0.6):table_roi.shape[1]]
            game_algorithms.inform_beers(beers_right, beer_area_right, None, [(50, 0.6, 0.5), (20, 0.4, 0.5)], game_algorithms.TABLE_SIDE_RIGHT)
            # TODO inform_beers with marked cups

            # game_algorithms.check_for_balls(beers_left, beers_right, table_roi)
            # turns = algorithms.detectTurns()

        elif game_phase == "game_over":
            # if there are more screens, different IP stuff on each
            pass


        # GAME LOGIC
        # any game logic and game mechanics related stuff here, also whos turns is it to drink etc.




        # KEYBOARD INPUT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app_running = False



        # PROJECTION

        screen.fill(0)

        # Conditionals controlling the projected table image
        if game_phase == "game_mode":
            change_table_img("choose_game_mode.png")

        elif game_phase == "game_play":
            change_table_img("PlaceCups.png")
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
                            drink_color_left = RED_DISPLAY_COLOR
                            player_1_drinks = False
                        elif left_drinks and not player_1_drinks:
                            drink_color_left = GREEN_DISPLAY_COLOR
                            player_1_drinks = True
                elif beer.green_ball:
                    if not left_drinks:
                        left_drinks = True
                        players_scores[1] += 1
                        if left_drinks and player_1_drinks:
                            drink_color_left = RED_DISPLAY_COLOR
                            player_1_drinks = False
                        elif left_drinks and not player_1_drinks:
                            drink_color_left = GREEN_DISPLAY_COLOR
                            player_1_drinks = True
                else:
                    left_drinks = False
                    drink_color_left = WHITE_DISPLAY_COLOR

                pygame.draw.circle(screen, drink_color_left,
                                   (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 40)

            # if beers_left != 10 and beers_right != 10:
            #     change_table_img("GameStarted.png")

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
                drink_color_right = WHITE_DISPLAY_COLOR

                pygame.draw.circle(screen, drink_color_right,
                                   (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 40)

        # displays that current path to the image, change image with change_table_img()
        display_table_img()

        pygame.display.update()

    cap.release()
    cv2.destroyAllWindows()
