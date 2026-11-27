# Data preparation for reported food shortages

[Download the editable Word section with both figures](Q51_data_preparation.docx?raw=1)

These figures accompany Section 3, Data Preparation. Both use the 96,704 respondents who answered World Values Survey question Q51. The percentages describe the pooled, unweighted sample.

## How often did respondents report going without enough food?

![Q51 responses in the previous 12 months. Often 3,958, sometimes 10,933, rarely 15,041, never 66,772.](q51_responses.png)

**Figure 1.** The four-category member dataset preserves “never” (class 0), “rarely” (1), “sometimes” (2) and “often” (3). The 15,041 people who answered “rarely” have their own class. “Never” is the largest class (66,772) and “often” is the smallest (3,958), so an overall accuracy score can obscure how well a model identifies frequent shortages. [Target codes and dataset](../README.md)

## Which questions had the most missing answers?

![Missing responses for the six inputs. Income 2,805, employment 1,134, education 980, age 502, financial satisfaction 493 and self-rated health 178.](missing_predictors.png)

**Figure 2.** Relative household income was the question most often skipped (2.90%). A respondent can appear in several bars. Requiring all six answers would remove 5,107 people (5.28%) and leave 91,597. Missing-answer flags allow all 96,704 to be retained.

## Source and reproduction

The figures use the [counts by survey sample](../q51_by_country.csv) from [World Values Survey Wave 7, v6.0.0](https://doi.org/10.14281/18241.24). The [member log](../log.md) records the cleaning and weighting checks.

To regenerate both 300 dpi PNGs, run the following command from the repository root with pandas and Matplotlib installed.

```bash
python work/muscat/report/make_figures.py
```
