"""Regression tests for StatsBomb event parsing and goalkeeper metrics."""
import unittest
from unittest.mock import patch

from src.build_analysis import build_tables, is_save, location_distance


def event(kind, **kwargs):
    return {"id": kwargs.pop("id", None), "type": {"name": kind}, **kwargs}


class MetricHelperTests(unittest.TestCase):
    def test_save_outcomes_are_classified(self):
        self.assertTrue(is_save({"name": "Saved"}))
        self.assertTrue(is_save("Saved to Post"))
        self.assertFalse(is_save({"name": "Goal"}))
        self.assertFalse(is_save("Off T"))

    def test_goal_kick_distance(self):
        self.assertAlmostEqual(location_distance([0, 0], [3, 4]), 5.0)
        self.assertTrue(__import__("math").isnan(location_distance(None, [1, 2])))


class BuildTablesTests(unittest.TestCase):
    def test_shot_link_and_nested_goalkeeper_action_are_parsed(self):
        shot_saved = event(
            "Shot", id="shot-saved",
            shot={"statsbomb_xg": 0.2, "outcome": {"name": "Saved"}},
            related_events=["keeper-save"],
            team={"name": "Opponent"},
        )
        keeper_save = event(
            "Goal Keeper", id="keeper-save",
            player={"id": 77, "name": "Test Keeper"},
            goalkeeper={
                "type": {"name": "Shot Saved"},
                "outcome": {"name": "Success"},
            },
            related_events=["shot-saved"],
        )
        shot_goal = event(
            "Shot", id="shot-goal",
            shot={"statsbomb_xg": 0.5, "outcome": {"name": "Goal"}},
            related_events=["keeper-goal"],
            team={"name": "Opponent"},
        )
        keeper_goal = event(
            "Goal Keeper", id="keeper-goal",
            player={"id": 77, "name": "Test Keeper"},
            goalkeeper={
                "type": {"name": "Goal Conceded"},
                "outcome": {"name": "Lost"},
            },
            related_events=["shot-goal"],
        )
        keeper_claim = event(
            "Goal Keeper", id="keeper-claim",
            player={"id": 77, "name": "Test Keeper"},
            goalkeeper={
                "type": {"name": "Collected"},
                "outcome": {"name": "Claim"},
            },
            related_events=[],
        )
        goal_kick = event(
            "Pass", id="goal-kick",
            player={"id": 77, "name": "Test Keeper"},
            pass_={"type": {"name": "Goal Kick"}},
            location=[0, 0],
        )
        # StatsBomb uses the nested event property literally named 'pass'.
        goal_kick["pass"] = goal_kick.pop("pass_")
        goal_kick["pass"]["end_location"] = [3, 4]

        match = {
            "match_id": 1001, "match_date": "2024-06-15",
            "home_team": {"home_team_name": "Home"},
            "away_team": {"away_team_name": "Opponent"},
        }
        events = [shot_saved, keeper_save, shot_goal, keeper_goal, keeper_claim, goal_kick]
        with patch("src.build_analysis.load_events", return_value=[(match, events)]):
            _, shots, keeper_events, kicks, summary, coverage = build_tables()

        self.assertEqual(int(coverage.iloc[0]["shots_with_goalkeeper_link"]), 2)
        self.assertEqual(len(shots), 2)
        self.assertEqual(len(kicks), 1)
        row = summary.iloc[0]
        self.assertEqual(row["goalkeeper"], "Test Keeper")
        self.assertEqual(row["saves"], 1)
        self.assertEqual(row["goals_conceded_attributed"], 1)
        self.assertAlmostEqual(row["save_percentage"], 50.0)
        self.assertAlmostEqual(row["gsae_attributed"], -0.3)
        self.assertEqual(row["claims"], 1)
        self.assertEqual(len(keeper_events), 3)


if __name__ == "__main__":
    unittest.main()
