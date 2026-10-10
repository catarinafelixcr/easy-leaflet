from easy_leaflet.assistant import LeafletAssistant
from easy_leaflet.chunker import Chunker
from easy_leaflet.llm import LLMClient
from easy_leaflet.loader import LeafletLoader
from easy_leaflet.retriever import Retriever

# Load and cut all leaflets
loader = LeafletLoader("data")
chunker = Chunker()
chunks = []
for name in loader.list_names():
    chunks.extend(chunker.split(loader.load(name)))

# Build the search index
retriever = Retriever()
retriever.index(chunks)

# Create the assistant one time
assistant = LeafletAssistant(retriever, LLMClient())

# The questions to try: (question, leaflet)
questions = [
    ("Posso beber álcool?", "benuron"),
    ("Posso conduzir depois de tomar?", "zolpidem"),
    ("Quanto custa a embalagem?", "benuron"),
]

for question, leaflet_name in questions:
    answer = assistant.answer(question, leaflet_name=leaflet_name)

    print()
    print("PERGUNTA:", question, f"({leaflet_name})")
    print("ENCONTRADO:", answer.found)
    print("RESPOSTA:", answer.text)
    print("FONTES USADAS:")
    for chunk in answer.sources:
        print("-", chunk.leaflet_name, chunk.index)