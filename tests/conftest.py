from typing import List
import pytest

from utils.nlp import NLP


@pytest.fixture(scope="module")
def nlp_instance() -> NLP:
    return NLP()


@pytest.fixture(scope="module")
def names():
    return [
        "Mauricio Felicio Pereira",
        "Fabio Bertolazzi",
        "Rita de Cassia Medeiros Lamego",
        "Rafaela Brandão Balan",
        "Priscila Lie Kawamura",
        "Tiago Ferreira Rodrigues",
        "Valdei de Oliveira Santos Rocha",
        "Valteir Cardoso da Silva",
        "Fabiano Bergamo",
        "Rafael Branwavski Balantimes",
    ]


@pytest.fixture(scope="module")
def input_file(names):
    file_path = "/tmp/input.txt"
    with open(file_path, "w", encoding="ISO-8859-1") as f:
        f.write("\n".join(names))

    return file_path
