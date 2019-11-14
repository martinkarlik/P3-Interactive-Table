import pygame

if __name__ == '__main__':

    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    # Setup the frame
    pygame.display.set_caption("BeerPong")
    icon = pygame.image.load("images/cheers.png")
    pygame.display.set_icon(icon)

    tableimg1 = pygame.image.load("images/tableImages/PlaceCups.png")
    circle_white = pygame.image.load("images//tableImages/circle_white.png")


    def showTable(image, x, y):
        screen.blit(image, (x, y))


    def addCircle(x, y, identifier):
        screen.blit(circle_white, (x, y))


    app_running = True
    while app_running:
        # Background
        screen.fill((0, 0, 0))
        showTable(tableimg1, 0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app_running = False

        # call this to display the circles
        # for beer in beerArray:
        #     addCircle(1920/2, 1080/2, 1)

    pygame.display.update()