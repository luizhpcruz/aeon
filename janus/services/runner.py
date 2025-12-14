import argparse
import os
from datetime import datetime

from janus.core.engine import JanusEngine
from janus.adapters.yfinance_adapter import fetch_series
from janus.logging.csv_logger import CSVLogger


def main():
    parser = argparse.ArgumentParser(
        description="JANUS — Market Regime Anomaly Sensor"
    )

    parser.add_argument(
        "symbol",
        type=str,
        help="Asset symbol (e.g. AAPL, BTC-USD, ^GSPC)"
    )

    parser.add_argument(
        "--period",
        type=str,
        default="6mo",
        help="Data period (default: 6mo)"
    )

    parser.add_argument(
        "--interval",
        type=str,
        default="1d",
        help="Candle interval (default: 1d)"
    )

    parser.add_argument(
        "--log",
        action="store_true",
        help="Enable CSV logging to data/janus_log.csv"
    )

    parser.add_argument(
        "--silent",
        action="store_true",
        help="Do not print step-by-step output"
    )

    args = parser.parse_args()

    symbol = args.symbol
    period = args.period
    interval = args.interval

    print(f"Running JANUS on {symbol} ({interval}, {period})")

    # --- Fetch data ---
    series = fetch_series(symbol, interval=interval, period=period)
    if not series:
        raise RuntimeError("No data returned for symbol")

    # --- Engine ---
    engine = JanusEngine()

    # --- Logger ---
    logger = None
    if args.log:
        os.makedirs("data", exist_ok=True)
        logger = CSVLogger("data/janus_log.csv")

    last_state = None

    # --- Run ---
    for price in series:
        out = engine.ingest(float(price))

        event = ""
        if last_state is not None and out.state != last_state:
            event = f"REGIME_CHANGE:{last_state}->{out.state}"

        last_state = out.state
        ts = datetime.utcnow().isoformat()

        if logger:
            logger.log(
                timestamp=ts,
                symbol=symbol,
                price=float(price),
                score=out.score,
                state=out.state,
                event=event
            )

        if not args.silent:
            line = f"{ts} | {price:.2f} | {out.score:6.2f} | {out.state}"
            if event:
                line += f" | {event}"
            print(line)

    if logger:
        logger.close()

    print("Done.")


if __name__ == "__main__":
    main()
