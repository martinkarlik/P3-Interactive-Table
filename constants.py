# just some data Id rather not yeet if we need to use it

beers_centers_10_left = [[20, 21], [70, 18], [118, 15], [170, 12], [43, 64], [93, 61], [142, 56], [67, 107],
                              [118, 102], [92, 147]]

beers_centers_10_right = [[11, 144], [60, 148], [109, 150], [158, 150], [33, 101], [84, 107], [133, 107], [64, 61],
                          [113, 62], [91, 21]]

green_color = (120, 0.7, 0.5)
red_color = (350, 0.9, 0.5)
color_offset = (10, 0.3, 0.5)

beer_color = (50, 0.6, 0.6)

green_display_color = 7, 129, 30
red_display_color = 242, 81, 87
white_display_color = 255, 255, 255



# TODO doesn't work, fix
# def getImgKernel(x, y):
#     imgKernel = np.array([
#         [x - 1, y - 1, x, y - 1, x + 1, y - 1],
#         [x - 1, y, x, y, x + 1, y],
#         [x - 1, y + 1, x, y + 1, x + 1, y + 1]])
#     return imgKernel

# def matchTemplateSelf(source, template):
#     tempImg = np.copy(source)
#     templateArray = [[]]
#     templateBlue = template[:, :, 0]
#     templateGreen = template[:, :, 1]
#     templateRed = template[:, :, 2]
#
#     height = template.shape[1]
#     width = template.shape[0]
#     for x in range(0, width):
#         for y in range(0, height):
#             templateArray = x, y
#
#     for x in range(0, source.shape[0]):
#         for y in range(0, source.shape[1]):
#             sourceBlueKernel = getImgKernel(x, y)
#             sourceGreenKernel = getImgKernel(x, y)
#             sourceRedKernel = getImgKernel(x, y)
#
#             corrBlue = signal.correlate2d(sourceBlueKernel, templateBlue, boundary='symm', mode='same')
#             corrGreen = signal.correlate2d(sourceGreenKernel, templateGreen, boundary='symm', mode='same')
#             corrRed = signal.correlate2d(sourceRedKernel, templateRed, boundary='symm', mode='same')
#             i, j = np.unravel_index(np.argmax(corrBlue), corrBlue.shape)
#             tempImg = corrBlue
#
#     return tempImg

# for beer in beers_left:
#     if beer.red_ball and not left_drinks:
#         left_drinks = True
#         drink_color_left = turn_to_drink_right()
#         players_scores[0] += 1
#     elif beer.green_ball and left_drinks:
#         left_drinks = True
#         drink_color_left = turn_to_drink_right()
#         players_scores[1] += 1
#     else:
#         left_drinks = False
#         drink_color_left = constants.white_display_color
#     pygame.draw.circle(screen, drink_color_left,
#                        (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 20)
#
# for beer in beers_right:
#     if beer.red_ball and not right_drinks:
#         right_drinks = True
#         drink_color_right = turn_to_drink_right()
#         players_scores[2] += 1
#     elif beer.green_ball and right_drinks:
#         right_drinks = True
#         drink_color_right = turn_to_drink_right()
#         players_scores[3] += 1
#     else:
#         right_drinks = False
#         drink_color_right = constants.white_display_color
#     pygame.draw.circle(screen, drink_color_right,
#                        (int(beer.center[1] * DISPLAY_WIDTH), int(beer.center[0] * DISPLAY_HEIGHT)), 20)

golden_jingle = 'sound/hit_the_golden_cup_jingle.mp3'
sudden_death_jingle = 'sound/sudden_death_jingle.mp3'
