from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass

# beer_frame = cv2.imread("images/test2_nonhighlighted.png")

class ThirdScreen(Screen):
    pass

cv2.imshow("green ball", green_ball)

class FourthScreen(Screen):
    pass

# beer = beer_frame[200:240, 100:140]
# cv2.imshow("beer", beer)
# cv2.imwrite("images/beer_reg_left.jpg", beer)

class MyScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        Clock.schedule_once(self.screen_switch_one, 2)

    def screen_switch_one(self, dt):
        self.current = '_first_screen_'
        Clock.schedule_once(self.screen_switch_two, 2)

    def screen_switch_two(self, dt):
        self.current = '_second_screen_'
        self.ids.first_screen.ids.first_screen_label.text = "Hi I'm The Fifth Screen"
        Clock.schedule_once(self.screen_switch_three, 2)

    def screen_switch_three(self, dt):
        self.current = '_third_screen_'
        Clock.schedule_once(self.screen_switch_four, 2)

    def screen_switch_four(self, dt):
        self.current = '_fourth_screen_'
        Clock.schedule_once(self.screen_switch_one, 2)


class GIApp(App):

    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    GIApp().run()
