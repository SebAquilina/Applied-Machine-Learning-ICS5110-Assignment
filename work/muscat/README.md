# Matthias Muscat · Q51 food shortage data

[Download the four-category CSV from Matthias’s private Google Drive](https://drive.google.com/file/d/1UCF87lgEG38w1EhA2LnCVSkCG2zPgbBd/view?usp=drivesdk)

[Open Matthias’s four-category logistic regression notebook](../../03_code/03_logistic_regression_muscat.ipynb)

[View the two cleaning graphs and download the Word section for the group report](report/)

**What changed.** The World Values Survey Wave 7 v6.0 file contains 97,220 respondents. Removing 516 people with no usable Q51 answer leaves **96,704 people across 66 country or territory samples**. The cleaned file keeps respondents who skipped an input. Six background questions produce **18 numeric model inputs**, including missing-answer indicators. All 18 can be passed directly to scikit-learn.

**What the model predicts.** How often did the respondent or their family go without enough food in the previous 12 months? Matthias chose to keep all four Q51 answers for this version. The target column is `target_frequency`. Higher class numbers mean more frequent shortages. The class numbers express order and do not specify how many times a shortage occurred. [Team discussion](https://github.com/SebAquilina/Applied-Machine-Learning-ICS5110-Assignment/issues/3#issuecomment-7213984459)

| Output class | Q51 answer | Original WVS code | Respondents | Share of valid answers |
|---:|---|---:|---:|---:|
| 0 | Never | 4 | 66,772 | 69.05% |
| 1 | Rarely | 3 | 15,041 | 15.55% |
| 2 | Sometimes | 2 | 10,933 | 11.31% |
| 3 | Often | 1 | 3,958 | 4.09% |

These are unweighted counts and percentages. The “often” class is the smallest, so report its performance separately when comparing techniques. The team still needs to agree on the split and evaluation protocol for its shared comparison.

## Rebuild the CSV

Team members with the original survey can generate their own copy. From the repository root, run this after placing the team CSV at the path described in [PR #1](https://github.com/SebAquilina/Applied-Machine-Learning-ICS5110-Assignment/pull/1). The script uses pandas and NumPy.

```bash
python work/muscat/clean_q51.py 04_data/raw/WVS_Cross-National_Wave_7_csv_v6_0.csv
```

The output is `work/muscat/private/ICS5110_Q51_clean_frequency.csv`. The [dataset record](q51_dataset.json) lists its filename, SHA-256 checksum, 18 input columns, class counts, private download and rebuild command. The public repository stores the code and aggregates. The respondent CSV is kept private because WVS restricts redistribution of its data files. [WVS conditions of use](https://www.worldvaluessurvey.org/AJDownloadLicense.jsp)

The default is `--target frequency`. To reproduce the earlier binary comparisons, use `--target any` for any reported shortage or `--target sometimes-often` for shortages reported sometimes or often. Each option writes a separate file. If you have the exact review CSV produced by [review_q51.py](review_q51.py), pass that file with `--from-review` to reproduce the same output.

## Use the model inputs

```python
import pandas as pd

data = pd.read_csv("work/muscat/private/ICS5110_Q51_clean_frequency.csv")
X = data.filter(regex="^x_")           # six questions encoded into 18 numeric columns
y = data["target_frequency"]           # 0 never, 1 rarely, 2 sometimes, 3 often
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

The script preserves source order. Use the same split for every model and fit any scaling, imputation or tuning on training folds. Run `python work/muscat/test_clean_q51.py` to check the code mapping on a small example. [Four-category cleaning decisions and verification](log.md#27-november-2026--four-category-q51-dataset)

## Run the logistic regression notebook

Open the [notebook](../../03_code/03_logistic_regression_muscat.ipynb) in Jupyter and select **Run All**. From a fresh checkout, its default run fits a model to 600 fictional respondents and shows probabilities for the four answers, overall and per-class metrics, a confusion matrix and a threshold comparison. It was checked with Python 3.12.14, scikit-learn 1.8.0, pandas 2.2.3 and NumPy 2.3.5.

For the survey experiment, put the CSV at the rebuild path above and change `DATA_SOURCE` from `"demo"` to `"survey"`. The loader checks the dataset fingerprint before fitting. If the team adopts the proposed split, `SPLIT_CSV = None` reproduces it. It sorts by the source-row key, stratifies by the four answers and uses seed 42. This gives 77,363 training respondents and 19,341 test respondents. To use another shared split, set `SPLIT_CSV` to a CSV containing `meta_source_row` and `split` (train or test). The model fits the scaler on the training set and uses the held-out set for evaluation. [Shared split proposal](https://github.com/SebAquilina/Applied-Machine-Learning-ICS5110-Assignment/issues/3#issuecomment-7214244801)
