import unittest
import numpy as np
from src.manual_mlp import ManualMLPRegressor


class ManualMLPTests(unittest.TestCase):
    def test_training_reduces_loss(self):
        x = np.linspace(-1, 1, 80).reshape(-1, 1)
        y = 2 * x + 0.5
        model = ManualMLPRegressor(1, hidden_size=12, learning_rate=0.02, seed=7)
        losses = model.fit(x, y, epochs=250, batch_size=16)
        self.assertLess(losses[-1], losses[0])
        self.assertEqual(model.predict(x[:3]).shape, (3, 1))

    def test_invalid_feature_shape(self):
        model = ManualMLPRegressor(2)
        with self.assertRaises(ValueError):
            model.predict(np.ones((3, 1)))


if __name__ == "__main__":
    unittest.main()
