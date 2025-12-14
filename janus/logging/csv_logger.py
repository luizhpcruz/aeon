import csv
from pathlib import Path
from datetime import datetime


class JanusCSVLogger:
    def __init__(self, symbol: str, base_dir="logs"):
        self.symbol = symbol
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

        self.filepath = self.base_dir / f"{symbol}.csv"
        self._ensure_header()

    def _ensure_header(self):
        if not self.filepath.exists():
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "symbol",
                    "price",
                    "score",
                    "state",
                    "event"
                ])

    def log(self, price, score, state, event=None):
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.utcnow().isoformat(),
                self.symbol,
                round(price, 6),
                score,
                state,
                event or ""
            ])
