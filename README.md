# Evaluation of Goalkeeper Performance at the UEFA Euro 2024 Men's Championship

## Project overview

This project evaluates and compares goalkeeper performances during the UEFA Euro 2024 Men's Championship using Python and StatsBomb Open Data.

The analysis will investigate shot-stopping, distribution, and defensive actions. Metrics and rankings will be calculated from the downloaded event data, with definitions and limitations documented as the project develops.

**Status:** In progress

## Objectives

- Download and inspect UEFA Euro 2024 match and event data.
- Identify goalkeeper-related actions and relevant shot events.
- Develop transparent performance indicators for shot-stopping and distribution.
- Analyse claims, punches, and other defensive actions where the data supports them.
- Compare goalkeeper performances with statistical visualisations.
- Build an interactive dashboard.

## Data source

The project uses [StatsBomb Open Data](https://github.com/statsbomb/open-data).

- Competition ID: `55`
- Season ID: `282`
- Competition: UEFA Euro 2024

Please consult the StatsBomb Open Data repository and its terms before using or redistributing the data.

## Tools

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Plotly
- Requests
- SciPy
- Jupyter

## Planned workflow

1. Download the match list and match event JSON files.
2. Inspect event types, player information, and goalkeeper-related fields.
3. Define and calculate performance metrics.
4. Validate calculations against the source event data.
5. Compare goalkeepers and create visualisations.
6. Develop a dashboard and document findings.

## Planned repository structure

```text
euro-2024-goalkeeper-performance-analysis/
├── data/
│   ├── raw/
│   │   ├── matches/
│   │   └── events/
│   └── processed/
├── notebooks/
├── scripts/
├── dashboards/
├── reports/
├── README.md
└── requirements.txt
```

The data directories are created locally by the download script. Large raw data files are not committed to this repository.

## Running the project

Create and activate a virtual environment, then install dependencies:

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

Install packages and download the data:

```bash
python -m pip install -r requirements.txt
python scripts/download_data.py
python scripts/inspect_data.py
```

## Important methodology note

Goalkeeper metrics depend on clear event definitions and context. Save rates, goals prevented, and goalkeeper rankings will not be presented as verified until the underlying events, shot outcomes, goalkeeper attribution, and calculation methods have been checked.

## Project goal

Build a reproducible, transparent, data-driven evaluation of goalkeeper performance at UEFA Euro 2024 for a football analytics portfolio.
