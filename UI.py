from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


class MainWindow(Screen):
    name_1 = ObjectProperty(None)
    name_2 = ObjectProperty(None)
    name_3 = ObjectProperty(None)
    name_4 = ObjectProperty(None)


class SecondWindow(Screen):
    pass


class ThirdWindow(Screen):
    pass


class FourthWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class UI(App):

    def build(self):
        return Builder.load_file("ui.kv")


