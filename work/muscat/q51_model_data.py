"""Load the four-category Q51 model inputs and align a respondent-level split."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from clean_q51 import make_table
from review_q51 import EMPLOYMENT, FREQUENCY, HEALTH, INPUTS


MEMBER = Path(__file__).resolve().parent
DATASET = json.loads((MEMBER / "q51_dataset.json").read_text(encoding="utf-8"))
FEATURES = DATASET["features"]
TARGET = DATASET["target"]
KEY = DATASET["row_key"]
CODES = [item["code"] for item in DATASET["classes"]]
LABELS = [item["label"] for item in DATASET["classes"]]


def load_survey(path):
    """Verify the dataset version used for the model and for row-level split alignment."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}. Rebuild it with: {DATASET['rebuild_from_repository_root']}")
    with path.open("rb") as source:
        if hashlib.file_digest(source, "sha256").hexdigest() != DATASET["sha256"]:
            raise ValueError("This CSV differs from the four-category dataset in q51_dataset.json.")
        source.seek(0)
        return pd.read_csv(source)


def proposed_split(data):
    """80/20 split stratified by Q51, seeded after sorting by the stable source-row key."""
    ordered = data.sort_values(KEY)
    _, test_keys = train_test_split(
        ordered[KEY], test_size=0.20, random_state=42, stratify=ordered[TARGET],
    )
    return pd.DataFrame({
        KEY: ordered[KEY], "split": np.where(ordered[KEY].isin(test_keys), "test", "train"),
    }).reset_index(drop=True)


def align_split(data, assignments):
    """Match private train/test assignments to data rows, independently of file order."""
    if not {KEY, "split"}.issubset(assignments.columns):
        raise ValueError(f"The split CSV needs columns {KEY} and split.")
    for keys in (data[KEY], assignments[KEY]):
        if keys.hasnans or not keys.is_unique or not pd.api.types.is_integer_dtype(keys) or keys.le(0).any():
            raise ValueError(f"{KEY} must contain a unique positive integer for each respondent.")
    groups = assignments.set_index(KEY)["split"]
    if groups.isna().any() or set(groups) != {"train", "test"}:
        raise ValueError("The split must contain both train and test and use only those values.")
    matched = data[KEY].map(groups)
    if len(data) != len(groups) or matched.isna().any():
        raise ValueError("The split and dataset must cover exactly the same source rows.")
    if not data[TARGET].isin(CODES).all() or set(data.loc[matched.eq("train"), TARGET]) != set(CODES):
        raise ValueError("Use the four Q51 classes and include each class in the training data.")
    return matched.rename("split")


def example_data():
    """Generate fictional survey answers for a reproducible end-to-end notebook run."""
    rng = np.random.default_rng(5110)
    n = 600
    income = rng.integers(1, 11, n)
    finances = rng.integers(1, 11, n)
    # This invented relationship gives the example a signal that a classifier can learn.
    score = (6 - income) * 0.4 + (6 - finances) * 0.2 + rng.logistic(size=n)
    frequency = np.digitize(score, [0.6, 1.6, 2.6])
    review = pd.DataFrame({
        "Q51_original_code": 4 - frequency, "B_COUNTRY_ALPHA": "SIM", "A_YEAR": 2020,
        "W_WEIGHT": "1", "S018": "1", INPUTS["Q262"]: rng.integers(18, 91, n),
        INPUTS["Q275"]: rng.integers(0, 9, n), INPUTS["Q279"]: rng.choice(list(EMPLOYMENT.values()), n),
        INPUTS["Q288"]: income, INPUTS["Q50"]: finances, INPUTS["Q47"]: rng.choice(list(HEALTH.values()), n),
        INPUTS["Q54"]: rng.choice(list(FREQUENCY.values()), n),
    })
    for column in INPUTS.values():
        review.loc[rng.random(n) < 0.03, column] = pd.NA
    return make_table(review, "frequency")
