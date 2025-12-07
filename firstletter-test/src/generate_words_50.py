import os
from wordfreq import top_n_list

# Generate 50-word test file
candidates = top_n_list("en", 100)
filtered = [w.lower() for w in candidates if w.isalpha() and len(w) >= 2]
words = filtered[:50]

os.makedirs("data", exist_ok=True)
with open("data/words_50.txt", "w", encoding="utf-8") as f:
    for word in words:
        f.write(word + "\n")

print(f"Created 50-word test file with {len(words)} words")
print(f"Sample: {words[:5]}")
