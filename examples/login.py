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

def login(username, password, cb):
    query = gql(
        """
        mutation ($data: LoginInput!) {
          login(data: $data) {
              token
          }
        }
    """
    )
    params = {
        "data": {
            "username": username,
            "password": password,
        },
    }
    app.gqlrunner.execute(query, cb, variable_values=params)

class MyGame(app.App):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.username = ''
        self.password = ''
        self.message = ''

    def setup(self):
        pass

    def draw(self):
        imgui.begin("Test Window")

        changed, self.username = imgui.input_text(
            'User Name',
            self.username,
            256
        )

        changed, self.password = imgui.input_text(
            'Password',
            self.password,
            256
        )

        if imgui.button("Login"):
            def cb(token):
                self.message = token
            login(self.username, self.password, cb)

        imgui.end()

        # Put the text on the screen.
        output = f"Username: {self.username}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 13)

        output = f"Password: {self.password}"
        arcade.draw_text(output, 10, 50, arcade.color.WHITE, 13)

        output = f"Message: {self.message}"
        arcade.draw_text(output, 10, 30, arcade.color.WHITE, 13)

def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()