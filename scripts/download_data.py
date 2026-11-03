"""Download StatsBomb Open Data for UEFA Euro 2024.

Run from the repository root:
    python scripts/download_data.py
"""

import json
import time
from pathlib import Path

import requests

BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
COMPETITION_ID = 55
SEASON_ID = 282
RAW_DIR = Path("data/raw")
MATCHES_DIR = RAW_DIR / "matches"
EVENTS_DIR = RAW_DIR / "events"
REQUEST_DELAY_SECONDS = 0.2


def download_json(url: str, output_path: Path):
    """Download JSON from url and save it to output_path."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return data


def main() -> None:
    """Download the tournament match list and each match's events."""
    MATCHES_DIR.mkdir(parents=True, exist_ok=True)
    EVENTS_DIR.mkdir(parents=True, exist_ok=True)

    matches_url = f"{BASE_URL}/matches/{COMPETITION_ID}/{SEASON_ID}.json"
    matches_path = MATCHES_DIR / "euro_2024_matches.json"

    print("Downloading UEFA Euro 2024 match list...")
    matches = download_json(matches_url, matches_path)
    print(f"Found {len(matches)} matches.")

    failed_match_ids = []

    for index, match in enumerate(matches, start=1):
        match_id = match["match_id"]
        events_path = EVENTS_DIR / f"{match_id}.json"

        if events_path.exists():
            print(f"[{index}/{len(matches)}] Skipping existing file: {match_id}")
            continue

        events_url = f"{BASE_URL}/events/{match_id}.json"

        try:
            download_json(events_url, events_path)
            print(f"[{index}/{len(matches)}] Downloaded match {match_id}")
        except (requests.RequestException, ValueError, json.JSONDecodeError) as error:
            failed_match_ids.append(match_id)
            print(f"[{index}/{len(matches)}] Failed match {match_id}: {error}")

        time.sleep(REQUEST_DELAY_SECONDS)

    if failed_match_ids:
        print("\nSome match files could not be downloaded:")
        print(", ".join(map(str, failed_match_ids)))
        print("Run the script again to retry missing files.")
    else:
        print("\nAll match event files are present.")

    print(f"Match list: {matches_path}")
    print(f"Event files: {EVENTS_DIR}")


if __name__ == "__main__":
    main()
