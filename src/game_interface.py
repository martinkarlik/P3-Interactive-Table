import pygame
DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540
FONT_SANS_BOLD = 'freesansbold.ttf'
TABLE_IMG1 = "../images/tableImages/choose_game_mode.png"
GREEN_DISPLAY_COLOR = 7, 129, 30
RED_DISPLAY_COLOR = 242, 81, 87
WHITE_DISPLAY_COLOR = 255, 255, 255
PLAYERS_POS = [[0.1, 0.1], [0.9, 0.9]]
class Player:
    def __init__(self):
        pass
class Mode:
    def __init__(self, title, pos):
        self.title = title
        self.pos = pos
        self.meter = 40
        self.chosen = False
def display_text(font, score, player):
    if player == 1:
        score = font.render(str(score), True, RED_DISPLAY_COLOR)
        return score
    if player == 2:
        score = font.render(str(score), True, GREEN_DISPLAY_COLOR)
        return score
# the function that is responsible for changing the table image
def set_table_img(path):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
# The function that shows the current table image
def display_table_img(target, img):
    target.blit(img, (0, 0))
def display_mode_selection(target, font, modes):
    for i in range(0, len(modes)):
        x = int(modes[i].pos[2] * DISPLAY_WIDTH)
        y = int(modes[i].pos[0] * DISPLAY_HEIGHT)
        w = int(modes[i].pos[3] * DISPLAY_WIDTH) - int(modes[i].pos[2] * DISPLAY_WIDTH)
        h = int(modes[i].pos[1] * DISPLAY_HEIGHT) - int(modes[i].pos[0] * DISPLAY_HEIGHT)
        pygame.draw.rect(target, (50, 50, 50), (x, y, w, h), 3)
        text = modes[i].title
        i = 0
        fire_len = int(modes[i].meter / 100 * (2*w + 2*h))
        while fire_len > 0:
            start_x = x if i < 2 else x + w
            start_y = y if i == 0 or i == 3 else y + h
            end_x = x if i == 0 or i == 3 else x + w
            end_y = y if i > 2 else y + h
            fire_x = start_x + min(fire_len, end_x - start_x) if i < 2 else start_x - min(fire_len, end_x - start_x)
            fire_y = start_y + min(fire_len, end_y - start_y) if i < 2 else start_y - min(fire_len, end_y - start_y)
            pygame.draw.line(target, (255, 255, 255), (start_x, start_y), (fire_x, fire_y), 3)
            fire_len = fire_len - h if i % 2 == 0 else fire_len - w
            i += 1
def display_score(target, scores):
    for i in range(0, len(scores)):
        x = int(scores[i][1] * DISPLAY_WIDTH)
        y = int(scores[i][0] * DISPLAY_HEIGHT)
        target.blit(pygame.transform.rotate(display_text(scores[i], i % 2), -90), (x, y))
    # target.blit(pygame.transform.rotate(display_text(int(scores[1]), 2), -90),
    #             (92 / 1920 * DISPLAY_WIDTH, 870 / 1080 * DISPLAY_HEIGHT))
    # target.blit(pygame.transform.rotate(display_text(int(scores[2]), 1), 90),
    #             (1725 / 1920 * DISPLAY_WIDTH, 160 / 1080 * DISPLAY_HEIGHT))
    # target.blit(pygame.transform.rotate(display_text(int(scores[3]), 2), 90),
    #             (1725 / 1920 * DISPLAY_WIDTH, 870 / 1080 * DISPLAY_HEIGHT))
def display_beers(target, beers_left, beers_right):
    return
def play_audio(audio):
    pygame.mixer.music.load(audio)
    pygame.mixer.music.queue(audio)
    pygame.mixer.music.play()