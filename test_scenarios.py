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
from shared.miscellaneous import (
    run_tabu, run_genetic, get_input_data
)

@logger.catch
def main():
    warnings.filterwarnings("ignore")
    initialize_logger()
    # seed, size, constraints

    # np.random.seed(12)
    # size, constraints = get_input_data()
    # run_genetic(size, constraints)
    # run_tabu(size, constraints)

    np.random.seed(13)
    inputs = get_input_data()
    for index, data in enumerate(inputs):
        logger.info(f"Test case number {index}")
        size = data["n"]
        constraints = data["constraints"]
        run_genetic(size, constraints, population_size=50)
        run_tabu(size, constraints)


if __name__ == "__main__":
    main()
