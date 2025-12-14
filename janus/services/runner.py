import sys
import csv
from pathlib import Path
from datetime import datetime

from janus.core.engine import JanusEngine
from janus.adapters.yfinance_adapter import fetch_series


# =========================================================
# PATHS
# =========================================================
DATA_DIR = Path("data")
LOG_FILE = DATA_DIR / "janus_log.csv"


# =========================================================
# INIT CSV
# =========================================================
def init_csv():
    DATA_DIR.mkdir(exist_ok=True)

    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "symbol",
            "price",
            "score",
            "state",
            "event"
        ])


# =========================================================
# MAIN
# =========================================================
def main():
    # -------------------------
    # Symbol
    # -------------------------
    if len(sys.argv) < 2:
        print("Usage: python -m janus.services.runner <SYMBOL>")
        sys.exit(1)

    symbol = sys.argv[1]
    print(f"Running JANUS on {symbol}")

    # -------------------------
    # Init
    # -------------------------
    init_csv()
    engine = JanusEngine()

    # -------------------------
    # Fetch data
    # -------------------------
    series = fetch_series(symbol)

    if not series:
        print("No data returned. Exiting.")
        sys.exit(1)

    # -------------------------
    # Process
    # -------------------------
    prev_state = None

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for price in series:
            # Blindagem absoluta
            if not isinstance(price, (int, float)):
                continue

            out = engine.ingest(price)

            event = ""
            if prev_state and prev_state != out.state:
                event = f"REGIME_CHANGE:{prev_state}->{out.state}"

            prev_state = out.state

            writer.writerow([
                datetime.utcnow().isoformat(),
                symbol,
                float(price),
                out.score,
                out.state,
                event
            ])

            # Console feedback
            line = f"Score={out.score:6.2f} | State={out.state}"
            if event:
                line += f" | {event}"
            print(line)


# =========================================================
# ENTRY
# =========================================================
if __name__ == "__main__":
    main()
