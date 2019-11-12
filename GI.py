from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source='images/tableImages/PlaceCups.png'))

    def AddCircle(self, positionX, positionY, identifier):
        # TODO Get Screen name
        # TODO add circle to the current screen
        self.add_widget(Image(source='images/tableImages/circle_white.png', pos=(positionX, positionY), id=identifier,
                              size_hint_x=0.05, allow_stretch=True))


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source='images/tableImages/GameStarted.png'))


class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source='images/tableImages/GameStarted.png'))


class GIApp(App):
    Config.set('graphics', 'position', 'auto')
    Config.write()

    def build(self):
        self.screen_manager = ScreenManager()

        self.first_screen = FirstScreen()
        screen_1 = Screen(name="first_screen")
        screen_1.add_widget(self.first_screen)
        self.screen_manager.add_widget(screen_1)

        self.second_screen = SecondScreen()
        screen_2 = Screen(name="second_screen")
        screen_2.add_widget(self.second_screen)
        self.screen_manager.add_widget(screen_2)

        return self.screen_manager


if __name__ == "__main__":
    gi_app = GIApp()
    gi_app.run()

