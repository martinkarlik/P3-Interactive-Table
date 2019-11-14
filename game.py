import pygame
import cv2
import algorithms

if __name__ == '__main__':

    cap = cv2.VideoCapture("recordings/dark.avi")
    beer_template_left = cv2.imread("images/beer_reg_left.jpg")
    beer_template_right = cv2.imread("images/beer_reg_right.jpg")

    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode((640, 480))

    # Setup the frame
    pygame.display.set_caption("BeerPong")
    icon = pygame.image.load("images/tableImages/cheers.png")
    pygame.display.set_icon(icon)

    tableimg1 = pygame.image.load("images/tableImages/PlaceCups.png")
    circle_white = pygame.image.load("images/tableImages/circle_white.png")

    app_running = True
    while cap.isOpened():

        _, frame = cap.read()

        beer_area_left = frame[130:350, 0:220]
        templates = [beer_template_left]
        beers_left = algorithms.extractBeers(beer_area_left, templates)

        beer_area_right = frame[130:350, 420:640]
        templates = [beer_template_right]
        beers_right = algorithms.extractBeers(beer_area_right, templates)

        screen.fill(0)

        # The exit conditions, both pressing x and esc works so far
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app_running = False

        pygame.draw.circle(screen, (255, 255, 255), (50, 50), 20)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
