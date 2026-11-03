"""Tests for goalkeeper outcome definitions used by the reconstructed pipeline."""
import unittest

from src.build_analysis import is_on_target, is_save


class MetricDefinitionTests(unittest.TestCase):
    def test_outcome_classification(self):
        self.assertTrue(is_save("Saved"))
        self.assertTrue(is_save({"name": "Saved to Post"}))
        self.assertTrue(is_on_target("Goal"))
        self.assertTrue(is_on_target("Saved"))
        self.assertTrue(is_on_target("Saved to Post"))
        self.assertFalse(is_on_target("Off T"))
        self.assertFalse(is_on_target("Blocked"))


if __name__ == "__main__":
    unittest.main()
