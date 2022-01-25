import numpy as np


class Board:
    def __init__(self, size) -> None:
        self._size = size
        self._fields = np.zeros((size, size))

    def copy_values(self, board):
        self._size = board.get_size()
        self._fields = np.zeros((self._size, self._size))
        for i in range(0, self._size):
            for j in range(0, self._size):
                self._fields[i][j] = board.get_field(i, j)

    def get_size(self):
        return self._size

    def get_field(self, row, col):
        return self._fields[row][col]

    def set_field(self, row, col, field):
        self._fields[row][col] = field

    def get_row(self, row):
        return self._fields[row]

    def get_col(self, col):
        return self._fields[:, col]

    def set_fields(self, fields):
        self._fields = fields

    def swap_fields(self, row1, col1, row2, col2):
        tmp = self._fields[row1, col1]
        self._fields[row1, col1] = self._fields[row2, col2]
        self._fields[row2, col2] = tmp

    def __str__(self) -> str:
        board_str = ""
        for row in self._fields:
            for col in row:
                board_str += str(int(col)) + " "
            board_str += "\n"

        return board_str
