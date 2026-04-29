import math
from collections import Counter


def _bucketize(values: list[float], precision: int = 4) -> list[float]:
    return [round(v, precision) for v in values]


def shannon_entropy(values: list[float]) -> float:
    if not values:
        return 0.0
    buckets = _bucketize(values)
    counts = Counter(buckets)
    total = len(buckets)
    entropy = 0.0
    for c in counts.values():
        p = c / total
        entropy -= p * math.log2(p)
    return entropy


def renyi_entropy(values: list[float], alpha: float = 2.0) -> float:
    if not values:
        return 0.0
    if alpha <= 0 or alpha == 1:
        raise ValueError("alpha must be > 0 and != 1")
    buckets = _bucketize(values)
    counts = Counter(buckets)
    total = len(buckets)
    probs = [(c / total) for c in counts.values()]
    s = sum(p**alpha for p in probs)
    return (1 / (1 - alpha)) * math.log2(s)

