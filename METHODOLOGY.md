# Methodology

This document records the method as described in the supplied Soccer Analytics presentation. It does not add undocumented processing steps.

## Data source and variables

The presentation names **StatsBomb Euro 2024 open event data** as the data source.

Variables listed in the presentation:

- Shots faced
- Saves
- Expected goals faced (xG faced)
- Goals conceded
- Sweeper actions
- Claims
- Punches
- Goal kicks (short and long)

## Derived measures

**Save percentage**

\[
\text{Save \%} = \frac{\text{saves}}{\text{shots on target}}
\]

**Goals Saved Above Expectation (GSaE)**

\[
\text{GSaE} = \text{xG faced} - \text{goals conceded}
\]

The presentation interprets a higher GSaE as better performance relative to the xG expectation.

## Standardization

The presentation states that goalkeeper measures were standardized using **Z-scores**, with a higher score representing better performance. It also includes a goalkeeper Z-score comparison.

The slide deck does not provide the full variable-weighting scheme, missing-value treatment, exact standardization population, or all cutoffs. These should be documented before attempting an exact reproduction.

## Statistical analysis

The presentation lists:

- Correlation: save percentage versus GSaE
- One-sample t-test on GSaE
- Matches played versus save percentage

It also reports additional pairwise correlations for xG faced versus goals conceded, shots faced versus save percentage, sweeper actions per match versus claims per match, and goal kicks per match versus average kick length.

The supplied slides do not specify the full t-test null hypothesis, test statistic, degrees of freedom, confidence intervals, or sample-size details. These are intentionally not inferred here.

## Reproduction requirements

For a reproducible implementation, retain and document:

1. The exact StatsBomb Euro 2024 files and event filters used.
2. The goalkeeper inclusion criteria and minimum playing-time threshold, if any.
3. The operational definitions for shots on target, saves, claims, punches, sweeper actions, and goal kicks.
4. The aggregation level (match, goalkeeper, or tournament) for each metric.
5. Missing-data handling and per-match normalization rules.
6. Z-score reference population, direction, and any composite weights.
7. Statistical test hypotheses, assumptions, sample sizes, and software versions.
8. The exact scripts and commands used to generate every table and figure.

These details are not fully available in the supplied presentation, so this repository does not claim exact computational reproducibility yet.
