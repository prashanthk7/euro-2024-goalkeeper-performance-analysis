# LinkedIn project post — Euro 2024 Goalkeeper Analytics

I reconstructed my soccer analytics project on goalkeeper performance at the UEFA Euro 2024 Men's Championship.

The project examines three dimensions of goalkeeper performance:

- **Shot-stopping:** shots faced, saves, save percentage, expected goals faced (xG) and Goals Saved Above Expectation (GSaE)
- **Goalkeeper actions:** claims, punches and sweeper actions
- **Distribution:** goal-kick volume and average goal-kick length

The GitHub project includes a Streamlit dashboard structure with four individual goalkeeper profile tabs:

1. Koen Casteels
2. Unai Simón
3. Fehmi Mert Günok
4. Predrag Rajković

**Methods and tools:** Python, Pandas, NumPy, Streamlit, Plotly, event-data processing, Z-score standardization and correlation analysis.

**Reproducibility note:** My original notebooks and local data were lost, so this is a transparent reconstruction from my surviving project report and the public StatsBomb event data. I have corrected the goalkeeper-event parsing and added a data-link coverage audit. Reconstructed values are kept separate from figures reported in the original presentation; they should not be treated as validated until the pipeline and tests have been run against the complete tournament data.

**Data source:** StatsBomb Open Data (UEFA Euro 2024, competition 55, season 282).

Project repository:
https://github.com/prashanthk7/euro-2024-goalkeeper-performance-analysis

#SoccerAnalytics #FootballAnalytics #SportsAnalytics #Python #DataAnalytics #GoalkeeperAnalysis #StatsBomb
