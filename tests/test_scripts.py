"""Basic tests for the repository's data utility scripts."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from scripts.download_data import download_json
from scripts.inspect_data import get_name


class DownloadJsonTests(unittest.TestCase):
    def test_download_json_writes_valid_json(self):
        session = Mock()
        response = Mock()
        response.json.return_value = [{"match_id": 123}]
        session.get.return_value = response

        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "nested" / "matches.json"
            result = download_json(session, "https://example.test/matches.json", destination)

            self.assertEqual(result, [{"match_id": 123}])
            self.assertTrue(destination.exists())
            with destination.open("r", encoding="utf-8") as file:
                self.assertEqual(json.load(file), [{"match_id": 123}])
            self.assertFalse(destination.with_suffix(".json.tmp").exists())

        session.get.assert_called_once()


class InspectDataTests(unittest.TestCase):
    def test_get_name_from_statsbomb_object(self):
        self.assertEqual(get_name({"name": "Goal Keeper"}), "Goal Keeper")

    def test_get_name_returns_plain_value(self):
        self.assertEqual(get_name("Goal Keeper"), "Goal Keeper")

    def test_get_name_handles_none(self):
        self.assertIsNone(get_name(None))


if __name__ == "__main__":
    unittest.main()
