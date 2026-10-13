from easy_leaflet.evaluation import contains_keywords


def test_one_keyword_found():
    assert contains_keywords("álcool", "Não beba álcool.") is True


def test_one_keyword_missing():
    assert contains_keywords("álcool", "Pode tomar com comida.") is False


def test_upper_case_does_not_matter():
    assert contains_keywords("álcool", "ÁLCOOL é perigoso.") is True


def test_and_needs_all_keywords():
    assert contains_keywords("álcool;fígado", "O álcool faz mal.") is False


def test_or_needs_only_one_option():
    assert contains_keywords("8 horas|oito horas", "Espere oito horas.") is True


def test_part_of_a_word_is_enough():
    assert contains_keywords("amament", "Não tome se estiver a amamentar.") is True