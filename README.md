# UEFA Euro 2024 Goalkeeper Performance Analysis

A football analytics project evaluating goalkeeper performance during the UEFA Euro 2024 Men's Championship using [StatsBomb Open Data](https://github.com/statsbomb/open-data).

## Project overview

The project evaluates goalkeeper performance through shot-stopping, expected goals, defensive actions, and distribution. The analysis described in the project report includes descriptive comparisons, correlation analysis, Z-score standardisation, and goalkeeper dashboards.

The individual dashboard compares four selected goalkeepers, including Manuel Neuer, from an individual player-performance perspective. It is not presented as a ranking of the tournament's top four goalkeepers.

## Analysis objectives

- Evaluate shot-stopping using shots faced, saves, goals conceded, and save percentage.
- Examine expected goals (xG) faced and Goals Saved Above Expectation (GSaE).
- Explore defensive actions such as sweeping actions, claims, and punches.
- Analyse goal-kick distribution, including short and long goal kicks and average kick length.
- Explore relationships between selected performance indicators using correlation analysis.
- Standardise metrics with Z-scores to support comparisons across different measurement scales.
- Present overall and individual goalkeeper comparisons in dashboards.

## Selected metrics

| Performance area | Indicators |
|---|---|
| Shot-stopping | Shots faced, saves, goals conceded, save percentage |
| Expected goals | xG faced, Goals Saved Above Expectation (GSaE) |
| Defensive actions | Sweeping actions, claims, punches |
| Distribution | Goal kicks, short/long goal kicks, average goal-kick length |

In this project, GSaE is defined as:

`GSaE = xG faced - goals conceded`

A positive value means goals conceded were lower than xG faced; a negative value means goals conceded were higher than xG faced.

## Selected findings from the project report

- Save percentage and GSaE: `r = 0.522`, `p = 0.009`.
- xG faced and goals conceded: `r = 0.763`, `p < 0.001`.
- Goal kicks per match and average goal-kick length: `r = 0.581`, `p = 0.003`.
- Shots faced and save percentage: `r = -0.018`, `p = 0.935`.
- Koen Casteels recorded a reported 93.3% save rate across 57 shots faced.
- Unai Simón recorded a reported GSaE of +2.94.

Correlation describes association and does not establish causation. Individual metrics should be interpreted in context, including shot quality, minutes played, team defensive structure, and the definitions used in the analysis.

## Dashboards

- **Overall goalkeeper dashboard:** overview of the selected goalkeeper performance indicators.
- **Individual goalkeeper dashboard:** comparison of four selected goalkeepers, including Manuel Neuer, using indicators such as save percentage, GSaE, xG faced, and distribution performance.

The dashboards and full project presentation are described in the project report. Dashboard source files and exported dashboard images are not currently present in this repository.

## Data source

The project uses StatsBomb Open Data for UEFA Euro 2024.

- Competition ID: `55`
- Season ID: `282`
- Season ID and competition metadata can be checked in the [StatsBomb Open Data repository](https://github.com/statsbomb/open-data).

Please follow StatsBomb's data terms and attribution requirements. Raw event data is downloaded locally and is not committed to this repository.

## Repository contents

```text
.
├── scripts/
│   ├── download_data.py
│   └── inspect_data.py
├── .gitignore
├── README.md
└── requirements.txt
```

### Scripts

- `scripts/download_data.py` downloads the UEFA Euro 2024 match list and match event JSON files from StatsBomb Open Data into `data/raw/`.
- `scripts/inspect_data.py` prints a basic overview of the downloaded match list and inspects event columns and event types from the first available match file.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/prashanthk7/euro-2024-goalkeeper-performance-analysis.git
cd euro-2024-goalkeeper-performance-analysis
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Download and inspect the data

Run these commands from the repository root:

```bash
python scripts/download_data.py
python scripts/inspect_data.py
```

The downloader skips event files that already exist and reports match files that failed to download so they can be retried by running the script again.

## Methodology and limitations

- Goalkeeper performance is affected by shot quality, match context, playing time, and team defensive structure.
- Event-data definitions and goalkeeper attribution affect calculated metrics.
- Z-scores support comparison across differently scaled indicators but do not, by themselves, create a definitive overall ranking.
- Correlation indicates association, not causation.
- This repository currently contains data-download and data-inspection scripts. It does not yet contain the full analysis notebooks, dashboard implementation, or dashboard exports.

## Author

Prashanth Kodipally

## Acknowledgement

Data source: [StatsBomb Open Data](https://github.com/statsbomb/open-data).
