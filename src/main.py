import pygame
import cv2
from src import game_algorithms
from src import game_interface

if __name__ == '__main__':
    # CAPTURE SETUP
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_EXPOSURE, 3)
    # cap = cv2.VideoCapture("../recordings/cups.avi")

    # PYGAME SETUP
    pygame.init()
    pygame.display.set_caption("BeerPong")
    icon = pygame.image.load("../images/cheers.png")
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((game_interface.DISPLAY_WIDTH, game_interface.DISPLAY_HEIGHT))
    font = pygame.font.Font(game_interface.FONT_SANS_BOLD[0], game_interface.FONT_SANS_BOLD[1])
    table_img = game_interface.set_table_img(game_interface.TABLE_IMG1)

    # GAME LOGIC SETUP
    game_phase = "game_mode"
    modes = [game_interface.Mode("CASUAL", [0.3, 0.5, 0.1, 0.4]),
             game_interface.Mode("COMPETITIVE", [0.3, 0.5, 0.6, 0.9]),
             game_interface.Mode("CUSTOM", [0.7, 0.9, 0.1, 0.4]),
             game_interface.Mode("EASTERN EUROPEAN", [0.7, 0.9, 0.6, 0.9])]

    scores = [0 for i in range(0, 4)]

    beers_left = []
    beers_right = []
    drink_color_left = game_interface.WHITE_DISPLAY_COLOR
    left_drinks = False
    player_1_drinks = True
    right_drinks = False
    player_3_drinks = True

    _, frame = cap.read()
    # cropped_dimensions = game_algorithms.find_crop(frame)
    cropped_dimensions = [65, 378, 21, 620]

    app_running = True
    while app_running and cap.isOpened():

        _, frame = cap.read()
        table_roi = frame[cropped_dimensions[0]:cropped_dimensions[1], cropped_dimensions[2]:cropped_dimensions[3]]

        if game_phase == "game_mode":
            game_algorithms.choose_mode(table_roi, modes)
            # -------------------------

            for mode in modes:
                if mode.chosen:
                    mode.meter += 2
                else:
                    mode.meter = max(mode.meter - 8, 0)

                if mode.meter >= 100:
                    game_phase = "game_play"
                    table_img = game_interface.set_table_img(game_interface.TABLE_IMG2)

            # -------------------------
            game_interface.display_table_img(screen, table_img)
            game_interface.display_mode_selection(screen, font, modes)

        elif game_phase == "game_play":

            beers_left = []
            beers_right = []

            game_algorithms.inform_beers(table_roi, beers_left, beers_right)
            game_algorithms.check_for_balls(table_roi, beers_left, beers_right)
            # turns = algorithms.detectTurns()
            # -------------------------
            for beer in beers_left:
                if beer.red_ball:
                    if not left_drinks:
                        left_drinks = True
                        scores[0] += 1
                        if left_drinks and player_1_drinks:
                            drink_color_left = game_interface.RED_DISPLAY_COLOR
                            player_1_drinks = False
                        elif left_drinks and not player_1_drinks:
                            drink_color_left = game_interface.GREEN_DISPLAY_COLOR
                            player_1_drinks = True
                elif beer.green_ball:
                    if not left_drinks:
                        left_drinks = True
                        scores[1] += 1
                        if left_drinks and player_1_drinks:
                            drink_color_left = game_interface.RED_DISPLAY_COLOR
                            player_1_drinks = False
                        elif left_drinks and not player_1_drinks:
                            drink_color_left = game_interface.GREEN_DISPLAY_COLOR
                            player_1_drinks = True
                else:
                    left_drinks = False
                    drink_color_left = game_interface.WHITE_DISPLAY_COLOR
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
                drink_color_right = game_interface.WHITE_DISPLAY_COLOR

            # -------------------------
            game_interface.display_table_img(screen, table_img)
            # game_interface.display_score(screen)
            game_interface.display_beers(screen, beers_left, beers_right)

        elif game_phase == "game_over":
            # if there are more screens, different IP stuff on each
            pass

        # KEYBOARD INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app_running = False


        pygame.display.update()

        cv2.imshow("table", table_roi)
        cv2.waitKey(20)


    cap.release()
    cv2.destroyAllWindows()



# TODO Live beer detection, make accurate, make not detect highlighted circles
# TODO Live game mode choosing reliable, doesnt go crazy, detect only the wand or the finger
# TODO Detect balls in the cups
# TODO Classify liquids in the cups
# TODO Detect turns




