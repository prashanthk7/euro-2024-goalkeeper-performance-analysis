# UEFA Euro 2024 Goalkeeper Performance Analysis

A reproducible reconstruction of a UEFA Euro 2024 goalkeeper analytics project using StatsBomb Open Data. The project examines shot-stopping, goalkeeper actions, and distribution, with player-level summaries, correlation analysis, standardized comparisons, and an interactive dashboard.

**Author:** Prashanth Kodipally

> **Reconstruction notice:** The original analysis scripts and dashboard files were lost. This repository rebuilds the workflow using the surviving project presentation as a reference. The recreated code and outputs are not represented as the original implementation or exact reproduction of its results.

## Project objectives

- Explore goalkeeper performance beyond traditional counts.
- Summarize shots faced, saves, goals conceded, and expected goals faced where event attribution is available.
- Calculate save percentage and Goals Saved Above Expectation (GSaE = xG faced − goals conceded).
- Describe claims, punches, sweeper actions, and goal-kick distribution.
- Compare selected goalkeepers with Z-score standardized metrics.
- Explore selected relationships using Pearson correlation.
- Present individual player comparisons in an interactive dashboard.

The individual dashboard can be used to examine four selected goalkeepers, including Manuel Neuer, from an individual player-performance perspective. The selection is user-controlled; it is not a claim that the four are the tournament's top four.

## Data source

The data downloader uses the public [StatsBomb Open Data](https://github.com/statsbomb/open-data) repository and targets UEFA Euro 2024 (competition ID 55, season ID 282). Raw event JSON is downloaded locally and is excluded from Git.

Please review and comply with the StatsBomb Open Data terms and attribution requirements before reusing or redistributing the data.

## Metrics and definitions

| Metric | Project definition |
|---|---|
| Save percentage | Saves from goalkeeper events ÷ explicitly attributed shots × 100 |
| xG faced | Sum of StatsBomb shot xG for shots explicitly linked to a goalkeeper |
| Goals conceded | Count of attributed shots with outcome Goal |
| GSaE | Attributed xG faced − attributed goals conceded |
| Claims | Goalkeeper events whose action label contains Claim or Collected |
| Punches | Goalkeeper events whose action label contains Punch |
| Sweeper actions | Goalkeeper events whose action label contains Sweeper |
| Goal-kick volume | Count of passes with pass type Goal Kick |
| Average goal-kick length | Mean Euclidean distance between event start and pass end locations |
| Z-score | Standardized value across goalkeepers for each metric |

**Important data limitation:** StatsBomb event feeds do not necessarily provide a goalkeeper link for every shot. This reconstruction deliberately includes only explicit links and does not guess the responsible goalkeeper. Consequently, attributed shot counts, save rates, xG faced, and GSaE can differ from the original presentation or from other data providers. The code exports event-level tables so coverage can be audited. Do not compare players or make strong claims when attribution coverage is low.

## Repository structure

```text
.
├── .github/workflows/python-checks.yml
├── app.py
├── requirements.txt
├── scripts/
│   ├── download_data.py
│   └── inspect_data.py
├── src/
│   ├── build_analysis.py
│   └── manual_mlp.py
└── tests/
    ├── test_manual_mlp.py
    └── test_scripts.py
```

## Setup

Python 3.11 or newer is recommended.

```bash
git clone https://github.com/prashanthk7/euro-2024-goalkeeper-performance-analysis.git
cd euro-2024-goalkeeper-performance-analysis

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Download and inspect the data

```bash
python scripts/download_data.py
python scripts/inspect_data.py
```

The downloader retrieves the Euro 2024 match list and match event files into `data/raw/`. The raw data directory is git-ignored.

## Build the analysis tables

```bash
python -m src.build_analysis
```

CSV outputs are written to `data/processed/`:

- `matches.csv`
- `shots.csv`
- `goalkeeper_events.csv`
- `goal_kicks.csv`
- `goalkeeper_summary.csv`

The summary includes player-level counts, derived metrics, and Z-scores. Inspect the exported shot table and attribution note before interpreting goalkeeper-level results.

## Run the dashboard

```bash
streamlit run app.py
```

The dashboard provides:
- Player selection and a metric table.
- Individual save-percentage and GSaE comparisons.
- xG faced versus goals conceded.
- Z-score comparisons across the selected metrics.
- Pearson correlation summaries when enough complete observations exist.

## Manual neural network implementation

The original presentation identifies a manual neural-network component, but it does not preserve the model architecture, prediction target, feature list, training procedure, or evaluation results. To make the repository useful without inventing those details, `src/manual_mlp.py` provides a transparent, generic one-hidden-layer regression MLP implemented with NumPy: forward propagation, ReLU activation, mean-squared-error loss, manual backpropagation, and mini-batch gradient descent.

This is a **new educational reconstruction**, not evidence of the original network or its results. It is not trained on tournament goalkeeper data by default. A domain-specific model should only be configured after its target variable, input features, sample size, and evaluation plan have been established.

## Tests

```bash
python -m unittest discover -s tests -v
python -m compileall -q scripts src app.py
```

GitHub Actions runs automated Python checks on pushes and pull requests to `main`.

## Analysis notes

The surviving presentation reports selected correlations, including save percentage versus GSaE and xG faced versus goals conceded. Those figures are historical presentation results, not outputs verified by this reconstructed pipeline. This repository recalculates descriptive correlations from its own generated summary and does not include the unpublished one-sample hypothesis-testing section.

## Acknowledgements

- [StatsBomb Open Data](https://github.com/statsbomb/open-data) for the event data.
- UEFA Euro 2024 tournament data contributors.

