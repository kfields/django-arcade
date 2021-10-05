from gql import gql

from loguru import logger

import arcade
import imgui

from .page import Page
import app


#allGames(after: String, before: String, first: Int, last: Int): UserConnection!
def allGames(cb):
    query = gql("""
    query {
        allGames(after: "", before: "", first: 0, last: 0) {
            edges {
                cursor
                node {
                    id
                }
            }
        }
    }
    """)

    app.gqlrunner.execute(query, cb)

def newGame(cb):
    query = gql(
        """
        mutation {
          createGame {
              id
          }
        }
    """
    )
    params = {
        "data": {
        },
    }
    #app.gqlrunner.execute(query, cb, variable_values=params)
    app.gqlrunner.execute(query, cb)

class Home(Page):

    def reset(self):
        self.games = None

        def cb(data):
            print(data)
            allGames = data['allGames']
            self.games = [edge['node'] for edge in allGames['edges']] if allGames else None
        allGames(cb)

    def draw(self):
        imgui.begin("Games")

        imgui.columns(3, 'Games')
        imgui.separator()
        imgui.text("ID")
        '''
        imgui.next_column()
        imgui.text("Name")
        imgui.next_column()
        imgui.text("Email")
        '''
        imgui.separator()
        imgui.set_column_offset(1, 40)

        if self.games:
            for game in self.games:
                imgui.next_column()
                imgui.text(user['id'])
                imgui.next_column()
                '''
                imgui.text(user['username'])
                imgui.next_column()
                imgui.text(user['email'])
                imgui.next_column()
                '''
        imgui.columns(1)

        if imgui.button("New Game"):
            def cb(game):
                self.game = game
                logger.debug(f"Game:  {game}")
            newGame(cb)

        imgui.end()

def install(app):
    app.add_page(Home, "home", "Home")