import random
import time
from typing import Any

from web3 import Web3


class MempoolIngestion:
    def __init__(self, rpc_url: str | None = None) -> None:
        self.rpc_url = rpc_url
        self.w3 = Web3(Web3.HTTPProvider(rpc_url)) if rpc_url else None
        self._last_block = None

    def _simulate(self) -> dict[str, Any]:
        return {
            "timestamp": time.time(),
            "price_delta": random.uniform(-0.015, 0.015),
            "mempool_volume": random.uniform(0.0, 1.0),
            "source": "simulated",
        }

    def read_tick(self) -> dict[str, Any]:
        if self.w3 is None:
            return self._simulate()

        if not self.w3.is_connected():
            return self._simulate()

        latest = self.w3.eth.get_block("latest", full_transactions=False)
        block_number = int(latest.number)
        gas_used = float(latest.gasUsed)
        tx_count = float(len(latest.transactions))

        if self._last_block is None:
            price_delta = 0.0
        else:
            price_delta = (block_number - self._last_block) / max(self._last_block, 1)

        self._last_block = block_number
        mempool_volume = tx_count + (gas_used / 1_000_000)

        return {
            "timestamp": time.time(),
            "price_delta": price_delta,
            "mempool_volume": mempool_volume,
            "source": "rpc",
            "block_number": block_number,
        }

