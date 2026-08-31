#!/usr/bin/env python3
"""Run an offline, local-only AEON prediction experiment.

The input file is never copied, uploaded, or committed. Outputs are written to
an explicit local run directory and contain only experiment artifacts.
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


def load_series(path: Path, date_column: str, value_column: str) -> list[tuple[str, float]]:
    if not path.is_file():
        raise ValueError(f"arquivo não encontrado: {path}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        data_lines = (line for line in handle if not line.lstrip().startswith("#"))
        reader = csv.DictReader(data_lines, skipinitialspace=True)
        if not reader.fieldnames:
            raise ValueError("CSV sem cabeçalho")
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        missing = {date_column, value_column} - set(reader.fieldnames)
        if missing:
            raise ValueError(f"colunas ausentes: {', '.join(sorted(missing))}")
        rows: list[tuple[str, float]] = []
        for line_number, row in enumerate(reader, start=2):
            row = {key.strip(): value for key, value in row.items() if key is not None}
            date = (row.get(date_column) or "").strip()
            raw_value = (row.get(value_column) or "").strip()
            if not date or not raw_value:
                continue
            try:
                value = float(raw_value)
            except ValueError as exc:
                raise ValueError(f"valor inválido na linha {line_number}") from exc
            if not math.isfinite(value):
                continue
            rows.append((date, value))
    rows.sort(key=lambda item: item[0])
    if len(rows) < 4:
        raise ValueError("são necessárias pelo menos 4 observações válidas")
    return rows


def mae(actual: Iterable[float], predicted: Iterable[float]) -> float:
    values = [abs(a - p) for a, p in zip(actual, predicted)]
    return sum(values) / len(values) if values else 0.0


def rmse(actual: Iterable[float], predicted: Iterable[float]) -> float:
    values = [(a - p) ** 2 for a, p in zip(actual, predicted)]
    return math.sqrt(sum(values) / len(values)) if values else 0.0


def run_experiment(rows: list[tuple[str, float]], holdout: int) -> tuple[dict, list[dict]]:
    if holdout < 1 or holdout >= len(rows) - 3:
        raise ValueError("holdout deve deixar pelo menos 4 observações no treino")
    train = rows[:-holdout]
    test = rows[-holdout:]
    history = [value for _, value in train]
    predictor = ScenarioPredictor()
    output: list[dict] = []
    for date, actual in test:
        result = predictor.predict(history)
        output.append({
            "date": date,
            "actual": actual,
            "aeon_forecast": result.forecast,
            "aeon_confidence": result.confidence,
            "aeon_abstained": result.abstained,
            "naive_last": history[-1],
        })
        history.append(actual)
    actual = [row["actual"] for row in output]
    aeon = [row["aeon_forecast"] for row in output]
    naive = [row["naive_last"] for row in output]
    summary = {
        "train_records": len(train),
        "holdout_records": len(test),
        "metrics": {
            "aeon": {"mae": mae(actual, aeon), "rmse": rmse(actual, aeon)},
            "naive_last": {"mae": mae(actual, naive), "rmse": rmse(actual, naive)},
        },
        "aeon_abstention_rate": sum(row["aeon_abstained"] for row in output) / len(output),
        "aeon_mean_confidence": sum(row["aeon_confidence"] for row in output) / len(output),
    }
    return summary, output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="CSV local")
    parser.add_argument("--date-column", default="date")
    parser.add_argument("--value-column", required=True)
    parser.add_argument("--holdout", type=int, default=12)
    parser.add_argument("--output-dir", type=Path, default=Path("runs/offline"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        rows = load_series(args.input, args.date_column, args.value_column)
        summary, predictions = run_experiment(rows, args.holdout)
    except ValueError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary.update({
        "input_sha256": sha256_file(args.input),
        "input_file_name": args.input.name,
        "date_start": rows[0][0],
        "date_end": rows[-1][0],
        "value_column": args.value_column,
        "offline_only": True,
    })
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (args.output_dir / "predictions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=predictions[0].keys())
        writer.writeheader()
        writer.writerows(predictions)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
