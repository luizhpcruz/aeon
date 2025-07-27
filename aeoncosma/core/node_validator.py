# aeoncosma/core/node_validator.py
"""
🔍 NODE VALIDATOR - Sistema Avançado de Validação de Nós
Validação cruzada com feedback inteligente e análise de confiança
Desenvolvido por Luiz Cruz - 2025
"""

import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class FeedbackModule:
    """
    Sistema de pontuação e feedback para nós
    """
    
    def __init__(self):
        self.scores = {}  # {node_id: score}
        self.interactions = {}  # Histórico de interações
        
    def get_score(self, node_id: str) -> float:
        """Retorna score do nó (0.0 a 1.0)"""
        return self.scores.get(node_id, 0.5)  # Score neutro inicial
        
    def update_score(self, node_id: str, action: str, success: bool):
        """Atualiza score baseado em ações"""
        current_score = self.get_score(node_id)
        
        # Ajuste baseado na ação
        if success:
            if action == "validation":
                current_score += 0.1
            elif action == "connection":
                current_score += 0.05
            elif action == "broadcast":
                current_score += 0.02
        else:
            current_score -= 0.15 if action == "validation" else 0.05
            
        # Mantém no range 0.0-1.0
        self.scores[node_id] = max(0.0, min(1.0, current_score))
        
        # Registra interação
        if node_id not in self.interactions:
            self.interactions[node_id] = []
            
        self.interactions[node_id].append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "success": success,
            "new_score": self.scores[node_id]
        })

