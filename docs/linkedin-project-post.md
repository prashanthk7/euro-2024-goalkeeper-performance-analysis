# LinkedIn project post — Euro 2024 Goalkeeper Analytics

I recently revisited a soccer analytics project from the UEFA Euro 2024 Men's Championship: **Evaluation of Goalkeeper Performance**.

The aim was to look beyond clean sheets and save counts and assess goalkeepers across three areas:

- **Shot-stopping:** shots faced, saves, save percentage, xG faced and Goals Saved Above Expectation (GSaE)
- **Goalkeeper actions:** claims, punches and sweeper actions
- **Distribution:** goal-kick volume and average goal-kick length

I have reconstructed the project workflow using the public StatsBomb Euro 2024 event dataset and built four individual goalkeeper dashboard views:

1. Koen Casteels
2. Unai Simón
3. Fehmi Mert Günok
4. Predrag Rajković

The dashboard is designed to make each goalkeeper's profile easy to inspect individually, with a consistent set of performance indicators and an overview for comparison.

**Tools and methods:** Python, Pandas, NumPy, SciPy, Streamlit, Plotly, Z-score standardization and correlation analysis.

A note on reproducibility: my original notebooks and local data were lost, so this is a documented reconstruction rather than a claim to have recovered the original code. The figures from the original report are clearly separated from metrics that have been independently recalculated. StatsBomb is credited as the data source.

Project repository:
https://github.com/prashanthk7/euro-2024-goalkeeper-performance-analysis

#SoccerAnalytics #FootballAnalytics #SportsAnalytics #Python #DataAnalytics #GoalkeeperAnalysis #StatsBomb
