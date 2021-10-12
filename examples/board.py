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
        self.cell_size = int(width/columns), int(height/columns)
        self.cell_padding = CELL_PADDING, CELL_PADDING

    def draw(self):
        self.draw_lines()
        self.draw_symbols()

    def draw_lines(self):
        for i in range(2):
            cell_width, cell_height = self.cell_size
            x = self.x
            x1 = self.x1
            y =  self.y-cell_height-(i*cell_height)
            y1 = y
            arcade.draw_line(x, y, x1, y1, arcade.color.WHITE_SMOKE, 4)

        for j in range(2):
            cell_width, cell_height = self.cell_size
            x = self.x + (cell_width+j*cell_width)
            x1 = x
            y =  self.y
            y1 = y - (cell_height * 3)
            arcade.draw_line(x, y, x1, y1, arcade.color.WHITE_SMOKE, 4)

    def draw_symbols(self):
        cell_width, cell_height = self.cell_size
        for i in range(3):
            for j in range(3):
                x = self.x + (j*cell_width) + CELL_PADDING
                y = self.y - cell_height - (i*cell_height) + CELL_PADDING
                arcade.draw_text(board[i][j], x, y, arcade.color.WHITE_SMOKE, SYMBOL_SIZE)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if x < self.x or x > self.x1 or y > self.y or y < self.y1:
            return
        cell_width, cell_height = self.cell_size
        j = int((x-self.x) / cell_width)
        i = int((self.y-y) / cell_height)
        board[i][j]='K'

class MyGame(app.App):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.board = Board(256, self.height - 256, 192, 192)

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