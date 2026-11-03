"""Rebuild goalkeeper metrics from StatsBomb Euro 2024 event data.

Run:
    python scripts/download_data.py
    python -m src.build_analysis

Shots are attributed only through the StatsBomb Shot -> Goal Keeper event
relationship. Missing links are not guessed. Goalkeeper action subtypes are
read from the nested 'goalkeeper' event object.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

MATCH_FILE = Path("data/raw/matches/euro_2024_matches.json")
EVENT_DIR = Path("data/raw/events")
OUT_DIR = Path("data/processed")

# StatsBomb event outcome labels. The on-target denominator is goals + saves.
SAVE_OUTCOMES = {"saved", "saved to post"}
GOAL_OUTCOME = "goal"


def name(value):
    return value.get("name") if isinstance(value, dict) else value


def obj_id(value):
    return value.get("id") if isinstance(value, dict) else None


def location_distance(start, end):
    if not (
        isinstance(start, list) and isinstance(end, list)
        and len(start) >= 2 and len(end) >= 2
    ):
        return np.nan
    return float(np.hypot(float(end[0]) - float(start[0]),
                          float(end[1]) - float(start[1])))


def is_save(outcome):
    return str(outcome or "").strip().lower() in SAVE_OUTCOMES


def load_events():
    if not MATCH_FILE.exists():
        raise FileNotFoundError("Run python scripts/download_data.py first.")
    matches = json.loads(MATCH_FILE.read_text(encoding="utf-8"))
    if not isinstance(matches, list):
        raise ValueError("Match file must contain a JSON array.")
    for match in matches:
        path = EVENT_DIR / f"{match['match_id']}.json"
        if not path.exists():
            print(f"WARNING: missing event file for match {match['match_id']}")
            continue
        events = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(events, list):
            print(f"WARNING: invalid event file {path}")
            continue
        yield match, events


def build_tables():
    match_rows, shot_rows, keeper_rows, kick_rows = [], [], [], []
    for match, events in load_events():
        mid = match.get("match_id")
        match_rows.append({
            "match_id": mid,
            "match_date": match.get("match_date"),
            "home_team": name(match.get("home_team")),
            "away_team": name(match.get("away_team")),
            "home_score": match.get("home_score"),
            "away_score": match.get("away_score"),
        })

        # related_events is bidirectional: the keeper event references the
        # shot UUID. Use player identity from that goalkeeper event.
        keeper_event_by_shot = {}
        for ev in events:
            if name(ev.get("type")) == "Goal Keeper":
                for related_id in ev.get("related_events") or []:
                    keeper_event_by_shot[related_id] = ev

        for ev in events:
            etype = name(ev.get("type"))
            if etype == "Shot":
                shot = ev.get("shot") or {}
                linked_keeper = keeper_event_by_shot.get(ev.get("id"))
                keeper_ref = shot.get("goalkeeper")
                keeper_player = (linked_keeper or {}).get("player") or {}
                keeper_id = obj_id(keeper_ref) or obj_id(keeper_player)
                keeper_name = name(keeper_ref) or name(keeper_player)
                shot_rows.append({
                    "match_id": mid,
                    "shot_id": ev.get("id"),
                    "goalkeeper_id": keeper_id,
                    "goalkeeper": keeper_name,
                    "xg": shot.get("statsbomb_xg"),
                    "shot_outcome": name(shot.get("outcome")),
                    "shooting_team": name(ev.get("team")),
                    "linked_goalkeeper_event": linked_keeper is not None,
                })

            if etype == "Goal Keeper":
                player = ev.get("player") or {}
                keeper_detail = ev.get("goalkeeper") or {}
                keeper_rows.append({
                    "match_id": mid,
                    "event_id": ev.get("id"),
                    "goalkeeper_id": obj_id(player),
                    "goalkeeper": name(player),
                    "action": name(keeper_detail.get("type")),
                    "outcome": name(keeper_detail.get("outcome")),
                    "position": name(ev.get("position")),
                    "related_events": ev.get("related_events") or [],
                })

            if etype == "Pass" and name((ev.get("pass") or {}).get("type")) == "Goal Kick":
                pass_detail = ev.get("pass") or {}
                player = ev.get("player") or {}
                kick_rows.append({
                    "match_id": mid,
                    "goalkeeper_id": obj_id(player),
                    "goalkeeper": name(player),
                    "kick_length": location_distance(
                        ev.get("location"), pass_detail.get("end_location")
                    ),
                    "outcome": name(pass_detail.get("outcome")),
                })

    matches_df = pd.DataFrame(match_rows)
    shots = pd.DataFrame(shot_rows)
    keeper_events = pd.DataFrame(keeper_rows)
    kicks = pd.DataFrame(kick_rows)

    if keeper_events.empty and shots.empty and kicks.empty:
        raise ValueError("No goalkeeper-related events found in downloaded data.")

    identity_frames = []
    for frame in (keeper_events, shots, kicks):
        if not frame.empty:
            identity_frames.append(
                frame[["goalkeeper_id", "goalkeeper"]].dropna(subset=["goalkeeper_id"])
            )
    if not identity_frames:
        raise ValueError("No goalkeeper player IDs were resolved from event data.")
    players = (
        pd.concat(identity_frames, ignore_index=True)
        .drop_duplicates("goalkeeper_id")
    )

    rows = []
    for _, player in players.iterrows():
        pid = player["goalkeeper_id"]
        pname = player["goalkeeper"]
        ke = keeper_events[keeper_events.goalkeeper_id == pid] if not keeper_events.empty else pd.DataFrame()
        sh = shots[shots.goalkeeper_id == pid] if not shots.empty else pd.DataFrame()
        kg = kicks[kicks.goalkeeper_id == pid] if not kicks.empty else pd.DataFrame()

        outcomes = (
            sh["shot_outcome"].fillna("").astype(str).str.strip().str.lower()
            if not sh.empty else pd.Series(dtype=str)
        )
        saves = int(outcomes.isin(SAVE_OUTCOMES).sum())
        goals = int((outcomes == GOAL_OUTCOME).sum())
        xg_faced = (
            float(pd.to_numeric(sh["xg"], errors="coerce").sum(min_count=1) or 0)
            if not sh.empty else 0.0
        )
        on_target = saves + goals
        actions = (
            ke["action"].fillna("").astype(str).str.lower()
            if not ke.empty else pd.Series(dtype=str)
        )

        rows.append({
            "goalkeeper_id": pid,
            "goalkeeper": pname,
            "matches_with_goalkeeper_events": int(ke["match_id"].nunique()) if not ke.empty else 0,
            "matches_with_attributed_shots": int(sh["match_id"].nunique()) if not sh.empty else 0,
            "shots_faced_attributed": int(len(sh)),
            "shots_on_target_attributed": on_target,
            "saves": saves,
            "goals_conceded_attributed": goals,
            "xg_faced_attributed": xg_faced,
            "save_percentage": (100 * saves / on_target) if on_target else np.nan,
            "gsae_attributed": xg_faced - goals,
            "claims": int(actions.str.contains("claim|collected", regex=True).sum()),
            "punches": int(actions.str.contains("punch", regex=False).sum()),
            "sweeper_actions": int(actions.str.contains("sweeper", regex=False).sum()),
            "goal_kicks": int(len(kg)),
            "average_goal_kick_length": (
                float(pd.to_numeric(kg["kick_length"], errors="coerce").mean())
                if not kg.empty else np.nan
            ),
            "attribution_note": (
                "Shots counted only when a StatsBomb goalkeeper event is explicitly "
                "linked. Save percentage = saved outcomes / (saved outcomes + goals). "
                "Substitutions and missing links may reduce coverage."
            ),
        })

    summary = pd.DataFrame(rows)
    summary["save_percentage"] = summary["save_percentage"].round(2)
    for column in ("gsae_attributed", "xg_faced_attributed", "average_goal_kick_length"):
        summary[column] = summary[column].round(3)

    # Do not create a single composite rank: xG faced and goal-kick volume are
    # exposure/style variables, not automatically positive performance.
    zscore_metrics = [
        "save_percentage", "gsae_attributed", "claims",
        "punches", "sweeper_actions",
    ]
    z = summary[zscore_metrics].apply(pd.to_numeric, errors="coerce")
    standard_deviation = z.std(ddof=0).replace(0, np.nan)
    zscores = (z - z.mean()) / standard_deviation
    zscores.columns = [f"{column}_zscore" for column in zscores.columns]
    summary = pd.concat([summary, zscores.round(3)], axis=1)

    coverage = pd.DataFrame([{
        "matches_in_match_list": len(matches_df),
        "matches_with_event_files": int(matches_df["match_id"].nunique()),
        "total_shot_events": int(len(shots)),
        "shots_with_goalkeeper_link": int(shots["goalkeeper_id"].notna().sum()) if not shots.empty else 0,
        "shot_link_coverage_pct": (
            100 * shots["goalkeeper_id"].notna().mean() if not shots.empty else 0.0
        ),
        "goalkeeper_event_rows": int(len(keeper_events)),
        "goal_kick_rows": int(len(kicks)),
    }])

    return matches_df, shots, keeper_events, kicks, summary, coverage


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tables = build_tables()
    filenames = [
        "matches.csv", "shots.csv", "goalkeeper_events.csv",
        "goal_kicks.csv", "goalkeeper_summary.csv", "data_coverage.csv",
    ]
    for filename, frame in zip(filenames, tables):
        destination = OUT_DIR / filename
        frame.to_csv(destination, index=False)
        print(f"Wrote {destination} ({len(frame)} rows)")
    print("\nComposite rankings are intentionally omitted: exposure and style metrics")
    print("should not be interpreted as universally positive performance indicators.")


if __name__ == "__main__":
    main()
