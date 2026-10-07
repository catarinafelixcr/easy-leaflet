from easy_leaflet.chunker import Chunker
from easy_leaflet.loader import LeafletLoader
from easy_leaflet.retriever import Retriever

# Load and cut all leaflets
loader = LeafletLoader("data")
chunker = Chunker()
chunks = []
for name in loader.list_names():
    chunks.extend(chunker.split(loader.load(name)))

# Build the index and search
retriever = Retriever()
retriever.index(chunks)

question = "Posso beber álcool?"
for chunk in retriever.search(question, leaflet_name="benuron"):
    print("=====", chunk.leaflet_name, chunk.index)
    print(chunk.text[:300])