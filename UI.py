# This script is for creating the interface that the user will interact with on the PC
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image

kivy.require("1.11.1")


class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Input your game names:", font_size=30))

        # T
        self.inside = GridLayout()
        self.inside.cols = 4
        self.inside.rows = 5

        # The text displaying the teams
        self.inside.add_widget(Label(text="Team 1", font_size=25))
        self.inside.add_widget(Label())
        self.inside.add_widget(Label(text="Team 2", font_size=25))
        self.inside.add_widget(Label())

        self.inside.add_widget(Image(source="Images/Blue_ball.png", size=(30, 30)))
        self.inside.player1 = TextInput(multiline=False, text="Input name here")
        self.inside.add_widget(self.inside.player1)
        self.inside.add_widget(Image(source="Images/Red_ball.png"))
        self.inside.player2 = TextInput(multiline=False)
        self.inside.add_widget(self.inside.player2)
        # self.inside.add_widget(Label())
        # self.inside.add_widget(Label())
        # self.inside.add_widget(Label())
        # self.inside.add_widget(Label())
        self.inside.add_widget(Image(source="Images/Blue_ball.png"))
        self.inside.player3 = TextInput(multiline=False)
        self.inside.add_widget(self.inside.player3)
        self.inside.add_widget(Image(source="Images/Red_ball.png"))
        self.inside.player4 = TextInput(multiline=False)
        self.inside.add_widget(self.inside.player4)

        self.add_widget(self.inside)

class UserInterface(App):
    def build(self):
        return ConnectPage()


if __name__ == '__main__':
    UserInterface().run()
