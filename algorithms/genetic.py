import numpy as np
from algorithms.solver import Solver
from shared.board import Board


class Genetic(Solver):
    def __init__(self, board: Board, constraints, pop_size) -> None:
        super().__init__(board, constraints)
        self._pop_size = pop_size
        self._pop = np.array([])
        for i in range(0, pop_size):
            self._pop = np.append(self._pop, Individual(board.get_size()))
            self.rand_init(self._pop[i].board)
        self._children = np.empty(pop_size, dtype=Individual)
        self._pop_scores = np.empty(pop_size, dtype=np.double)
        self._probability = np.empty(pop_size, dtype=Range)
        for i in range(0, pop_size):
            self._probability[i] = Range()
        self._solution_found = False
        self.MUTATION = 0.9

    def run(self):
        print("Genetic algorithm has started solving the problem")
        i = 0
        while not self._solution_found:
            print(i)
            self.asses_pop(self._pop, False)
            self.selection()
            self.crossover()
            self.mutation()
            self.asses_pop(self._children, True)
            self.succession()
            i += 1

        print("Solution: ")
        print(self._board)
        return True

    def asses_pop(self, pop, is_children):
        for i in range(0, self._pop_size):
            if self._solution_found:
                return
            self.assess(pop[i])
        pop = np.sort(pop)

        if not is_children:
            for i in range(0, self._pop_size):
                self._pop_scores[i] = pop[i].score
            qmin = self._pop_scores[0]
            qmax = self._pop_scores[self._pop_size - 1]
            if qmax != qmin:
                for i in range(0, self._pop_size):
                    self._pop_scores[i] = 1 - (
                        (self._pop_scores[i] - qmin) / (qmax - qmin)
                    )

    def assess(self, ind):
        size = ind.board.get_size()
        score = 0
        for i in range(0, size):
            score += self.check_col_constraint(ind.board, i) * size
            score += self.check_row_constraint(ind.board, i) * size
            for j in range(0, size):
                score += self.check_if_val_unique(
                    ind.board, i, ind.board.get_field(j, i)
                )
                score += self.check_if_val_unique_in_row(
                    ind.board, j, ind.board.get_field(j, i)
                )

        if score == 0:
            self._board.copy_values(ind.board)
            self._solution_found = True
            return

        ind.score = score

    def check_if_val_unique_in_row(self, board, row, val):
        matched_vals = -1
        for col in range(self.get_size()):
            if board.get_field(row, col) == val:
                matched_vals += 1

        return matched_vals

    def selection(self):
        score_sum = 0
        for i in range(0, self._pop_size):
            score_sum += self._pop_scores[i]

        self._probability[0].start = 0
        for i in range(0, self._pop_size - 1):
            self._probability[i].end = (
                self._probability[i].start + self._pop_scores[i] / score_sum
            )
            self._probability[i + 1].start = self._probability[i].end
        self._probability[self._pop_size - 1].end = 1

    def get_max_score(self):
        max_score = 0
        for i in range(0, self._pop_size):
            if self._pop_scores[i] > max_score:
                max_score = self._pop_scores[i]

    def crossover(self):
        parent1 = None
        parent2 = None
        for i in range(0, self._pop_size):
            rand1 = np.random.rand()
            rand2 = np.random.rand()

            for j in range(0, self._pop_size):
                if (
                    rand1 >= self._probability[j].start
                    and rand1 < self._probability[j].end
                ):
                    parent1 = self._pop[j]
                    break
            if parent1 is None:
                parent1 = self._pop[0]

            for j in range(0, self._pop_size):
                if (
                    rand2 >= self._probability[j].start
                    and rand2 < self._probability[j].end
                ):
                    parent2 = self._pop[j]
                    break
            if parent2 is None:
                parent2 = self._pop[0]

            self._children[i] = self.create_child(parent1, parent2)

    def mutation(self):
        board_size = self._board.get_size()
        for i in range(0, self._pop_size):
            for j in range(0, board_size):
                for k in range(0, board_size):
                    if np.random.rand() > self.MUTATION:
                        self._children[i].board.set_field(
                            k,
                            j,
                            np.random.randint(board_size) + 1,
                        )

    def succession(self):
        if self._pop[0].score > self._children[0].score:
            self._pop[0] = self._children[0]
        else:
            self._children[0] = None
        for i in range(1, self._pop_size - 1):
            self._pop[i] = self._children[i]

    def create_child(self, parent1, parent2):
        size = parent1.board.get_size()
        child = Individual(size)
        for i in range(0, size):
            for j in range(0, round(size / 2)):
                child.board.set_field(j, i, parent1.board.get_field(j, i))

            for j in range(round(size / 2), size):
                child.board.set_field(j, i, parent2.board.get_field(j, i))

        return child

    def __str__(self) -> str:
        string = ""
        for i in range(0, self._pop_size):
            string += (
                str(i)
                + "\n"
                + str(self._pop[i].board)
                + "\n"
                + "score"
                + str(self._pop[i].score)
                + "\n"
                + "chances"
                + str(self._probability[i].start)
                + " - "
                + str(self._probability[i].end)
                + "\n\n"
            )


class Individual:
    def __init__(self, size):
        self.board = Board(size)
        self.score = 0

    def __lt__(self, i):
        return self.score < i.score

    def __gt__(self, i):
        return self.score > i.score

    def __str__(self) -> str:
        return f"Board:\n{str(self.board)}\nScore: {self.score}"


class Range:
    def __init__(self) -> None:
        self.start = 0
        self.end = 0
