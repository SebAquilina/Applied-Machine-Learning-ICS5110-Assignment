"""Aggregate metrics and portable outputs for Matthias's Q51 classification experiment."""

import hashlib
import json

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, recall_score

from q51_model_data import CODES, FEATURES, LABELS


def assignment_digest(frame):
    """Hash the ordered CSV including its header, using LF line endings."""
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode()).hexdigest()


def multiclass_scores(observed, predicted, weights=None):
    return {
        "accuracy": float(accuracy_score(observed, predicted, sample_weight=weights)),
        "macro_f1": float(f1_score(observed, predicted, labels=CODES, average="macro",
                                  zero_division=0, sample_weight=weights)),
        "macro_recall": float(recall_score(observed, predicted, labels=CODES, average="macro",
                                           zero_division=0, sample_weight=weights)),
        "mean_absolute_class_error": float(mean_absolute_error(observed, predicted, sample_weight=weights)),
    }


def alert_counts(observed, scores, threshold):
    """Illustrative costs for a recurring shortage: two units per miss, one per false alarm."""
    observed = np.asarray(observed) >= 2
    flagged = np.asarray(scores) >= threshold
    if observed.shape != flagged.shape:
        raise ValueError("Expected one recurring-shortage score per respondent.")
    hits = int((observed & flagged).sum())
    misses = int((observed & ~flagged).sum())
    false_alarms = int((~observed & flagged).sum())
    return {
        "threshold": float(threshold), "respondents": int(observed.size),
        "hits": hits, "misses": misses, "false_alarms": false_alarms,
        "correct_negatives": int((~observed & ~flagged).sum()),
        "illustrative_cost": 2 * misses + false_alarms,
    }


def choose_alert(observed, oof_scores):
    rows = [alert_counts(observed, oof_scores, step / 100) for step in range(0, 101, 5)]
    # A tie goes to the higher cutoff, which flags fewer or the same number of respondents.
    chosen = min(rows, key=lambda r: (r["illustrative_cost"], -r["threshold"]))
    return rows, chosen["threshold"]


def export_model(pipeline, dataset_hash, split_hash):
    scaler = pipeline.named_steps["standardscaler"]
    classifier = pipeline.named_steps["logisticregression"]
    return {
        "type": "StandardScaler + multinomial LogisticRegression (L2, lbfgs)",
        "dataset_sha256": dataset_hash, "split_sha256": split_hash, "features": FEATURES,
        "classes": classifier.classes_.tolist(), "class_labels": LABELS,
        "C": float(classifier.C), "class_weight": classifier.class_weight,
        "scaler_mean": scaler.mean_.tolist(), "scaler_scale": scaler.scale_.tolist(),
        "coefficients": classifier.coef_.tolist(), "intercepts": classifier.intercept_.tolist(),
        "inference": "Standardise the features in the listed order. Multiply by the transposed coefficient matrix, add the intercepts and apply row-wise softmax.",
    }


def save_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def save_confusion_plot(matrix, destination):
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    supports = matrix.sum(axis=1, keepdims=True)
    rates = np.divide(matrix, supports, out=np.zeros(matrix.shape, dtype=float), where=supports != 0)
    palette = LinearSegmentedColormap.from_list("q51_frequency", ["#f4f8fa", "#80b9c3", "#15465d"])
    fig = plt.figure(figsize=(7.2, 5.25), facecolor="white")
    fig.text(0.065, 0.96, "How often did the model predict each answer?", va="top",
             fontsize=15, fontweight="bold", color="#172e3b")
    fig.text(0.065, 0.885, f"Held-out survey respondents (n = {matrix.sum():,}). "
             "Percentages are within each actual answer.", fontsize=9.4, color="#375260")
    ax = fig.add_axes([0.275, 0.16, 0.68, 0.62])
    ax.imshow(rates, vmin=0, vmax=1, cmap=palette, aspect="auto", interpolation="nearest")
    ax.set_xticks(range(len(LABELS)), LABELS, fontsize=10)
    ax.set_yticks(range(len(LABELS)), LABELS, fontsize=10)
    ax.set_xlabel("Model prediction", fontsize=10, fontweight="bold", labelpad=10)
    ax.set_ylabel("Actual survey answer", fontsize=10, fontweight="bold", labelpad=9)
    ax.tick_params(length=0, pad=7, colors="#243b46")
    for i, j in np.ndindex(rates.shape):
        foreground = "white" if rates[i, j] > 0.69 else "#152d39"
        ax.text(j, i, f"{matrix[i,j]:,}\n{rates[i,j]:.1%}", ha="center", va="center",
                fontsize=10.2, color=foreground, fontweight="bold" if i == j else "normal")
    for edge in np.arange(0.5, len(LABELS) - 0.5, 1):
        ax.axhline(edge, color="white", linewidth=1.3)
        ax.axvline(edge, color="white", linewidth=1.3)
    ax.spines[:].set_visible(False)
    fig.savefig(destination, dpi=220, facecolor="white", metadata={"Software": "Matplotlib"})
    plt.close(fig)
