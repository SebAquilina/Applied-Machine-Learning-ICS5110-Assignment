# Matthias Muscat · Q51 food shortage data

[Open the cleaned CSV in Google Drive (Matthias's private copy)](https://drive.google.com/file/d/1fd0KxumeZjYCFpVEgWpSIyoCUAYt2xvJ/view?usp=drivesdk)

[View the two cleaning graphs and download the Word section for the group report](report/)

**What changed.** The World Values Survey Wave 7 v6.0 file contains 97,220 respondents. Removing 516 people with no usable Q51 answer leaves **96,704 people across 66 country or territory samples**. The cleaned file keeps respondents who skipped an input. Six background questions produce **18 numeric model inputs**, including missing-answer indicators. All 18 can be passed directly to scikit-learn.

**Working definition for the group to review.** The default target is 1 when a respondent said they or their family **often, sometimes or rarely** went without enough food in the past 12 months, and 0 for **never**. That gives 29,932 positive and 66,772 negative examples. The alternative definition counts only “sometimes” and “often” as positive, giving 14,891 positives on the same rows. [Team discussion](https://github.com/SebAquilina/Applied-Machine-Learning-ICS5110-Assignment/issues/3#issuecomment-7171698228)

## Rebuild the CSV

Team members with the original survey can generate their own copy. From the repository root, run this after placing the team CSV at the path described in [PR #1](https://github.com/SebAquilina/Applied-Machine-Learning-ICS5110-Assignment/pull/1). The script uses pandas and NumPy.

```bash
python work/muscat/clean_q51.py 04_data/raw/WVS_Cross-National_Wave_7_csv_v6_0.csv
```

The output is `work/muscat/private/ICS5110_Q51_clean_any_shortage.csv`. The public repository stores the code and aggregate results. The Drive link uses the file owner's access controls. The default CSV's SHA-256 is `d1ac155065ce09e51dd20c102fa7e7bf5d33f5e1fb6b4e6758637085585d9c5e`.

Add `--target sometimes-often` to generate a separate file for the stricter definition. If you already have the exact review CSV produced by [review_q51.py](review_q51.py), pass that file and add `--from-review` to get the same output.

## Use the model inputs

```python
import pandas as pd

data = pd.read_csv("work/muscat/private/ICS5110_Q51_clean_any_shortage.csv")
X = data.filter(regex="^x_")           # six questions encoded into 18 numeric columns
y = data["target_any_shortage"]        # one outcome per respondent
```

| Field | What it supplies |
|---|---|
| Q262, age | Age in years |
| Q275, education | International education scale, 0–8. A reported zero is a valid answer. |
| Q288, household income | Self-reported position on the country's income scale, 1–10 |
| Q50, financial satisfaction | Satisfaction with household finances, 1 low to 10 high |
| Q47, self-rated health | 1 very good, 2 good, 3 fair, 4 poor, 5 very poor |
| Q279, employment | Binary columns for codes 2–8 (part-time, self-employed, retired, homemaker, student, unemployed, other). Full-time work is the reference. Missing employment has its own flag. |

For the five numeric or ordered inputs, a missing answer has value 0 and a matching `_missing` flag of 1. All recorded responses have flag 0, including the 4,869 valid education zeros. These fixed rules retain **5,107** respondents who skipped at least one of the six background questions. They can be applied before selecting a split because they use no averages or other quantities learned from the data.

**Optional comparison.** The two `optional_` columns encode Q54, frequency of going without cash income (1 often to 4 never), and its missing flag. Add them together only for the comparison that includes same-period cash hardship. The five `meta_` columns hold the original one-based data-record number, survey sample, year and two survey weights. Keep them separate from `X` for split alignment, weighting and subgroup analysis.

The script preserves source order and leaves the team’s train/test split open. Fit any scaling, imputation or tuning that uses data on training folds when the team agrees its evaluation protocol. [Cleaning decisions and verification](log.md#26-november-2026--cleaning-for-machine-learning)
