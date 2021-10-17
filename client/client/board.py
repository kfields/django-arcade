import arcade

CELL_SIZE = 64
CELL_PADDING = 8
SYMBOL_SIZE = CELL_SIZE - CELL_PADDING * 2

empty_board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' '],
]

class Board:
    def __init__(self, cb, x, y, width, height, columns=3, rows=3) -> None:
        self.enabled = False
        self.cb = cb
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
        self.board = empty_board
        self.symbol = ' '
        self.symbol_size = self.cell_size[0] - CELL_PADDING * 2, self.cell_size[1] - CELL_PADDING * 2

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def mark(self, symbol, x, y):
        self.board[x][y] = symbol

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
                #arcade.draw_text(self.board[i][j], x, y, arcade.color.WHITE_SMOKE, self.symbol_size[0])
                #TODO:Arcade/Pyglet/Intel driver bug workaround
                arcade.draw_text(self.board[i][j] + ' ' * 4, x, y, arcade.color.WHITE_SMOKE, self.symbol_size[0])

    def on_mouse_press(self, x, y, button, key_modifiers):
        if not self.enabled or x < self.x or x > self.x1 or y > self.y or y < self.y1:
            return
        cell_width, cell_height = self.cell_size
        j = int((x-self.x) / cell_width)
        i = int((self.y-y) / cell_height)
        if self.board[i][j] != ' ':
            return
        self.board[i][j] = self.symbol
        self.cb(i, j)
