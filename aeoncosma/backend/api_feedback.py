# aeoncosma/backend/api_feedback.py
"""
🚀 AEONCOSMA BACKEND API - Sistema de Feedback e Validação
FastAPI backend para supervisão e validação de nós P2P
Desenvolvido por Luiz Cruz - 2025
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import uvicorn
import asyncio
import os
import sys

# Adiciona path para importações
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = FastAPI(
    title="AEONCOSMA P2P Backend",
    description="Sistema de validação e feedback para rede P2P AEONCOSMA",
    version="1.0.0"
)

# CORS para desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class NodeInfo(BaseModel):
    node_id: str
    host: str
    port: int
    timestamp: str
    previous: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ValidationRequest(BaseModel):
    node_data: NodeInfo
    validator_id: str
    existing_peers: List[Dict[str, Any]] = []

class NetworkStats(BaseModel):
    total_nodes: int
    active_nodes: int
    validation_requests: int
    network_health: float

# Estado global da aplicação
app_state = {
    "validated_nodes": [],
    "validation_history": [],
    "network_stats": {
        "total_validations": 0,
        "approved_validations": 0,
        "rejected_validations": 0,
        "start_time": datetime.now()
    },
    "active_validators": set()
}

def calculate_aeon_score(node_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sistema AEON de pontuação inteligente para validação de nós
    """
    score = 0
    details = {}
    
    # 1. Estrutura dos dados (25 pontos)
    required_fields = ["node_id", "host", "port", "timestamp"]
    structure_score = sum(10 if field in node_data else 0 for field in required_fields[:4])
    if len(required_fields) == 4 and all(field in node_data for field in required_fields):
        structure_score = 25
    score += structure_score
    details["structure"] = structure_score
    
    # 2. Qualidade do node_id (20 pontos)
    node_id = node_data.get("node_id", "")
    if len(node_id) >= 8:
        id_score = 20
    elif len(node_id) >= 5:
        id_score = 15
    else:
        id_score = 5
    score += id_score
    details["node_id_quality"] = id_score
    
    # 3. Timestamp válido (20 pontos)
    try:
        timestamp = datetime.fromisoformat(node_data.get("timestamp", "").replace('Z', '+00:00'))
        age_seconds = (datetime.now() - timestamp).total_seconds()
        
        if age_seconds < 60:  # Menos de 1 minuto
            timestamp_score = 20
        elif age_seconds < 300:  # Menos de 5 minutos
            timestamp_score = 15
        elif age_seconds < 3600:  # Menos de 1 hora
            timestamp_score = 10
        else:
            timestamp_score = 0
            
        score += timestamp_score
        details["timestamp_freshness"] = timestamp_score
        
    except Exception:
        details["timestamp_freshness"] = 0
    
    # 4. Contexto e metadados (20 pontos)
    context = node_data.get("context", {})
    if isinstance(context, dict):
        context_score = min(20, len(context) * 5)  # 5 pontos por campo de contexto
    else:
        context_score = 0
    score += context_score
    details["context_richness"] = context_score
    
    # 5. Conectividade (15 pontos)
    host = node_data.get("host", "")
    port = node_data.get("port", 0)
    
    connectivity_score = 0
    if host in ["127.0.0.1", "localhost"]:
        connectivity_score = 10  # Local válido
    elif host.startswith("192.168.") or host.startswith("10."):
        connectivity_score = 12  # Rede privada
    elif len(host.split(".")) == 4:  # IP público
        connectivity_score = 15
    
    if isinstance(port, int) and 1000 <= port <= 65535:
        connectivity_score = min(15, connectivity_score + 5)
    
    score += connectivity_score
    details["connectivity"] = connectivity_score
    
    # Determinação final
    max_score = 100
    percentage = (score / max_score) * 100
    
    return {
        "score": score,
        "max_score": max_score,
        "percentage": percentage,
        "status": "approved" if percentage >= 70 else "rejected",
        "details": details,
        "recommendation": {
            "action": "accept" if percentage >= 70 else "reject",
            "confidence": percentage / 100,
            "reason": f"Score {score}/{max_score} ({percentage:.1f}%)"
        }
    }

@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "service": "AEONCOSMA P2P Backend",
        "version": "1.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/validate - Validação de nós",
            "/network/stats - Estatísticas da rede",
            "/network/nodes - Lista de nós validados",
            "/health - Status da aplicação"
        ]
    }

