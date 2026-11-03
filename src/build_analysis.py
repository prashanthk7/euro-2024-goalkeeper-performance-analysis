"""Build goalkeeper match-level metrics from StatsBomb Euro 2024 event JSON.

Run after scripts/download_data.py:
    python -m src.build_analysis

Definitions are explicit and intentionally conservative. A shot is attributed
to a goalkeeper only when the shot event contains a goalkeeper reference or is
linked to a goalkeeper event via related_events. Missing attribution is not
silently guessed.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

MATCH_FILE = Path("data/raw/matches/euro_2024_matches.json")
EVENT_DIR = Path("data/raw/events")
OUT_DIR = Path("data/processed")


def name(value):
    return value.get("name") if isinstance(value, dict) else value


def obj_id(value):
    return value.get("id") if isinstance(value, dict) else None


def location_distance(start, end):
    if not (isinstance(start, list) and isinstance(end, list) and len(start) >= 2 and len(end) >= 2):
        return np.nan
    return float(np.hypot(end[0] - start[0], end[1] - start[1]))


def load_events():
    if not MATCH_FILE.exists():
        raise FileNotFoundError("Run python scripts/download_data.py first.")
    matches = json.loads(MATCH_FILE.read_text(encoding="utf-8"))
    for match in matches:
        path = EVENT_DIR / f"{match['match_id']}.json"
        if not path.exists():
            continue
        events = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(events, list):
            yield match, events


def build_tables():
    match_rows, shot_rows, keeper_rows, kick_rows = [], [], [], []
    for match, events in load_events():
        mid = match.get("match_id")
        match_rows.append({
            "match_id": mid, "match_date": match.get("match_date"),
            "home_team": name(match.get("home_team")),
            "away_team": name(match.get("away_team")),
            "home_score": match.get("home_score"), "away_score": match.get("away_score")
        })
        # Link goalkeeper events to shots through StatsBomb related event IDs.
        keeper_event_to_shot = {}
        for ev in events:
            if name(ev.get("type")) == "Goal Keeper":
                for related in ev.get("related_events", []) or []:
                    keeper_event_to_shot[related] = ev
        for ev in events:
            etype = name(ev.get("type"))
            if etype == "Shot":
                shot = ev.get("shot") or {}
                keeper_ref = shot.get("goalkeeper")
                related_keeper = keeper_event_to_shot.get(ev.get("id"))
                keeper_id = obj_id(keeper_ref) or (obj_id(related_keeper.get("player")) if related_keeper else None)
                keeper_name = name(keeper_ref) or (name(related_keeper.get("player")) if related_keeper else None)
                shot_rows.append({
                    "match_id": mid, "shot_id": ev.get("id"),
                    "goalkeeper_id": keeper_id, "goalkeeper": keeper_name,
                    "xg": shot.get("statsbomb_xg"),
                    "shot_outcome": name(shot.get("outcome")),
                    "team": name(ev.get("team")),
                })
            if etype == "Goal Keeper":
                player = ev.get("player") or {}
                subtype = name(ev.get("goalkeeper_type")) or name(ev.get("type"))
                keeper_rows.append({
                    "match_id": mid, "goalkeeper_id": obj_id(player),
                    "goalkeeper": name(player), "action": subtype,
                    "outcome": name(ev.get("goalkeeper_type")),
                    "position": name(ev.get("position")),
                })
            if etype == "Pass" and name((ev.get("pass") or {}).get("type")) == "Goal Kick":
                p = ev.get("pass") or {}
                player = ev.get("player") or {}
                kick_rows.append({
                    "match_id": mid, "goalkeeper_id": obj_id(player),
                    "goalkeeper": name(player),
                    "kick_length": location_distance(ev.get("location"), p.get("end_location")),
                    "outcome": name(p.get("outcome")),
                })

    matches = pd.DataFrame(match_rows).drop_duplicates("match_id")
    shots = pd.DataFrame(shot_rows)
    keeper_events = pd.DataFrame(keeper_rows)
    kicks = pd.DataFrame(kick_rows)
    if keeper_events.empty and shots.empty:
        raise ValueError("No goalkeeper or shot events found. Check downloaded StatsBomb event files.")

    # Player IDs are the primary key; names are retained for display.
    identities = []
    for frame in (keeper_events, shots, kicks):
        if not frame.empty and "goalkeeper_id" in frame:
            identities.append(frame[["goalkeeper_id", "goalkeeper"]].dropna(subset=["goalkeeper_id"]))
    players = pd.concat(identities, ignore_index=True).drop_duplicates("goalkeeper_id") if identities else pd.DataFrame(columns=["goalkeeper_id", "goalkeeper"])
    if players.empty:
        raise ValueError("No goalkeeper identities could be resolved from the event data.")

    rows = []
    for _, player in players.iterrows():
        pid, pname = player["goalkeeper_id"], player["goalkeeper"]
        ke = keeper_events[keeper_events.goalkeeper_id == pid] if not keeper_events.empty else pd.DataFrame()
        sh = shots[shots.goalkeeper_id == pid] if not shots.empty else pd.DataFrame()
        kg = kicks[kicks.goalkeeper_id == pid] if not kicks.empty else pd.DataFrame()
        matches_played = int(ke.match_id.nunique()) if not ke.empty else int(sh.match_id.nunique())
        action_names = ke.action.fillna("").astype(str).str.lower() if not ke.empty else pd.Series(dtype=str)
        saves = int(action_names.str.contains("save").sum())
        goals_conceded = int((sh.shot_outcome == "Goal").sum()) if not sh.empty else 0
        xg_faced = float(pd.to_numeric(sh.xg, errors="coerce").sum()) if not sh.empty else 0.0
        shots_on_target = int(len(sh)) if not sh.empty else 0
        claims = int(action_names.str.contains("claim|collected", regex=True).sum())
        punches = int(action_names.str.contains("punch", regex=False).sum())
        sweeper = int(action_names.str.contains("sweeper", regex=False).sum())
        rows.append({
            "goalkeeper_id": pid, "goalkeeper": pname,
            "matches_played": matches_played,
            "shots_faced_attributed": shots_on_target,
            "saves_from_goalkeeper_events": saves,
            "goals_conceded_attributed": goals_conceded,
            "xg_faced_attributed": xg_faced,
            "save_percentage": (100 * saves / shots_on_target) if shots_on_target else np.nan,
            "gsae_attributed": xg_faced - goals_conceded,
            "claims": claims, "punches": punches, "sweeper_actions": sweeper,
            "goal_kicks": int(len(kg)),
            "average_goal_kick_length": float(pd.to_numeric(kg.kick_length, errors="coerce").mean()) if not kg.empty else np.nan,
            "attribution_note": "Shot metrics include only shots with an explicit goalkeeper link; inspect coverage before interpretation."
        })
    summary = pd.DataFrame(rows)
    summary["save_percentage"] = summary["save_percentage"].round(2)
    summary["gsae_attributed"] = summary["gsae_attributed"].round(3)
    summary["xg_faced_attributed"] = summary["xg_faced_attributed"].round(3)
    # Z-scores are descriptive cross-player comparisons, not rankings.
    metric_cols = ["save_percentage", "gsae_attributed", "xg_faced_attributed",
                   "claims", "punches", "sweeper_actions", "goal_kicks",
                   "average_goal_kick_length"]
    z = summary[metric_cols].apply(pd.to_numeric, errors="coerce")
    std = z.std(ddof=0).replace(0, np.nan)
    zscores = (z - z.mean()) / std
    zscores.columns = [f"{c}_zscore" for c in zscores.columns]
    summary = pd.concat([summary, zscores.round(3)], axis=1)
    return matches, shots, keeper_events, kicks, summary


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tables = build_tables()
    names = ["matches", "shots", "goalkeeper_events", "goal_kicks", "goalkeeper_summary"]
    for name_, frame in zip(names, tables):
        frame.to_csv(OUT_DIR / f"{name_}.csv", index=False)
        print(f"Wrote {OUT_DIR / f'{name_}.csv'} ({len(frame)} rows)")
    print("\nImportant: event-level goalkeeper attribution can be incomplete. Review the")
    print("attribution note and compare event counts with the source before drawing conclusions.")


if __name__ == "__main__":
    main()
