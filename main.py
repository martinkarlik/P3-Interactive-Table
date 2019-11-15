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

    cap = cv2.VideoCapture("recordings/black1.avi")
    beer_template_left = cv2.imread("images/testImages/templates/beer_reg_left.jpg")
    beer_template_right = cv2.imread("images/testImages/templates/beer_reg_right.jpg")

    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode((1280, 720))  # just so that the whole screen isnt covered every time its run

    # Setup the frame
    pygame.display.set_caption("BeerPong")
    icon = pygame.image.load("images/cheers.png")
    pygame.display.set_icon(icon)

    # change_table_img(("images/tableImages/GameStarted.png"))
    circle_white = pygame.image.load("images//tableImages/circle_white.png")

    # Setup general things
    font = pygame.font.Font('freesansbold.ttf', 30)

    # player variables
    players = ['Joe', 'Jim', 'Caren', 'Ginger']
    playersScore = [0, 0, 0, 0]

    app_running = True

    # cropped_dimensions = algorithms.findCrop()

    while app_running and cap.isOpened():
        _, frame = cap.read()

        beer_area_left = frame[130:350, 0:220]
        templates = [beer_template_left]
        beers_left = algorithms.extractBeers(beer_area_left, templates)

        beer_area_right = frame[130:350, 420:640]
        templates = [beer_template_right]
        beers_right = algorithms.extractBeers(beer_area_right, templates)

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
            screen.blit(pygame.transform.rotate(display_text(players[0], playersScore[0], 1), -90), (92, 160))
            screen.blit(pygame.transform.rotate(display_text(players[1], playersScore[1], 2), -90), (92, 870))
            screen.blit(pygame.transform.rotate(display_text(players[2], playersScore[2], 1), 90), (1725, 160))
            screen.blit(pygame.transform.rotate(display_text(players[3], playersScore[3], 2), 90), (1725, 870))


        for beer in beers_left:
            pygame.draw.circle(screen, (255, 255, 255), (int(beer.center[1] * 1270/640), int((beer.center[0] + 130) * 680/480)), 40)

        for beer in beers_right:
            pass
            pygame.draw.circle(screen, (255, 255, 255), (int((beer.center[1] + 420) * 1270/640), int((beer.center[0] + 130) * 680/480)), 40)

        pygame.display.update()

    cap.release()
    cv2.destroyAllWindows()
