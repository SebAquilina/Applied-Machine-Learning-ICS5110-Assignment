"""Build Matthias's model-ready Q51 data from WVS Wave 7 v6.0."""

import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

from review_q51 import EMPLOYMENT, FREQUENCY, HEALTH, INPUTS, review_tables, write_csv


DEFINITIONS = {
    "any": ("any_shortage", (1, 2, 3)),
    "sometimes-often": ("sometimes_or_often", (1, 2)),
}
REVIEW_SHA256 = "80da1b8b0ed8d51fa94fa5ada9488d35df3d06ac1e86214d6f81f702f0b2094b"
PRIVATE_DIR = Path(__file__).resolve().parent / "private"


def load_review(source, from_review):
    if not from_review:
        review, _ = review_tables(source)
        return review

    # This shortcut relies on the same release and row order as the audited extract.
    if hashlib.sha256(source.read_bytes()).hexdigest() != REVIEW_SHA256:
        raise ValueError("The review CSV differs from the audited extract. Use the original team CSV without --from-review.")
    return pd.read_csv(source, dtype={"W_WEIGHT": str, "S018": str})


def encode_item(output, name, values):
    """The flag distinguishes a fixed zero placeholder from an observed zero."""
    output[name] = values.fillna(0).astype(int)
    output[f"{name}_missing"] = values.isna().astype(int)


def make_table(review, definition):
    suffix, positives = DEFINITIONS[definition]
    labelled = review.loc[review["Q51_original_code"].isin(FREQUENCY)]
    output = pd.DataFrame(index=labelled.index)
    output[f"target_{suffix}"] = labelled["Q51_original_code"].isin(positives).astype(int)

    for field, name in [
        ("Q262", "x_age"), ("Q275", "x_education"), ("Q288", "x_income"),
        ("Q50", "x_financial_satisfaction"),
    ]:
        encode_item(output, name, labelled[INPUTS[field]])

    health_codes = {label: code for code, label in HEALTH.items()}
    encode_item(output, "x_health", labelled[INPUTS["Q47"]].map(health_codes))

    employment = labelled[INPUTS["Q279"]]
    # Full-time employment is the reference. Code 8 ("other") is a valid category.
    for code, label in EMPLOYMENT.items():
        if code != 1:
            output[f"x_employment_{code}"] = employment.eq(label).fillna(False).astype(int)
    output["x_employment_missing"] = employment.isna().astype(int)

    cash_codes = {label: code for code, label in FREQUENCY.items()}
    encode_item(output, "optional_cash_shortage", labelled[INPUTS["Q54"]].map(cash_codes))

    # One-based record ordinal, excluding the header, before filtering the source.
    output["meta_source_row"] = labelled.index + 1
    output["meta_country"] = labelled["B_COUNTRY_ALPHA"]
    output["meta_year"] = labelled["A_YEAR"]
    output["meta_W_WEIGHT"] = labelled["W_WEIGHT"]
    output["meta_S018"] = labelled["S018"]

    weights = output[["meta_W_WEIGHT", "meta_S018"]].astype(float)
    if not np.isfinite(weights).all().all() or weights.le(0).any().any():
        raise ValueError("Expected finite positive survey weights.")
    if output.isna().any().any() or not output["meta_source_row"].is_unique:
        raise ValueError("Missing output value or duplicated source-row key.")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Original WVS Wave 7 v6.0 CSV")
    parser.add_argument("--from-review", action="store_true", help="Use the audited private review CSV")
    parser.add_argument("--target", choices=DEFINITIONS, default="any", help="Which Q51 responses count as positive")
    parser.add_argument("--output", type=Path, help="Optional CSV path. The default is under work/muscat/private/")
    args = parser.parse_args()
    suffix, _ = DEFINITIONS[args.target]
    destination = args.output or PRIVATE_DIR / f"ICS5110_Q51_clean_{suffix}.csv"
    if destination.resolve() == args.source.resolve():
        parser.error("The source and output must be different files.")
    review = load_review(args.source, args.from_review)
    output = make_table(review, args.target)
    destination.parent.mkdir(parents=True, exist_ok=True)
    write_csv(output, destination)
    positives = int(output[f"target_{suffix}"].sum())
    print(f"Saved {destination} with {len(output):,} labelled records and {positives:,} positives.")
    print(f"Removed {len(review) - len(output):,} records without a valid Q51 response.")


if __name__ == "__main__":
    main()
