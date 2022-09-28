import logging
import os
from typing import List

from utils.nlp import NLP

file_name = "Massa de Dados.txt"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))


def read_names(file_name: str) -> List[str]:
    try:
        assert ".txt" in file_name[-4:]
    except AssertionError:
        logger.exception("Invalid text file.")
        raise
    try:
        logger.debug("Reading text file.")
        with open(file_name, "r", encoding="latin-1") as f:
            names = f.read().split("\n")
        logger.debug("Succesfully reading.")
        return names
    except FileNotFoundError:
        logger.exception("It wasn't possible to open the file.")
        raise


if __name__ == "__main__":
    logger.info("Program started.")
    names = read_names(file_name)
    nlp = NLP(logger=logger)
    normalized_names = [nlp.normalize(name) for name in names]
    logger.info("Finished program.")