class NodeValidator:
    """
    Validador avançado de nós com integração AEON Core
    """
    
    def __init__(self, aeon_core, feedback_module: Optional[FeedbackModule] = None):
        self.aeon_core = aeon_core  # Referência ao AEON Core
        self.feedback = feedback_module or FeedbackModule()
        
        # Configurações de validação
        self.validation_config = {
            "min_score_threshold": 0.4,
            "require_previous_validation": True,
            "max_validation_time": 30,  # segundos
            "chain_depth_check": 3  # quantos nós anteriores verificar
        }
        
        print("🔍 NodeValidator inicializado com AEON Core")
        print(f"⚙️ Threshold mínimo: {self.validation_config['min_score_threshold']}")

    def validate_node(self, node_info: Dict[str, Any], previous_nodes: List[str], next_nodes: List[str]) -> Dict[str, Any]:
        """
        Valida um novo nó com base na aprovação dos vizinhos e do AEON
        
        Args:
            node_info: Informações do nó a ser validado
            previous_nodes: IDs dos nós anteriores na cadeia
            next_nodes: IDs dos nós seguintes na cadeia
            
        Returns:
            Dict com resultado detalhado da validação
        """
        node_id = node_info.get("id", node_info.get("node_id", "unknown"))
        
        print(f"🔍 [Validator] Iniciando validação de {node_id}...")
        
        validation_start = time.time()
        
        validation_result = {
            "node_id": node_id,
            "validated": False,
            "timestamp": datetime.now().isoformat(),
            "details": {
                "score_check": False,
                "previous_trust": False,
                "next_trust": False,
                "aeon_decision": False,
                "hash_verification": False,
                "chain_integrity": False
            },
            "scores": {},
            "issues": [],
            "recommendations": []
        }
        
        try:
            # 1. Verificação de score atual
            current_score = self.feedback.get_score(node_id)
            validation_result["scores"]["current"] = current_score
            
            print(f"🔍 [Validator] Score atual do nó {node_id}: {current_score:.3f}")
            
            if current_score >= self.validation_config["min_score_threshold"]:
                validation_result["details"]["score_check"] = True
                print(f"✅ [Validator] Score suficiente")
            else:
                validation_result["issues"].append(f"Score insuficiente: {current_score:.3f} < {self.validation_config['min_score_threshold']}")
                print(f"❌ [Validator] Score insuficiente")
            
            # 2. Validação cruzada entre nós vizinhos
            previous_scores = []
            for prev_node in previous_nodes:
                prev_score = self.feedback.get_score(prev_node)
                previous_scores.append(prev_score)
                
            validation_result["scores"]["previous"] = previous_scores
            trust_previous = all(score >= 0.5 for score in previous_scores) if previous_nodes else True
            validation_result["details"]["previous_trust"] = trust_previous
            
            if trust_previous:
                print(f"✅ [Validator] Nós anteriores confiáveis: {previous_scores}")
            else:
                validation_result["issues"].append(f"Nós anteriores não confiáveis: {previous_scores}")
                print(f"❌ [Validator] Nós anteriores não confiáveis")
            
            # 3. Verificação dos nós seguintes (se existirem)
            next_scores = []
            for next_node in next_nodes:
                next_score = self.feedback.get_score(next_node)
                next_scores.append(next_score)
                
            validation_result["scores"]["next"] = next_scores
            trust_next = all(score >= 0.5 for score in next_scores) if next_nodes else True
            validation_result["details"]["next_trust"] = trust_next
            
            if trust_next:
                print(f"✅ [Validator] Nós seguintes confiáveis: {next_scores}")
            else:
                validation_result["issues"].append(f"Nós seguintes não confiáveis: {next_scores}")
                print(f"❌ [Validator] Nós seguintes não confiáveis")
            
            # 4. Verificação de hash e integridade
            node_hash = self.hash_node_info(node_info)
            validation_result["node_hash"] = node_hash
            validation_result["details"]["hash_verification"] = True
            print(f"🔐 [Validator] Hash do nó: {node_hash[:16]}...")
            
            # 5. Verificação de integridade da cadeia
            chain_integrity = self.verify_chain_integrity(node_info, previous_nodes)
            validation_result["details"]["chain_integrity"] = chain_integrity
            
            if chain_integrity:
                print(f"✅ [Validator] Integridade da cadeia verificada")
            else:
                validation_result["issues"].append("Falha na integridade da cadeia")
                print(f"❌ [Validator] Falha na integridade da cadeia")
            
            # 6. Decisão final do AEON
            aeon_decision = self.aeon_core.assess_node(node_info)
            validation_result["details"]["aeon_decision"] = aeon_decision
            
            if aeon_decision:
                print(f"✅ [Validator] AEON aprovou o nó")
            else:
                validation_result["issues"].append("AEON rejeitou o nó")
                print(f"❌ [Validator] AEON rejeitou o nó")
            
            # 7. Decisão final
            all_checks = [
                validation_result["details"]["score_check"],
                validation_result["details"]["previous_trust"],
                validation_result["details"]["next_trust"],
                validation_result["details"]["aeon_decision"],
                validation_result["details"]["hash_verification"],
                validation_result["details"]["chain_integrity"]
            ]
            
            validation_result["validated"] = all(all_checks)
            
            # 8. Atualiza score baseado no resultado
            self.feedback.update_score(
                node_id, 
                "validation", 
                validation_result["validated"]
            )
            
            # 9. Registra no AEON Core
            if validation_result["validated"]:
                prev_id = previous_nodes[0] if previous_nodes else None
                next_id = next_nodes[0] if next_nodes else None
                
                aeon_result = self.aeon_core.register_node(
                    node_id, 
                    node_info, 
                    prev_id=prev_id, 
                    next_id=next_id
                )
                
                validation_result["aeon_registration"] = aeon_result
                print(f"✅ [Validator] Nó registrado no AEON Core")
            
            # 10. Gera recomendações
            validation_result["recommendations"] = self.generate_recommendations(validation_result)
            
            validation_time = time.time() - validation_start
            validation_result["validation_time"] = validation_time
            
            print(f"🎯 [Validator] Resultado final: {'✅ Aprovado' if validation_result['validated'] else '❌ Rejeitado'}")
            print(f"⏱️ [Validator] Tempo de validação: {validation_time:.3f}s")
            
            return validation_result
            
        except Exception as e:
            print(f"❌ [Validator] Erro durante validação: {e}")
            validation_result["issues"].append(f"Erro interno: {str(e)}")
            return validation_result

    def hash_node_info(self, node_info: Dict[str, Any]) -> str:
        """
        Gera hash SHA256 da identidade do nó para segurança
        """
        # Remove campos que podem variar (como timestamp exato)
        hashable_data = {
            k: v for k, v in node_info.items() 
            if k not in ["timestamp", "context"]
        }
        
        # Adiciona timestamp normalizado (só data/hora sem microssegundos)
        if "timestamp" in node_info:
            try:
                dt = datetime.fromisoformat(node_info["timestamp"].replace('Z', '+00:00'))
                hashable_data["timestamp"] = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                hashable_data["timestamp"] = str(node_info["timestamp"])
        
        raw = json.dumps(hashable_data, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def verify_chain_integrity(self, node_info: Dict[str, Any], previous_nodes: List[str]) -> bool:
        """
        Verifica integridade da cadeia de nós
        """
        try:
            # Se não há nós anteriores, é válido (genesis)
            if not previous_nodes:
                return True
            
            # Verifica se nós anteriores existem no AEON
            for prev_node in previous_nodes:
                if prev_node not in self.aeon_core.nodes:
                    print(f"❌ Nó anterior {prev_node} não encontrado no AEON")
                    return False
                    
                if self.aeon_core.nodes[prev_node]["status"] != "VALID":
                    print(f"❌ Nó anterior {prev_node} não é válido")
                    return False
            
            # Verifica referência anterior no node_info
            declared_previous = node_info.get("previous")
            if declared_previous and declared_previous not in previous_nodes:
                print(f"❌ Nó anterior declarado {declared_previous} não está na lista")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na verificação de integridade: {e}")
            return False

    def generate_recommendations(self, validation_result: Dict[str, Any]) -> List[str]:
        """
        Gera recomendações baseadas no resultado da validação
        """
        recommendations = []
        
        if not validation_result["validated"]:
            # Recomendações para nós rejeitados
            if not validation_result["details"]["score_check"]:
                recommendations.append("Melhore a reputação participando de mais validações")
            
            if not validation_result["details"]["previous_trust"]:
                recommendations.append("Conecte-se a nós com melhor reputação")
            
            if not validation_result["details"]["aeon_decision"]:
                recommendations.append("Verifique estrutura de dados e metadados")
                
            if not validation_result["details"]["chain_integrity"]:
                recommendations.append("Verifique referências a nós anteriores")
        else:
            # Recomendações para nós validados
            current_score = validation_result["scores"].get("current", 0.5)
            if current_score < 0.8:
                recommendations.append("Continue melhorando a reputação")
            
            recommendations.append("Mantenha conectividade estável")
            recommendations.append("Participe ativamente da rede")
        
        return recommendations

    def get_validation_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas das validações
        """
        total_nodes = len(self.feedback.scores)
        high_score_nodes = sum(1 for score in self.feedback.scores.values() if score >= 0.8)
        low_score_nodes = sum(1 for score in self.feedback.scores.values() if score < 0.4)
        
        return {
            "total_tracked_nodes": total_nodes,
            "high_reputation_nodes": high_score_nodes,
            "low_reputation_nodes": low_score_nodes,
            "average_score": sum(self.feedback.scores.values()) / total_nodes if total_nodes > 0 else 0,
            "validation_config": self.validation_config,
            "aeon_network_state": self.aeon_core.network_state
        }

def main():
    """Função de teste para o NodeValidator"""
    print("🧪 Testando NodeValidator...")
    
    # Importa e cria AEON Core
    from aeon_core import AeonCore
    
    aeon_core = AeonCore()
    feedback = FeedbackModule()
    validator = NodeValidator(aeon_core, feedback)
    
    # Teste 1: Primeiro nó (sem predecessores)
    print("\n--- Teste 1: Nó Genesis ---")
    genesis_node = {
        "id": "genesis_001",
        "node_id": "genesis_001",
        "host": "127.0.0.1",
        "port": 9001,
        "timestamp": datetime.now().isoformat(),
        "context": {"type": "genesis"}
    }
    
    result1 = validator.validate_node(genesis_node, [], [])
    print(f"Resultado Genesis: {'✅ Validado' if result1['validated'] else '❌ Rejeitado'}")
    print(f"Issues: {result1['issues']}")
    
    # Teste 2: Segundo nó (com predecessor)
    print("\n--- Teste 2: Segundo Nó ---")
    second_node = {
        "id": "node_002",
        "node_id": "node_002", 
        "host": "127.0.0.1",
        "port": 9002,
        "timestamp": datetime.now().isoformat(),
        "previous": "genesis_001",
        "context": {"peers_count": 1}
    }
    
    result2 = validator.validate_node(second_node, ["genesis_001"], [])
    print(f"Resultado Node 002: {'✅ Validado' if result2['validated'] else '❌ Rejeitado'}")
    print(f"Issues: {result2['issues']}")
    
    # Teste 3: Estatísticas
    print("\n--- Teste 3: Estatísticas ---")
    stats = validator.get_validation_stats()
    print(f"Estatísticas: {json.dumps(stats, indent=2, default=str)}")

if __name__ == "__main__":
    main()
