import numpy as np
from shared.board import Board


class Solver:

    def __init__(self, board: Board, constraints) -> None:
        self._board = board
        self._top_constr = constraints["top"]
        self._bottom_constr = constraints["bottom"]
        self._left_constr = constraints["left"]
        self._right_constr = constraints["right"]

    def get_size(self):
        return self._board.get_size()

    def rand_init(self):
        fields = None
        for _ in range(0, self.get_size() - 1):
            stop = False
            while not stop:
                row = np.random.permutation(self.get_size()) + 1
                if fields is None:
                    fields = np.array([row])
                else:
                    unique_row = True
                    for existing_row in fields:
                        if (existing_row == row).all():
                            unique_row = False
                    if unique_row:
                        fields = np.vstack((fields, row))
                        stop = True

        self._board.set_fields(fields)

    def check_col_constraint(self, board: Board, col):
        seen_pyramids = 0
        highest_pyramid = 0
        broken_constraints = 0
        if self._top_constr[col] != 0:
            for row in range(0, self.get_size()):
                curr_pyramid = board.get_field(row, col)
                if curr_pyramid > highest_pyramid:
                    highest_pyramid = curr_pyramid
                    seen_pyramids += 1

            if seen_pyramids != self._top_constr[col]:
                broken_constraints += 1

        if self._bottom_constr[col] != 0:
            seen_pyramids = 0
            highest_pyramid = 0
            for row in range(self.get_size() - 1, -1, -1):
                curr_pyramid = board.get_field(row, col)
                if curr_pyramid > highest_pyramid:
                    highest_pyramid = curr_pyramid
                    seen_pyramids += 1
            if seen_pyramids != self._bottom_constr[col]:
                broken_constraints += 1

        return broken_constraints

    def check_row_constraint(self, board: Board, row):
        seen_pyramids = 0
        highest_pyramid = 0
        broken_constraints = 0
        if self._left_constr[row] != 0:
            for col in range(0, self.get_size()):
                curr_pyramid = board.get_field(row, col)
                if curr_pyramid > highest_pyramid:
                    highest_pyramid = curr_pyramid
                    seen_pyramids += 1

            if seen_pyramids != self._left_constr[row]:
                broken_constraints += 1

        if self._right_constr[row] != 0:
            seen_pyramids = 0
            highest_pyramid = 0
            for col in range(self.get_size() - 1, -1, -1):
                curr_pyramid = board.get_field(row, col)
                if curr_pyramid > highest_pyramid:
                    highest_pyramid = curr_pyramid
                    seen_pyramids += 1
            if seen_pyramids != self._right_constr[row]:
                broken_constraints += 1

        return broken_constraints

    def is_solution(self, board):
        for col in range(0, self.get_size()):
            if not self.is_col_unique(col) or self.check_col_constraint(
                    board, col):
                return False

            for row in range(0, self.get_size()):
                if not self.is_row_unique(row) or self.check_row_constraint(
                        board, row):
                    return False

        return True

    def check_if_val_unique(self, board: Board, col, val):
        matched_vals = -1
        for row in range(0, self.get_size()):
            if board.get_field(row, col) == val:
                matched_vals += 1

        return matched_vals

    def is_row_unique(self, row):
        return len(np.unique(self._board.get_row(row))) == len(
            self._board.get_row(row))

    def is_col_unique(self, col):
        return len(np.unique(self._board.get_col(col))) == len(
            self._board.get_col(col))
