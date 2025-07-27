# aeoncosma/core/aeon_core.py
"""
🧠 AEON CORE - Motor de Validação e Blockchain Leve
Sistema inteligente de validação de nós com registro blockchain
Desenvolvido por Luiz Cruz - 2025
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class AeonCore:
    """
    Motor central do AEON para validação de nós com blockchain leve
    """
    
    def __init__(self):
        self.ledger = []  # Registro das ações tipo blockchain
        self.nodes = {}   # Dicionário de nós {id: status}
        self.network_state = {
            "total_nodes": 0,
            "valid_nodes": 0,
            "invalid_nodes": 0,
            "last_update": datetime.now().isoformat()
        }
        
        print("🧠 AEON Core inicializado")
        print("📋 Ledger blockchain leve ativo")
        print("🔍 Sistema de validação inteligente pronto")

    def hash_block(self, block: Dict[str, Any]) -> str:
        """Gera hash SHA256 de um bloco"""
        block_string = json.dumps(block, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def get_previous_hash(self) -> str:
        """Retorna hash do último bloco no ledger"""
        if not self.ledger:
            return "0" * 64  # Genesis hash
        return self.ledger[-1]["hash"]

    def validate_node_structure(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida estrutura básica dos dados do nó
        """
        validation_result = {
            "valid": True,
            "score": 0,
            "issues": [],
            "details": {}
        }
        
        # Campos obrigatórios
        required_fields = ["node_id", "host", "port", "timestamp"]
        for field in required_fields:
            if field in node_data:
                validation_result["score"] += 25
                validation_result["details"][f"{field}_present"] = True
            else:
                validation_result["valid"] = False
                validation_result["issues"].append(f"Campo obrigatório ausente: {field}")
                validation_result["details"][f"{field}_present"] = False
        
        # Validação de tipos
        if "port" in node_data:
            if isinstance(node_data["port"], int) and 1000 <= node_data["port"] <= 65535:
                validation_result["details"]["port_valid"] = True
            else:
                validation_result["issues"].append("Porta inválida")
                validation_result["details"]["port_valid"] = False
        
        # Validação de timestamp
        if "timestamp" in node_data:
            try:
                timestamp = datetime.fromisoformat(node_data["timestamp"].replace('Z', '+00:00'))
                age_seconds = (datetime.now() - timestamp).total_seconds()
                
                if age_seconds < 300:  # Menos de 5 minutos
                    validation_result["details"]["timestamp_fresh"] = True
                else:
                    validation_result["issues"].append("Timestamp muito antigo")
                    validation_result["details"]["timestamp_fresh"] = False
                    
            except Exception:
                validation_result["issues"].append("Timestamp inválido")
                validation_result["details"]["timestamp_fresh"] = False
        
        return validation_result

    def validate_node_chain(self, node_data: Dict[str, Any], prev_node_id: Optional[str], next_node_id: Optional[str]) -> bool:
        """
        Verifica se os nós anterior e posterior validam este nó na cadeia
        """
        # Se é o primeiro nó da rede
        if not self.nodes and not prev_node_id:
            return True
        
        # Verifica nó anterior
        if prev_node_id:
            prev_node = self.nodes.get(prev_node_id)
            if not prev_node:
                print(f"❌ Nó anterior {prev_node_id} não encontrado")
                return False
                
            if prev_node["status"] != "VALID":
                print(f"❌ Nó anterior {prev_node_id} não é válido")
                return False
        
        # Verifica nó seguinte (se especificado)
        if next_node_id:
            next_node = self.nodes.get(next_node_id)
            if next_node and next_node["status"] != "VALID":
                print(f"❌ Nó seguinte {next_node_id} não é válido")
                return False
        
        return True

    def assess_node(self, node_info: Dict[str, Any]) -> bool:
        """
        Avaliação inteligente do nó pelo AEON
        """
        # Validação estrutural
        structure_validation = self.validate_node_structure(node_info)
        
        if not structure_validation["valid"]:
            print(f"🧠 AEON: Estrutura inválida - {structure_validation['issues']}")
            return False
        
        # Score baseado em características
        score = structure_validation["score"]
        
        # Pontuação adicional por contexto
        context = node_info.get("context", {})
        if isinstance(context, dict):
            score += min(20, len(context) * 5)  # Até 20 pontos por contexto rico
        
        # Análise de comportamento (baseado em histórico)
        node_id = node_info.get("node_id")
        if node_id in self.nodes:
            # Nó conhecido - verifica histórico
            historical_score = self.get_node_reputation(node_id)
            score = (score + historical_score) / 2  # Média com histórico
        
        # Decisão final do AEON
        approval_threshold = 70
        approved = score >= approval_threshold
        
        print(f"🧠 AEON Assessment: Score {score:.1f}/100 - {'✅ Aprovado' if approved else '❌ Rejeitado'}")
        
        return approved

    def get_node_reputation(self, node_id: str) -> float:
        """
        Calcula reputação do nó baseado no histórico
        """
        if node_id not in self.nodes:
            return 50.0  # Score neutro para nós novos
        
        node_history = [block for block in self.ledger if block.get("node_id") == node_id]
        
        if not node_history:
            return 50.0
        
        # Calcula score baseado no histórico
        valid_actions = sum(1 for block in node_history if block.get("status") == "VALID")
        total_actions = len(node_history)
        
        reputation = (valid_actions / total_actions) * 100 if total_actions > 0 else 50.0
        
        return reputation

    def register_node(self, node_id: str, data: Dict[str, Any], prev_id: Optional[str] = None, next_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Registra um novo nó no sistema AEON com validação completa
        """
        print(f"🧠 AEON: Registrando nó {node_id}...")
        
        # Cria bloco para o ledger
        block = {
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "node_id": node_id,
            "data": data,
            "prev_id": prev_id,
            "next_id": next_id,
            "prev_hash": self.get_previous_hash(),
            "block_number": len(self.ledger) + 1
        }
        
        # Gera hash do bloco
        block_hash = self.hash_block(block)
        block["hash"] = block_hash
        
        # Validação completa
        structure_valid = self.validate_node_structure(data)["valid"]
        chain_valid = self.validate_node_chain(data, prev_id, next_id)
        aeon_approved = self.assess_node(data)
        
        is_valid = structure_valid and chain_valid and aeon_approved
        
        # Registro no sistema
        self.nodes[node_id] = {
            "data": data,
            "last_hash": block_hash,
            "status": "VALID" if is_valid else "INVALID",
            "registered_at": datetime.now().isoformat(),
            "validation_details": {
                "structure_valid": structure_valid,
                "chain_valid": chain_valid,
                "aeon_approved": aeon_approved
            }
        }
        
        # Adiciona ao ledger
        block["status"] = "VALID" if is_valid else "INVALID"
        block["validation_score"] = self.get_node_reputation(node_id) if is_valid else 0
        self.ledger.append(block)
        
        # Atualiza estado da rede
        self.network_state["total_nodes"] = len(self.nodes)
        self.network_state["valid_nodes"] = sum(1 for node in self.nodes.values() if node["status"] == "VALID")
        self.network_state["invalid_nodes"] = self.network_state["total_nodes"] - self.network_state["valid_nodes"]
        self.network_state["last_update"] = datetime.now().isoformat()
        
        print(f"🧠 AEON: Nó {node_id} {'✅ VALIDADO' if is_valid else '❌ REJEITADO'}")
        print(f"📊 Estado da rede: {self.network_state['valid_nodes']}/{self.network_state['total_nodes']} nós válidos")
        
        return {
            "status": self.nodes[node_id]["status"],
            "hash": block_hash,
            "block_number": block["block_number"],
            "validation_details": self.nodes[node_id]["validation_details"]
        }

    def feedback_to_node(self, node_id: str) -> Dict[str, Any]:
        """
        Gera feedback inteligente para o nó
        """
        if node_id not in self.nodes:
            return {
                "msg": "Node not found in AEON registry",
                "code": 404,
                "status": "NOT_FOUND"
            }
        
        node = self.nodes[node_id]
        status = node["status"]
        reputation = self.get_node_reputation(node_id)
        
        if status == "VALID":
            return {
                "msg": "Node accepted by AEON Core",
                "code": 200,
                "status": "VALID",
                "reputation": reputation,
                "network_position": self.get_network_position(node_id),
                "recommendations": self.get_recommendations(node_id)
            }
        else:
            validation_details = node.get("validation_details", {})
            issues = []
            
            if not validation_details.get("structure_valid"):
                issues.append("Invalid data structure")
            if not validation_details.get("chain_valid"):
                issues.append("Chain validation failed")
            if not validation_details.get("aeon_approved"):
                issues.append("AEON assessment failed")
            
            return {
                "msg": "Node rejected by AEON Core",
                "code": 403,
                "status": "INVALID",
                "issues": issues,
                "reputation": reputation,
                "suggestions": self.get_improvement_suggestions(node_id)
            }

    def get_network_position(self, node_id: str) -> Dict[str, Any]:
        """
        Retorna posição do nó na rede
        """
        if node_id not in self.nodes:
            return {}
        
        reputation = self.get_node_reputation(node_id)
        total_valid = self.network_state["valid_nodes"]
        
        # Ranking baseado em reputação
        all_reputations = [self.get_node_reputation(nid) for nid in self.nodes.keys() if self.nodes[nid]["status"] == "VALID"]
        all_reputations.sort(reverse=True)
        
        rank = all_reputations.index(reputation) + 1 if reputation in all_reputations else total_valid
        
        return {
            "rank": rank,
            "total_valid_nodes": total_valid,
            "percentile": ((total_valid - rank + 1) / total_valid) * 100 if total_valid > 0 else 0,
            "reputation": reputation
        }

    def get_recommendations(self, node_id: str) -> List[str]:
        """
        Gera recomendações para nós válidos
        """
        recommendations = []
        reputation = self.get_node_reputation(node_id)
        
        if reputation < 80:
            recommendations.append("Manter consistência nas validações para melhorar reputação")
        
        if len(self.nodes) > 3:
            recommendations.append("Considerar participar de validações cruzadas")
        
        recommendations.append("Manter conectividade estável com peers")
        
        return recommendations

    def get_improvement_suggestions(self, node_id: str) -> List[str]:
        """
        Gera sugestões de melhoria para nós rejeitados
        """
        suggestions = []
        
        if node_id in self.nodes:
            validation_details = self.nodes[node_id].get("validation_details", {})
            
            if not validation_details.get("structure_valid"):
                suggestions.append("Verificar estrutura de dados - campos obrigatórios missing")
            
            if not validation_details.get("chain_valid"):
                suggestions.append("Validar referências a nós anterior/posterior")
            
            if not validation_details.get("aeon_approved"):
                suggestions.append("Melhorar contexto e metadados do nó")
        
        suggestions.append("Verificar conectividade de rede")
        suggestions.append("Aguardar e tentar novamente")
        
        return suggestions

    def get_ledger_summary(self) -> Dict[str, Any]:
        """
        Retorna resumo do ledger blockchain
        """
        if not self.ledger:
            return {
                "total_blocks": 0,
                "genesis_hash": "0" * 64,
                "latest_hash": "0" * 64,
                "chain_integrity": True
            }
        
        # Verifica integridade da cadeia
        chain_integrity = True
        for i in range(1, len(self.ledger)):
            if self.ledger[i]["prev_hash"] != self.ledger[i-1]["hash"]:
                chain_integrity = False
                break
        
        return {
            "total_blocks": len(self.ledger),
            "genesis_hash": self.ledger[0]["hash"] if self.ledger else "0" * 64,
            "latest_hash": self.ledger[-1]["hash"] if self.ledger else "0" * 64,
            "chain_integrity": chain_integrity,
            "network_state": self.network_state,
            "latest_block": self.ledger[-1] if self.ledger else None
        }

    def export_ledger(self) -> str:
        """
        Exporta ledger completo em JSON
        """
        export_data = {
            "ledger": self.ledger,
            "nodes": self.nodes,
            "network_state": self.network_state,
            "export_timestamp": datetime.now().isoformat(),
            "ledger_summary": self.get_ledger_summary()
        }
        
        return json.dumps(export_data, indent=2, default=str)

def main():
    """Função de teste para o AEON Core"""
    print("🧪 Testando AEON Core...")
    
    aeon = AeonCore()
    
    # Teste 1: Primeiro nó (genesis)
    print("\n--- Teste 1: Nó Genesis ---")
    genesis_data = {
        "node_id": "genesis_node",
        "host": "127.0.0.1",
        "port": 9001,
        "timestamp": datetime.now().isoformat(),
        "context": {"type": "genesis", "version": "1.0"}
    }
    
    result1 = aeon.register_node("genesis_node", genesis_data)
    print(f"Resultado: {result1}")
    
    # Teste 2: Segundo nó
    print("\n--- Teste 2: Segundo Nó ---")
    node2_data = {
        "node_id": "node_002",
        "host": "127.0.0.1", 
        "port": 9002,
        "timestamp": datetime.now().isoformat(),
        "previous": "genesis_node",
        "context": {"peers_count": 1, "uptime": 60}
    }
    
    result2 = aeon.register_node("node_002", node2_data, prev_id="genesis_node")
    print(f"Resultado: {result2}")
    
    # Teste 3: Feedback
    print("\n--- Teste 3: Feedback ---")
    feedback1 = aeon.feedback_to_node("genesis_node")
    feedback2 = aeon.feedback_to_node("node_002")
    
    print(f"Feedback Genesis: {feedback1}")
    print(f"Feedback Node 002: {feedback2}")
    
    # Teste 4: Resumo do ledger
    print("\n--- Teste 4: Resumo do Ledger ---")
    summary = aeon.get_ledger_summary()
    print(f"Resumo: {json.dumps(summary, indent=2, default=str)}")

if __name__ == "__main__":
    main()
