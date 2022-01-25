import math
import random
import numpy as np
from algorithms.solver import Solver
from shared.board import Board


class Tabu(Solver):

    def __init__(self, board: Board, constraints) -> None:
        super().__init__(board, constraints)
        self.row_params = np.array([])
        self.TABU_LENGTH = 4
        self.LOOP_RESET = 50000
        for i in range(0, self.get_size()):
            self.row_params = np.append(self.row_params, Row(0))

    def run(self):
        print("Tabu algorithm has started solving the problem")
        loops = 0
        self.rand_init(self._board)

        while not self.is_solution(self._board):
            if loops == self.LOOP_RESET:
                self.rand_init(self._board)
                loops = 0

            self.calc_rows_loss_func()

            for row in range(0, self.get_size()):
                self.iterate_neighbours_in_row(row)
                self.make_best_swap(row)
                self.add_to_tabu(row)

            loops += 1
        print("Solution: ")
        print(self._board)

    def calc_rows_loss_func(self):
        for row in range(0, self.get_size()):
            self.row_params[row].loss_func = self.calc_row_loss_func(row)

    def iterate_neighbours_in_row(self, row):
        max_diff = -math.inf
        self.row_params[row].fields_to_swap = np.array([])
        for col in range(0, self.get_size()):
            for neighbour in range(0, self.get_size()):
                if neighbour == col:
                    continue

                diff = self.loss_func_diff_after_swap(col, row, neighbour)
                if diff > max_diff:
                    max_diff = diff

                    self.row_params[row].fields_to_swap = np.array(
                        [[col, neighbour]])
                if diff == max_diff:
                    if len(self.row_params[row].fields_to_swap) == 0:
                        self.row_params[row].fields_to_swap = np.array(
                            [[col, neighbour]])
                    else:
                        self.row_params[row].fields_to_swap = np.concatenate(
                            (self.row_params[row].fields_to_swap,
                             [[col, neighbour]]))

        self.row_params[row].loss_func -= max_diff

    def calc_row_loss_func(self, row):
        loss_val = 0
        for col in range(0, self.get_size()):
            loss_val += self.field_loss_func(col, row)

        return loss_val

    def field_loss_func(self, col, row):
        loss_func = 0
        loss_func += self.check_row_constraint(self._board,
                                               row) * self.get_size()
        loss_func += self.check_col_constraint(self._board,
                                               col) * self.get_size()
        loss_func += self.check_if_val_unique(self._board, col,
                                              self._board.get_field(row, col))

        return loss_func

    def loss_func_diff_after_swap(self, col, row, neighbour):
        lowest_val = -math.inf
        curr_loss_val = self.row_params[row].loss_func
        self._board.swap_fields(row, col, row, neighbour)
        if self.check_if_in_tabu(row):
            return lowest_val

        loss_val_after_swap = self.calc_row_loss_func(row)
        self._board.swap_fields(row, col, row, neighbour)
        diff = curr_loss_val - loss_val_after_swap

        return diff

    def add_to_tabu(self, row):
        tabu_row = np.array([])
        for col in range(0, self.get_size()):
            tabu_row = np.append(tabu_row, self._board.get_field(row, col))
        if self.row_params[row].tabu_list is None:
            list = np.array([tabu_row])
            self.row_params[row].tabu_list = list
        else:
            self.row_params[row].tabu_list = np.concatenate(
                (self.row_params[row].tabu_list, [tabu_row]))
        if len(self.row_params[row].tabu_list) > self.TABU_LENGTH:
            self.row_params[row].tabu_list = np.delete(
                self.row_params[row].tabu_list, 0, 0)

    def check_if_in_tabu(self, row):
        tabu_row = np.array([])
        for col in range(0, self.get_size()):
            tabu_row = np.append(tabu_row, self._board.get_field(row, col))

        if self.row_params[row].tabu_list is not None:
            for tabu in self.row_params[row].tabu_list:
                if (tabu == tabu_row).all():
                    return True

        return False

    def make_best_swap(self, row):
        if self.row_params[row].fields_to_swap.size == 0:
            return

        rand_swap = random.randint(
            0,
            len(self.row_params[row].fields_to_swap) - 1)
        fields_to_swap = self.row_params[row].fields_to_swap[rand_swap]

        self._board.swap_fields(row, fields_to_swap[0], row, fields_to_swap[1])


class Row:

    def __init__(self, loss_func) -> None:
        self.loss_func = loss_func
        self.fields_to_swap = None
        self.tabu_list = None
