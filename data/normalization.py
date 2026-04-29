def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def normalize_price_delta(price_delta: float, clip: float = 0.05) -> float:
    if clip <= 0:
        return price_delta
    clipped = clamp(price_delta, -clip, clip)
    return clipped / clip


def normalize_mempool_volume(volume: float, scale: float = 500.0) -> float:
    if scale <= 0:
        return volume
    return clamp(volume / scale, 0.0, 1.0)


def normalize_tick(price_delta: float, mempool_volume: float) -> tuple[float, float]:
    return normalize_price_delta(price_delta), normalize_mempool_volume(mempool_volume)

