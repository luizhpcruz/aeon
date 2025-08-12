from __future__ import annotations
import asyncio
from typing import Dict, Callable, Awaitable
from .protocol import Message

Handler = Callable[[Message], Awaitable[None]]

class Node:
    def __init__(self, name: str):
        self.name = name
        self.inbox: 'asyncio.Queue[Message]' = asyncio.Queue()
        self.peers: Dict[str, Node] = {}
        self.handlers: Dict[str, Handler] = {}
        self._task: asyncio.Task | None = None

    def connect(self, other: 'Node'):
        self.peers[other.name] = other

    def on(self, kind: str, handler: Handler):
        self.handlers[kind] = handler

    async def send(self, dst: str, kind: str, payload: dict):
        msg = Message(kind=kind, src=self.name, dst=dst, payload=payload)
        await self.peers[dst].inbox.put(msg)

    async def dispatch(self, msg: Message):
        h = self.handlers.get(msg.kind)
        if h:
            await h(msg)

    async def _loop(self):
        while True:
            msg = await self.inbox.get()
            await self.dispatch(msg)

    def start(self):
        if not self._task:
            self._task = asyncio.create_task(self._loop())
