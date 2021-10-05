from gql import gql

from loguru import logger

import arcade
import imgui

from .page import Page
import app

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

class Login(Page):
    def reset(self):
        self.username = ''
        self.password = ''
        self.message = ''

    def draw(self):
        imgui.begin("Login")

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
            def cb(data):
                token = data['login']['token']
                logger.debug(f"token:  {token}")
                self.message = token
                if token:
                    self.app.runner.token = token
                    self.app.user.logged_in = True
                    self.app.router.go('home')
            login(self.username, self.password, cb)

        imgui.end()

        # Put the text on the screen.
        output = f"Username: {self.username}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 13)

        output = f"Password: {self.password}"
        arcade.draw_text(output, 10, 50, arcade.color.WHITE, 13)

        output = f"Message: {self.message}"
        arcade.draw_text(output, 10, 30, arcade.color.WHITE, 13)

def install(app):
    app.add_page(Login, "login", "Login")
