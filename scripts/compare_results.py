import pandas as pd

v1 = pd.read_csv("results/eval_prompt_v1.csv")
v2 = pd.read_csv("results/eval_prompt_v2.csv")

# Put the two runs side by side, one line per question
both = v1.merge(v2, on="id", suffixes=("_v1", "_v2"))

print(f"Accuracy v1: {v1['correct'].mean():.0%}")
print(f"Accuracy v2: {v2['correct'].mean():.0%}")
print()

print("Fixed by v2 (wrong in v1, correct in v2):")
fixed = both[~both["correct_v1"] & both["correct_v2"]]
for row in fixed.itertuples():
    print(f"- [{row.id}] {row.question_v1}")
print()

print("Broken by v2 (correct in v1, wrong in v2):")
broken = both[both["correct_v1"] & ~both["correct_v2"]]
for row in broken.itertuples():
    print(f"- [{row.id}] {row.question_v1}")

def count_words(text):
    return len(str(text).split())


def count_sources(text):
    # sources look like "minigeste 9; minigeste 12; ", so we count the ";"
    if pd.isna(text):
        return 0
    return str(text).count(";")


print()
print("Answers that were found (found = True):")
for name, run in [("v1", v1), ("v2", v2)]:
    found = run[run["found"]]
    words = found["answer"].apply(count_words).mean()
    sources = found["sources"].apply(count_sources).mean()
    print(f"{name}: {words:.0f} words per answer, {sources:.1f} sources per answer")