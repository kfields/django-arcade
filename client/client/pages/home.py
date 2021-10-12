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

def createGame(cb):
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

        imgui.columns(1, 'Games')
        imgui.separator()
        imgui.text("ID")
        '''
        imgui.next_column()
        imgui.text("Name")
        imgui.next_column()
        imgui.text("Email")
        '''
        imgui.separator()
        #imgui.set_column_offset(1, 40)

        if self.games:
            for game in self.games:
                imgui.next_column()
                opened, _ = imgui.selectable(game['id'], flags=imgui.SELECTABLE_SPAN_ALL_COLUMNS)
                '''
                opened, self.selected[0] = imgui.selectable(
                    game['id'], self.selected[0], flags=imgui.SELECTABLE_SPAN_ALL_COLUMNS
                )
                '''
                if opened:
                    self.app.router.go('game', id=game['id'])
                #imgui.text(game['id'])
                imgui.next_column()
                '''
                imgui.text(user['username'])
                imgui.next_column()
                imgui.text(user['email'])
                imgui.next_column()
                '''
        imgui.columns(1)

        if imgui.button("New Game"):
            def cb(data):
                game = data['createGame']
                self.game = game
                logger.debug(f"Game:  {game}")
                self.app.router.go('game', id=game['id'])
            createGame(cb)

        imgui.end()

def install(app):
    app.add_page(Home, "home", "Home")