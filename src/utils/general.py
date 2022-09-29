import logging
from typing import List, Set


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


def write_on_file(file_name: str, data: List[str]) -> None:
    with open(file_name, "w") as f:
        f.writelines(data)


def combine(words: List[str], logins: Set[str]) -> str:
    _4_words = [word[:4] for word in words]
    _3_words = {word[:4]: word[:3] for word in reversed(words)}

    for possible_4_word in _4_words:
        for possible_3_word in _3_words.values():
            logger.debug(possible_3_word, possible_4_word)
            possible_login = possible_4_word + possible_3_word
            if possible_3_word == _3_words[possible_4_word]:
                continue
            if possible_login in logins:
                possible_login = possible_3_word + possible_4_word
            if possible_login in logins:
                continue

            return possible_login

    raise AlreadyUsedError(words)
