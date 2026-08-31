import csv
import json
from pathlib import Path

import pytest

from scripts.offline_predict import load_series, run_experiment


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "value"])
        writer.writeheader()
        writer.writerows(rows)


def test_load_series_sorts_and_skips_missing(tmp_path):
    path = tmp_path / "series.csv"
    write_csv(path, [
        {"date": "2024-03", "value": 3},
        {"date": "2024-01", "value": 1},
        {"date": "2024-02", "value": ""},
        {"date": "2024-04", "value": 4},
        {"date": "2024-05", "value": 5},
    ])

    assert load_series(path, "date", "value") == [
        ("2024-01", 1.0), ("2024-03", 3.0), ("2024-04", 4.0), ("2024-05", 5.0)
    ]


def test_run_experiment_keeps_holdout_temporal_and_compares_baseline():
    rows = [(f"2024-{month:02d}", float(month)) for month in range(1, 9)]

    summary, predictions = run_experiment(rows, holdout=2)

    assert summary["train_records"] == 6
    assert summary["holdout_records"] == 2
    assert len(predictions) == 2
    assert predictions[0]["date"] == "2024-07"
    assert predictions[0]["actual"] == 7.0
    assert predictions[0]["naive_last"] == 6.0
    assert summary["metrics"]["aeon"]["mae"] >= 0


def test_load_series_rejects_unknown_column(tmp_path):
    path = tmp_path / "series.csv"
    write_csv(path, [{"date": "2024-01", "value": 1}] * 4)

    with pytest.raises(ValueError, match="colunas ausentes"):
        load_series(path, "date", "other")
