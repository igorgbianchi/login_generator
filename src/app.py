import logging
import os
from typing import Set

from utils.general import combine, read_names, write_on_file, AlreadyUsedError
from utils.nlp import NLP

file_name = "Massa de Dados.txt"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))


if __name__ == "__main__":
    logger.info("Program started.")
    names = read_names(file_name)
    nlp = NLP(logger=logger)
    normalized_names = [nlp.normalize(name) for name in names]
    logger.info("Names normalized.")
    logins: Set[str] = set()
    output = []
    for n in normalized_names:
        try:
            login = combine(n.split(" "), logins)
            logins.add(login)
            output.append(f"{n} | {login}\n")
        except AlreadyUsedError as e:
            logger.warning(str(e))
    logger.info("Logins generated.")
    write_on_file("output.txt", output)
    logger.info("Program finished.")
