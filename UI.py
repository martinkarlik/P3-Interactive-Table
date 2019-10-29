# This script is for creating the interface that the user will interact with on the PC

from kivy.app import App
from kivy.uix.label import Label


class FirstKivy(App):
    def build(self):
        return Label(text="Hello")


if __name__ == '__main__':
    FirstKivy().run()