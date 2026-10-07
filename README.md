# EASY LEAFLET

Ask questions about Portuguese medicine leaflets and get a simple answer, with the original leaflet text as proof.

> **Warning:** This is a study project. It is not medical advice! Always ask your doctor or pharmacist.

**Status:** work in progress. The data is ready; the code is being built.

## Goal

Medicine leaflets are long and hard to read. This app lets a person ask a question in Portuguese (for example, "Posso tomar com álcool?") and answers using only the official leaflet. Each answer shows the part of the leaflet it used, so the person can check it.

## Data

Six official patient leaflets ("folheto informativo") of medicines sold in Portugal. Where possible they come from [Infomed](https://extranet.infarmed.pt/INFOMED-fo/), the public medicine
database of Infarmed.

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

Planned approach: RAG (retrieval-augmented generation).

1. Read the text of each leaflet PDF and cut it into small parts.
2. For each question, find the parts of the leaflet that are most relevant.
3. Send the question and those parts to an LLM, which answers using only    that text and returns JSON.
4. Measure the quality on a test set of questions with expected answers.

## Results

Coming soon.

## Project structure

```
easy-leaflet/
├── data/              leaflets.csv (the PDFs go here, not in Git)
├── src/easy_leaflet/  Python package
├── tests/             PyTest tests
└── README.md
```

## How to run

Coming soon.

## License

MIT