# here use both algorithms to solve multiple problems and measure performance time
import json
import time
from shared.board import Board
from algorithms.tabu import Tabu


def main():
    size, constraints = get_input_data()
    board = Board(size)
    tabu = Tabu(board, constraints)
    start = time.time()
    tabu.run()
    end = time.time()
    print("Finished in time: ", end - start)


def get_input_data():
    with open('input.json') as json_file:
        data = json.load(json_file)
        return data["n"], data["constraints"]


if __name__ == "__main__":
    main()