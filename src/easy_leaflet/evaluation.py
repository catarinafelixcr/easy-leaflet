import time

import pandas as pd

from easy_leaflet.assistant import ERROR_MESSAGE


def contains_keywords(keywords, text):
    # "a;b" means a AND b must be in the text
    # "a|b" means a OR b is enough
    # Upper or lower case does not matter
    text = text.lower()
    for group in keywords.split(";"):
        found_one = False
        for option in group.split("|"):
            if option.strip().lower() in text:
                found_one = True
        if not found_one:
            return False
    return True


# The worker that asks every test question and checks the answers
class Evaluator:

    def __init__(self, assistant, pause_seconds=4):
        self.assistant = assistant
        self.pause_seconds = pause_seconds

    def evaluate_one(self, question, leaflet_name, answerable, keywords):
        answer = self.assistant.answer(question, leaflet_name=leaflet_name)

        # All the text we sent to the LLM
        context = ""
        for chunk in answer.chunks:
            context += chunk.text + "\n"

        if answerable:
            retrieval_hit = contains_keywords(keywords, context)
            correct = answer.found and contains_keywords(keywords, answer.text)
        else:
            retrieval_hit = None
            correct = not answer.found

        # A broken answer is never correct.
        # Without this, a broken answer to a "no" question would count as correct,
        # because a broken answer also has found = False.
        if answer.text == ERROR_MESSAGE:
            correct = False

        sources = ""
        for chunk in answer.sources:
            sources += f"{chunk.leaflet_name} {chunk.index}; "

        return {
            "found": answer.found, "correct": correct, "retrieval_hit": retrieval_hit,
            "answer": answer.text, "sources": sources,
        }

    def run(self, questions):
        # questions is a pandas DataFrame read from eval_questions.csv
        results = []
        total = len(questions)

        for number, row in enumerate(questions.itertuples(), start=1):
            print(f"[{number}/{total}] {row.leaflet}: {row.question}")
            answerable = row.answerable == "yes"

            try:
                result = self.evaluate_one(row.question, row.leaflet, answerable, row.keywords)
            except Exception as error:
                # For example error 503 or a timeout: record it and continue
                print("   ERROR:", error)
                result = {
                    "found": False, "correct": False,
                    "retrieval_hit": None, "answer": f"ERROR: {error}", "sources": "",
                }

            # Keep the question information next to the result
            result["id"] = row.id
            result["leaflet"] = row.leaflet
            result["topic"] = row.topic
            result["question"] = row.question
            result["answerable"] = answerable
            results.append(result)

            # Wait a little, to stay inside the free API limits
            time.sleep(self.pause_seconds)

        return pd.DataFrame(results)