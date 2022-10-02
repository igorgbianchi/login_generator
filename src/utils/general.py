import itertools
import logging
from typing import List, Optional, Set

import models

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


def write_on_file(filepath: str, output: models.LoginGeneratorOutput) -> None:
    with open(f"{filepath}.json", "w") as f:
        f.write(output.json())


def combine_2_2_3_words(words: List[str], logins: Set[str]) -> Optional[str]:
    _2_words = {word[:2] for word in words}
    _3_words = {word[:3]: word[:2] for word in words}

    for possible_3_word in _3_words:
        filtered_2_words = set(_2_words)
        filtered_2_words.remove(_3_words[possible_3_word])
        possible_combinations = itertools.permutations(
            list(filtered_2_words) + [possible_3_word], r=3
        )
        for combination in possible_combinations:
            if (possible_login := "".join(combination)) not in logins:
                return possible_login

    return None


def combine_3_4_words(words: List[str], logins: Set[str]) -> Optional[str]:
    _4_words = [word[:4] for word in words]
    _3_words = {word[:4]: word[:3] for word in reversed(words)}

    for possible_4_word in _4_words:
        for possible_3_word in _3_words.values():
            possible_login = possible_4_word + possible_3_word
            if possible_3_word == _3_words[possible_4_word]:
                continue
            if possible_login in logins:
                possible_login = possible_3_word + possible_4_word
            if possible_login in logins:
                continue

            return possible_login

    return None


def combine(words: List[str], logins: Set[str]) -> str:
    logger.debug(f"Name to generate login: {' '.join(words)}")
    logger.debug("Trying to generate login using words with 3 and 4 characters.")
    if (possible_login := combine_3_4_words(words, logins)) is not None:
        return possible_login

    logger.debug("Trying to generate login using words with 2 and 3 characters.")
    if (possible_login := combine_2_2_3_words(words, logins)) is not None:
        return possible_login

    raise AlreadyUsedError(words)


def combine_all(
    normalized_names: List[models.NormalizationOutput],
) -> models.LoginGeneratorOutput:
    logins: Set[str] = set()
    output = models.LoginGeneratorOutput()
    for n in normalized_names:
        try:
            login = combine(n.normalized.split(" "), logins)
            logins.add(login)
            output.data.append(models.Login(name=n.original, username=login))
        except AlreadyUsedError as e:
            logger.warning(str(e))

    return output


def get_logger(log_level: str) -> logging.Logger:
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=log_level
    )
    logger = logging.getLogger(__name__)

    return logger
