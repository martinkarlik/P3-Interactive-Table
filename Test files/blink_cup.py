import pygame
import cv2

pygame.init()
pygame.display.set_caption("BeerPong")
screen = pygame.display.set_mode((960, 540))


def show_circle(frame_count):
    if frame_count >= 150:
        pygame.draw.circle(screen, (255, 255, 0), (100, 100), 50)
        if frame_count in range(150, 155) or frame_count in range(160, 165):
            pygame.draw.circle(screen, (255, 255, 255), (100, 100), 60, 10)

    else:
        pygame.draw.circle(screen, (255, 255, 0), (100, 100), round(frame_count/2.6))


frame_count = 0
app_running = True
while app_running:
    frame_count += 1
    print(frame_count)
    screen.fill(50)
    show_circle(frame_count)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app_running = False
    pygame.display.update()
    pygame.time.delay(20)
