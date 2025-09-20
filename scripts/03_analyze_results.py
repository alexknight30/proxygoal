import argparse
import glob
import os
from collections import defaultdict

import pandas as pd


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate misalignment experiment results")
    parser.add_argument("--runs", required=True, help="Glob for run CSVs, e.g., data/runs/run_*.csv")
    parser.add_argument("--out-table", required=True)
    parser.add_argument("--out-figure", required=False)
    args = parser.parse_args()

    files = sorted(glob.glob(args.runs))
    if not files:
        raise SystemExit("No run files matched")

    frames = [pd.read_csv(p) for p in files]
    df = pd.concat(frames, ignore_index=True)

    group_cols = ["model", "prompt_variant"]
    summary = (
        df.groupby(group_cols)
        .agg(
            n=("question_id", "count"),
            naive_acc=("naive_eval_pass", "mean"),
            robust_acc=("robust_eval_pass", "mean"),
            misaligned_rate=("misaligned", "mean"),
            avg_latency_ms=("latency_ms", "mean"),
        )
        .reset_index()
    )

    ensure_parent_dir(args.out_table)
    summary.to_csv(args.out_table, index=False)
    print(args.out_table)

    if args.out_figure:
        import matplotlib.pyplot as plt

        ensure_parent_dir(args.out_figure)
        variants = sorted(summary["prompt_variant"].unique())
        models = sorted(summary["model"].unique())

        fig, ax = plt.subplots(figsize=(8, 4))
        width = 0.35
        x = range(len(variants))

        for i, model in enumerate(models):
            sub = summary[summary["model"] == model].set_index("prompt_variant").loc[variants]
            ax.bar([xi + i * width for xi in x], sub["robust_acc"].values, width, label=f"{model} robust")
            ax.bar([xi + i * width for xi in x], sub["naive_acc"].values, width, bottom=sub["robust_acc"].values * 0, alpha=0.3, label=f"{model} naive")

        ax.set_xticks([xi + (len(models) - 1) * width / 2 for xi in x])
        ax.set_xticklabels(variants)
        ax.set_ylim(0, 1.0)
        ax.set_ylabel("Accuracy")
        ax.set_title("Naive vs Robust Accuracy by Prompt Variant")
        ax.legend()
        plt.tight_layout()
        plt.savefig(args.out_figure)
        print(args.out_figure)


if __name__ == "__main__":
    main()


