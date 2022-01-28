import json
import time
from loguru import logger

from algorithms.genetic import Genetic
from shared.board import Board
from algorithms.tabu import Tabu
from shared.settings_getter import get_settings




def run_tabu(size, constraints):
    board = Board(size)
    tabu = Tabu(board, constraints)
    start = time.time()
    tabu.run()
    end = time.time()
    logger.info(f"Finished in {round(end - start, 2)} seconds")


def run_genetic(size, constraints, population_size=500):
    board = Board(size)
    genetic = Genetic(board, constraints, population_size)
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
    raise NotImplementedError("Use as package")