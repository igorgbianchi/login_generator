import pytest

from utils.nlp import NLP


@pytest.fixture(scope="module")
def nlp_instance() -> NLP:
    return NLP()
