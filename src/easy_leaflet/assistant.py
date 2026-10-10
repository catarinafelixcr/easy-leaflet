from dataclasses import dataclass

from pydantic import ValidationError

from easy_leaflet.prompts import PROMPT_V1
from easy_leaflet.schema import parse_llm_output

ERROR_MESSAGE = "Não foi possível gerar uma resposta. Por favor, tente novamente."


# The final answer for the user
@dataclass
class Answer:
    text: str
    found: bool
    sources: list   # the chunks the LLM said it used
    chunks: list    # all the chunks we sent to the LLM


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
        raw_text = self.llm.ask(prompt)

        # Check the format. If the LLM broke the rules, do not show a broken answer.
        try:
            output = parse_llm_output(raw_text)
        except ValidationError as error:
            # The user sees a safe message, but we print the problem for the developer
            print("The LLM answer was not valid JSON:")
            print(raw_text)
            print(error)
            return Answer(text=ERROR_MESSAGE, found=False, sources=[], chunks=chunks)

        # Turn the excerpt numbers (1, 2, 3, 4) into the real chunks
        sources = []
        for number in output.excerpts:
            # Ignore numbers that do not exist (the LLM can make mistakes)
            if 1 <= number <= len(chunks):
                sources.append(chunks[number - 1])

        return Answer(text=output.answer, found=output.found, sources=sources, chunks=chunks)