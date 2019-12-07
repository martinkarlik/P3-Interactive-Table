import pygame

DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540

FONT_MYRIAD_PRO_REGULAR = ['../fonts/MyriadProRegular.ttf', 60]
FONT_MYRIAD_PRO_REGULAR2 = ['../fonts/MyriadProRegular.ttf', 97]
#FONT_SANS_BOLD = ['freesansbold.ttf', 40]
TABLE_IMG1 = "../images/tableImages/choose_game_mode.png"
TABLE_IMG2 = "../images/tableImages/PlaceCups.png"
TABLE_IMG3 = "../images/tableImages/gameover_screen.png"
TABLE_IMG4 = "../images/tableImages/digital_design.jpg"


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


def gamebutton (target, font, gameoverbutton):
    for i in range(0, len(gameoverbutton)):
        w = int(gameoverbutton[i].pos[3] * DISPLAY_WIDTH) - int(gameoverbutton[i].pos[2] * DISPLAY_WIDTH)
        h = int(gameoverbutton[i].pos[1] * DISPLAY_HEIGHT) - int(gameoverbutton[i].pos[0] * DISPLAY_HEIGHT)
        x = int(DISPLAY_WIDTH/2 - w/2)
        y = int(DISPLAY_HEIGHT*3/4)
        pygame.draw.rect(target, (50, 50, 50), (x, y, w, h), 5)

        text = font.render(gameoverbutton[i].title, True, WHITE_DISPLAY_COLOR)
        text_rect = text.get_rect(center=(DISPLAY_WIDTH/2, DISPLAY_HEIGHT*6/7))
        target.blit(text, text_rect)

        fire_len = int(gameoverbutton[i].meter / 100 * (2 * w + 2 * h))
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


def display_score(target, font, team_a, team_b):

    for player in team_a:
        print("team a", player.score)

    for player in team_b:
        print("team b", player.score)

    # for player in team_a:
    #     text = font.render(player.score, True, player.color)
    #     text_rect = text.get_rect(center=(0.1 * DISPLAY_WIDTH, 0.1 * DISPLAY_HEIGHT))
    #     target.blit(text, text_rect)
    #
    #     # target.blit(pygame.transform.rotate(display_text(scores[i], i % 2), -90, (x, y))
    #
    # for player in team_b:
    #     text = font.render(player.score, True, player.color)
    #     text_rect = text.get_rect(center=(0.1 * DISPLAY_WIDTH, 0.1 * DISPLAY_HEIGHT))
    #     target.blit(text, text_rect)


def display_beers(target, beers_left, beers_right):

    for beer in beers_left:

        if beer.balls[0] or beer.balls[1]:
            pygame.draw.circle(target, (255 * int(beer.balls[0]), 255 * int(beer.balls[1]), 50),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        elif beer.yellow:
            pygame.draw.circle(target, (238, 232, 170),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        elif beer.red:
            pygame.draw.circle(target, (255, 0, 0,),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        else:
            pygame.draw.circle(target, (255, 255, 255),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)

    for beer in beers_right:

        if beer.balls[0] or beer.balls[1]:
            pygame.draw.circle(target, (255 * int(beer.balls[0]), 255 * int(beer.balls[1]), 50),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        elif beer.yellow:
            pygame.draw.circle(target, (238, 232, 170),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        elif beer.red:
            pygame.draw.circle(target, (255, 0, 0,),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)
        else:
            pygame.draw.circle(target, (255, 255, 255),
                               (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 30)

def team_win_one(team_a,team_b):
    scorea =  team_a[0].score + team_a[1].score
    scoreb = team_b[0].score + team_b[1].score
    if scorea> scoreb:
        return True


def game_over(target, team_a, team_b, font2, font):
    team1 = ("1", (0.3, 0.5, 0.1, 0.4))
    team2 = ("2", (0.3, 0.5, 0.1, 0.4))

    scoreA1 = str(team_a[0].score)
    scoreA2 = str(team_a[1].score)
    scoreB1 = str(team_b[0].score)
    scoreB2 = str(team_b[1].score)



    textA1 = font.render(scoreA1, True, WHITE_DISPLAY_COLOR)
    text_rectA1 = textA1.get_rect(center=(DISPLAY_WIDTH/15, DISPLAY_HEIGHT/6))
    target.blit(pygame.transform.rotate(textA1, -90), text_rectA1)


    textA2 = font.render(scoreA2, True, WHITE_DISPLAY_COLOR)
    text_rectA2 = textA2.get_rect(center=(DISPLAY_WIDTH/15, DISPLAY_HEIGHT*5.2/5.5))
    target.blit(pygame.transform.rotate(textA2, -90), text_rectA2)

    textB1 = font.render(scoreB1, True, WHITE_DISPLAY_COLOR)
    text_rectB1 = textB1.get_rect(center=(DISPLAY_WIDTH*13.65/15, DISPLAY_HEIGHT/12))
    target.blit(pygame.transform.rotate(textB1, 90), text_rectB1)

    textB2 = font.render(scoreB2, True, WHITE_DISPLAY_COLOR)
    text_rectB2 = textB2.get_rect(center=(DISPLAY_WIDTH*13.65/15, DISPLAY_HEIGHT*10.2/12))
    target.blit(pygame.transform.rotate(textB2, 90), text_rectB2)

    teamScoreA = team_a[0].score + team_a[1].score
    teamScoreB = team_b[0].score + team_b[1].score

    if teamScoreA > teamScoreB:
        text = font2.render("1", True, WHITE_DISPLAY_COLOR)
        text_rect = text.get_rect(center=(DISPLAY_WIDTH*4/7, DISPLAY_HEIGHT/8))
        target.blit(text, text_rect)
    elif teamScoreB > teamScoreA:
        text = font2.render("2", True, WHITE_DISPLAY_COLOR)
        text_rect = text.get_rect(center=(DISPLAY_WIDTH*4/7, DISPLAY_HEIGHT/8))
        target.blit(text, text_rect)
