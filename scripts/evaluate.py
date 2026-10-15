from pathlib import Path
import sys

import pandas as pd

from easy_leaflet.assistant import LeafletAssistant
from easy_leaflet.chunker import Chunker
from easy_leaflet.evaluation import Evaluator
from easy_leaflet.llm import LLMClient
from easy_leaflet.loader import LeafletLoader
from easy_leaflet.retriever import Retriever
from easy_leaflet.prompts import PROMPT_V1, PROMPT_V2

# Build the system, like in ask.py
loader = LeafletLoader("data")
chunker = Chunker()
chunks = []
for name in loader.list_names():
    chunks.extend(chunker.split(loader.load(name)))

retriever = Retriever()
# Search with medicine names? "python scripts\evaluate.py v1 titles"
use_titles = len(sys.argv) > 2 and sys.argv[2] == "titles"
if use_titles:
    leaflets = pd.read_csv("data/leaflets.csv")
    titles = {}
    for row in leaflets.itertuples():
        titles[row.name] = row.medicine
    retriever.index(chunks, titles=titles)
else:
    retriever.index(chunks)
    
#assistant = LeafletAssistant(retriever, LLMClient())
if len(sys.argv) > 1:
    version = sys.argv[1]
else:
    version = "v1"
prompts = {"v1": PROMPT_V1, "v2": PROMPT_V2}
assistant = LeafletAssistant(retriever, LLMClient(), prompt=prompts[version])

run_name = f"prompt_{version}"
if use_titles:
    run_name += "_titles"

# Ask all the test questions
questions = pd.read_csv("data/eval_questions.csv", encoding="utf-8")
results = Evaluator(assistant).run(questions)

# Summary
# Questions with API errors were never answered, so they are not counted
errors = results["error"].sum()
valid = results[~results["error"]]
answerable = valid[valid["answerable"]]
not_answerable = valid[~valid["answerable"]]

print()
print(f"=== RESULTS: {run_name} ===")
print(f"API errors:         {errors} of {len(results)} (not counted below)")
if errors > 0:
    print("WARNING: some questions failed. Run again before trusting these numbers.")
print(f"Accuracy:           {valid['correct'].mean():.0%}  ({valid['correct'].sum()} of {len(valid)})")
print(f"Answerable:         {answerable['correct'].mean():.0%}")
print(f"Not in leaflet:     {not_answerable['correct'].mean():.0%}")
print(f"Retrieval hit rate: {answerable['retrieval_hit'].astype(float).mean():.0%}")
print()

# Save everything, to read it later
Path("results").mkdir(exist_ok=True)
results.to_csv(f"results/eval_{run_name}.csv", index=False, encoding="utf-8-sig")
print()
print(f"Saved to results/eval_{run_name}.csv")