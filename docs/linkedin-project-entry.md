# LinkedIn — Project section entry

**Project title:** Evaluation of Goalkeeper Performance at UEFA Euro 2024

**Associated with:** Soccer Analytics Portfolio

**Description:**

Reconstructed a soccer analytics project evaluating goalkeeper performance at the UEFA Euro 2024 Men's Championship using StatsBomb Open Data.

Developed a Python-based analysis workflow and event-level Streamlit dashboards for the top three Euro 2024 goalkeepers by reconstructed GSaE (minimum four matches): Unai Simón, Koen Casteels and Jan Oblak, plus Manuel Neuer as a comparison profile.

The analysis focuses on shot-stopping (shots faced, saves, save percentage, xG faced and GSaE), goalkeeper actions (claims, punches and sweeper actions), and distribution (goal-kick volume and average kick length).

**Tools:** Python, Pandas, NumPy, Streamlit, Plotly, SciPy.

**Methods:** Event-data processing, metric engineering, Z-score standardization and correlation analysis.

**Data source:** StatsBomb Open Data — UEFA Euro 2024 (competition 55, season 282).

**Reproducibility note:** The original notebooks and local data were lost. This repository is a transparent reconstruction. The original report's values are labeled as report-derived; rebuilt values are not presented as validated until the full pipeline and coverage audit complete.

**Project URL:** https://github.com/prashanthk7/euro-2024-goalkeeper-performance-analysis

## Four individual dashboard profiles

1. Koen Casteels — original report Z-score 1.05; original report highlights 93.3% save rate from 57 shots.
2. Unai Simón — original report Z-score 0.70; original report highlights +2.94 GSaE.
3. Fehmi Mert Günok — original report Z-score 0.61.
4. Predrag Rajković — original report Z-score 0.57.

The four Z-scores and highlighted statistics above are transcribed from the surviving presentation and are not independent recalculations.


## Dashboard visual structure

Each profile follows the supplied reference: shot-danger pitch map, claims/punches map, long- and short-distribution maps, shots/set-piece summary and Z-score radar. Maps use StatsBomb event coordinates when available; missing data is not fabricated.

## Reconstructed tournament shortlist

- Unai Simón — 2.945 GSaE; 82.35% save rate; 65 attributed shots; 6 matches.
- Koen Casteels — 2.928 GSaE; 93.33% save rate; 57 attributed shots; 4 matches.
- Jan Oblak — 2.800 GSaE; 75.00% save rate; 66 attributed shots; 4 matches.
- Manuel Neuer comparison — 1.176 GSaE; 76.92% save rate; 45 attributed shots; 5 matches.

These figures are from the reconstructed StatsBomb pipeline, not the original report's transcribed results. GSaE is a single-metric shortlist, not an overall goalkeeper rating.
