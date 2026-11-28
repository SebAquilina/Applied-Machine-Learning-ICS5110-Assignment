"""Build Matthias's private Q51 review extract and a country-level audit table."""

import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd


FREQUENCY = {1: "Often", 2: "Sometimes", 3: "Rarely", 4: "Never"}
HEALTH = {1: "Very good", 2: "Good", 3: "Fair", 4: "Poor", 5: "Very poor"}
EMPLOYMENT = {
    1: "Full-time employed", 2: "Part-time employed", 3: "Self-employed",
    4: "Retired", 5: "Homemaker", 6: "Student", 7: "Unemployed", 8: "Other",
}
INPUTS = {
    "Q262": "Q262_age_years",
    "Q275": "Q275_education_ISCED_0_to_8",
    "Q279": "Q279_employment_status",
    "Q288": "Q288_relative_household_income_1_to_10",
    "Q50": "Q50_financial_satisfaction_1_to_10",
    "Q47": "Q47_self_rated_health",
    "Q54": "Q54_went_without_cash_income",
}
RESPONSE_CODES = {
    "Q51": FREQUENCY, "Q275": range(9), "Q279": EMPLOYMENT,
    "Q288": range(1, 11), "Q50": range(1, 11), "Q47": HEALTH, "Q54": FREQUENCY,
}
MISSING_CODES = [-1, -2, -4, -5]


def review_tables(source):
    metadata = ["version", "doi", "A_STUDY", "A_WAVE", "B_COUNTRY_ALPHA", "A_YEAR", "W_WEIGHT", "S018"]
    items = ["Q51", *INPUTS]
    # Preserve the source precision of both weights when writing the CSV.
    raw = pd.read_csv(source, usecols=metadata + items, dtype=str, keep_default_na=False)
    if raw.empty or not (
        raw["version"].str.startswith("6-0-0 ").all()
        and raw["doi"].eq("doi.org/10.14281/18241.24").all()
        and raw["A_STUDY"].eq("2").all()
        and raw["A_WAVE"].eq("7").all()
    ):
        raise ValueError("Expected the WVS Wave 7 cross-national v6.0 CSV.")
    if raw[["B_COUNTRY_ALPHA", "A_YEAR"]].eq("").any().any():
        raise ValueError("A survey sample or year is missing.")

    original = raw[items].replace("", pd.NA).astype("Int64")
    clean = original.mask(original.isin(MISSING_CODES))
    for field, allowed in RESPONSE_CODES.items():
        unexpected = clean[field].dropna().loc[lambda s: ~s.isin(list(allowed))]
        if not unexpected.empty:
            raise ValueError(f"Unexpected {field} codes: {sorted(unexpected.unique())}")
    if clean["Q262"].dropna().le(0).any():
        raise ValueError("Unexpected nonpositive age after removing missing codes.")

    review = raw[["B_COUNTRY_ALPHA", "A_YEAR"]].copy()
    review["Q51_original_code"] = original["Q51"]
    review["Q51_food_shortage_response"] = clean["Q51"].map(FREQUENCY)
    labels = {"Q279": EMPLOYMENT, "Q47": HEALTH, "Q54": FREQUENCY}
    for field, heading in INPUTS.items():
        review[heading] = clean[field].map(labels[field]) if field in labels else clean[field]
    review[["W_WEIGHT", "S018"]] = raw[["W_WEIGHT", "S018"]]

    valid_target = clean["Q51"].notna()
    tally = pd.DataFrame(index=raw.index)
    tally["respondents"] = 1
    tally["valid_Q51"] = valid_target
    tally["missing_Q51"] = ~valid_target
    for code, label in FREQUENCY.items():
        tally[f"Q51_{label.lower()}"] = clean["Q51"].eq(code).fillna(False)
    for field in INPUTS:
        tally[f"valid_Q51_missing_{field}"] = valid_target & clean[field].isna()
    tally["valid_Q51_complete_seven_inputs"] = valid_target & clean[list(INPUTS)].notna().all(axis=1)
    by_country = tally.groupby([raw["B_COUNTRY_ALPHA"], raw["A_YEAR"]], sort=True).sum().reset_index()
    return review, by_country


def write_csv(table, destination):
    # Stage on the same filesystem so an interrupted write cannot truncate an existing CSV.
    with TemporaryDirectory(dir=destination.parent) as staging:
        temporary = Path(staging) / "output.csv"
        table.to_csv(temporary, index=False, lineterminator="\n")
        temporary.replace(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Original WVS v6.0 CSV")
    parser.add_argument("review_csv", type=Path, help="Private respondent-level output, kept outside public Git")
    parser.add_argument("country_csv", type=Path, help="Aggregate count output by survey sample and year")
    args = parser.parse_args()
    paths = [args.source.resolve(), args.review_csv.resolve(), args.country_csv.resolve()]
    if len(set(paths)) != len(paths):
        parser.error("Choose distinct source and output files.")
    if not all(path.parent.is_dir() for path in paths[1:]):
        parser.error("Create the output directories before running.")
    review, by_country = review_tables(args.source)
    write_csv(review, args.review_csv)
    write_csv(by_country, args.country_csv)
    print(f"Review rows: {len(review):,}; survey samples: {len(by_country):,}; "
          f"valid Q51 responses: {by_country.valid_Q51.sum():,}")


if __name__ == "__main__":
    main()
