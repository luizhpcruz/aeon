import asyncio, hashlib, json
import websockets

class PeerNode:
    def __init__(self, port=8000):
        self.port = port
        self.ledger = []

    def compute_hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    async def serve(self, websocket, _):
        async for message in websocket:
            block = json.loads(message)
            if block["prev_hash"] == self.ledger[-1]["hash"]:
                self.ledger.append(block)
    
    def new_block(self, data):
        prev = self.ledger[-1] if self.ledger else {"hash": ""}
        block = {"data": data, "prev_hash": prev["hash"]}
        block["hash"] = self.compute_hash(block)
        self.ledger.append(block)
        return block
