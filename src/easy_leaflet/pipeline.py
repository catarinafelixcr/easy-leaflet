import pandas as pd

from easy_leaflet.assistant import LeafletAssistant
from easy_leaflet.chunker import Chunker
from easy_leaflet.llm import LLMClient
from easy_leaflet.loader import LeafletLoader
from easy_leaflet.prompts import PROMPT_V1
from easy_leaflet.retriever import Retriever


def load_leaflet_info(csv_path="data/leaflets.csv"):
    # One row per leaflet: name, medicine, url, dates...
    return pd.read_csv(csv_path)


def build_assistant(data_dir="data", prompt=PROMPT_V1, use_titles=True):
    # Read and cut all the leaflets
    loader = LeafletLoader(data_dir)
    chunker = Chunker()
    chunks = []
    for name in loader.list_names():
        chunks.extend(chunker.split(loader.load(name)))

    # The search, with the medicine name in every chunk (our final choice)
    retriever = Retriever()
    if use_titles:
        titles = {}
        for row in load_leaflet_info(f"{data_dir}/leaflets.csv").itertuples():
            titles[row.name] = row.medicine
        retriever.index(chunks, titles=titles)
    else:
        retriever.index(chunks)

    return LeafletAssistant(retriever, LLMClient(), prompt=prompt)