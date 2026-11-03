"""A generic one-hidden-layer MLP regressor implemented with NumPy.

The source presentation confirms a manual neural-network component but does not
specify its architecture, target, inputs, or training protocol. This reusable
implementation is therefore a transparent reconstruction, not a claim to
recover the original model or its results.
"""
from __future__ import annotations
import numpy as np


class ManualMLPRegressor:
    """One-hidden-layer fully connected regressor with manual backpropagation."""

    def __init__(self, input_size: int, hidden_size: int = 8,
                 output_size: int = 1, learning_rate: float = 0.01,
                 seed: int = 42) -> None:
        if min(input_size, hidden_size, output_size) < 1:
            raise ValueError("Layer sizes must be positive.")
        if learning_rate <= 0:
            raise ValueError("learning_rate must be positive.")
        rng = np.random.default_rng(seed)
        self.w1 = rng.normal(0, np.sqrt(2 / input_size), (input_size, hidden_size))
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = rng.normal(0, np.sqrt(2 / hidden_size), (hidden_size, output_size))
        self.b2 = np.zeros((1, output_size))
        self.learning_rate = learning_rate
        self.loss_history: list[float] = []

    @staticmethod
    def _relu(z: np.ndarray) -> np.ndarray:
        return np.maximum(0, z)

    def _forward(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        z1 = x @ self.w1 + self.b1
        hidden = self._relu(z1)
        return hidden, hidden @ self.w2 + self.b2

    def predict(self, features: np.ndarray) -> np.ndarray:
        x = np.asarray(features, dtype=float)
        if x.ndim != 2 or x.shape[1] != self.w1.shape[0]:
            raise ValueError("features must be 2-D with configured input_size.")
        return self._forward(x)[1]

    def fit(self, features: np.ndarray, targets: np.ndarray, epochs: int = 500,
            batch_size: int = 16, shuffle: bool = True,
            seed: int = 42) -> list[float]:
        x = np.asarray(features, dtype=float)
        y = np.asarray(targets, dtype=float)
        if y.ndim == 1:
            y = y.reshape(-1, 1)
        if x.ndim != 2 or x.shape[1] != self.w1.shape[0]:
            raise ValueError("features must be 2-D with configured input_size.")
        if y.shape != (len(x), self.w2.shape[1]):
            raise ValueError("targets shape does not match samples/output_size.")
        if len(x) == 0 or epochs < 1 or batch_size < 1:
            raise ValueError("Data, epochs, and batch_size must be positive.")
        if not np.isfinite(x).all() or not np.isfinite(y).all():
            raise ValueError("Training data must be finite.")
        rng = np.random.default_rng(seed)
        self.loss_history = []
        for _ in range(epochs):
            order = rng.permutation(len(x)) if shuffle else np.arange(len(x))
            for start in range(0, len(x), batch_size):
                idx = order[start:start + batch_size]
                xb, yb = x[idx], y[idx]
                z1 = xb @ self.w1 + self.b1
                hidden = self._relu(z1)
                pred = hidden @ self.w2 + self.b2
                grad_out = (2.0 / len(xb)) * (pred - yb)
                grad_w2 = hidden.T @ grad_out
                grad_b2 = grad_out.sum(axis=0, keepdims=True)
                grad_hidden = grad_out @ self.w2.T
                grad_z1 = grad_hidden * (z1 > 0)
                grad_w1 = xb.T @ grad_z1
                grad_b1 = grad_z1.sum(axis=0, keepdims=True)
                self.w2 -= self.learning_rate * grad_w2
                self.b2 -= self.learning_rate * grad_b2
                self.w1 -= self.learning_rate * grad_w1
                self.b1 -= self.learning_rate * grad_b1
            pred_all = self._forward(x)[1]
            self.loss_history.append(float(np.mean((pred_all - y) ** 2)))
        return self.loss_history
