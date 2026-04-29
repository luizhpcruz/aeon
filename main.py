import argparse
import time
from collections import deque

from core.engine import ResonanceEngine
from core.entropy import renyi_entropy, shannon_entropy
from data.ingestion import MempoolIngestion
from data.normalization import normalize_tick
from utils.metrics import PerformanceMetrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AEON Synapse V1")
    parser.add_argument("--rpc-url", default=None, help="EVM RPC URL (optional)")
    parser.add_argument("--samples", type=int, default=200, help="Number of ticks to process")
    parser.add_argument("--entropy-window", type=int, default=24, help="Window for entropy")
    parser.add_argument("--entropy-drop-threshold", type=float, default=0.35)
    parser.add_argument("--sleep-ms", type=int, default=50)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ingestion = MempoolIngestion(args.rpc_url)
    engine = ResonanceEngine()
    metrics = PerformanceMetrics()

    signal_window: deque[float] = deque(maxlen=args.entropy_window)
    last_entropy = None

    for _ in range(args.samples):
        start = time.perf_counter()
        tick = ingestion.read_tick()
        x, y = normalize_tick(tick["price_delta"], tick["mempool_volume"])

        triggered, confidence = engine.process_signal(x, y)
        combined_signal = 0.6 * abs(x) + 0.4 * y
        signal_window.append(combined_signal)

        sh = shannon_entropy(list(signal_window))
        re = renyi_entropy(list(signal_window)) if len(signal_window) > 1 else 0.0

        entropy_drop = 0.0 if last_entropy is None else (last_entropy - sh)
        entropy_event = entropy_drop > args.entropy_drop_threshold
        final_trigger = triggered and entropy_event

        # Placeholder PnL proxy: if trigger occurs on low entropy regime.
        pnl_proxy = confidence * 0.001 if final_trigger else -0.0001
        metrics.record_outcome(final_trigger, pnl_proxy)
        metrics.record_latency(start)
        last_entropy = sh

        time.sleep(args.sleep_ms / 1000)

    report = metrics.get_report()
    report["last_shannon_entropy"] = round(last_entropy or 0.0, 6)
    report["last_renyi_entropy"] = round(re, 6)
    print(report)


if __name__ == "__main__":
    main()

