from gql import gql

from loguru import logger

import pyglet
import arcade

import imgui

import app

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Hello World!"

getMessageQuery = gql("""
query {
  getMessage
}
""")

counterQuery = gql("""
subscription {
  counter
}
""")

def cb(data):
    print(data)


class MyGame(app.App):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.counter = 0
        self.test_input = 0

    def setup(self):
        def cb(data):
            self.counter = data['counter']

        app.gqlrunner.subscribe(counterQuery, cb)


    def draw(self):
        imgui.begin("Test Window")
        imgui.text('Count:  ')
        imgui.same_line()
        imgui.text(str(self.counter))
        changed, self.test_input = imgui.input_int("Integer Input Test", self.test_input)

        imgui.end()

        arcade.draw_text(str(self.counter), 512, 128, arcade.color.WHITE_SMOKE, 64)

def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()