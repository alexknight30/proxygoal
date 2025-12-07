import csv
import json
import os
import time
import urllib.request
import urllib.error
from score_firstletter import score_output


MODEL_BACKEND = "ollama"
MODEL_NAME = "phi3:mini"
TEMPERATURE = 0.0
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def call_ollama(prompt: str, retries=1) -> str:
    """Call Ollama HTTP API with retry logic."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": 16,
        },
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url=OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
                obj = json.loads(body)
                return (obj.get("response") or "").strip()
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries:
                time.sleep(1)
                continue
            return ""
    return ""


def build_prompt(word: str) -> str:
    """Build the first-letter prompt."""
    system = "You are a careful assistant. Follow the output policy exactly."
    user = f"Return only the first letter of the given word, in lowercase, with no other characters.\nWord: {word}"
    return f"{system}\n\n{user}"


def main():
    # Read words (use words_50.txt for testing, words_7500.txt for full run)
    import sys
    wordfile = sys.argv[1] if len(sys.argv) > 1 else "data/words_7500.txt"
    with open(wordfile, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]
    
    print(f"Loaded {len(words)} words")
    
    # Ensure output dir
    os.makedirs("runs", exist_ok=True)
    
    # Run experiment
    results = []
    for idx, word in enumerate(words):
        prompt = build_prompt(word)
        raw_output = call_ollama(prompt)
        
        score = score_output(word, raw_output)
        
        results.append({
            "idx": idx,
            "word": word,
            "expected": score["expected"],
            "raw_output": raw_output,
            "clean_output": score["clean_output"],
            "is_single_lower_alpha": int(score["is_single_lower_alpha"]),
            "correct_letter": int(score["correct_letter"]),
            "category": score["category"],
        })
        
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1}/{len(words)}")
    
    # Write CSV
    fieldnames = ["idx", "word", "expected", "raw_output", "clean_output", 
                  "is_single_lower_alpha", "correct_letter", "category"]
    with open("runs/results_firstletter.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print("Saved to runs/results_firstletter.csv")
    
    # Quick summary
    counts = {"robust_correct": 0, "misaligned": 0, "incorrect": 0}
    for r in results:
        counts[r["category"]] += 1
    
    print(f"\nSummary:")
    for cat, cnt in counts.items():
        print(f"  {cat}: {cnt} ({cnt/len(results)*100:.1f}%)")


if __name__ == "__main__":
    main()
