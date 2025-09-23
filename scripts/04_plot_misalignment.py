import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot stacked robust/misaligned/incorrect by variant")
    parser.add_argument("--summary", required=True, help="Path to summary CSV (results/tables/summary_*.csv)")
    parser.add_argument("--out", required=True, help="Output PNG path")
    args = parser.parse_args()

    df = pd.read_csv(args.summary)

    # Expect columns: model, prompt_variant, n, naive_acc, robust_acc, misaligned_rate, avg_latency_ms
    df = df.sort_values(["prompt_variant"])  # normal, proxy, shifted

    robust = df["robust_acc"].values
    misaligned = df["misaligned_rate"].values
    incorrect = 1.0 - df["naive_acc"].values  # fails even naive

    labels = df["prompt_variant"].tolist()

    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(len(labels))

    ax.bar(x, robust, label="robust correct", color="#2ca02c")
    ax.bar(x, misaligned, bottom=robust, label="misaligned (naive-only)", color="#ff7f0e")
    ax.bar(x, incorrect, bottom=robust + misaligned, label="incorrect", color="#7f7f7f")

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Proportion of questions")
    ax.set_title("Outcome breakdown by prompt variant")
    ax.legend()
    plt.tight_layout()

    ensure_parent_dir(args.out)
    plt.savefig(args.out)
    print(args.out)


if __name__ == "__main__":
    main()


