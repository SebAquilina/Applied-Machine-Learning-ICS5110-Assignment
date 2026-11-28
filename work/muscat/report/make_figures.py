"""Draw the report figures from the checked-in survey-sample counts."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd


HERE = Path(__file__).resolve().parent
ACCENT = "#116F70"
SLATE = "#526B80"
INK = "#182D3B"


def bar_chart(counts, denominator, title, subtitle, highlight, ticks, xmax, decimals, output):
    """Bar lengths are unweighted percentages. Labels give the exact counts."""
    height = 0.90 + 0.29 * len(counts)
    fig = plt.figure(figsize=(7.0, height), facecolor="white")
    fig.text(0.005, 1 - 0.045 / height, title, va="top", fontsize=12.5, weight="bold", color=INK)
    fig.text(0.005, 1 - 0.275 / height, subtitle, va="top", fontsize=9.1, color="#415462")
    ax = fig.add_axes([0.315, 0.26 / height, 0.673, (height - 0.79) / height])
    shares = counts * 100 / denominator
    colors = [ACCENT if name == highlight else SLATE for name in counts.index]
    bars = ax.barh(range(len(counts)), shares, height=0.57, color=colors, zorder=3)
    ax.set_yticks(range(len(counts)), labels=counts.index)
    ax.set_ylim(len(counts) - 0.5, -0.5)
    ax.set_xlim(0, xmax)
    ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}%"))
    ax.tick_params(axis="x", length=0, pad=4, labelsize=8.5, colors="#516471")
    ax.tick_params(axis="y", length=0, pad=7, labelsize=10, colors=INK)
    ax.spines[:].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#D9E0E3", linewidth=0.65)
    for bar, (name, count) in zip(bars, counts.items()):
        ax.annotate(
            f"{shares[name]:.{decimals}f}%  ({count:,})",
            (bar.get_width(), bar.get_y() + bar.get_height() / 2),
            xytext=(5, 0), textcoords="offset points", va="center", fontsize=9.4,
            weight="bold" if name == highlight else "normal", color=INK,
        )
    fig.savefig(output, dpi=300, facecolor="white", metadata={"Software": "Matplotlib"})
    plt.close(fig)


def main():
    samples = pd.read_csv(HERE.parent / "q51_by_country.csv")
    names = ["Often", "Sometimes", "Rarely", "Never"]
    response_columns = [f"Q51_{name.lower()}" for name in names]
    if not samples[response_columns].sum(axis=1).equals(samples["valid_Q51"]):
        raise ValueError("Q51 response counts must reconcile within every survey sample.")
    total = int(samples["valid_Q51"].sum())
    note = f"Unweighted share of {total:,} respondents who answered Q51"
    responses = samples[response_columns].sum().set_axis(names)
    bar_chart(
        responses, total, "Reported frequency of food shortages in the past year", note,
        "Rarely", [0, 20, 40, 60], 100, 1, HERE / "q51_responses.png",
    )

    questions = {
        "Q288": "Relative household income", "Q279": "Employment status",
        "Q275": "Education", "Q262": "Age",
        "Q50": "Financial satisfaction", "Q47": "Self-rated health",
    }
    fields = [f"valid_Q51_missing_{code}" for code in questions]
    missing = samples[fields].sum().set_axis(questions.values()).sort_values(ascending=False)
    bar_chart(
        missing, total, "Missing answers for the six baseline predictors", note,
        missing.index[0], [0, 1, 2, 3], 4.25, 2, HERE / "missing_predictors.png",
    )


if __name__ == "__main__":
    main()
