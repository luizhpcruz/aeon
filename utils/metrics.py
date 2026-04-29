import statistics
import time


class PerformanceMetrics:
    def __init__(self) -> None:
        self.start_time = time.perf_counter()
        self.latencies: list[float] = []
        self.returns: list[float] = []
        self.hits = 0
        self.misses = 0

    def record_latency(self, start: float) -> None:
        self.latencies.append(time.perf_counter() - start)

    def record_outcome(self, triggered: bool, pnl: float = 0.0) -> None:
        if triggered:
            self.hits += 1
        else:
            self.misses += 1
        self.returns.append(pnl)

    def sharpe(self, risk_free: float = 0.0) -> float:
        if len(self.returns) < 2:
            return 0.0
        avg = statistics.mean(self.returns) - risk_free
        std = statistics.pstdev(self.returns)
        if std == 0:
            return 0.0
        return avg / std

    def max_drawdown(self) -> float:
        equity = 0.0
        peak = 0.0
        max_dd = 0.0
        for r in self.returns:
            equity += r
            peak = max(peak, equity)
            dd = peak - equity
            max_dd = max(max_dd, dd)
        return max_dd

    def get_report(self) -> dict:
        avg_lat = (sum(self.latencies) / len(self.latencies)) if self.latencies else 0.0
        total = self.hits + self.misses
        hit_rate = (self.hits / total) if total else 0.0
        return {
            "avg_latency_ms": round(avg_lat * 1000, 4),
            "hit_rate": round(hit_rate, 6),
            "sharpe": round(self.sharpe(), 6),
            "max_drawdown": round(self.max_drawdown(), 6),
            "uptime_s": round(time.perf_counter() - self.start_time, 4),
            "samples": total,
        }

