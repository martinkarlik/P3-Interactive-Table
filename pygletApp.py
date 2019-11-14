import cv2
import pyglet
import beer
from pyglet.window import key
from pyglet.gl import *
import algorithms

pyglet.options['audio'] = ('directsound', 'openal', 'pulse', 'silent')
display = pyglet.canvas.get_display()
screens = display.get_screens()
window = (pyglet.window.Window(width=1920, height=1080, fullscreen=True, screen=screens[1], caption="Beer pong"))
window2 = (
    pyglet.window.Window(width=1, height=1, fullscreen=False, screen=screens[0], caption="Image pro", visible=False))
circle_white = pyglet.image.load('images/tableImages/circle_white.png')
names = ["Joe", "Jim", "Janis", "Jay-z"]

# used to control the screens displayed
screen = 1


def create_label(text, x, y, player):
    # red player
    if player == 1:
        return pyglet.text.Label(text + ": 0",
                                 font_name='Times New Roman',
                                 font_size=30,
                                 x=x, y=y,
                                 anchor_x='center',
                                 anchor_y='center',
                                 color=(242, 81, 87, 255))
    # green player
    if player == 2:
        return pyglet.text.Label(text + ": 0",
                                 font_name='Times New Roman',
                                 font_size=30,
                                 x=x, y=y,
                                 anchor_x='center',
                                 anchor_y='center',
                                 color=(7, 129, 30, 255))


def place_circle(posX, posY):
    circle_white.blit(posX - circle_white.width // 2, posY - circle_white.width // 2)


def first_screen(table_img):
    window.clear()
    table_img.blit(0, 0)


def second_screen(table_img, namesArr):
    window.clear()
    table_img.blit(0, 0)

    # Rotate and make the first two names
    glLoadIdentity()
    glTranslatef(window.width // 2, window.height // 2, 0.0)
    glRotatef(-90.0, 0.0, 0.0, 1.0)
    create_label(namesArr[0], -window.height / 2 + 150, -window.width / 2 + 150, 1).draw()
    create_label(namesArr[1], window.height / 2 - 150, -window.width / 2 + 150, 2).draw()

    # Rotate and make the last two names
    glLoadIdentity()
    glTranslatef(window.width // 2, window.height // 2, 0.0)
    glRotatef(90.0, 0.0, 0.0, 1.0)
    create_label(namesArr[2], -window.height / 2 + 150, -window.width / 2 + 150, 1).draw()
    create_label(namesArr[3], window.height / 2 - 150, -window.width / 2 + 150, 2).draw()

    glLoadIdentity()


@window.event
def on_key_pressed(symbol, modifiers):
    if symbol == key.ESCAPE:
        pyglet.app.exit()



# Main draw window for displaying the UI
@window.event
def on_draw():
    # beer_area_left = frame[130:350, 0:220]
    # templates = [beer_template_left]
    # beers_left = algorithms.extractBeers(beer_area_left, templates)
    #
    # beer_area_right = frame[130:350, 420:640]
    # templates = [beer_template_right]
    # beers_right = algorithms.extractBeers(beer_area_right, templates)

    if screen == 1:
        first_screen(pyglet.image.load('images/tableImages/PlaceCups.png'))
        # how to display the circle
        # circle_white.blit(window.width // 2 - circle_white.width // 2, window.height // 2 - circle_white.width // 2)
    elif screen == 2:
        second_screen(pyglet.image.load('images/tableImages/GameTemplate.png'), names)
    else:
        window.clear()
        label = pyglet.text.Label('Error, no screen like that',
                                  font_name='Castellar',
                                  font_size=70,
                                  x=window.width // 2, y=window.height // 2,
                                  anchor_x='center', anchor_y='center',
                                  color=(255, 255, 0, 255))
        label.draw()

    # TODO find a way to make this function call work
    # for beer in beers_left:
    #     place_circle(beer.center[0], beer.center[1])
    # for beer in beers_right:
    #     place_circle(beer.center[0], beer.center[1])


# draw window for displaying the cv2 video
@window2.event
def on_draw():
    while cap.isOpened():
        _, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(50) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    # beer_template_left = cv2.imread("images/beer_reg_left.jpg")
    # beer_template_right = cv2.imread("images/beer_reg_right.jpg")

    pyglet.app.run()
