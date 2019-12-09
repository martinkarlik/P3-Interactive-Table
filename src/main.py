import pygame
import cv2
import random
from src import game_algorithms
from src import game_interface


congratulations = True
team_a_won = False

FONT_SANS_BOLD = ['freesansbold.ttf', 25]
FONT_MYRIAD_PRO_REGULAR = ['../fonts/MyriadProRegular.ttf', 60]
FONT_MYRIAD_PRO_REGULAR2 = ['../fonts/MyriadProRegular.ttf', 97]


ICON = "../images/tableImages/cheers.png"
TAPE_IMAGE = "../images/tableImages/tape.png"
TABLE_IMAGES = ["../images/tableImages/mode_selection.png", "../images/tableImages/game_play_competitive.png",
                "../images/tableImages/game_over.png"]
SONGS = ["../sound/mass_effect_elevator_music_2.mp3", "../sound/epic_musix.mp3"]  # you_can_add_more

SOUNDS = ["../sound/cuteguisoundsset/Wav/Select.wav", "../sound/cuteguisoundsset/Wav/Achievement.wav",
          "../sound/cuteguisoundsset/Wav/Cursor.wav", "../sound/hit_the_golden_cup_jingle.wav"]
whosTurnA = (0, 0, 0)
whosTurnB = (0, 0, 0)
whoHit = (0, 0, 0)
totalScoreRight = 0
totalScoreLeft = 0

SPEAK = ["../sound/Speak/team_1_wins.wav", "../sound/Speak/team_2_wins.wav", "../sound/Speak/well_done.wav",
         "../sound/Speak/great_job.wav", "../sound/Speak/what_a_shot.wav",
         "../sound/Speak/wow.wav", "../sound/Speak/you_did_it.wav", "../sound/Speak/brilliantly_done.wav", "../sound/Speak/fantastic.wav",
         "../sound/Speak/incredible_shot.wav", "../sound/Speak/keep_up_the_work.wav", "../sound/Speak/oh_yea.wav",
         "../sound/Speak/you're_a_star.wav"]


