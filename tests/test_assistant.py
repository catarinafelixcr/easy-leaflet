from easy_leaflet.assistant import ERROR_MESSAGE, LeafletAssistant
from easy_leaflet.chunker import Chunk


# A fake LLM: always returns the reply we choose, and remembers the prompt
class FakeLLM:

    def __init__(self, reply):
        self.reply = reply
        self.last_prompt = None

    def ask(self, prompt):
        self.last_prompt = prompt
        return self.reply


# A fake retriever: always returns the same chunks, and remembers the leaflet
class FakeRetriever:

    def __init__(self, chunks):
        self.chunks = chunks
        self.last_leaflet_name = None

    def search(self, question, k=4, leaflet_name=None):
        self.last_leaflet_name = leaflet_name
        return self.chunks


def make_chunks():
    chunks = []
    for i in range(4):
        chunks.append(Chunk("benuron", i, f"Texto do excerto {i + 1}"))
    return chunks


def test_found_answer_uses_the_right_source():
    chunks = make_chunks()
    llm = FakeLLM('{"found": true, "answer": "Não beba álcool.", "excerpts": [2]}')
    assistant = LeafletAssistant(FakeRetriever(chunks), llm)

    answer = assistant.answer("Posso beber álcool?", leaflet_name="benuron")

    assert answer.found is True
    assert answer.text == "Não beba álcool."
    assert answer.sources == [chunks[1]]


def test_invalid_llm_reply_gives_error_message():
    llm = FakeLLM("Isto não é JSON")
    assistant = LeafletAssistant(FakeRetriever(make_chunks()), llm)

    answer = assistant.answer("Posso beber álcool?", leaflet_name="benuron")

    assert answer.text == ERROR_MESSAGE
    assert answer.found is False
    assert answer.sources == []


def test_prompt_has_question_and_excerpts():
    llm = FakeLLM('{"found": false, "answer": "Não encontrei.", "excerpts": []}')
    assistant = LeafletAssistant(FakeRetriever(make_chunks()), llm)

    assistant.answer("Posso conduzir?", leaflet_name="benuron")

    assert "Posso conduzir?" in llm.last_prompt
    assert "[Excerto 4]" in llm.last_prompt
    assert "Texto do excerto 4" in llm.last_prompt


def test_search_uses_the_chosen_leaflet():
    retriever = FakeRetriever(make_chunks())
    llm = FakeLLM('{"found": false, "answer": "Não encontrei.", "excerpts": []}')
    assistant = LeafletAssistant(retriever, llm)

    assistant.answer("Posso conduzir?", leaflet_name="zolpidem")

    assert retriever.last_leaflet_name == "zolpidem"


# TODO: your test
# def test_excerpt_number_out_of_range_is_ignored():