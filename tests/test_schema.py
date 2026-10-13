import pytest
from pydantic import ValidationError

from easy_leaflet.schema import parse_llm_output


def test_good_json():
    output = parse_llm_output('{"found": true, "answer": "Sim.", "excerpts": [1, 2]}')
    assert output.found is True
    assert output.answer == "Sim."
    assert output.excerpts == [1, 2]


def test_json_inside_code_fences():
    raw = '```json\n{"found": false, "answer": "Não encontrei.", "excerpts": []}\n```'
    output = parse_llm_output(raw)
    assert output.found is False
    assert output.excerpts == []


def test_wrong_type_is_rejected():
    with pytest.raises(ValidationError):
        parse_llm_output('{"found": "talvez", "answer": "Não sei.", "excerpts": []}')


def test_missing_field_is_rejected():
    with pytest.raises(ValidationError):
        parse_llm_output('{"found": true, "answer": "Sim."}')


def test_text_that_is_not_json_is_rejected():
    with pytest.raises(ValidationError):
        parse_llm_output("Desculpe, não consigo responder.")