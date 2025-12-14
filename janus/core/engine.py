import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class JanusOutput:
    score: float
    state: str
    event: Optional[str] = None


class JanusEngine:
    def __init__(self, window=50, baseline_ratio=0.8, std_floor=1e-4):
        self.window = window
        self.baseline_ratio = baseline_ratio
        self.std_floor = std_floor
        self.buffer = []
        self.state = "Normal"

    def ingest(self, value: float) -> JanusOutput:
        self.buffer.append(value)
        if len(self.buffer) > self.window:
            self.buffer.pop(0)

        score = self._compute_score()
        new_state = self._classify(score)

        event = None
        if new_state != self.state:
            event = f"REGIME_CHANGE:{self.state}->{new_state}"

        self.state = new_state
        return JanusOutput(score=score, state=self.state, event=event)

    def _compute_score(self) -> float:
        if len(self.buffer) < self.window:
            return 0.0

        split = int(self.window * self.baseline_ratio)
        baseline = np.array(self.buffer[:split])
        recent = np.array(self.buffer[split:])

        mean_base = baseline.mean()
        std_base = max(baseline.std(), self.std_floor)
        mean_recent = recent.mean()

        z = abs(mean_recent - mean_base) / std_base
        return min(100.0, round(z * 20, 2))

    def _classify(self, score: float) -> str:
        if self.state == "Normal":
            return "Attention" if score >= 32 else "Normal"

        if self.state == "Attention":
            if score >= 65:
                return "Stress"
            if score <= 25:
                return "Normal"
            return "Attention"

        if self.state == "Stress":
            return "Attention" if score <= 55 else "Stress"
