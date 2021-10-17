from loguru import logger

from gql import gql

import arcade

import imgui

import app

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "All Users"

#allUsers(after: String, before: String, first: Int, last: Int): UserConnection!


def allUsers(cb):
    query = gql("""
    query {
        allUsers(after: "", before: "", first: 0, last: 0) {
            edges {
                cursor
                node {
                    id
                    username
                    email
                }
            }
        }
    }
    """)

    app.gqlrunner.execute(query, cb)

class MyGame(app.App):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.counter = 0
        self.test_input = 0
        self.users = None

    def setup(self):
        def cb(data):
            print(data)
            self.users = [edge['node'] for edge in data['allUsers']['edges']]
        allUsers(cb)

    def draw(self):
        imgui.begin("All Users")

        imgui.columns(3, 'Users')
        imgui.separator()
        imgui.text("ID")
        imgui.next_column()
        imgui.text("Name")
        imgui.next_column()
        imgui.text("Email")
        imgui.separator()
        imgui.set_column_offset(1, 40)

        if self.users:
            for user in self.users:
                imgui.next_column()
                imgui.text(user['id'])
                imgui.next_column()
                imgui.text(user['username'])
                imgui.next_column()
                imgui.text(user['email'])
                imgui.next_column()

        imgui.columns(1)
        imgui.end()

def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()