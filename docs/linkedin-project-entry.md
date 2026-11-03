# LinkedIn — Project section entry

**Project title:** Evaluation of Goalkeeper Performance at UEFA Euro 2024

**Associated with:** Soccer Analytics Portfolio

**Description:**

Reconstructed a soccer analytics project evaluating goalkeeper performance at the UEFA Euro 2024 Men's Championship using StatsBomb Open Data.

Developed a Python-based analysis workflow and a Streamlit dashboard structure with four individual goalkeeper profile views:

- Koen Casteels
- Unai Simón
- Fehmi Mert Günok
- Predrag Rajković

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
