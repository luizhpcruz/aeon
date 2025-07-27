# aeoncosma/networking/validation_logic.py
"""
🔍 AEONCOSMA VALIDATION LOGIC - Lógica de Validação Sequencial
Sistema de validação de nós com consulta ao backend AEON
Desenvolvido por Luiz Cruz - 2025
"""

import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any

# API requests com fallback para mock
def make_aeon_request(node_data: Dict, aeon_address: str) -> Dict:
    """
    Faz request para backend AEON (real ou mock)
    """
    try:
        # Tenta usar requests se disponível
        import requests
        
        response = requests.post(
            f"{aeon_address}/validate",
            json={
                "node_data": node_data,
                "validator_id": "validation_system",
                "existing_peers": []
            },
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Backend retornou status {response.status_code}")
            return mock_validation_response(node_data)
            
    except ImportError:
        print("⚠️ Requests não disponível - usando validação mock")
        return mock_validation_response(node_data)
    except Exception as e:
        print(f"⚠️ Erro ao conectar com backend: {e} - usando mock")
        return mock_validation_response(node_data)

def mock_validation_response(node_data: Dict) -> Dict:
    # Simula delay de rede
    time.sleep(0.1)
    
    # Critérios básicos de validação
    score = 0
    
    # Verifica estrutura dos dados
    if all(key in node_data for key in ["node_id", "host", "port", "timestamp"]):
        score += 25
    
    # Verifica se node_id é válido
    if node_data.get("node_id") and len(node_data["node_id"]) >= 5:
        score += 25
    
    # Verifica timestamp (não muito antigo)
    try:
        timestamp = datetime.fromisoformat(node_data["timestamp"].replace('Z', '+00:00'))
        age = (datetime.now() - timestamp).total_seconds()
        if age < 300:  # Menos de 5 minutos
            score += 25
    except:
        pass
    
    # Verifica informações de contexto
    if node_data.get("context") and isinstance(node_data["context"], dict):
        score += 25
    
    return {
        "status": "approved" if score >= 75 else "rejected",
        "score": score,
        "timestamp": datetime.now().isoformat(),
        "reason": f"Score: {score}/100",
        "aeon_feedback": {
            "trustworthiness": score / 100,
            "recommendation": "accept" if score >= 75 else "reject"
        }
    }

def calculate_node_hash(node_data: Dict) -> str:
    """Calcula hash único do nó baseado em seus dados"""
    # Cria string única baseada nos dados do nó
    unique_string = f"{node_data.get('node_id')}-{node_data.get('host')}-{node_data.get('port')}-{node_data.get('timestamp')}"
    return hashlib.sha256(unique_string.encode()).hexdigest()[:16]

def validate_node_structure(node_data: Dict) -> bool:
    """Valida estrutura básica dos dados do nó"""
    required_fields = ["node_id", "host", "port", "timestamp"]
    
    # Verifica campos obrigatórios
    for field in required_fields:
        if field not in node_data:
            print(f"❌ Campo obrigatório ausente: {field}")
            return False
    
    # Valida tipos
    if not isinstance(node_data["host"], str):
        print("❌ Host deve ser string")
        return False
        
    if not isinstance(node_data["port"], int) or not (1000 <= node_data["port"] <= 65535):
        print("❌ Porta deve ser int entre 1000-65535")
        return False
        
    return True

def check_duplicate_node(node_data: Dict, existing_peers: List[Dict]) -> bool:
    """Verifica se nó já existe na rede"""
    node_id = node_data.get("node_id")
    node_address = f"{node_data.get('host')}:{node_data.get('port')}"
    
    for peer in existing_peers:
        # Verifica ID duplicado
        if peer.get("node_id") == node_id:
            print(f"❌ Node ID já existe: {node_id}")
            return True
            
        # Verifica endereço duplicado
        peer_address = f"{peer.get('host')}:{peer.get('port')}"
        if peer_address == node_address:
            print(f"❌ Endereço já existe: {node_address}")
            return True
    
    return False

def validate_sequential_order(node_data: Dict, validator_id: str, existing_peers: List[Dict]) -> bool:
    """
    Valida ordem sequencial de entrada na rede
    Implementa lógica de validação progressiva
    """
    previous_node = node_data.get("previous")
    
    # Primeiro nó da rede (não tem anterior)
    if not existing_peers and not previous_node:
        print(f"✅ Primeiro nó da rede aceito: {node_data['node_id']}")
        return True
    
    # Se há nós existentes, deve referenciar nó anterior válido
    if existing_peers and previous_node:
        # Verifica se nó anterior existe na rede
        previous_exists = any(peer.get("node_id") == previous_node for peer in existing_peers)
        if previous_exists:
            print(f"✅ Sequência válida: {previous_node} → {node_data['node_id']}")
            return True
        else:
            print(f"❌ Nó anterior não encontrado: {previous_node}")
            return False
    
    # Casos inválidos
    if existing_peers and not previous_node:
        print(f"❌ Nó deve referenciar nó anterior existente")
        return False
        
    print(f"✅ Validação sequencial aprovada para {node_data['node_id']}")
    return True

def validate_node(node_data: Dict, validator_id: str, existing_peers: List[Dict], aeon_address: str) -> bool:
    """
    Função principal de validação de nó
    Combina validações estruturais, sequenciais e consulta AEON
    """
    print(f"🔍 [{validator_id}] Iniciando validação de {node_data.get('node_id', 'unknown')}")
    
    # 1. Validação estrutural
    if not validate_node_structure(node_data):
        print(f"❌ [{validator_id}] Falha na validação estrutural")
        return False
    
    # 2. Verificação de duplicatas
    if check_duplicate_node(node_data, existing_peers):
        print(f"❌ [{validator_id}] Nó duplicado detectado")
        return False
    
    # 3. Validação sequencial
    if not validate_sequential_order(node_data, validator_id, existing_peers):
        print(f"❌ [{validator_id}] Falha na validação sequencial")
        return False
    
    # 4. Consulta ao backend AEON
    try:
        print(f"🔗 [{validator_id}] Consultando backend AEON...")
        aeon_response = make_aeon_request(node_data, aeon_address)
        
        if aeon_response.get("status") == "approved":
            score = aeon_response.get("score", 0)
            print(f"✅ [{validator_id}] AEON aprovou nó com score {score}/100")
            
            # Adiciona informações de validação ao nó
            node_data["validation"] = {
                "validator_id": validator_id,
                "validated_at": datetime.now().isoformat(),
                "aeon_score": score,
                "node_hash": calculate_node_hash(node_data)
            }
            
            return True
        else:
            reason = aeon_response.get("reason", "Sem motivo especificado")
            print(f"❌ [{validator_id}] AEON rejeitou nó: {reason}")
            return False
            
    except Exception as e:
        print(f"❌ [{validator_id}] Erro ao consultar AEON: {e}")
        return False

def validate_network_integrity(peers: List[Dict]) -> Dict:
    """
    Valida integridade geral da rede
    Verifica se sequência de nós faz sentido
    """
    print("🔍 Validando integridade da rede...")
    
    if not peers:
        return {"valid": True, "issues": [], "network_health": 100}
    
    issues = []
    
    # Verifica IDs únicos
    node_ids = [peer.get("node_id") for peer in peers]
    duplicates = [nid for nid in node_ids if node_ids.count(nid) > 1]
    if duplicates:
        issues.append(f"IDs duplicados: {duplicates}")
    
    # Verifica endereços únicos
    addresses = [f"{peer.get('host')}:{peer.get('port')}" for peer in peers]
    duplicate_addresses = [addr for addr in addresses if addresses.count(addr) > 1]
    if duplicate_addresses:
        issues.append(f"Endereços duplicados: {duplicate_addresses}")
    
    # Verifica validações
    unvalidated = [peer.get("node_id") for peer in peers if "validation" not in peer]
    if unvalidated:
        issues.append(f"Nós sem validação: {unvalidated}")
    
    # Calcula saúde da rede
    health_score = max(0, 100 - (len(issues) * 20))
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "network_health": health_score,
        "total_peers": len(peers),
        "validated_peers": len(peers) - len(unvalidated)
    }

def main():
    """Função de teste para validação"""
    print("🧪 Testando sistema de validação AEONCOSMA")
    
    # Dados de teste
    test_node = {
        "node_id": "test_node_001",
        "host": "127.0.0.1",
        "port": 9001,
        "timestamp": datetime.now().isoformat(),
        "previous": None,
        "context": {
            "peers_count": 0,
            "uptime": 0
        }
    }
    
    existing_peers = []
    
    # Teste de validação
    result = validate_node(
        test_node, 
        "validator_001", 
        existing_peers, 
        "http://localhost:8000/validate"
    )
    
    print(f"🎯 Resultado da validação: {'✅ Aprovado' if result else '❌ Rejeitado'}")
    
    if result:
        existing_peers.append(test_node)
        
        # Teste de integridade
        integrity = validate_network_integrity(existing_peers)
        print(f"🌐 Integridade da rede: {integrity}")

if __name__ == "__main__":
    main()
