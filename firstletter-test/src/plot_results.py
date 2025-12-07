import pandas as pd
import matplotlib.pyplot as plt
import os


def main():
    df = pd.read_csv("runs/results_firstletter.csv")
    
    total = len(df)
    counts = df["category"].value_counts()
    
    p_correct = counts.get("robust_correct", 0) / total
    p_misaligned = counts.get("misaligned", 0) / total
    p_incorrect = counts.get("incorrect", 0) / total
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.bar([0], [p_correct], label="robust correct", color="#2ca02c")
    ax.bar([0], [p_misaligned], bottom=[p_correct], label="misaligned (format)", color="#ff7f0e")
    ax.bar([0], [p_incorrect], bottom=[p_correct + p_misaligned], label="incorrect", color="#7f7f7f")
    
    ax.set_xticks([0])
    ax.set_xticklabels(["first_letter"])
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Proportion of questions")
    ax.set_title("Outcome breakdown for first-letter task")
    ax.legend()
    plt.tight_layout()
    
    os.makedirs("runs", exist_ok=True)
    plt.savefig("runs/plot_firstletter.png")
    print("Saved to runs/plot_firstletter.png")
    
    print(f"\nProportions:")
    print(f"  robust_correct: {p_correct:.4f}")
    print(f"  misaligned: {p_misaligned:.4f}")
    print(f"  incorrect: {p_incorrect:.4f}")


if __name__ == "__main__":
    main()
