from models import NormalizationOutput


def test_remove_stop_words(nlp_instance):
    assert nlp_instance.remove_stop_words("João da Silva") == "João Silva"
    assert nlp_instance.remove_stop_words("João dos Santos") == "João Santos"
    assert nlp_instance.remove_stop_words("João de Jesus") == "João Jesus"
    assert nlp_instance.remove_stop_words("João do Nascimento") == "João Nascimento"


def test_remove_stop_words_without_stop_words(nlp_instance):
    assert (
        nlp_instance.remove_stop_words("João Destro Dante Donizete Dasmes")
        == "João Destro Dante Donizete Dasmes"
    )


def test_remove_accent_marks(nlp_instance):
    assert (
        nlp_instance.remove_accent_marks(
            "João Pajé Camaleão Björn Caçador Menêzes Àgora"
        )
        == "Joao Paje Camaleao Bjorn Cacador Menezes Agora"
    )


def test_normalize(nlp_instance):
    assert (
        nlp_instance.normalize(
            " João Pajé de Camaleão da Björn dos Caçadores do Menêzes Àgora  "
        )
        == "JOAO PAJE CAMALEAO BJORN CACADORES MENEZES AGORA"
    )


def test_normalize_many(nlp_instance):
    names = [" João Pajé de Camaleão", "Björn dos Caçadores ", " Menêzes Àgora "]
    expected_output = [
        NormalizationOutput(original=name, normalized=nlp_instance.normalize(name))
        for name in names
    ]

    assert expected_output == nlp_instance.normalize_many(names)
