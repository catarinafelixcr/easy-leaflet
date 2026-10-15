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

question = "Vomitei duas horas depois de tomar a pílula. O que faço?"
for chunk in retriever.search(question, k=4, leaflet_name="minigeste"):
    text = chunk.text.lower()
    print(f"chunk {chunk.index}: has 'vomit' = {'vomit' in text}, has 'esquec' = {'esquec' in text}")

# How many Minigeste chunks contain each word?
count_vomit = 0
count_esquec = 0
for chunk in chunks:
    if chunk.leaflet_name == "minigeste":
        if "vomit" in chunk.text.lower():
            count_vomit += 1
        if "esquec" in chunk.text.lower():
            count_esquec += 1
print(f"Minigeste chunks with 'vomit': {count_vomit}, with 'esquec': {count_esquec}")