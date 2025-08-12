from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from typing import Any, Dict

@dataclass
class Message:
    kind: str
    src: str
    dst: str
    payload: Dict[str, Any]

    def to_jsonl(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @staticmethod
    def from_jsonl(line: str) -> 'Message':
        obj = json.loads(line)
        return Message(**obj)
