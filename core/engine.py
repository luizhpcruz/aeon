import numpy as np


class ResonanceEngine:
    def __init__(self, threshold: float = (2 ** 0.5) / 2) -> None:
        self.phi = (1 + 5**0.5) / 2
        self.threshold = threshold
        self.state_vector = np.array([0.0, 0.0], dtype=float)

    def process_signal(self, price_delta: float, mempool_volume: float) -> tuple[bool, float]:
        signal = np.array([price_delta, mempool_volume], dtype=float)
        resonance = np.tanh(np.dot(signal, np.array([self.phi, 1 / self.phi], dtype=float)))
        observation = np.array([resonance, resonance], dtype=float)

        # Exponential smoothing as a lightweight state update.
        self.state_vector = 0.9 * self.state_vector + 0.1 * observation
        confidence = float(np.linalg.norm(self.state_vector))
        return confidence > self.threshold, confidence

