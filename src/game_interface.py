import pygame

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080


GREEN_DISPLAY_COLOR = 7, 129, 30
RED_DISPLAY_COLOR = 242, 81, 87
BLUE_DISPLAY_COLOR = 50, 50, 200
WHITE_DISPLAY_COLOR = 255, 255, 255




class Player:
    # static fields... python is weird about it, you don't have to declare anything, it's just static
    # "static" = variable same for every object of this class, "field" = instance variable

    team_colors = [RED_DISPLAY_COLOR, GREEN_DISPLAY_COLOR, BLUE_DISPLAY_COLOR]
    team_names = ["Red", "Green", "Blue"]
    players_num = 2

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 0
        self.drinks = False
        self.hit = False


class Button:
    def __init__(self, title, pos, working):
        self.title = title
        self.pos = pos
        self.meter = 0
        self.chosen = False
        self.working = working



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


def display_mode_selection(target, font, tape, modes):
    for i in range(0, len(modes)):
        x = int(modes[i].pos[2] * DISPLAY_WIDTH)
        y = int(modes[i].pos[0] * DISPLAY_HEIGHT)
        w = int(modes[i].pos[3] * DISPLAY_WIDTH) - int(modes[i].pos[2] * DISPLAY_WIDTH)
        h = int(modes[i].pos[1] * DISPLAY_HEIGHT) - int(modes[i].pos[0] * DISPLAY_HEIGHT)

        pygame.draw.rect(target, (50, 50, 50), (x, y, w, h), 5)

        text = font.render(modes[i].title, True, WHITE_DISPLAY_COLOR)
        text_rect = text.get_rect(center=(x + w / 2, y + h / 2))
        target.blit(text, text_rect)

        if modes[i].working:
            fire_len = int(modes[i].meter / 100 * (2 * w + 2 * h))
            line_num = 0

            while fire_len > 0:
                start_x = x if line_num < 2 else x + w
                start_y = y if line_num == 0 or line_num == 3 else y + h
                end_x = x if line_num == 0 or line_num == 3 else x + w
                end_y = y if line_num >= 2 else y + h

                fire_end_x = start_x + min(fire_len, abs(end_x - start_x)) if line_num < 2 else start_x - min(fire_len, abs(
                    end_x - start_x))
                fire_end_y = start_y + min(fire_len, abs(end_y - start_y)) if line_num < 2 else start_y - min(fire_len, abs(
                    end_y - start_y))

                pygame.draw.line(target, (255, 255, 255), (start_x, start_y), (fire_end_x, fire_end_y), 5)

                fire_len = fire_len - h if line_num % 2 == 0 else fire_len - w
                line_num += 1
        else:
            tape = pygame.transform.scale(tape, (int(0.3 * DISPLAY_WIDTH), int(0.2 * DISPLAY_HEIGHT)))
            target.blit(tape, (x, y))



def display_score(target, team_a, team_b):
    return
    # for i in range(0, len(scores)):
    #     x = int(scores[i][1] * DISPLAY_WIDTH)
    #     y = int(scores[i][0] * DISPLAY_HEIGHT)
    #     target.blit(pygame.transform.rotate(display_text(scores[i], i % 2), -90), (x, y))


def display_beers(target, beers_left, beers_right):

    for beer in beers_left:
        if beer.balls[0] or beer.balls[1]:
            pygame.draw.circle(target, (255 * int(beer.balls[0]), 255 * int(beer.balls[1]), 0),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        elif beer.yellow:
            pygame.draw.circle(target, (0, 255, 255,),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        elif beer.red:
            pygame.draw.circle(target, (255, 0, 0,),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        else:
            pygame.draw.circle(target, (255, 255, 255),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)

    for beer in beers_right:
        if beer.balls[0] or beer.balls[1]:
            pygame.draw.circle(target, (255 * int(beer.balls[0]), 255 * int(beer.balls[1]), 0),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        elif beer.yellow:
            pygame.draw.circle(target, (0, 255, 255,),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        elif beer.red:
            pygame.draw.circle(target, (255, 0, 0,),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        else:
            pygame.draw.circle(target, (255, 255, 255),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
