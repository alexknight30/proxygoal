import os
import random
from wordfreq import top_n_list


def main():
    random.seed(42)
    
    # Fetch top 20k English words
    candidates = top_n_list("en", 20000)
    
    # Filter: alphabetic only, lowercase, length >= 2
    filtered = [
        w.lower() for w in candidates
        if w.isalpha() and len(w) >= 2
    ]
    
    # Dedupe and take first 7500
    unique = list(dict.fromkeys(filtered))[:7500]
    
    # Ensure output dir exists
    os.makedirs("data", exist_ok=True)
    
    # Write to file
    with open("data/words_7500.txt", "w", encoding="utf-8") as f:
        for word in unique:
            f.write(word + "\n")
    
    print(f"Generated {len(unique)} unique words")
    print(f"Sample: {unique[:10]}")
    print("Saved to data/words_7500.txt")


if __name__ == "__main__":
    main()
