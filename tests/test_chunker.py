from easy_leaflet.chunker import Chunker
from easy_leaflet.loader import Leaflet


def make_text(length):
    # A text that never repeats: "0000 0001 0002 ..x."
    text = ""
    number = 0
    while len(text) < length:
        text += f"{number:04d} "
        number += 1
    return text[:length]


def test_number_of_chunks():
    # 2600 characters, steps of 800 (1000 - 200): starts at 0, 800, 1600, 2400
    leaflet = Leaflet(name="test", text=make_text(2600))
    chunks = Chunker(max_chars=1000, overlap=200).split(leaflet)
    assert len(chunks) == 4


def test_chunks_overlap():
    # The last 200 characters of a chunk are the first 200 of the next one
    leaflet = Leaflet(name="test", text=make_text(2600))
    chunks = Chunker(max_chars=1000, overlap=200).split(leaflet)
    assert chunks[0].text[-200:] == chunks[1].text[:200]


def test_short_text_gives_one_chunk():
    leaflet = Leaflet(name="test", text=make_text(500))
    chunks = Chunker().split(leaflet)
    assert len(chunks) == 1
    assert chunks[0].text == leaflet.text


def test_empty_text_gives_no_chunks():
    leaflet = Leaflet(name="test", text="")
    chunks = Chunker().split(leaflet)
    assert chunks == []


def test_chunks_keep_name_and_index():
    leaflet = Leaflet(name="benuron", text=make_text(2600))
    chunks = Chunker().split(leaflet)
    assert chunks[2].leaflet_name == "benuron"
    assert chunks[2].index == 2