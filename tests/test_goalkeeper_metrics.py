import unittest
from unittest.mock import patch

from src.build_analysis import build_tables, is_on_target, is_save


class MetricDefinitionTests(unittest.TestCase):
    def test_outcome_classification(self):
        self.assertTrue(is_save("Saved"))
        self.assertTrue(is_save("Saved to Post"))
        self.assertTrue(is_on_target("Goal"))
        self.assertTrue(is_on_target("Saved"))
        self.assertFalse(is_on_target("Off T"))

    def test_build_tables_uses_consistent_shot_denominators(self):
        goalkeeper = {"id": 99, "name": "Test Keeper"}
        events = [
            {"id": "s1", "type": {"name": "Shot"},
             "shot": {"statsbomb_xg": 0.4, "outcome": {"name": "Saved"}},
             "team": {"name": "Opponent"}},
            {"id": "s2", "type": {"name": "Shot"},
             "shot": {"statsbomb_xg": 0.3, "outcome": {"name": "Goal"}},
             "team": {"name": "Opponent"}},
            {"id": "s3", "type": {"name": "Shot"},
             "shot": {"statsbomb_xg": 0.2, "outcome": {"name": "Off T"}},
             "team": {"name": "Opponent"}},
            {"id": "g1", "type": {"name": "Goal Keeper"},
             "related_events": ["s1"], "player": goalkeeper,
             "goalkeeper_type": {"name": "Shot Saved"}},
            {"id": "g2", "type": {"name": "Goal Keeper"},
             "related_events": ["s2"], "player": goalkeeper,
             "goalkeeper_type": {"name": "Shot Faced"}},
            {"id": "g3", "type": {"name": "Goal Keeper"},
             "related_events": ["s3"], "player": goalkeeper,
             "goalkeeper_type": {"name": "Other"}},
        ]
        match = {"match_id": 123, "match_date": "2024-06-01",
                 "home_team": {"name": "Home"}, "away_team": {"name": "Away"},
                 "home_score": 1, "away_score": 0}
        with patch("src.build_analysis.load_events", return_value=iter([(match, events)])):
            _, shots, _, _, summary = build_tables()

        row = summary.iloc[0]
        self.assertEqual(len(shots), 3)
        self.assertEqual(row["shots_faced_attributed"], 3)
        self.assertEqual(row["shots_on_target_attributed"], 2)
        self.assertEqual(row["saves"], 1)
        self.assertEqual(row["goals_conceded_attributed"], 1)
        self.assertAlmostEqual(row["save_percentage"], 50.0)
        self.assertAlmostEqual(row["xg_faced_attributed"], 0.9)
        self.assertAlmostEqual(row["gsae_attributed"], -0.1)


if __name__ == "__main__":
    unittest.main()
