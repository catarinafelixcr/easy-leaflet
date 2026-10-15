import sys

import pandas as pd

# Example: python scripts\compare_results.py results\eval_prompt_v1.csv results\eval_prompt_v1_titles.csv
first_file = sys.argv[1]
second_file = sys.argv[2]
first = pd.read_csv(first_file)
second = pd.read_csv(second_file)

both = first.merge(second, on="id", suffixes=("_a", "_b"))

print(f"A = {first_file}")
print(f"B = {second_file}")
print()
print(f"Accuracy A: {first['correct'].mean():.0%}")
print(f"Accuracy B: {second['correct'].mean():.0%}")
print()

print("Fixed by B (wrong in A, correct in B):")
fixed = both[~both["correct_a"] & both["correct_b"]]
for row in fixed.itertuples():
    print(f"- [{row.id}] {row.question_a}")
print()

print("Broken by B (correct in A, wrong in B):")
broken = both[both["correct_a"] & ~both["correct_b"]]
for row in broken.itertuples():
    print(f"- [{row.id}] {row.question_a}")


def count_words(text):
    return len(str(text).split())


def count_sources(text):
    if pd.isna(text):
        return 0
    return str(text).count(";")


print()
print("Answers that were found (found = True):")
for name, run in [("A", first), ("B", second)]:
    found = run[run["found"]]
    words = found["answer"].apply(count_words).mean()
    sources = found["sources"].apply(count_sources).mean()
    print(f"{name}: {words:.0f} words per answer, {sources:.1f} sources per answer")