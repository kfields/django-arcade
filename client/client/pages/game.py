from gql import gql

from loguru import logger

import arcade

import imgui

from .page import Page
from game import Game
from player import Player

import app

gameQuery = gql("""
subscription ($gameId: ID!) {
  game
}
""")

def observeGame(id, cb):
    query = gql(
        """
        subscription ($id: ID!) {
            game(id: $id) {
                __typename
                id
                ... on JoinGameEvent {
                    playerId
                }
            }
        }
    """
    )
    params = {
        "id": id,
    }
    app.gqlrunner.subscribe(query, cb, variable_values=params)

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
        gameId = kwargs['id']
        self.game = Game(gameId)

        def cb(data):
            logger.debug(f'GameEvent:  {data}')
        observeGame(gameId, cb)

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
