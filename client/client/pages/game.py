from gql import gql

from loguru import logger

import arcade

import imgui

from .page import Page
from game import Game
from player import Player

import app

counterQuery = gql("""
subscription {
  counter
}
""")

def joinGame(gameId, cb):
    query = gql(
        """
        mutation ($gameId: ID!) {
          joinGame(gameId: $gameId) {
            id
          }
        }
    """
    )
    params = {
        "gameId": gameId,
    }
    app.gqlrunner.execute(query, cb, variable_values=params)

class GamePage(Page):

    def __init__(self, window, name, title, **kwargs):
        super().__init__(window, name, title)
        self.game = Game(kwargs['id'])

        def cb(data):
            logger.debug(f'joinGame:  {data}')
            player = self.player = Player(data['joinGame']['id'])
            logger.debug(f'Player:  {player}')

        joinGame(self.game.id, cb)


    def draw(self):
        imgui.begin("Tic Tac Toe")
        #imgui.text(f'Count:  ')

        imgui.end()


def install(app):
    app.add_page(GamePage, "game", "Game")
