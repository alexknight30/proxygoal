import argparse
import csv
import os
import random
from datetime import datetime, timezone


UNITS = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"
]
TENS = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
]


def int_to_words(n: int) -> str:
    if n < 0:
        return "minus " + int_to_words(-n)
    if n < 20:
        return UNITS[n]
    if n < 100:
        tens, rem = divmod(n, 10)
        return TENS[tens] + ("-" + UNITS[rem] if rem else "")
    if n < 1000:
        h, rem = divmod(n, 100)
        if rem == 0:
            return UNITS[h] + " hundred"
        return UNITS[h] + " hundred " + int_to_words(rem)
    # Fallback for larger numbers
    return str(n)


def op_to_words(op: str) -> str:
    return "+" == op and "plus" or ("-" == op and "minus" or op)


def build_questions(n: int, a_min: int, a_max: int, ops: list[int | str], seed: int) -> list[dict]:
    rng = random.Random(seed)
    now = datetime.now(timezone.utc).isoformat()
    questions = []
    for i in range(n):
        a = rng.randint(a_min, a_max)
        b = rng.randint(a_min, a_max)
        op = rng.choice(ops)
        if op == "+":
            correct = a + b
        elif op == "-":
            correct = a - b
        else:
            raise ValueError(f"Unsupported op: {op}")
        digits = f"{a} {op} {b}"
        words = f"{int_to_words(a)} {op_to_words(op)} {int_to_words(b)}"
        questions.append({
            "question_id": f"q_{i+1:04d}",
            "question_digits": digits,
            "question_words": words,
            "correct_answer": correct,
            "op": op,
            "a": a,
            "b": b,
            "seed": seed,
            "created_at": now,
        })
    return questions


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate math QA dataset CSV")
    parser.add_argument("--out", required=True, help="Output CSV path")
    parser.add_argument("--n", type=int, required=True, help="Number of questions")
    parser.add_argument("--min", dest="amin", type=int, required=True, help="Min integer value")
    parser.add_argument("--max", dest="amax", type=int, required=True, help="Max integer value")
    parser.add_argument("--ops", nargs="+", default=["+", "-"], help="Allowed ops, e.g., + -")
    parser.add_argument("--seed", type=int, default=1234)
    args = parser.parse_args()

    questions = build_questions(args.n, args.amin, args.amax, args.ops, args.seed)
    ensure_parent_dir(args.out)

    fieldnames = [
        "question_id", "question_digits", "question_words", "correct_answer",
        "op", "a", "b", "seed", "created_at"
    ]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(questions)

    print(args.out)


if __name__ == "__main__":
    main()


