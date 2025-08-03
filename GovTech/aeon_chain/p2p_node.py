from fastapi import FastAPI
from app.api import kernel, cosma, chain, ops

app = FastAPI(title="AEON‑GPT Orchestrator")
app.include_router(kernel.router, prefix="/kernel", tags=["Kernel"])
app.include_router(cosma.router, prefix="/cosma", tags=["Cosma"])
app.include_router(chain.router, prefix="/chain", tags=["Chain"])
app.include_router(ops.router, prefix="/ops", tags=["Ops"])

# Placeholder for p2p_node.py
# Logic for managing P2P nodes will be implemented here.
