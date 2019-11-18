import pygame
import cv2
import algorithms

table_img = ""


def display_text(player_name, score, player):
    if player == 1:
        score = font.render(str(player_name) + ": " + str(score), True, (242, 81, 87))
        return score
    if player == 2:
        score = font.render(str(player_name) + ": " + str(score), True, (7, 129, 30))
        return score


def change_table_img(path):
    global table_img
    table_img = path


def display_table_img():
    global table_img
    screen.blit(pygame.image.load(table_img), (0, 0))


if __name__ == '__main__':

    # cap = cv2.VideoCapture("recordings/test2_gameplay2.mp4")
    cap = cv2.VideoCapture(0)
    beer_template_left = cv2.imread("images/testImages/templates/beer_reg_left.jpg")
    beer_template_right = cv2.imread("images/testImages/templates/beer_reg_right.jpg")

    pygame.init()

    DISPLAY_WIDTH = 1920
    DISPLAY_HEIGHT = 1080

    # Create the screen
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)

    # Setup the frame
    pygame.display.set_caption("BeerPong")
    icon = pygame.image.load("images/cheers.png")
    pygame.display.set_icon(icon)

    # change_table_img(("images/tableImages/GameStarted.png"))
    circle_white = pygame.image.load("images/tableImages/circle_white.png")

    # Setup general things
    font = pygame.font.Font('freesansbold.ttf', 30)

    # player variables
    players = ['Joe', 'Jim', 'Caren', 'Ginger']
    players_scores = [0, 0, 0, 0]

    _, frame = cap.read()
    cropped_dimensions = algorithms.find_crop(frame)

    # cropped_dimensions = [0, frame.shape[0], 0, frame.shape[1]]

    app_running = True
    while app_running and cap.isOpened():
        _, frame = cap.read()

        table_roi = frame[cropped_dimensions[0]:cropped_dimensions[1], cropped_dimensions[2]:cropped_dimensions[3]]
        cv2.imshow("table", table_roi)

        beer_area_left = table_roi[0:table_roi.shape[0], 0:int(table_roi.shape[1] * 0.4)]
        beers_left = algorithms.extract_beers(algorithms.LEFT, beer_area_left, [beer_template_left])

        beer_area_right = table_roi[0:table_roi.shape[0], int(table_roi.shape[1] * 0.6):table_roi.shape[1]]
        beers_right = algorithms.extract_beers(algorithms.RIGHT, beer_area_right, [beer_template_right])

        # algorithms.checkForBalls(beers_left, beers_right, color, table_roi)
        # turns = algorithms.detectTurns()

        # The exit conditions, both pressing x and esc works so far
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app_running = False

        screen.fill(0)

        if not players:
            change_table_img("images/tableImages/PlaceCups.png")

        elif beers_left != 10 and beers_right != 10:
            change_table_img("images/tableImages/GameStarted.png")

        # displays that current path to the image, change image with change_table_img()
        display_table_img()

        # Display the player score and names
        if players:
            screen.blit(pygame.transform.rotate(display_text(players[0], players_scores[0], 1), -90), (92, 160))
            screen.blit(pygame.transform.rotate(display_text(players[1], players_scores[1], 2), -90), (92, 870))
            screen.blit(pygame.transform.rotate(display_text(players[2], players_scores[2], 1), 90), (1725, 160))
            screen.blit(pygame.transform.rotate(display_text(players[3], players_scores[3], 2), 90), (1725, 870))

        for beer in beers_left:
            pygame.draw.circle(screen, (255, 255, 255), (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 40)

        for beer in beers_right:
            pygame.draw.circle(screen, (255, 255, 255), (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 40)

        pygame.display.update()

        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
