from dataclasses import dataclass

from easy_leaflet.prompts import PROMPT_V1


# The answer and the chunks that were used to write it
@dataclass
class Answer:
    text: str
    chunks: list


# The worker that joins the search and the LLM (this is the RAG part)
class LeafletAssistant:

    def __init__(self, retriever, llm, prompt=PROMPT_V1, k=4):
        self.retriever = retriever
        self.llm = llm
        self.prompt = prompt
        self.k = k
        
    def build_prompt(self, question, chunks):
        # Put the chunks together in one text, each with a small label
        context = ""
        for number, chunk in enumerate(chunks, start=1):
            context += f"[Excerto {number}]\n{chunk.text}\n\n"
        return self.prompt.format(context=context, question=question)
    
    def answer(self, question, leaflet_name):
        # R: find the best chunks, only in the chosen leaflet
        chunks = self.retriever.search(question, k=self.k, leaflet_name=leaflet_name)

        # A: put the chunks in the prompt
        prompt = self.build_prompt(question, chunks)

        # G: the LLM writes the answer
        text = self.llm.ask(prompt)
        return Answer(text=text, chunks=chunks)