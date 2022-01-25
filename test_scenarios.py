# here use both algorithms to solve multiple problems and measure performance time
import json
import time
import warnings
from algorithms.genetic import Genetic
from shared.board import Board
from algorithms.tabu import Tabu


def main():
    warnings.filterwarnings("ignore")
    size, constraints = get_input_data()
    # run_tabu(size, constraints)
    run_genetic(size, constraints)


def run_tabu(size, constraints):
    board = Board(size)
    tabu = Tabu(board, constraints)
    start = time.time()
    tabu.run()
    end = time.time()
    print("Finished in time: ", end - start)


def run_genetic(size, constraints):
    board = Board(size)
    genetic = Genetic(board, constraints, 5)
    start = time.time()
    genetic.run()
    end = time.time()
    print("Finished in time: ", end - start)


def get_input_data():
    with open("input.json") as json_file:
        data = json.load(json_file)
        return data["n"], data["constraints"]


if __name__ == "__main__":
    main()
