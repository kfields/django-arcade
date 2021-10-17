from gql import gql

from loguru import logger

import arcade
import imgui

from .page import Page
import app


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

class Users(Page):

    def reset(self):
        self.users = None

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
                #imgui.next_column()

        imgui.columns(1)
        imgui.end()

def install(app):
    app.add_page(Users, "users", "Users")
