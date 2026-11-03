"""Four-player Streamlit dashboard for the reconstructed Euro 2024 goalkeeper analysis."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

DATA = Path("data/processed/goalkeeper_summary.csv")
PROFILES = ["Koen Casteels", "Unai Simón", "Fehmi Mert Günok", "Predrag Rajković"]

st.set_page_config(page_title="Euro 2024 | Four Goalkeeper Dashboards", page_icon="🧤", layout="wide")
st.title("UEFA Euro 2024 — Goalkeeper Performance")
st.caption("Four individual goalkeeper dashboards | Shot-stopping • Sweeping • Distribution")
st.markdown("**Data source:** StatsBomb Open Data (competition 55, season 282). The reconstructed pipeline only attributes shots when the event data explicitly links them to a goalkeeper.")

if not DATA.exists():
    st.warning("Processed data is not available yet.")
    st.code("python scripts/download_data.py\npython -m src.build_analysis\nstreamlit run app.py")
    st.stop()

df = pd.read_csv(DATA)
if df.empty:
    st.error("The goalkeeper summary is empty.")
    st.stop()

# The four profile names are taken from the surviving presentation's overall Z-score comparison.
# The data is not fabricated: if event attribution does not yield a profile, show that transparently.
available = set(df["goalkeeper"].dropna().astype(str))
tabs = st.tabs(["Tournament overview", *PROFILES])

with tabs[0]:
    st.subheader("Four selected goalkeeper profiles")
    st.caption("Selection follows the four names in the original presentation's overall Z-score chart; these are not claimed to be the four best performers after independent recalculation.")
    overview = df[df["goalkeeper"].isin(PROFILES)].copy()
    if overview.empty:
        st.warning("None of the four presentation profiles have sufficient explicit goalkeeper-linked events in the current processed table. Inspect event attribution before interpreting or ranking them.")
    else:
        cols = st.columns(4)
        for col, keeper in zip(cols, PROFILES):
            row = overview[overview["goalkeeper"] == keeper]
            if row.empty:
                col.metric(keeper, "Not attributed")
            else:
                val = row.iloc[0]["save_percentage"]
                col.metric(keeper, f"{val:.1f}%" if pd.notna(val) else "n/a", "Save percentage")
        st.dataframe(overview[["goalkeeper", "matches_with_goalkeeper_events", "matches_with_attributed_shots", "shots_faced_attributed",
            "shots_on_target_attributed", "saves", "goals_conceded_attributed",
            "save_percentage", "xg_faced_attributed", "gsae_attributed",
            "claims", "punches", "sweeper_actions", "goal_kicks",
            "average_goal_kick_length"]], use_container_width=True, hide_index=True)
        if not overview.empty:
            st.plotly_chart(px.bar(overview, x="goalkeeper", y="gsae_attributed",
                title="GSaE comparison (explicitly attributed shots)",
                labels={"gsae_attributed": "xG faced − goals conceded"}),
                use_container_width=True)

for tab, keeper in zip(tabs[1:], PROFILES):
    with tab:
        subset = df[df["goalkeeper"].astype(str) == keeper]
        st.header(keeper)
        if subset.empty:
            st.warning("No goalkeeper summary row was produced for this player. This is not a zero-performance result; it means the current event-level attribution method did not resolve a usable player record.")
            st.info("Check the StatsBomb event links and lineup/substitution data before adding a value to this dashboard.")
            continue
        row = subset.iloc[0]
        st.caption(f"Player ID: {row.get('goalkeeper_id', 'not available')} | Matches with goalkeeper events: {int(row.get('matches_with_goalkeeper_events', 0))}")
        metric_cols = st.columns(4)
        metrics = [
            ("Save percentage", row.get("save_percentage"), "{:.1f}%"),
            ("GSaE", row.get("gsae_attributed"), "{:+.2f}"),
            ("xG faced", row.get("xg_faced_attributed"), "{:.2f}"),
            ("Goals conceded", row.get("goals_conceded_attributed"), "{:.0f}"),
        ]
        for col, (label, value, fmt) in zip(metric_cols, metrics):
            col.metric(label, fmt.format(value) if pd.notna(value) else "n/a")
        left, right = st.columns(2)
        with left:
            st.plotly_chart(px.bar(pd.DataFrame({
                "Metric": ["Shots faced", "Saves", "Goals conceded", "Claims", "Punches", "Sweeper actions"],
                "Count": [row.get("shots_faced_attributed", 0), row.get("saves", 0),
                          row.get("goals_conceded_attributed", 0), row.get("claims", 0),
                          row.get("punches", 0), row.get("sweeper_actions", 0)]
            }), x="Metric", y="Count", title="Shot-stopping and goalkeeper actions"),
            use_container_width=True)
        with right:
            st.plotly_chart(px.bar(pd.DataFrame({
                "Metric": ["Goal kicks", "Average kick length"],
                "Value": [row.get("goal_kicks", 0), row.get("average_goal_kick_length", float("nan"))]
            }), x="Metric", y="Value", title="Distribution profile"),
            use_container_width=True)
        zcols = [c for c in row.index if c.endswith("_zscore") and pd.notna(row[c])]
        if zcols:
            zdf = pd.DataFrame({"Metric": [c.replace("_zscore", "") for c in zcols],
                                "Z-score": [row[c] for c in zcols]})
            st.plotly_chart(px.bar(zdf, x="Metric", y="Z-score", title="Standardized profile"),
                            use_container_width=True)
        st.caption("Metric coverage depends on explicit event-level goalkeeper attribution. Missing values are not treated as zero.")
        st.caption(str(row.get("attribution_note", "")))

st.divider()
st.caption("StatsBomb asks users who publish or share analysis based on Open Data to credit StatsBomb and use its logo. Validate attribution coverage and definitions before public interpretation.")
