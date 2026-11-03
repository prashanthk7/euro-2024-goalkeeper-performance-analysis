"""Download StatsBomb Open Data for UEFA Euro 2024.

Run from the repository root:
    python scripts/download_data.py

Downloaded JSON files are stored under data/raw/ and are excluded from Git.
"""

import json
import os
import time
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
COMPETITION_ID = 55
SEASON_ID = 282
RAW_DIR = Path("data/raw")
MATCHES_DIR = RAW_DIR / "matches"
EVENTS_DIR = RAW_DIR / "events"
REQUEST_DELAY_SECONDS = 0.2
TIMEOUT_SECONDS = 30


def build_session() -> requests.Session:
    """Create an HTTP session with retries for transient network failures."""
    retry = Retry(
        total=4,
        connect=4,
        read=4,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": "euro-2024-goalkeeper-analysis/1.0"})
    return session


def download_json(
    session: requests.Session, url: str, output_path: Path
) -> Any:
    """Download valid JSON and atomically save it to output_path."""
    response = session.get(url, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    data = response.json()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
        os.replace(temporary_path, output_path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    return data


def main() -> None:
    """Download the tournament match list and each match's event data."""
    MATCHES_DIR.mkdir(parents=True, exist_ok=True)
    EVENTS_DIR.mkdir(parents=True, exist_ok=True)
    session = build_session()

    matches_url = f"{BASE_URL}/matches/{COMPETITION_ID}/{SEASON_ID}.json"
    matches_path = MATCHES_DIR / "euro_2024_matches.json"

    print("Downloading UEFA Euro 2024 match list...")
    try:
        matches = download_json(session, matches_url, matches_path)
    except (requests.RequestException, ValueError) as error:
        raise SystemExit(f"Could not download the match list: {error}") from error

    if not isinstance(matches, list):
        raise SystemExit("Unexpected match-list format: expected a JSON array.")

    print(f"Found {len(matches)} matches.")
    failed_match_ids = []

    for index, match in enumerate(matches, start=1):
        if not isinstance(match, dict) or "match_id" not in match:
            print(f"[{index}/{len(matches)}] Skipping malformed match entry.")
            continue

        match_id = match["match_id"]
        events_path = EVENTS_DIR / f"{match_id}.json"

        if events_path.exists():
            try:
                with events_path.open("r", encoding="utf-8") as file:
                    existing_data = json.load(file)
                if isinstance(existing_data, list):
                    print(f"[{index}/{len(matches)}] Already downloaded: {match_id}")
                    continue
            except (OSError, ValueError):
                events_path.unlink(missing_ok=True)

        events_url = f"{BASE_URL}/events/{match_id}.json"
        try:
            download_json(session, events_url, events_path)
            print(f"[{index}/{len(matches)}] Downloaded match {match_id}")
        except (requests.RequestException, ValueError) as error:
            failed_match_ids.append(match_id)
            print(f"[{index}/{len(matches)}] Failed match {match_id}: {error}")

        if index < len(matches):
            time.sleep(REQUEST_DELAY_SECONDS)

    if failed_match_ids:
        print("\nSome match event files could not be downloaded:")
        print(", ".join(map(str, failed_match_ids)))
        print("Run the script again to retry missing files.")
    else:
        print("\nAll match event files are present.")

    print(f"Match list: {matches_path}")
    print(f"Event files: {EVENTS_DIR}")


if __name__ == "__main__":
    main()