if __name__ == '__main__':

    # CAPTURE SETUP
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv2.CAP_PROP_EXPOSURE, -5)

    # INTERFACE SETUP
    pygame.init()
    pygame.display.set_caption("BeerPong")
    icon = pygame.image.load(ICON)
    pygame.display.set_icon(icon)

    songs = pygame.mixer.Channel(2)
    songs.set_volume(0.7)
    speak = pygame.mixer.Channel(4)
    speak_fx = []
    for sound in SPEAK:
        speak_fx.append(pygame.mixer.Sound(sound))
    jingle = pygame.mixer.Channel(3)
    sound_fx = []
    for sound in SOUNDS:
        sound_fx.append(pygame.mixer.Sound(sound))

    screen = pygame.display.set_mode((game_interface.DISPLAY_WIDTH, game_interface.DISPLAY_HEIGHT))
    font = pygame.font.Font(FONT_SANS_BOLD[0], FONT_SANS_BOLD[1])

    table_img = game_interface.set_table_image(TABLE_IMAGES[0])
    tape_img = pygame.image.load(TAPE_IMAGE)
    template = cv2.imread("../images/testImages/beer.jpg", cv2.IMREAD_GRAYSCALE)

    # GAME LOGIC SETUP
    game_phase = "mode_selection"
    modes = [game_interface.Button("CASUAL", [0.35, 0.55, 0.1, 0.4], True),
             game_interface.Button("COMPETITIVE", [0.35, 0.55, 0.6, 0.9], True),
             game_interface.Button("CUSTOM", [0.7, 0.9, 0.1, 0.4], False),
             game_interface.Button("EASTERN EUROPEAN", [0.7, 0.9, 0.6, 0.9], False)]

    play_again_button = game_interface.Button("PLAY AGAIN", [0.75, 0.95, 0.3, 0.7], True)

    teams = [[], []]
    team_a_won = True

    teams[0] = [game_algorithms.Player(game_algorithms.Player.team_names[i], game_algorithms.Player.team_colors[i]) for i in range(0, game_algorithms.Player.players_num)]
    teams[0][random.randint(0, len(teams[0]) - 1)].drinks = True

    teams[1] = [game_algorithms.Player(game_algorithms.Player.team_names[i], game_algorithms.Player.team_colors[i]) for i in
              range(0, game_algorithms.Player.players_num)]
    teams[1][random.randint(0, len(teams[1]) - 1)].drinks = True

    cups = [[], []]

    selection_music_playing = False
    gameplay_music_playing = False

    _, frame = cap.read()
    table_transform = game_algorithms.find_table_transform(frame, game_algorithms.TABLE_SHAPE)
    table = cv2.imread("../images/testImages/table_trans.jpg")

    app_running = True
    while app_running and cap.isOpened():

        _, frame = cap.read()
        # table = game_algorithms.apply_transform(frame, table_transform, game_algorithms.TABLE_SHAPE)

        if game_phase == "mode_selection":
            game_algorithms.choose_option(table, modes)

            for mode in modes:
                if mode.chosen:
                    mode.selection_meter = min(mode.selection_meter + 2, 100)
                else:
                    pygame.mixer.stop()
                    mode.selection_meter = max(mode.selection_meter - 6, 0)

                if mode.selection_meter >= 100:
                    sound_fx[0].play()
                    game_phase = "game_play"
                    table_img = game_interface.set_table_image(TABLE_IMAGES[1])

            if not selection_music_playing:
                selection_music_playing = True
                pygame.mixer.music.stop()
                songs.play(pygame.mixer.music.load(SONGS[0]),-1)

            game_interface.display_table_image(screen, table_img)
            game_interface.display_options(screen, font, tape_img, modes)

        elif game_phase == "game_play":

            current_cups = [[], []]

            game_algorithms.get_current_cups(table, template, current_cups)
            game_algorithms.update_cups(current_cups, cups)
            game_algorithms.check_for_objects(table, cups)

            if len(cups[0]) == len(cups[1]) == 0 and (game_algorithms.Player.game_score[0] > 0 or game_algorithms.Player.game_score[1] > 0):
                game_phase = "game_over"
                table_img = game_interface.set_table_image(TABLE_IMAGES[2])

            # region Cup selection

            for side in cups:
                for cup in side:
                    if cup.has_wand:
                        cup.selection_meter = min(cup.selection_meter + 1, 100)
                    else:
                        cup.selection_meter = max(cup.selection_meter - 10, 0)

                    if not cup.is_yellow and cup.selection_meter >= 100 and not jingle.get_busy():
                        jingle.play(sound_fx[3])
                        cup.is_yellow = True

                        min_distance = 1
                        closest_cup_index = -1
                        for i in range(0, len(side)):
                            if cup is not side[i]:
                                distance = abs(cup.center[0] - side[i].center[0]) + abs(cup.center[1] - side[i].center[1])
                                if distance < min_distance:
                                    min_distance = distance
                                    closest_cup_index = i
                        if closest_cup_index > -1:
                            side[closest_cup_index].is_red = True

                    if cup.is_yellow:
                        cup.selected_time -= 1
                        if cup.selected_time <= 0:
                            cup.is_yellow = False
                            cup.selected_time = cup.max_selected_time

            # endregion

            # region Score checking

            for i in range(0, len(teams)):
                for cup in cups[i]:
                    for j in range(0, len(cup.has_balls)):
                        current_team = teams[i]
                        opposite_team = teams[len(teams) - i - 1]

                        if cup.has_balls[j] and not current_team[j].hit:
                            if not pygame.mixer.find_channel(speak).get_busy():
                                pygame.mixer.music.pause()
                                speak.play(speak_fx[random.randrange(2, len(SPEAK))])
                                if pygame.mixer.find_channel(speak).get_busy():
                                    pygame.mixer.music.unpause()

                            current_team[j].score += 1
                            game_algorithms.Player.game_score[i] += 1
                            current_team[j].hit = True

                        elif current_team[j].hit and not cup.has_balls[j]:
                            for k in range(0, len(opposite_team)):
                                if opposite_team[k].drinks:
                                    opposite_team[k].drinks = False
                                    opposite_team[k + 1 if k + 1 < len(opposite_team) else 0].drinks = True
                                    break

            # endregion

            if not gameplay_music_playing:
                gameplay_music_playing = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load(SONGS[1])
                pygame.mixer.music.play(-1)

            game_interface.display_table_image(screen, table_img)
            game_interface.display_score(screen, font, teams)
            game_interface.display_cups(screen, cups)

        elif game_phase == "game_over":

            game_algorithms.choose_option(table, [play_again_button])

            if play_again_button.chosen:
                play_again_button.selection_meter = min(play_again_button.selection_meter + 2, 100)
            else:
                play_again_button.selection_meter = max(play_again_button.selection_meter - 6, 0)

            if play_again_button.selection_meter >= 100:
                sound_fx[0].play()
                game_phase = "mode_selection"
                table_img = game_interface.set_table_image(TABLE_IMAGES[0])
                game_algorithms.Player.game_score = [0, 0]
                for side in teams:
                    for player in side:
                        player.score = 0

                for mode in modes:
                    mode.selection_meter = 0

            game_interface.display_table_image(screen, table_img)
            game_interface.game_over(screen, teams, font, font)
            game_interface.display_options(screen, font, tape_img, [play_again_button])

            if team_a_won:
                if not pygame.mixer.get_busy():
                    speak.play(speak_fx[0], 0)
            else:
                if not pygame.mixer.get_busy():
                    speak.play(speak_fx[1], 0)

        # KEYBOARD INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app_running = False
                if event.key == pygame.K_SPACE:
                    random_cup = True

        pygame.display.update()

    cap.release()
    cv2.destroyAllWindows()


# TODO better cup detection - make template matching not care about the middle part of the circle
# TODO better object detection - either Malte's method, or at least less naive color thresholding than "one pixel -> it's a ball!"
