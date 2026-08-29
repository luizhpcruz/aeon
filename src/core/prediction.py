"""Predição experimental e segura para séries numéricas.

Este módulo não coleta dados, não acessa a rede e não executa ações externas.
Ele fornece um baseline interpretável para comparar futuras abordagens quânticas.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from statistics import mean, pstdev
from typing import Iterable, Mapping


@dataclass(frozen=True)
class PredictionResult:
    """Resultado de uma previsão, sempre acompanhado de incerteza."""

    forecast: float
    scenarios: dict[str, float]
    confidence: float
    abstained: bool
    reason: str


class PrivacyFilter:
    """Remove campos identificáveis antes de uma série chegar ao preditor."""

    DEFAULT_SENSITIVE_FIELDS = frozenset(
        {
            "name",
            "full_name",
            "email",
            "phone",
            "address",
            "location",
            "document",
            "cpf",
            "password",
            "token",
            "api_key",
        }
    )

    def __init__(self, sensitive_fields: Iterable[str] | None = None) -> None:
        self.sensitive_fields = frozenset(
            field.lower()
            for field in (sensitive_fields or self.DEFAULT_SENSITIVE_FIELDS)
        )

    def remove_sensitive_fields(
        self, record: Mapping[str, object]
    ) -> dict[str, object]:
        """Retorna uma cópia sem campos identificáveis ou credenciais."""

        return {
            key: value
            for key, value in record.items()
            if key.lower() not in self.sensitive_fields
        }


class ScenarioPredictor:
    """Baseline explicável para previsão de um próximo ponto numérico.

    O modelo usa a média da primeira diferença como tendência. A confiança
    diminui com volatilidade relativa e a previsão se abstém quando há poucos
    dados ou valores não finitos. O resultado é experimental e não constitui
    diagnóstico, aconselhamento financeiro ou decisão automática.
    """

    def __init__(self, minimum_observations: int = 4, max_relative_volatility: float = 2.0):
        if minimum_observations < 2:
            raise ValueError("minimum_observations deve ser >= 2")
        if max_relative_volatility <= 0:
            raise ValueError("max_relative_volatility deve ser > 0")
        self.minimum_observations = minimum_observations
        self.max_relative_volatility = max_relative_volatility

    def predict(self, observations: Iterable[float]) -> PredictionResult:
        values = [float(value) for value in observations]
        if len(values) < self.minimum_observations:
            return self._abstain("observações insuficientes")
        if not all(isfinite(value) for value in values):
            return self._abstain("há valores não finitos")

        baseline = mean(values)
        changes = [current - previous for previous, current in zip(values, values[1:])]
        trend = mean(changes)
        volatility = pstdev(changes) if len(changes) > 1 else 0.0
        scale = max(abs(baseline), 1e-12)
        relative_volatility = volatility / scale
        forecast = values[-1] + trend

        stability = max(
            0.0,
            1.0 - min(relative_volatility / self.max_relative_volatility, 1.0),
        )
        sample_factor = min(1.0, len(values) / (self.minimum_observations * 3))
        confidence = round(stability * sample_factor, 6)
        direction = "alta" if trend > 0 else "baixa" if trend < 0 else "estável"
        scenarios = self._scenarios(forecast, trend, volatility)
        abstained = relative_volatility > self.max_relative_volatility
        reason = (
            "volatilidade acima do limite; resultado apenas informativo"
            if abstained
            else f"tendência {direction}; baseline interpretável"
        )
        return PredictionResult(
            forecast=forecast,
            scenarios=scenarios,
            confidence=confidence,
            abstained=abstained,
            reason=reason,
        )

    @staticmethod
    def _scenarios(forecast: float, trend: float, volatility: float) -> dict[str, float]:
        spread = max(volatility, abs(trend) * 0.5, 1e-12)
        return {
            "baixo": forecast - spread,
            "central": forecast,
            "alto": forecast + spread,
        }

    @staticmethod
    def _abstain(reason: str) -> PredictionResult:
        return PredictionResult(
            forecast=0.0,
            scenarios={},
            confidence=0.0,
            abstained=True,
            reason=reason,
        )
