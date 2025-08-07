from fastapi import FastAPI
from backend.api import kernel, ops, chat

app = FastAPI(
    title="AEON‑AI Hybrid Ops + Chat",
    description="Sistema integrado: IA simbólica + Digital Twin UHE + Comunicação corporativa + Documentação SSMA",
    version="2.0.0"
)

app.include_router(kernel.router, prefix="/kernel", tags=["Kernel"])
app.include_router(ops.router, prefix="/ops", tags=["Operações SSMA"])
app.include_router(chat.router, prefix="/chat", tags=["Comunicação"])

@app.get("/")
async def root():
    return {
        "message": "AEON Digital Twin + Chat Corporativo",
        "version": "2.0.0",
        "features": [
            "IA Simbólica Evolutiva",
            "Digital Twin de UHEs",
            "Chat Corporativo em Tempo Real",
            "Alertas SSMA Prioritários", 
            "Documentação APR/IT/PT",
            "Canal de Emergência",
            "Integração gov.br"
        ],
        "endpoints": {
            "kernel": "/kernel/evolve",
            "ops": "/ops/simulate, /ops/generate_and_sign",
            "chat": "/chat/ws/{user_id}, /chat/online_users",
            "docs": "/docs"
        }
    }
