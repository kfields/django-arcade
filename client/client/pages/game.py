from gql import gql

from loguru import logger

import arcade

import imgui

from django_arcade_core.game_event import GameEvent, JoinEvent, StartEvent, TurnEvent, MarkEvent

from .page import Page
from game import Game
from player import Player
from board import Board

import app

def getGameState(id, cb):
    query = gql(
        """
        query ($id: ID!) {
            game(id: $id) {
                state {
                    board
                    turn
                }
            }
        }
        """
    )
    params = {
        "id": id,
    }
    app.gqlrunner.execute(query, cb, variable_values=params)

def observeGame(id, cb):
    query = gql(
        """
        subscription ($id: ID!) {
            game(id: $id) {
                __typename
                id
                ... on JoinEvent {
                    playerId
                }
                ... on TurnEvent {
                    playerId
                }
                ... on MarkEvent {
                    symbol
                    x
                    y
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
              player {
                id
                symbol
            }
          }
        }
    """
    )
    params = {
        "gameId": gameId,
    }
    app.gqlrunner.execute(query, cb, variable_values=params)

def ready(gameId):
    query = gql(
        """
        mutation ($gameId: ID!) {
          ready(gameId: $gameId) {
            ok
            message
          }
        }
    """
    )
    params = {
        "gameId": gameId
    }
    app.gqlrunner.execute(query, lambda data: None, variable_values=params)

def mark(gameId, x, y, cb):
    query = gql(
        """
        mutation ($gameId: ID!, $x: Int!, $y: Int!) {
          mark(gameId: $gameId, x: $x, y: $y) {
            ok
            message
          }
        }
    """
    )
    params = {
        "gameId": gameId,
        "x": x,
        "y": y,
    }
    app.gqlrunner.execute(query, cb, variable_values=params)

class GamePage(Page):

    def __init__(self, window, name, title, **kwargs):
        super().__init__(window, name, title)
        gameId = kwargs['id']
        self.game = Game(gameId)

        def cb(x, y):
            def cb2(data):
                logger.debug(f'board:mark:  {data}')
            mark(gameId, x, y, cb2)
        self.board = Board(cb, 512, window.height - 256, 256, 256)

        def cb(data):
            logger.debug(f'observe:data:  {data}')
            self.dispatch(data['game'])
        observeGame(gameId, cb)

        def cb(data):
            logger.debug(f'joinGame:  {data}')
            player = self.player = Player(data['joinGame']['player']['id'])
            self.board.symbol = data['joinGame']['player']['symbol']
            logger.debug(f'Player:  {player}')
            def cb2(data):
                self.board.board = data['game']['state']['board']
            getGameState(self.game.id, cb2)
        joinGame(self.game.id, cb)

    def dispatch(self, data):
        logger.debug(f'dispatch:data:  {data}')
        event = GameEvent.produce(data)
        logger.debug(f'dispatch:event:  {event}')
        if isinstance(event, JoinEvent):
            pass
        elif isinstance(event, StartEvent):
            ready(self.game.id)
        elif isinstance(event, TurnEvent):
            if event.player_id == self.player.id:
                self.board.enable()
            else:
                self.board.disable()
        elif isinstance(event, MarkEvent):
            self.board.mark(event.symbol, event.x, event.y)


    def draw(self):
        self.board.draw()
        #imgui.begin("Tic Tac Toe")
        #imgui.end()

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.board.on_mouse_press(x, y, button, key_modifiers)

def install(app):
    app.add_page(GamePage, "game", "Game")
