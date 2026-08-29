import math

import pytest

from core.prediction import PrivacyFilter, ScenarioPredictor


def test_predicts_next_point_with_interpretable_scenarios():
    result = ScenarioPredictor().predict([10, 12, 14, 16, 18])

    assert result.forecast == pytest.approx(20)
    assert result.scenarios["central"] == pytest.approx(20)
    assert result.scenarios["baixo"] < result.scenarios["central"] < result.scenarios["alto"]
    assert result.confidence > 0
    assert not result.abstained


def test_abstains_when_data_is_insufficient_or_invalid():
    predictor = ScenarioPredictor()

    insufficient = predictor.predict([1, 2, 3])
    invalid = predictor.predict([1, math.nan, 3, 4])

    assert insufficient.abstained
    assert invalid.abstained
    assert insufficient.confidence == 0
    assert invalid.confidence == 0


def test_abstains_when_volatility_exceeds_limit():
    result = ScenarioPredictor(max_relative_volatility=0.1).predict([1, 10, 1, 10, 1])

    assert result.abstained
    assert result.confidence < 1


def test_privacy_filter_drops_identifiers_and_keeps_measurements():
    clean = PrivacyFilter().remove_sensitive_fields(
        {"email": "person@example.com", "name": "Pessoa", "energy": 0.7}
    )

    assert clean == {"energy": 0.7}
