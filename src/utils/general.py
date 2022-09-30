import json
import logging
from typing import Dict, List, Set


logger = logging.getLogger(__name__)


class AlreadyUsedError(Exception):
    def __init__(self, words: List[str]) -> None:
        self.words = words

    def __str__(self) -> str:
        return f"All possibilities were tested for these words: {' '.join(self.words)}"


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


def write_on_file(file_name: str, data: Dict[str, str]) -> None:
    with open(file_name, "w") as f:
        json.dump(data, f)


def combine(words: List[str], logins: Set[str]) -> str:
    logger.debug(f"Name to generate login: {' '.join(words)}")
    _4_words = [word[:4] for word in words]
    _3_words = {word[:4]: word[:3] for word in reversed(words)}

    for possible_4_word in _4_words:
        for possible_3_word in _3_words.values():
            logger.debug(f"Possible word with 3 characters: {possible_3_word}")
            logger.debug(f"Possible word with 4 characters: {possible_4_word}")
            possible_login = possible_4_word + possible_3_word
            if possible_3_word == _3_words[possible_4_word]:
                continue
            if possible_login in logins:
                possible_login = possible_3_word + possible_4_word
            if possible_login in logins:
                continue

            return possible_login

    raise AlreadyUsedError(words)


def combine_all(normalized_names: List[str]) -> Dict[str, str]:
    logins: Set[str] = set()
    output = {}
    for n in normalized_names:
        try:
            login = combine(n.split(" "), logins)
            logins.add(login)
            output[n] = login
        except AlreadyUsedError as e:
            logger.warning(str(e))

    return output


def get_logger(log_level: str) -> logging.Logger:
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=log_level
    )
    logger = logging.getLogger(__name__)

    return logger
