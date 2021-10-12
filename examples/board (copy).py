from gql import gql

from loguru import logger

import pyglet
import arcade

import imgui

import app

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Tic Tac Toe"

board = [
    ['X', 'Y', 'O'],
    ['X', 'X', 'O'],
    ['O', ' ', 'X'],
]

CELL_SIZE = 64
CELL_PADDING = 8
SYMBOL_SIZE = CELL_SIZE - CELL_PADDING * 2

class Board:
    def __init__(self, x, y, width, height, columns=3, rows=3) -> None:
        self.x = x
        self.y = y
        self.x1 = x + width
        self.y1 = y - height
        self.width = width
        self.height = height
        self.columns = columns
        self.rows = rows
        self.cell_width = int(width/columns)
        self.cell_height = int(height/columns)

    def draw(self):
        self.draw_symbols()
        self.draw_lines()

    def draw_lines(self):
        for i in range(2):
            x = 0
            x1 = x + 64 * 3
            y =  self.height-64-(i*64)
            y1 = y
            arcade.draw_line(x, y, x1, y1, arcade.color.WHITE_SMOKE, 4)

        for j in range(2):
            x = 64+j*64
            x1 = x
            y =  self.height
            y1 = y - (64 * 3)
            arcade.draw_line(x, y, x1, y1, arcade.color.WHITE_SMOKE, 4)

    def draw_symbols(self):
        for i in range(3):
            for j in range(3):
                x = (j*64) + CELL_PADDING
                y = self.height-64-(i*64) + CELL_PADDING
                arcade.draw_text(board[i][j], x, y, arcade.color.WHITE_SMOKE, SYMBOL_SIZE)

    def on_mouse_press(self, x, y, button, key_modifiers):
        j = int(x / 64)
        i = int((self.height-y) / 64)
        board[i][j]='K'

class MyGame(app.App):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.board = Board(256, self.height, 192, 192)

    def setup(self):
        pass

    def draw(self):
        self.board.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.board.on_mouse_press(x, y, button, key_modifiers)

def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()