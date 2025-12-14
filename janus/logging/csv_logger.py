import csv
import os


class CSVLogger:
    def __init__(self, path: str):
        self.path = path
        self.file = None
        self.writer = None

        self._open()

    def _open(self):
        file_exists = os.path.isfile(self.path)

        self.file = open(self.path, mode="a", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)

        if not file_exists:
            self.writer.writerow(
                ["timestamp", "symbol", "price", "score", "state", "event"]
            )
            self.file.flush()

    def log(
        self,
        timestamp: str,
        symbol: str,
        price: float,
        score: float,
        state: str,
        event: str = "",
    ):
        self.writer.writerow(
            [timestamp, symbol, price, score, state, event]
        )
        self.file.flush()

    def close(self):
        if self.file:
            self.file.close()
