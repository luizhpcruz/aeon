"""
🚀 AEONCOSMA FastAPI Application
API completa para plataforma modular AEONCOSMA
Copyright 2025 - Luiz H. P. Cruz
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime
import uvicorn

# Importar módulos AEONCOSMA
from aeoncosma.core.engine import AeonCosmaEngine
from aeoncosma.crypto.crypto_engine import CryptoEngine
from aeoncosma.p2p.p2p_node import P2PNode
from aeoncosma.quantum.quantum_channel import QuantumChannel
from aeoncosma.cosmos.cosmos_fitter import CosmosFitter

# Modelos Pydantic para requests
class IALearningRequest(BaseModel):
    data: List[Dict[str, Any]]
    model_type: str = "neural"
    epochs: int = 100

class EncryptionRequest(BaseModel):
    data: str
    algorithm: str = "AES-GCM"

class DecryptionRequest(BaseModel):
    encrypted_data: str
    key: str
    algorithm: str = "AES-GCM"

class P2PBroadcastRequest(BaseModel):
    message: str
    message_type: str = "general"
    priority: int = 1

class QuantumMessageRequest(BaseModel):
    message: str
    sender: str
    receiver: str
    protocol: str = "BB84"

class CosmologyFitRequest(BaseModel):
    model: str = "ΛCDM"
    data_type: str = "supernovas"

class MCMCRequest(BaseModel):
    steps: int = 1000
    model: str = "ΛCDM"

# Criar aplicação FastAPI
app = FastAPI(
    title="AEONCOSMA Engine API",
    description="API completa para plataforma modular AEONCOSMA integrando IA, Blockchain, P2P, Quantum e Cosmologia",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instâncias globais dos módulos
aeon_engine: Optional[AeonCosmaEngine] = None
crypto_engine: Optional[CryptoEngine] = None
p2p_node: Optional[P2PNode] = None
quantum_channel: Optional[QuantumChannel] = None
cosmos_fitter: Optional[CosmosFitter] = None

@app.on_event("startup")
async def startup_event():
    """Inicializar módulos AEONCOSMA na startup"""
    global aeon_engine, crypto_engine, p2p_node, quantum_channel, cosmos_fitter
    
    print("🚀 Inicializando AEONCOSMA Engine...")
    
    # Inicializar módulos
    aeon_engine = AeonCosmaEngine()
    crypto_engine = CryptoEngine()
    p2p_node = P2PNode("api_node")
    quantum_channel = QuantumChannel()
    cosmos_fitter = CosmosFitter()
    
    # Inicializar engine principal
    await aeon_engine.initialize()
    
    print("✅ AEONCOSMA Engine inicializado com sucesso!")

@app.on_event("shutdown")
async def shutdown_event():
    """Finalizar módulos na shutdown"""
    if quantum_channel:
        quantum_channel.shutdown()
    print("🔄 AEONCOSMA Engine finalizado")

# ============================================================================
# 🏠 ROUTES PRINCIPAIS
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "name": "AEONCOSMA Engine API",
        "version": "1.0.0",
        "author": "Luiz H. P. Cruz",
        "description": "Plataforma modular integrando IA, Blockchain, P2P, Quantum e Cosmologia",
        "modules": ["core", "crypto", "p2p", "quantum", "cosmos"],
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status")
async def get_system_status():
    """Status geral do sistema"""
    return {
        "system": "AEONCOSMA Engine",
        "modules": {
            "core": aeon_engine.get_status() if aeon_engine else "not_initialized",
            "crypto": crypto_engine.get_status() if crypto_engine else "not_initialized",
            "p2p": p2p_node.get_status() if p2p_node else "not_initialized",
            "quantum": quantum_channel.get_channel_status() if quantum_channel else "not_initialized",
            "cosmos": cosmos_fitter.get_engine_status() if cosmos_fitter else "not_initialized"
        },
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# 🧠 ROUTES DE INTELIGÊNCIA ARTIFICIAL
# ============================================================================

@app.post("/ia/learn")
async def ia_learning(request: IALearningRequest):
    """Executar aprendizado de IA"""
    if not aeon_engine:
        raise HTTPException(status_code=503, detail="Engine não inicializado")
    
    try:
        result = await aeon_engine.run_ia_learning(
            data=request.data,
            model_type=request.model_type,
            epochs=request.epochs
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no aprendizado: {str(e)}")

@app.get("/ia/models")
async def get_ia_models():
    """Listar modelos de IA disponíveis"""
    return {
        "available_models": ["neural", "symbolic", "hybrid"],
        "neural_architectures": ["MLP", "CNN", "RNN", "Transformer"],
        "symbolic_methods": ["Logic Programming", "Expert Systems", "Knowledge Graphs"],
        "hybrid_approaches": ["Neural-Symbolic", "Neuro-Evolution", "Quantum-Neural"]
    }

@app.post("/ia/predict")
async def ia_predict(data: Dict[str, Any]):
    """Fazer predição com modelo treinado"""
    if not aeon_engine:
        raise HTTPException(status_code=503, detail="Engine não inicializado")
    
    # Simulação de predição
    return {
        "prediction": "sample_prediction",
        "confidence": 0.95,
        "model_used": "latest_trained",
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# 🔐 ROUTES DE CRIPTOGRAFIA
# ============================================================================

@app.post("/crypto/encrypt")
async def encrypt_data(request: EncryptionRequest):
    """Criptografar dados"""
    if not crypto_engine:
        raise HTTPException(status_code=503, detail="Crypto engine não inicializado")
    
    try:
        result = await crypto_engine.encrypt(request.data, request.algorithm)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na criptografia: {str(e)}")

@app.post("/crypto/decrypt")
async def decrypt_data(request: DecryptionRequest):
    """Descriptografar dados"""
    if not crypto_engine:
        raise HTTPException(status_code=503, detail="Crypto engine não inicializado")
    
    try:
        result = await crypto_engine.decrypt(request.encrypted_data, request.key, request.algorithm)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na descriptografia: {str(e)}")

@app.post("/crypto/sign")
async def sign_data(data: Dict[str, str]):
    """Assinar dados digitalmente"""
    if not crypto_engine:
        raise HTTPException(status_code=503, detail="Crypto engine não inicializado")
    
    try:
        result = await crypto_engine.sign_data(data.get("message", ""))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na assinatura: {str(e)}")

@app.post("/crypto/verify")
async def verify_signature(data: Dict[str, str]):
    """Verificar assinatura digital"""
    if not crypto_engine:
        raise HTTPException(status_code=503, detail="Crypto engine não inicializado")
    
    try:
        result = await crypto_engine.verify_signature(
            data.get("message", ""),
            data.get("signature", ""),
            data.get("public_key", "")
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na verificação: {str(e)}")

@app.get("/crypto/algorithms")
async def get_crypto_algorithms():
    """Listar algoritmos criptográficos disponíveis"""
    return {
        "symmetric": ["AES-GCM", "AES-CBC", "ChaCha20-Poly1305"],
        "asymmetric": ["RSA-4096", "ECC-P256", "Ed25519"],
        "hashing": ["SHA3-256", "SHA3-512", "BLAKE2b"],
        "key_derivation": ["PBKDF2", "Scrypt", "Argon2"]
    }

# ============================================================================
# 🌐 ROUTES DE REDE P2P
# ============================================================================

@app.post("/p2p/broadcast")
async def p2p_broadcast(request: P2PBroadcastRequest):
    """Transmitir mensagem na rede P2P"""
    if not p2p_node:
        raise HTTPException(status_code=503, detail="P2P node não inicializado")
    
    try:
        result = await p2p_node.broadcast(request.message, request.message_type, request.priority)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no broadcast: {str(e)}")

@app.get("/p2p/peers")
async def get_p2p_peers():
    """Listar peers conectados"""
    if not p2p_node:
        raise HTTPException(status_code=503, detail="P2P node não inicializado")
    
    return p2p_node.get_status()

@app.post("/p2p/connect")
async def connect_peer(peer_data: Dict[str, str]):
    """Conectar a novo peer"""
    if not p2p_node:
        raise HTTPException(status_code=503, detail="P2P node não inicializado")
    
    try:
        result = await p2p_node.connect_peer(
            peer_data.get("peer_id", ""),
            peer_data.get("address", "")
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na conexão: {str(e)}")

@app.get("/p2p/messages")
async def get_p2p_messages():
    """Obter mensagens recebidas"""
    if not p2p_node:
        raise HTTPException(status_code=503, detail="P2P node não inicializado")
    
    return {
        "received_messages": p2p_node.received_messages[-10:],  # Últimas 10
        "total_messages": len(p2p_node.received_messages),
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# 📡 ROUTES DE COMUNICAÇÃO QUÂNTICA
# ============================================================================

@app.post("/quantum/send")
async def quantum_send(request: QuantumMessageRequest):
    """Enviar mensagem via canal quântico"""
    if not quantum_channel:
        raise HTTPException(status_code=503, detail="Quantum channel não inicializado")
    
    try:
        result = await quantum_channel.send_message({
            "message": request.message,
            "sender": request.sender,
            "receiver": request.receiver,
            "protocol": request.protocol
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no envio quântico: {str(e)}")

@app.get("/quantum/receive/{message_id}")
async def quantum_receive(message_id: str):
    """Receber mensagem quântica"""
    if not quantum_channel:
        raise HTTPException(status_code=503, detail="Quantum channel não inicializado")
    
    try:
        result = await quantum_channel.receive_message(message_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na recepção quântica: {str(e)}")

@app.post("/quantum/key")
async def generate_quantum_key(data: Dict[str, int]):
    """Gerar chave quântica"""
    if not quantum_channel:
        raise HTTPException(status_code=503, detail="Quantum channel não inicializado")
    
    key_length = data.get("length", 256)
    result = quantum_channel.generate_quantum_key(key_length)
    return result

@app.get("/quantum/status")
async def get_quantum_status():
    """Status do canal quântico"""
    if not quantum_channel:
        raise HTTPException(status_code=503, detail="Quantum channel não inicializado")
    
    return quantum_channel.get_channel_status()

# ============================================================================
# 🌌 ROUTES DE ANÁLISE COSMOLÓGICA
# ============================================================================

@app.post("/cosmos/fit")
async def cosmos_fit(request: CosmologyFitRequest):
    """Ajustar modelo cosmológico"""
    if not cosmos_fitter:
        raise HTTPException(status_code=503, detail="Cosmos fitter não inicializado")
    
    try:
        if request.model == "ΛCDM":
            result = await cosmos_fitter.fit_lambda_cdm(request.data_type)
        else:
            raise HTTPException(status_code=400, detail="Modelo não suportado")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no ajuste: {str(e)}")

@app.post("/cosmos/mcmc")
async def cosmos_mcmc(request: MCMCRequest):
    """Executar análise MCMC"""
    if not cosmos_fitter:
        raise HTTPException(status_code=503, detail="Cosmos fitter não inicializado")
    
    try:
        result = await cosmos_fitter.run_mcmc_analysis(request.steps)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no MCMC: {str(e)}")

@app.get("/cosmos/planck")
async def get_planck_parameters():
    """Parâmetros cosmológicos do Planck"""
    if not cosmos_fitter:
        raise HTTPException(status_code=503, detail="Cosmos fitter não inicializado")
    
    return {
        "planck_parameters": {
            name: param.to_dict() 
            for name, param in cosmos_fitter.planck_parameters.items()
        },
        "reference": "Planck Collaboration 2020",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/cosmos/tension")
async def get_hubble_tension():
    """Análise da tensão do H0"""
    if not cosmos_fitter:
        raise HTTPException(status_code=503, detail="Cosmos fitter não inicializado")
    
    return cosmos_fitter.get_hubble_tension_analysis()

@app.get("/cosmos/data")
async def get_cosmos_data():
    """Dados cosmológicos disponíveis"""
    if not cosmos_fitter:
        raise HTTPException(status_code=503, detail="Cosmos fitter não inicializado")
    
    return {
        "pantheon_supernovas": len(cosmos_fitter.pantheon_data),
        "bao_measurements": len(cosmos_fitter.bao_data),
        "planck_parameters": len(cosmos_fitter.planck_parameters),
        "sample_supernova": cosmos_fitter.pantheon_data[0].to_dict() if cosmos_fitter.pantheon_data else None,
        "sample_bao": cosmos_fitter.bao_data[0] if cosmos_fitter.bao_data else None
    }

# ============================================================================
# 🚀 EXECUÇÃO DA APLICAÇÃO
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "aeoncosma_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
