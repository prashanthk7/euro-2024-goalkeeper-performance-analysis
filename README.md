# UEFA Euro 2024 Goalkeeper Performance Analysis

A reproducible soccer analytics portfolio project reconstructing the evaluation of goalkeeper performance at the UEFA Euro 2024 Men's Championship using StatsBomb Open Data.

**Author:** Prashanth Kodipally

> **Reconstruction notice:** The original analysis scripts and raw files were lost. This repository rebuilds the workflow from the surviving presentation and public StatsBomb event data. The recreated code and outputs are not represented as the original implementation or an exact reproduction of the original results.

## Four individual goalkeeper dashboards

The Streamlit dashboard now features the top three tournament goalkeepers by reconstructed GSaE (minimum four matches with goalkeeper events): Unai Simón, Koen Casteels and Jan Oblak, plus Manuel Neuer as a comparison profile. This is a transparent GSaE shortlist, not a universal goalkeeper ranking. The original report's historical profile names and scores are retained as source-reported material below:

1. **Koen Casteels** — original report Z-score: 1.05
2. **Unai Simón** — original report Z-score: 0.70
3. **Fehmi Mert Günok** — original report Z-score: 0.61
4. **Predrag Rajković** — original report Z-score: 0.57

These Z-scores are transcribed from the original presentation; they are not recalculated results. If the reconstructed event data does not resolve a goalkeeper's linked events, the dashboard displays a transparent missing-data message rather than inventing values.

## Research question

Which goalkeepers at Euro 2024 performed best across shot-stopping, sweeping and distribution, and can data-driven metrics reveal performance value beyond traditional statistics?

## Data source

The downloader targets the official [StatsBomb Open Data](https://github.com/hudl/open-data) repository for UEFA Euro 2024 (competition ID **55**, season ID **282**). Hudl StatsBomb confirms the release covers all 51 matches and identifies these IDs for access: [official release note](https://www.hudl.com/blog/statsbomb-release-free-euro-2024-data).

StatsBomb requests that published research and visualizations identify StatsBomb as the data source and use its logo. Please review the data repository terms and StatsBomb user agreement before publishing.

## Metrics and definitions

- Save percentage = saves / (saves + goals conceded) × 100, based on explicitly attributed shots.
- Shots faced = shots explicitly linked to a goalkeeper.
- xG faced = sum of StatsBomb xG for explicitly attributed shots.
- Goals conceded = explicitly attributed shots with outcome Goal.
- GSaE = attributed xG faced − attributed goals conceded.
- Claims, punches and sweeper actions = counts of corresponding goalkeeper event labels.
- Goal-kick volume = count of passes tagged Goal Kick.
- Average goal-kick length = mean Euclidean distance between event start and pass end locations in StatsBomb pitch coordinates.
- Z-scores = descriptive standardized comparisons across available goalkeeper records, limited to shot-stopping and goalkeeper-action counts. The reconstruction deliberately avoids treating xG faced, goal-kick volume or kick length as automatically positive performance.

**Important attribution limitation:** StatsBomb event feeds do not necessarily link every shot to a goalkeeper. The pipeline reads goalkeeper subtypes from the nested `goalkeeper.type` object and links shots through related event IDs. It does not guess missing goalkeeper links. A `data_coverage.csv` audit reports linked-shot coverage. Therefore the resulting save rates, xG faced and GSaE may differ from the original presentation or from other providers. Inspect the exported shot-level CSV and coverage before comparing players. Substitution handling also requires careful review.

## Original report findings (reported, not independently reproduced)

- Save percentage vs GSaE: r = 0.522, p = 0.009.
- xG faced vs goals conceded: r = 0.763, p < 0.001.
- Shots faced vs save percentage: r = −0.018, p = 0.935.
- Sweeper actions per match vs claims per match: r = −0.129, p = 0.549.
- Goal kicks per match vs average kick length: r = 0.581, p = 0.003.
- Matches played vs save percentage: r = −0.046, p = 0.831.
- The report states Casteels recorded 93.3% from 57 shots and Simón recorded +2.94 GSaE.
- Group-level GSaE one-sample t-test: p = 0.075.

These are historical values from the surviving report, not outputs verified by the reconstruction. Do not describe them as independently reproduced until the rebuilt pipeline has been run and checked.

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

## Run locally

Python 3.11+ recommended.

```bash
git clone https://github.com/prashanthk7/euro-2024-goalkeeper-performance-analysis.git
cd euro-2024-goalkeeper-performance-analysis
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt

python scripts/download_data.py
python scripts/inspect_data.py
python -m src.build_analysis
streamlit run app.py
```

Raw match/event data is downloaded locally and excluded from Git. The app includes a tournament shortlist and individual dashboards for Unai Simón, Koen Casteels, Jan Oblak and Manuel Neuer, with event maps, summary metrics and a Z-score radar. Run the tests before interpreting metrics. CI is configured to compile the project and execute unit tests on pushes and pull requests.

## Neural-network component

The original presentation mentions a manual neural-network component but does not preserve the architecture, target, inputs or training protocol. `src/manual_mlp.py` is a generic educational one-hidden-layer NumPy regressor. It is a new transparent reconstruction, not a recovered original model or a model trained on the tournament goalkeeper data.

## Tests

```bash
python -m unittest discover -s tests -v
python -m compileall -q scripts src app.py
```

## LinkedIn portfolio description

**Evaluation of Goalkeeper Performance at UEFA Euro 2024**

Reconstructed a soccer analytics project using StatsBomb Open Data to evaluate goalkeeper performance beyond traditional statistics. Built four individual goalkeeper dashboards for Koen Casteels, Unai Simón, Fehmi Mert Günok and Predrag Rajković, covering shot-stopping, expected goals faced, Goals Saved Above Expectation (GSaE), sweeping actions and distribution.

**Methods:** Python, Pandas, NumPy, SciPy, Z-score standardization, correlation analysis and interactive visualization.

**Note:** The four profile Z-scores and selected statistics in the original report are identified as source-reported until independently recalculated from the reconstructed event data.

GitHub: https://github.com/prashanthk7/euro-2024-goalkeeper-performance-analysis

## Acknowledgements

- StatsBomb Open Data / Hudl StatsBomb.
- UEFA Euro 2024 event data contributors.
