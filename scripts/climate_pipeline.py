#!/usr/bin/env python3
"""Offline AEON pipeline for NOAA CO2 and NASA global temperature data.

The script reads two local public-data files, aligns them by month, evaluates
AEON's interpretable baseline against a last-value baseline, and writes only
local experiment artifacts. It never downloads data or accesses the network.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.prediction import ScenarioPredictor  # noqa: E402


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def month_key(year: int, month: int) -> str:
    return f"{year:04d}-{month:02d}"


def parse_float(value: str) -> float | None:
    value = value.strip()
    if not value or value in {"***", "-999.99", "-99.99"}:
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def load_noaa_co2(path: Path) -> dict[str, float]:
    """Load NOAA Mauna Loa monthly average CO2 values."""

    if not path.is_file():
        raise ValueError(f"arquivo NOAA não encontrado: {path}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        lines = (line for line in handle if not line.lstrip().startswith("#"))
        reader = csv.DictReader(lines, skipinitialspace=True)
        if not reader.fieldnames:
            raise ValueError("CSV NOAA sem cabeçalho")
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        required = {"year", "month", "average"}
        if not required.issubset(reader.fieldnames):
            raise ValueError("CSV NOAA precisa das colunas year, month e average")
        values: dict[str, float] = {}
        for row in reader:
            try:
                year = int((row.get("year") or "").strip())
                month = int((row.get("month") or "").strip())
            except ValueError:
                continue
            value = parse_float(row.get("average") or "")
            if value is not None and 1 <= month <= 12:
                values[month_key(year, month)] = value
    if len(values) < 4:
        raise ValueError("série NOAA sem observações válidas suficientes")
    return values


def load_nasa_temperature(path: Path) -> dict[str, float]:
    """Load NASA GISTEMP v4 global monthly LOTI anomalies."""

    if not path.is_file():
        raise ValueError(f"arquivo NASA não encontrado: {path}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header: list[str] | None = None
        values: dict[str, float] = {}
        for row in reader:
            cleaned = [cell.strip() for cell in row]
            if cleaned and cleaned[0].lower() == "year":
                header = cleaned
                continue
            if header is None or not cleaned:
                continue
            try:
                year = int(cleaned[0])
            except ValueError:
                continue
            for index, month_name in enumerate(
                ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"),
                start=1,
            ):
                if index >= len(cleaned):
                    continue
                value = parse_float(cleaned[index])
                if value is not None:
                    values[month_key(year, index)] = value
    if len(values) < 4:
        raise ValueError("série NASA sem observações válidas suficientes")
    return values


def mae(actual: Iterable[float], predicted: Iterable[float]) -> float:
    errors = [abs(a - p) for a, p in zip(actual, predicted)]
    return sum(errors) / len(errors) if errors else 0.0


def rmse(actual: Iterable[float], predicted: Iterable[float]) -> float:
    errors = [(a - p) ** 2 for a, p in zip(actual, predicted)]
    return math.sqrt(sum(errors) / len(errors)) if errors else 0.0


def bias(actual: Iterable[float], predicted: Iterable[float]) -> float:
    errors = [p - a for a, p in zip(actual, predicted)]
    return sum(errors) / len(errors) if errors else 0.0


def mase(actual: list[float], predicted: list[float], train: list[float]) -> float:
    denominator = mae(train[1:], train[:-1]) if len(train) > 1 else 0.0
    return mae(actual, predicted) / denominator if denominator > 0 else 0.0


def directional_accuracy(actual: list[float], predicted: list[float], previous: list[float]) -> float:
    comparisons = []
    for observed, forecast, prior in zip(actual, predicted, previous):
        observed_direction = (observed > prior) - (observed < prior)
        forecast_direction = (forecast > prior) - (forecast < prior)
        comparisons.append(observed_direction == forecast_direction)
    return sum(comparisons) / len(comparisons) if comparisons else 0.0


def evaluate_series(rows: list[tuple[str, float]], holdout: int) -> tuple[dict, list[dict]]:
    if holdout < 1 or holdout >= len(rows) - 3:
        raise ValueError("holdout deve deixar pelo menos 4 observações no treino")
    train_rows = rows[:-holdout]
    test_rows = rows[-holdout:]
    history = [value for _, value in train_rows]
    predictor = ScenarioPredictor()
    predictions: list[dict] = []
    for date, actual in test_rows:
        result = predictor.predict(history)
        predictions.append(
            {
                "date": date,
                "actual": actual,
                "aeon_forecast": result.forecast,
                "aeon_confidence": result.confidence,
                "aeon_abstained": result.abstained,
                "naive_last": history[-1],
            }
        )
        history.append(actual)

    actual_values = [row["actual"] for row in predictions]
    aeon_values = [row["aeon_forecast"] for row in predictions]
    naive_values = [row["naive_last"] for row in predictions]
    previous_values = [train_rows[-1][1]] + actual_values[:-1]
    metrics = {
        "aeon": {
            "mae": mae(actual_values, aeon_values),
            "rmse": rmse(actual_values, aeon_values),
            "bias": bias(actual_values, aeon_values),
            "mase": mase(actual_values, aeon_values, [value for _, value in train_rows]),
            "directional_accuracy": directional_accuracy(actual_values, aeon_values, previous_values),
        },
        "naive_last": {
            "mae": mae(actual_values, naive_values),
            "rmse": rmse(actual_values, naive_values),
            "bias": bias(actual_values, naive_values),
            "mase": mase(actual_values, naive_values, [value for _, value in train_rows]),
            "directional_accuracy": directional_accuracy(actual_values, naive_values, previous_values),
        },
    }
    summary = {
        "train_records": len(train_rows),
        "holdout_records": len(test_rows),
        "metrics": metrics,
        "aeon_abstention_rate": sum(row["aeon_abstained"] for row in predictions) / len(predictions),
        "aeon_mean_confidence": sum(row["aeon_confidence"] for row in predictions) / len(predictions),
    }
    return summary, predictions


def write_predictions(path: Path, predictions: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=predictions[0].keys())
        writer.writeheader()
        writer.writerows(predictions)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--co2", required=True, type=Path, help="CSV local da NOAA")
    parser.add_argument("--temperature", required=True, type=Path, help="CSV local da NASA GISTEMP")
    parser.add_argument("--holdout", type=int, default=24, help="meses fora do treino por série")
    parser.add_argument("--output-dir", type=Path, default=Path("runs/climate"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        co2 = load_noaa_co2(args.co2)
        temperature = load_nasa_temperature(args.temperature)
        common_dates = sorted(set(co2) & set(temperature))
        if len(common_dates) < args.holdout + 4:
            raise ValueError("período comum insuficiente entre NOAA e NASA")
        aligned = [(date, co2[date], temperature[date]) for date in common_dates]
        co2_summary, co2_predictions = evaluate_series(
            [(date, value) for date, value, _ in aligned], args.holdout
        )
        temp_summary, temp_predictions = evaluate_series(
            [(date, value) for date, _, value in aligned], args.holdout
        )
    except ValueError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "aligned_climate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["date", "co2_ppm", "global_temperature_anomaly_c"])
        writer.writerows(aligned)
    write_predictions(args.output_dir / "co2_predictions.csv", co2_predictions)
    write_predictions(args.output_dir / "temperature_predictions.csv", temp_predictions)

    summary = {
        "pipeline": "aeon-public-climate-offline-v1",
        "offline_only": True,
        "sources": {
            "noaa_co2": {"file": args.co2.name, "sha256": sha256_file(args.co2)},
            "nasa_gistemp": {"file": args.temperature.name, "sha256": sha256_file(args.temperature)},
        },
        "aligned_records": len(aligned),
        "date_start": common_dates[0],
        "date_end": common_dates[-1],
        "holdout_records": args.holdout,
        "targets": {"co2_ppm": co2_summary, "global_temperature_anomaly_c": temp_summary},
        "limitations": [
            "CO2 é medido em Mauna Loa e não é uma média global.",
            "A previsão é um baseline de tendência, não um modelo climático causal.",
            "Confiança é heurística até haver calibração fora da amostra.",
            "Nenhuma ação externa é executada pelo pipeline.",
        ],
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
