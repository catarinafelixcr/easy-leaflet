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

# Ask a question
assistant = LeafletAssistant(retriever, LLMClient())
question = "Posso beber álcool?"
answer = assistant.answer(question, leaflet_name="benuron")
print()
print("PERGUNTA:", question)
print("RESPOSTA:", answer.text)
print()
print("EXCERTOS USADOS:")
for chunk in answer.chunks:
    print("-", chunk.leaflet_name, chunk.index)
#print(assistant.build_prompt(question, answer.chunks))

# Ask a question
assistant = LeafletAssistant(retriever, LLMClient())
question = "Posso conduzir depois de tomar?"
answer = assistant.answer(question, leaflet_name="zolpidem")
print()
print("PERGUNTA:", question)
print("RESPOSTA:", answer.text)
print()
print("EXCERTOS USADOS:")
for chunk in answer.chunks:
    print("-", chunk.leaflet_name, chunk.index)
#print(assistant.build_prompt(question, answer.chunks))

# Ask a question
assistant = LeafletAssistant(retriever, LLMClient())
question = "Quanto custa a embalagem?"
answer = assistant.answer(question, leaflet_name="benuron")
print()
print("PERGUNTA:", question)
print("RESPOSTA:", answer.text)
print()
print("EXCERTOS USADOS:")
for chunk in answer.chunks:
    print("-", chunk.leaflet_name, chunk.index)
#print(assistant.build_prompt(question, answer.chunks))