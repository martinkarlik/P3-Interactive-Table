import pygame

DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540


GREEN_DISPLAY_COLOR = 7, 129, 30
RED_DISPLAY_COLOR = 242, 81, 87
BLUE_DISPLAY_COLOR = 50, 50, 200
WHITE_DISPLAY_COLOR = 255, 255, 255


class Button:
    def __init__(self, title, pos, working):
        self.title = title
        self.pos = pos
        self.selection_meter = 0
        self.chosen = False
        self.working = working


def display_text(font, score, player):
    if player == 1:
        score = font.render(str(score), True, RED_DISPLAY_COLOR)
        return score
    if player == 2:
        score = font.render(str(score), True, GREEN_DISPLAY_COLOR)
        return score


# The function that is responsible for changing the table image
def set_table_image(path):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))


# The function that shows the current table image
def display_table_image(target, img):
    target.blit(img, (0, 0))


def display_options(target, font, tape, options):
    for i in range(0, len(options)):
        x = int(options[i].pos[2] * DISPLAY_WIDTH)
        y = int(options[i].pos[0] * DISPLAY_HEIGHT)
        w = int(options[i].pos[3] * DISPLAY_WIDTH) - int(options[i].pos[2] * DISPLAY_WIDTH)
        h = int(options[i].pos[1] * DISPLAY_HEIGHT) - int(options[i].pos[0] * DISPLAY_HEIGHT)

        pygame.draw.rect(target, (50, 50, 50), (x, y, w, h), 5)

        text = font.render(options[i].title, True, WHITE_DISPLAY_COLOR)
        text_rect = text.get_rect(center=(x + w / 2, y + h / 2))
        target.blit(text, text_rect)

        if options[i].working:
            fire_len = int(options[i].selection_meter / 100 * (2 * w + 2 * h))
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


def display_score(target, font, teams):

    for i in range(0, len(teams)):
        for j in range(0, len(teams[i])):
            text = font.render(str(teams[i][j].score), True, teams[i][j].color)
            text_rect = text.get_rect(center=(0.05 * DISPLAY_WIDTH + i * 0.9 * DISPLAY_WIDTH, 0.05 * DISPLAY_HEIGHT + j * 0.9 * DISPLAY_HEIGHT))
            target.blit(pygame.transform.rotate(text, -90 + 180 * i), text_rect)


def display_cups(target, cups):

    for side in cups:
        for cup in side:

            x = int(cup.center[1] * DISPLAY_WIDTH)
            y = int(cup.center[0] * DISPLAY_HEIGHT)

            if any(cup.has_balls):
                pygame.draw.circle(target, (25 * cup.has_balls[0], 25 * cup.has_balls[1], 0), (x, y), 30)

            elif cup.is_yellow:
                pygame.draw.circle(target, (255, 223, 0), (x, y), 30)

            elif cup.is_red:
                pygame.draw.circle(target, (255, 0, 0), (x, y), 30)

            elif cup.selection_meter > 0:
                if cup.selection_meter >= 100:
                    if cup.selection_meter in range(100, 105) or cup.selection_meter in range(110, 115):
                        pygame.draw.circle(target, (255, 255, 255), (x, y), 50, 10)
                    else:
                        pygame.draw.circle(target, (255, 200, 0), (x, y), 30)
                else:
                    pygame.draw.arc(target, (255, 255, 0), (x-15, y-15, 30, 30), 0.0, (cup.selection_meter / 20) * 6.283, 3)

            else:
                pygame.draw.circle(target, (255, 255, 255), (x, y), 30)


def game_over(target, teams, font, font2):

    team_a = teams[0]
    team_b = teams[1]

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
        text = font2.render("TEAM 1 WON!", True, WHITE_DISPLAY_COLOR)
        text_rect = text.get_rect(center=(DISPLAY_WIDTH*4/7, DISPLAY_HEIGHT/8))
        target.blit(text, text_rect)
    elif teamScoreB > teamScoreA:
        text = font2.render("TEAM 2 WON!", True, WHITE_DISPLAY_COLOR)
        text_rect = text.get_rect(center=(DISPLAY_WIDTH*4/7, DISPLAY_HEIGHT/8))
        target.blit(text, text_rect)



# # Display text Gold cup text: for when the left side has highlighted a cup in the right side. So
#                         # a cup on the right is highlighted
#                         golden_cup_txt = font.render('Golden Cup active', True, (255, 255, 0))
#                         rotated_text = pygame.transform.rotate(golden_cup_txt, 90)
#                         screen.blit(rotated_text, rotated_text.get_rect(center=((game_interface.DISPLAY_WIDTH / 2) + 50,
#                                                                                 game_interface.DISPLAY_HEIGHT / 2)))