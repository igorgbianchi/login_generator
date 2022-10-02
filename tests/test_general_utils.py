import itertools
from os.path import exists

import pytest
from pydantic_factories import ModelFactory

import models
from utils import general as general_utils


class LoginGeneratorOutputFactory(ModelFactory):  # type: ignore
    __model__ = models.LoginGeneratorOutput
    __allow_none_optionals__ = False


def test_invalid_input_file_format():
    with pytest.raises(AssertionError):
        general_utils.read_names("input.json")


def test_input_file_not_found():
    with pytest.raises(FileNotFoundError):
        general_utils.read_names("input.txt")


def test_read_input_file(names, input_file):
    assert general_utils.read_names(input_file) == names


def test_write_on_file():
    output = LoginGeneratorOutputFactory.build()
    general_utils.write_on_file("/tmp/test", output)
    assert exists("/tmp/test.json")


def test_combine_2_2_3_words():
    WORDS = ["JOAO", "SILVA", "FILHO"]
    output = general_utils.combine_2_2_3_words(WORDS, {})
    assert output is not None
    assert len(output) == 7


def test_combine_2_2_3_words_one_option_available():
    WORDS = ["JOAO", "SILVA", "FILHO"]
    _2_WORDS = [word[:2] for word in WORDS]
    _3_WORDS = [word[:3] for word in WORDS]
    logins = [
        "".join(combination)
        for combination in itertools.permutations(_2_WORDS + _3_WORDS, r=3)
    ]
    logins.remove("JOSIFIL")
    assert general_utils.combine_2_2_3_words(WORDS, logins) == "JOSIFIL"


def test_combine_2_2_3_words_no_options_available():
    WORDS = ["JOAO", "SILVA", "FILHO"]
    _2_WORDS = [word[:2] for word in WORDS]
    _3_WORDS = [word[:3] for word in WORDS]
    logins = [
        "".join(combination)
        for combination in itertools.permutations(_2_WORDS + _3_WORDS, r=3)
    ]
    assert general_utils.combine_2_2_3_words(WORDS, logins) is None


def test_combine_3_4_words():
    WORDS = ["JOAO", "SILVA", "FILHO"]
    output = general_utils.combine_3_4_words(WORDS, {})
    assert output is not None
    assert len(output) == 7


def test_combine_3_4_words_one_option_available():
    WORDS = ["JOAO", "SILVA", "FILHO"]
    _4_WORDS = [word[:4] for word in WORDS]
    _3_WORDS = [word[:3] for word in WORDS]
    logins = [
        "".join(combination)
        for combination in itertools.permutations(_4_WORDS + _3_WORDS, r=2)
    ]
    logins.remove("JOAOSIL")
    assert general_utils.combine_3_4_words(WORDS, logins) == "JOAOSIL"


def test_combine_3_4_words_no_options_available():
    WORDS = ["JOAO", "SILVA", "FILHO"]
    _4_WORDS = [word[:4] for word in WORDS]
    _3_WORDS = [word[:3] for word in WORDS]
    logins = [
        "".join(combination)
        for combination in itertools.permutations(_4_WORDS + _3_WORDS, r=2)
    ]
    assert general_utils.combine_3_4_words(WORDS, logins) is None


def test_combine_already_used(mocker):
    mocker.patch("utils.general.combine_3_4_words", return_value=None)
    mocker.patch("utils.general.combine_2_2_3_words", return_value=None)
    with pytest.raises(general_utils.AlreadyUsedError):
        general_utils.combine(["JOAO", "SILVA"], {})


def test_combine_returning_3_4_combination():
    WORDS = ["JOAO", "SILVA", "FILHO"]
    output = general_utils.combine(WORDS, {})
    assert isinstance(output, str)
    assert len(output) == 7


def test_combine_returning_2_2_3_combination(mocker):
    mocker.patch("utils.general.combine_3_4_words", return_value=None)
    WORDS = ["JOAO", "SILVA", "FILHO"]
    output = general_utils.combine(WORDS, {})
    assert isinstance(output, str)
    assert len(output) == 7


def test_combine_all_same_names():
    NORMALIZED_NAMES = [
        models.NormalizationOutput(original="João Silva", normalized="JOAO SILVA"),
        models.NormalizationOutput(original="João Silva", normalized="JOAO SILVA"),
    ]
    assert general_utils.combine_all(NORMALIZED_NAMES) == models.LoginGeneratorOutput(
        data=[
            models.Login(name="João Silva", username="JOAOSIL"),
            models.Login(name="João Silva", username="SILJOAO"),
        ]
    )


def test_combine_all_already_used(mocker):
    mocker.patch(
        "utils.general.combine",
        side_effect=general_utils.AlreadyUsedError(["JOAO", "SILVA"]),
    )
    NORMALIZED_NAMES = [
        models.NormalizationOutput(original="João Silva", normalized="JOAO SILVA"),
    ]
    assert general_utils.combine_all(NORMALIZED_NAMES) == models.LoginGeneratorOutput(
        data=[]
    )


def test_combine_all():
    names = [
        models.NormalizationOutput(original="João Silva", normalized="JOAO SILVA"),
        models.NormalizationOutput(
            original="Rafael Branwavski Balantimes",
            normalized="RAFAEL BRANWAVSKI BALANTIMES",
        ),
        models.NormalizationOutput(
            original="Rafaela Brandão Balan", normalized="RAFAELA BRANDAO BALAN"
        ),
        models.NormalizationOutput(original="João Silvano", normalized="JOAO SILVANO"),
        models.NormalizationOutput(original="Silval João", normalized="SILVAL JOAO"),
        models.NormalizationOutput(original="João Silva", normalized="JOAO SILVA"),
        models.NormalizationOutput(original="João Silva", normalized="JOAO SILVA"),
        models.NormalizationOutput(original="João Silva", normalized="JOAO SILVA"),
    ]
    output = general_utils.combine_all(names)
    assert len(output.data) == 6
    for result in output.data:
        assert len(result.username) == 7
