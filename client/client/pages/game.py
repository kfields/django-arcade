from gql import gql

from loguru import logger

import arcade

import imgui

from .page import Page

import app

counterQuery = gql("""
subscription {
  counter
}
""")

def setCounter(val, cb):
    query = gql(
        """
        mutation ($val: Int!) {
          setCounter(val: $val)
        }
    """
    )
    params = {
        "val": val,
    }
    app.gqlrunner.execute(query, cb, variable_values=params)

class GamePage(Page):

    def reset(self):
        self.counter = 0
        self.test_input = 0

        def cb(data):
            self.counter = data['counter']

        app.gqlrunner.subscribe(counterQuery, cb)


    def draw(self):
        imgui.begin("Counter")

        imgui.text('Count:  ')
        imgui.same_line()
        imgui.text(str(self.counter))
        changed, self.test_input = imgui.input_int("Integer Input Test", self.test_input)

        if imgui.button("Set Counter"):
            def cb(data):
                pass
            setCounter(self.test_input, cb)

        imgui.end()

        arcade.draw_text(str(self.counter), 512, 128, arcade.color.WHITE_SMOKE, 64)

def install(app):
    app.add_page(GamePage, "game", "Game")
