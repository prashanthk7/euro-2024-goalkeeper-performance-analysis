"""Streamlit dashboard for the reconstructed Euro 2024 goalkeeper dataset.

Run: streamlit run app.py
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path("data/processed/goalkeeper_summary.csv")
st.set_page_config(page_title="Euro 2024 Goalkeeper Analysis", layout="wide")
st.title("UEFA Euro 2024 Goalkeeper Performance Analysis")
st.caption("Reconstructed analysis from StatsBomb Open Data. Metrics are limited by event-level goalkeeper attribution.")

if not DATA.exists():
    st.warning("Processed data is not available yet.")
    st.code("python scripts/download_data.py\npython -m src.build_analysis\nstreamlit run app.py")
    st.stop()

df = pd.read_csv(DATA)
if df.empty:
    st.error("The summary file is empty.")
    st.stop()

st.sidebar.header("Player selection")
names = sorted(df["goalkeeper"].dropna().astype(str).unique())
selected = st.sidebar.multiselect("Goalkeepers", names, default=names[:4])
view = df[df["goalkeeper"].isin(selected)].copy()

st.subheader("Goalkeeper overview")
cols = st.columns(3)
cols[0].metric("Goalkeepers in dataset", len(df))
cols[1].metric("Selected goalkeepers", len(view))
cols[2].metric("Attributed shots", int(view["shots_faced_attributed"].fillna(0).sum()))
st.dataframe(view[["goalkeeper", "matches_played", "shots_faced_attributed",
                   "shots_on_target_attributed", "saves", "goals_conceded_attributed",
                   "save_percentage", "xg_faced_attributed", "gsae_attributed",
                   "claims", "punches", "sweeper_actions", "goal_kicks",
                   "average_goal_kick_length"]], use_container_width=True, hide_index=True)

if not view.empty:
    st.subheader("Individual performance dashboard")
    st.plotly_chart(px.bar(view, x="goalkeeper", y="save_percentage",
                           title="Save percentage (attributed shots)", labels={"save_percentage":"Save %"}),
                    use_container_width=True)
    st.plotly_chart(px.bar(view, x="goalkeeper", y="gsae_attributed",
                           title="Goals Saved Above Expectation (attributed xG)",
                           labels={"gsae_attributed":"xG faced − goals conceded"}),
                    use_container_width=True)
    st.plotly_chart(px.scatter(view, x="xg_faced_attributed", y="goals_conceded_attributed",
                               text="goalkeeper", title="Attributed xG faced vs goals conceded",
                               labels={"xg_faced_attributed":"xG faced","goals_conceded_attributed":"Goals conceded"}),
                    use_container_width=True)

    zcols = [c for c in view.columns if c.endswith("_zscore")]
    if zcols:
        st.subheader("Z-score goalkeeper comparison")
        melted = view.melt(id_vars="goalkeeper", value_vars=zcols,
                           var_name="metric", value_name="z_score")
        melted["metric"] = melted["metric"].str.replace("_zscore", "", regex=False)
        st.plotly_chart(px.bar(melted, x="metric", y="z_score", color="goalkeeper",
                               barmode="group", title="Standardized metric comparison"),
                        use_container_width=True)

st.subheader("Correlation analysis")
st.caption("Pearson correlations are calculated only where at least three complete goalkeeper records exist. These are descriptive and should not be interpreted causally.")
pairs = [
    ("save_percentage", "gsae_attributed"),
    ("xg_faced_attributed", "goals_conceded_attributed"),
    ("sweeper_actions", "claims"),
    ("goal_kicks", "average_goal_kick_length"),
    ("matches_played", "save_percentage"),
]
from scipy.stats import pearsonr
results = []
for x, y in pairs:
    subset = df[[x, y]].apply(pd.to_numeric, errors="coerce").dropna()
    if len(subset) >= 3 and subset[x].nunique() > 1 and subset[y].nunique() > 1:
        r, p = pearsonr(subset[x], subset[y])
        results.append({"Metric pair": f"{x} vs {y}", "n": len(subset),
                        "Pearson r": round(float(r), 3), "p-value": round(float(p), 4)})
if results:
    st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
else:
    st.info("Not enough complete, varying observations to calculate correlations.")

st.info("Interpretation caution: the StatsBomb event feed may not explicitly attribute every shot to a goalkeeper. The pipeline does not infer missing links; verify coverage and definitions before comparing these outputs with the presentation's reported figures.")
