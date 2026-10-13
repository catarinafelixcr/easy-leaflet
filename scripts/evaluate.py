from pathlib import Path

import pandas as pd

from easy_leaflet.assistant import LeafletAssistant
from easy_leaflet.chunker import Chunker
from easy_leaflet.evaluation import Evaluator
from easy_leaflet.llm import LLMClient
from easy_leaflet.loader import LeafletLoader
from easy_leaflet.retriever import Retriever

# Build the system, like in ask.py
loader = LeafletLoader("data")
chunker = Chunker()
chunks = []
for name in loader.list_names():
    chunks.extend(chunker.split(loader.load(name)))

retriever = Retriever()
retriever.index(chunks)
assistant = LeafletAssistant(retriever, LLMClient())

# Ask all the test questions
questions = pd.read_csv("data/eval_questions.csv", encoding="utf-8")
results = Evaluator(assistant).run(questions)

# Summary
answerable = results[results["answerable"]]
not_answerable = results[~results["answerable"]]

print()
print("=== RESULTS: prompt v1 ===")
print(f"Accuracy:           {results['correct'].mean():.0%}  ({results['correct'].sum()} of {len(results)})")
print(f"Answerable:         {answerable['correct'].mean():.0%}")
print(f"Not in leaflet:     {not_answerable['correct'].mean():.0%}")
print(f"Retrieval hit rate: {answerable['retrieval_hit'].astype(float).mean():.0%}")
print()
print("Accuracy by leaflet:")
print(results.groupby("leaflet")["correct"].mean().round(2))
print()
print("Wrong answers:")
for row in results[~results["correct"]].itertuples():
    print(f"- [{row.id}] {row.leaflet}: {row.question}")

# Save everything, to read it later
Path("results").mkdir(exist_ok=True)
results.to_csv("results/eval_prompt_v1.csv", index=False, encoding="utf-8-sig")
print()
print("Saved to results/eval_prompt_v1.csv")