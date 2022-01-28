# here use both algorithms to solve multiple problems and measure performance time
import json
import time
import warnings
import numpy as np
from loguru import logger

from algorithms.genetic import Genetic
from shared.board import Board
from algorithms.tabu import Tabu
from shared.initialize_logger import initialize_logger
from shared.settings_getter import get_settings

@logger.catch
def main():
    warnings.filterwarnings("ignore")
    initialize_logger()
    # seed, size, constraints

    # np.random.seed(12)
    # size, constraints = get_input_data()
    # run_genetic(size, constraints)
    # run_tabu(size, constraints)

    np.random.seed(12)
    inputs = get_input_data()
    for index, data in enumerate(inputs):
        logger.info(f"Test case number {index}")
        size = data["n"]
        constraints = data["constraints"]
        run_genetic(size, constraints)
        run_tabu(size, constraints)


def run_tabu(size, constraints):
    board = Board(size)
    tabu = Tabu(board, constraints)
    start = time.time()
    tabu.run()
    end = time.time()
    logger.info(f"Finished in {round(end - start, 2)} seconds")


def run_genetic(size, constraints):
    board = Board(size)
    genetic = Genetic(board, constraints, 500)
    start = time.time()
    if genetic.run():
        end = time.time()
        logger.info(f"Finished in {round(end-start, 2)} seconds")


def get_input_data() -> list:
    with open(get_settings()["INPUT_FILE"]) as json_file:
        data = json.load(json_file)
        #return data["n"], data["constraints"]
    return data

if __name__ == "__main__":
    main()
