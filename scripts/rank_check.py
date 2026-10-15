from easy_leaflet.chunker import Chunker
from easy_leaflet.loader import LeafletLoader
from easy_leaflet.retriever import Retriever

loader = LeafletLoader("data")
chunker = Chunker()
chunks = []
for name in loader.list_names():
    chunks.extend(chunker.split(loader.load(name)))

retriever = Retriever()
retriever.index(chunks)

# The 4 failed questions, and a short phrase that only the right chunk contains
checks = [
    (6, "brufen", "Quanto tempo tenho de esperar entre dois comprimidos de Brufen?", "entre as tomas"),
    (7, "brufen", "Quantos comprimidos de Brufen posso tomar no máximo por dia?", "1.200 mg"),
    (23, "minigeste", "Vomitei duas horas depois de tomar a pílula. O que faço?", "vomitar nas 3 a 4 horas"),
    (24, "minigeste", "Fumo e tenho 38 anos. Posso tomar Minigeste?", "tiver mais de 35 anos"),
    (6, "brufen", "Quanto tempo tenho de esperar entre dois comprimidos?", "entre as tomas"),
    (7, "brufen", "Quantos comprimidos posso tomar no máximo por dia?", "1.200 mg"),
]

for question_id, leaflet, question, phrase in checks:
    # How many chunks does this leaflet have?
    total = 0
    for chunk in chunks:
        if chunk.leaflet_name == leaflet:
            total += 1

    # Rank ALL the chunks of the leaflet, then find the first one with the phrase
    ranked = retriever.search(question, k=total, leaflet_name=leaflet)
    rank = None
    for position, chunk in enumerate(ranked, start=1):
        if phrase in chunk.text.lower():
            rank = position
            break

    print(f"[{question_id}] {leaflet}: the right chunk is at rank {rank} of {total}")