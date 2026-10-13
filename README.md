# EASY LEAFLET

Ask questions about Portuguese medicine leaflets and get a simple answer, with the original leaflet text as proof.

> **Warning:** This is a study project. It is not medical advice! Always ask your doctor or pharmacist.

**Status:** work in progress. The question-answering pipeline works end to end and has tests. The evaluation is being run; the demo comes next.

## Goal

Medicine leaflets are long and hard to read. This app lets a person ask a question in Portuguese (for example, "Posso tomar com álcool?") and answers using only the official leaflet. Each answer shows the part of the leaflet it used, so the person can check it.

## Data

Six official patient leaflets ("folheto informativo") of medicines sold in Portugal. Where possible they come from [Infomed](https://extranet.infarmed.pt/INFOMED-fo/), the public medicine database of Infarmed.

| Medicine | Active substance | Leaflet date | Source |
|---|---|---|---|
| Ben-u-ron 500 mg | paracetamol | 03/2026 | Manufacturer |
| Brufen 200 mg | ibuprofeno | not stated | Infomed |
| Cêgripe 500 mg + 1 mg | paracetamol + clorofenamina | 02/2025 | Infomed |
| Imodium Rapid 2 mg | loperamida | not stated | Infomed |
| Minigeste | etinilestradiol + gestodeno | 12/2021 | Manufacturer |
| Zolpidem Aurovitas 10 mg | zolpidem | 11/2021 | Third-party site |

The PDF files are not in this repository. The links are in [`data/leaflets.csv`](data/leaflets.csv). To use the project, download each PDF and save it in `data/` with the name from the `name` column (for example `data/benuron.pdf`).

Leaflets change over time. The versions used here may not be the current ones!

## Method

The app uses RAG (retrieval-augmented generation): the LLM answers from the leaflet text, not from its memory.

```
question + chosen medicine
        │
        ▼
1. Search: find the 4 most similar parts of that leaflet
        │
        ▼
2. Prompt: question + the 4 parts + rules ("use only this text")
        │
        ▼
3. LLM: answers in JSON {found, answer, excerpts}
        │
        ▼
4. Validation: check the JSON; keep only the parts the LLM really used
        │
        ▼
answer + the leaflet text that proves it
```

| Part | Choice | Why |
|---|---|---|
| PDF reading | `pdfplumber` | `pypdf` put spaces inside words in one leaflet |
| Chunks | 1000 characters, 200 overlap (about 180 chunks) | About one small topic per chunk; fits the embedding model |
| Embeddings | `intfloat/multilingual-e5-small` | Free, runs locally, understands Portuguese |
| Search | Cosine similarity, top 4, **only inside the medicine the user chose** | Without this filter, a question about alcohol returned parts of three different leaflets |
| LLM | Google Gemini (`gemini-3.5-flash-lite`, free tier) | Free; the model name is a parameter, so it is easy to change |
| Output | JSON validated with Pydantic | The app knows if the answer was found and which parts were used; broken LLM output is refused safely |

The link to the original leaflet is taken from `data/leaflets.csv`, never written by the LLM, so it cannot be changed by mistake.

## Evaluation

The test set is [`data/eval_questions.csv`](data/eval_questions.csv): 30 questions written from the leaflets, 5 per medicine.

- 24 questions have the answer in the leaflet. Each has the leaflet sentence that proves it, and one or more keywords that a correct answer must contain.
- 6 questions have no answer in the leaflet (price, comparisons between brands, and similar). A correct answer must say "not found".
- Questions are written like a patient would ask them, not with the leaflet's own words.

Two numbers are measured:

- **Accuracy:** the share of questions with a correct final answer.
- **Retrieval hit rate:** for answerable questions, the share where the search found the text with the answer. This shows if an error comes from the search or from the LLM.

The test set was written and checked by a person against the PDFs, not by an LLM, so the LLM is not checking its own exam.

## Results

Coming soon: accuracy of prompt version 1, then a comparison with prompt version 2.

## Tests

The code has PyTest tests for the chunker, the JSON validation, the keyword check and the RAG assistant. The assistant is tested with a fake LLM and a fake search, so the tests are fast, free, need no internet and always give the same result.

```
pytest -v
```

## Limitations

- **Keyword checking is simple.** A correct answer that uses different words can be counted as wrong, and an answer can contain the keyword and still be incomplete. Wrong answers are also checked by hand.
- **Small test set.** 30 questions give a useful signal, not a precise number.
- **PDF text is messy.** Tables lose their columns and some words are joined, so questions about tables are harder.
- **Some leaflets are old** or come from non-official sites (see the Data table).

## Project structure

```
easy-leaflet/
├── data/              leaflets.csv, eval_questions.csv (the PDFs go here, not in Git)
├── docs/              API_KEY.md (how to get and protect the API key)
├── results/           evaluation results (one CSV per run)
├── scripts/           ask.py, evaluate.py and small try-out scripts
├── src/easy_leaflet/  Python package (loader, chunker, retriever, LLM client, assistant, evaluation)
├── tests/             PyTest tests
├── .env.example       shows which secret the project needs
└── README.md
```

## How to run

1. Clone the repository and open the folder.
2. Create a virtual environment and install the project with the developer tools (Windows PowerShell):

   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -e ".[dev]"
   ```

3. Download the leaflet PDFs listed in [`data/leaflets.csv`](data/leaflets.csv) and save them in `data/` with the names from the `name` column.
4. Create a free Gemini API key in [Google AI Studio](https://aistudio.google.com/api-keys). No credit card is needed.
5. Copy `.env.example` to a new file called `.env` and paste your key in it. The full guide, with the free limits and the safety rules, is in [`docs/API_KEY.md`](docs/API_KEY.md).
6. Ask a few questions:

   ```
   python scripts\ask.py
   ```

7. Run the evaluation (about 3 minutes):

   ```
   python scripts\evaluate.py
   ```

8. Run the tests:

   ```
   pytest -v
   ```

The first run downloads the embedding model (about 470 MB) once.

## License

MIT
