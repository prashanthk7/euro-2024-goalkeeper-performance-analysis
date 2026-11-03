"""Inspect downloaded StatsBomb Euro 2024 match and event data.

Run from the repository root:
    python scripts/inspect_data.py
"""

import json
from pathlib import Path
from typing import Any

import pandas as pd

MATCHES_FILE = Path("data/raw/matches/euro_2024_matches.json")
EVENTS_DIR = Path("data/raw/events")


def get_name(value: Any) -> Any:
    """Return the name from a StatsBomb nested object when available."""
    if isinstance(value, dict):
        return value.get("name")
    return value


def load_json(path: Path) -> Any:
    """Load a UTF-8 JSON file."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def inspect_matches() -> None:
    """Print a basic overview of the tournament match list."""
    if not MATCHES_FILE.exists():
        print(f"Match list not found: {MATCHES_FILE}")
        print("Run python scripts/download_data.py first.")
        return

    try:
        matches = load_json(MATCHES_FILE)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read match list: {error}")
        return

    if not isinstance(matches, list):
        print("Invalid match list: expected a JSON array.")
        return

    df = pd.DataFrame(matches)
    print("\n--- MATCH OVERVIEW ---")
    print(f"Total matches: {len(df)}")
    print("\nAvailable columns:")
    print(", ".join(map(str, df.columns)))

    display_columns = [
        column
        for column in (
            "match_id",
            "match_date",
            "home_team",
            "away_team",
            "home_score",
            "away_score",
        )
        if column in df.columns
    ]

    if display_columns:
        display_df = df[display_columns].copy()
        for column in ("home_team", "away_team"):
            if column in display_df.columns:
                display_df[column] = display_df[column].apply(get_name)
        print("\nSample match details:")
        print(display_df.head().to_string(index=False))


def inspect_events() -> None:
    """Inspect event types and columns in the first available event file."""
    if not EVENTS_DIR.exists():
        print(f"Events directory not found: {EVENTS_DIR}")
        print("Run python scripts/download_data.py first.")
        return

    event_files = sorted(EVENTS_DIR.glob("*.json"))
    if not event_files:
        print("\nNo event JSON files found. Run the download script first.")
        return

    sample_file = None
    events = None
    for candidate in event_files:
        try:
            candidate_events = load_json(candidate)
            if isinstance(candidate_events, list):
                sample_file = candidate
                events = candidate_events
                break
        except (OSError, json.JSONDecodeError):
            continue

    if sample_file is None:
        print("\nNo readable event JSON files were found.")
        return

    df = pd.DataFrame(events)
    print("\n--- EVENT OVERVIEW ---")
    print(f"Sample file: {sample_file.name}")
    print(f"Events in sample match: {len(df)}")
    print("\nAvailable event columns:")
    print(", ".join(map(str, df.columns)))

    if "type" in df.columns:
        event_types = df["type"].apply(get_name).value_counts(dropna=False)
        print("\nMost common event types in this match:")
        print(event_types.head(20).to_string())


def main() -> None:
    """Run the match and event data inspections."""
    inspect_matches()
    inspect_events()


if __name__ == "__main__":
    main()
