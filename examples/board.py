from gql import gql

from loguru import logger

import pyglet
import arcade

import imgui

import app

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Tic Tac Toe"

'''
board = [
    ['X', 'O', 'O'],
    ['X', 'X', 'O'],
    ['O', ' ', 'X'],
]
'''

board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' '],
]

CELL_SIZE = 64
CELL_PADDING = 8
SYMBOL_SIZE = CELL_SIZE - CELL_PADDING * 2

MATCH_HORZ = 0
MATCH_VERT = 1
MATCH_DIAG_1 = 2
MATCH_DIAG_2 = 3

class Board:
    def __init__(self, x, y, width, height, columns=3, rows=3) -> None:
        self.board = board
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
        self.shapes = []

    def draw(self):
        self.draw_lines()
        self.draw_symbols()
        self.draw_shapes()

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

    def draw_shapes(self):
        for shape in self.shapes:
            shape.draw()
            
    def on_mouse_press(self, x, y, button, key_modifiers):
        if x < self.x or x > self.x1 or y > self.y or y < self.y1:
            return
        cell_width, cell_height = self.cell_size
        j = int((x-self.x) / cell_width)
        i = int((self.y-y) / cell_height)
        if board[i][j] != ' ':
            return
        board[i][j]='X'
        self.check_win('X')

    def add_slash(self, start, end, match):
        cell_width, cell_height = self.cell_size
        if match == MATCH_HORZ:
            x = self.x + start[0] * cell_width
            x1 = self.x + end[0] * cell_width + cell_width
            y =  self.y-cell_height/2-(start[1]*cell_height)
            y1 =  self.y-cell_height/2-(end[1]*cell_height)
        elif match == MATCH_VERT:
            x = self.x + start[0] * cell_width + cell_width/2
            x1 = self.x + end[0] * cell_width + cell_width/2
            y =  self.y-(start[1]*cell_height)
            y1 =  self.y-(end[1]*cell_height)-cell_height
        elif match == MATCH_DIAG_1:
            x = self.x + start[0] * cell_width
            x1 = self.x + end[0] * cell_width + cell_width
            y =  self.y-(start[1]*cell_height)
            y1 =  self.y-(end[1]*cell_height)-cell_height
        elif match == MATCH_DIAG_2:
            x = self.x + start[0] * cell_width
            x1 = self.x + end[0] * cell_width + cell_width
            y =  self.y-(start[1]*cell_height)-cell_height
            y1 =  self.y-(end[1]*cell_height)

        print(f'{x} {y} {x1} {y1}')
        self.shapes.append(arcade.create_line(x, y, x1, y1, arcade.color.RED, 4))

    def check_win_rows(self, symbol):
        for i in range(3):
            if ''.join(self.board[i]) == symbol * 3:
                self.add_slash( (0, i), (2, i), MATCH_HORZ)

    def check_win_cols(self, symbol):
        for j in range(3):
            if self.board[0][j] + self.board[1][j] + self.board[2][j] == symbol * 3:
                print('win col')
                self.add_slash( (j, 0), (j, 2), MATCH_VERT )

    def check_win_diag(self, symbol):
        if self.board[0][0] + self.board[1][1] + self.board[2][2] == symbol * 3:
            print('win diag 1')
            self.add_slash( (0, 0), (2, 2), MATCH_DIAG_1 )
        if self.board[0][2] + self.board[1][1] + self.board[2][0] == symbol * 3:
            print('win diag 2')
            self.add_slash( (0, 2), (2, 0), MATCH_DIAG_2)

    def check_win(self, symbol):
        return self.check_win_rows(symbol) or self.check_win_cols(symbol) or self.check_win_diag(symbol)
        
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
    game.run()

if __name__ == "__main__":
    main()