@app.post("/validate")
async def validate_node_endpoint(validation_request: ValidationRequest, background_tasks: BackgroundTasks):
    """
    Endpoint principal para validação de nós P2P
    """
    node_data = validation_request.node_data.dict()
    validator_id = validation_request.validator_id
    
    print(f"🔍 Recebida solicitação de validação de {validator_id} para {node_data['node_id']}")
    
    # Registra validador ativo
    app_state["active_validators"].add(validator_id)
    app_state["network_stats"]["total_validations"] += 1
    
    # Calcula score AEON
    aeon_analysis = calculate_aeon_score(node_data)
    
    # Registra histórico
    validation_record = {
        "timestamp": datetime.now().isoformat(),
        "node_id": node_data["node_id"],
        "validator_id": validator_id,
        "score": aeon_analysis["score"],
        "status": aeon_analysis["status"],
        "details": aeon_analysis["details"]
    }
    
    app_state["validation_history"].append(validation_record)
    
    # Atualiza estatísticas
    if aeon_analysis["status"] == "approved":
        app_state["network_stats"]["approved_validations"] += 1
        
        # Adiciona à lista de nós validados se não existe
        existing_node = next(
            (n for n in app_state["validated_nodes"] if n["node_id"] == node_data["node_id"]), 
            None
        )
        
        if not existing_node:
            node_data["validated_at"] = datetime.now().isoformat()
            node_data["validator_id"] = validator_id
            node_data["aeon_score"] = aeon_analysis["score"]
            app_state["validated_nodes"].append(node_data)
            
    else:
        app_state["network_stats"]["rejected_validations"] += 1
    
    # Tarefa de background para limpeza
    background_tasks.add_task(cleanup_old_records)
    
    return {
        "status": aeon_analysis["status"],
        "score": aeon_analysis["score"],
        "percentage": aeon_analysis["percentage"],
        "timestamp": datetime.now().isoformat(),
        "aeon_feedback": aeon_analysis["recommendation"],
        "validation_id": f"val_{len(app_state['validation_history'])}",
        "network_context": {
            "total_nodes": len(app_state["validated_nodes"]),
            "total_validations": app_state["network_stats"]["total_validations"]
        }
    }

@app.get("/network/stats")
async def get_network_stats():
    """Retorna estatísticas da rede P2P"""
    uptime = (datetime.now() - app_state["network_stats"]["start_time"]).total_seconds()
    
    approval_rate = 0
    if app_state["network_stats"]["total_validations"] > 0:
        approval_rate = (app_state["network_stats"]["approved_validations"] / 
                        app_state["network_stats"]["total_validations"]) * 100
    
    return {
        "network_stats": {
            "total_nodes": len(app_state["validated_nodes"]),
            "active_validators": len(app_state["active_validators"]),
            "total_validations": app_state["network_stats"]["total_validations"],
            "approved_validations": app_state["network_stats"]["approved_validations"],
            "rejected_validations": app_state["network_stats"]["rejected_validations"],
            "approval_rate": f"{approval_rate:.1f}%",
            "uptime_seconds": int(uptime)
        },
        "recent_activity": app_state["validation_history"][-10:],  # Últimas 10 validações
        "timestamp": datetime.now().isoformat()
    }

@app.get("/network/nodes")
async def get_validated_nodes():
    """Lista todos os nós validados na rede"""
    return {
        "validated_nodes": app_state["validated_nodes"],
        "count": len(app_state["validated_nodes"]),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/network/node/{node_id}")
async def get_node_info(node_id: str):
    """Informações específicas de um nó"""
    node = next(
        (n for n in app_state["validated_nodes"] if n["node_id"] == node_id),
        None
    )
    
    if not node:
        raise HTTPException(status_code=404, detail="Nó não encontrado")
    
    # Histórico de validações deste nó
    node_history = [
        record for record in app_state["validation_history"] 
        if record["node_id"] == node_id
    ]
    
    return {
        "node_info": node,
        "validation_history": node_history,
        "total_validations": len(node_history),
        "timestamp": datetime.now().isoformat()
    }

@app.delete("/network/node/{node_id}")
async def remove_node(node_id: str):
    """Remove um nó da rede (para manutenção)"""
    initial_count = len(app_state["validated_nodes"])
    app_state["validated_nodes"] = [
        n for n in app_state["validated_nodes"] 
        if n["node_id"] != node_id
    ]
    
    removed = initial_count - len(app_state["validated_nodes"])
    
    if removed == 0:
        raise HTTPException(status_code=404, detail="Nó não encontrado")
    
    return {
        "message": f"Nó {node_id} removido com sucesso",
        "remaining_nodes": len(app_state["validated_nodes"]),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Status de saúde da aplicação"""
    return {
        "status": "healthy",
        "service": "AEONCOSMA P2P Backend",
        "uptime": (datetime.now() - app_state["network_stats"]["start_time"]).total_seconds(),
        "memory_usage": {
            "validated_nodes": len(app_state["validated_nodes"]),
            "validation_history": len(app_state["validation_history"]),
            "active_validators": len(app_state["active_validators"])
        },
        "timestamp": datetime.now().isoformat()
    }

async def cleanup_old_records():
    """Limpa registros antigos para otimizar memória"""
    # Mantém apenas últimas 1000 validações
    if len(app_state["validation_history"]) > 1000:
        app_state["validation_history"] = app_state["validation_history"][-1000:]
    
    # Remove validadores inativos (sem atividade por 1 hora)
    # Esta lógica pode ser expandida conforme necessário
    
def main():
    """Função principal para executar o servidor"""
    print("🚀 Iniciando AEONCOSMA P2P Backend...")
    print("📡 Servidor FastAPI para validação de nós P2P")
    print("🔗 Endpoints disponíveis:")
    print("   - http://localhost:8000/validate (POST)")
    print("   - http://localhost:8000/network/stats (GET)")
    print("   - http://localhost:8000/network/nodes (GET)")
    print("   - http://localhost:8000/health (GET)")
    print("   - http://localhost:8000/docs (Swagger UI)")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
