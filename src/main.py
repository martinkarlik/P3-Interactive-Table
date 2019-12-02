import pygame
import cv2
import random
from src import game_algorithms
from src import game_interface

if __name__ == '__main__':
    # CAPTURE SETUP
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_EXPOSURE, -5)
    # cap = cv2.VideoCapture("../recordings/cups.avi")

    # PYGAME SETUP
    pygame.init()
    pygame.display.set_caption("BeerPong")
    icon = pygame.image.load("../images/cheers.png")
    pygame.display.set_icon(icon)

    # Songs and music
    songs = [""]
    # Select, Achievement, cursor
    sounds = ["sound/cuteguisoundsset/Wav/Select.wav", "sound/cuteguisoundsset/Wav/Achievement.wav", "sound/cuteguisoundsset/Wav/Cursor.wav"]
    sound_fx = []
    for sound in sounds:
        sound_fx.append(pygame.mixer.Sound(sound))
    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(SONG_END)

    screen = pygame.display.set_mode((game_interface.DISPLAY_WIDTH, game_interface.DISPLAY_HEIGHT), pygame.FULLSCREEN)
    font = pygame.font.Font(game_interface.FONT_SANS_BOLD[0], game_interface.FONT_SANS_BOLD[1])
    table_img = game_interface.set_table_img(game_interface.TABLE_IMG1)

    # GAME LOGIC SETUP
    game_phase = "game_mode"
    modes = [game_interface.Mode("CASUAL", [0.3, 0.5, 0.1, 0.4]),
             game_interface.Mode("COMPETITIVE", [0.3, 0.5, 0.6, 0.9]),
             game_interface.Mode("CUSTOM", [0.7, 0.9, 0.1, 0.4]),
             game_interface.Mode("EASTERN EUROPEAN", [0.7, 0.9, 0.6, 0.9])]

    team_a = [game_interface.Player(game_interface.Player.team_colors[i]) for i in range(0, game_interface.Player.team_size)]
    team_a[random.randint(0, len(team_a) - 1)].drinks = True

    team_b = [game_interface.Player(game_interface.Player.team_colors[i]) for i in range(0, game_interface.Player.team_size)]
    team_b[random.randint(0, len(team_b) - 1)].drinks = True

    beers_left = []
    beers_right = []

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
                    pygame.mixer.stop()
                    mode.meter = max(mode.meter - 6, 0)

                if mode.meter >= 100:
                    sound_fx[0].play()
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
                for i in range(0, len(beer.balls)):
                    if beer.balls[i] and not team_b[i].hit:
                        team_b[i].score += 1
                        team_b[i].hit = True

                    elif team_b[i].hit and not beer.balls[i]:
                        for j in range(1, len(team_a)):
                            if team_a[j].drinks:
                                team_a[j].drinks = False
                                team_a[j + 1 if j + 1 < len(team_a) else 0].drinks = True

            for beer in beers_right:
                for i in range(0, len(beer.balls)):
                    if beer.balls[i] and not team_a[i].hit:
                        team_a[i].score += 1
                        team_a[i].hit = True

                    elif team_a[i].hit and not beer.balls[i]:
                        for j in range(1, len(team_b)):
                            if team_b[j].drinks:
                                team_b[j].drinks = False
                                team_b[j + 1 if j + 1 < len(team_b) else 0].drinks = True

            # -------------------------
            game_interface.display_table_img(screen, table_img)
            game_interface.display_score(screen, team_a, team_b)
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
            if event.type == SONG_END:
                print("the song ended!")
                game_interface.play_song()


        pygame.display.update()

        # cv2.imshow("table", table_roi)
        # cv2.waitKey(20)


    cap.release()
    cv2.destroyAllWindows()



# TODO Live beer detection, make accurate, make not detect highlighted circles
# TODO Live game mode choosing reliable, doesnt go crazy, detect only the wand or the finger
# TODO Detect balls in the cups
# TODO Classify liquids in the cups
# TODO Detect turns




