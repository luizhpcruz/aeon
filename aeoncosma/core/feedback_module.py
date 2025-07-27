# aeoncosma/core/feedback_module.py
"""
🧬 FEEDBACK MODULE - Sistema de Reputação e Confiança
Gerencia scores e reputação entre nós da rede AEONCOSMA
Desenvolvido por Luiz Cruz - 2025
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class FeedbackModule:
    """
    Sistema de feedback e reputação para nós P2P
    """
    
    def __init__(self, default_score: float = 0.5):
        self.scores = {}  # node_id -> score entre 0.0 e 1.0
        self.interactions = {}  # node_id -> lista de interações
        self.default_score = default_score
        
        # Configurações do sistema
        self.config = {
            "max_score": 1.0,
            "min_score": 0.0,
            "decay_rate": 0.99,  # Taxa de decaimento temporal
            "interaction_weight": {
                "validation_success": 0.1,
                "validation_failure": -0.15,
                "connection_success": 0.05,
                "connection_failure": -0.05,
                "broadcast_success": 0.02,
                "broadcast_failure": -0.02,
                "consensus_agreement": 0.08,
                "consensus_disagreement": -0.08
            }
        }
        
        # Estatísticas
        self.stats = {
            "total_interactions": 0,
            "positive_interactions": 0,
            "negative_interactions": 0,
            "nodes_tracked": 0,
            "last_update": None
        }
        
        print(f"🧬 [FeedbackModule] Sistema de reputação inicializado")
        print(f"⚙️ Score padrão: {default_score}, Range: [{self.config['min_score']}, {self.config['max_score']}]")

    def get_score(self, node_id: str) -> float:
        """Retorna score atual do nó"""
        if node_id not in self.scores:
            self.scores[node_id] = self.default_score
            self.stats["nodes_tracked"] = len(self.scores)
            print(f"🆕 [FeedbackModule] Novo nó registrado: {node_id} (score inicial: {self.default_score})")
        
        return self.scores[node_id]

    def update_score(self, node_id: str, interaction_type: str, success: bool = True, custom_delta: Optional[float] = None):
        """Atualiza score baseado em interação"""
        current_score = self.get_score(node_id)
        
        # Calcula delta do score
        if custom_delta is not None:
            delta = custom_delta
        else:
            # Usa configuração padrão baseada no tipo de interação
            weight_key = f"{interaction_type}_{'success' if success else 'failure'}"
            delta = self.config["interaction_weight"].get(weight_key, 0.0)
        
        # Aplica delta
        new_score = current_score + delta
        
        # Mantém no range válido
        new_score = max(self.config["min_score"], min(self.config["max_score"], new_score))
        
        # Atualiza score
        old_score = self.scores[node_id]
        self.scores[node_id] = new_score
        
        # Registra interação
        self._record_interaction(node_id, interaction_type, success, delta, old_score, new_score)
        
        # Atualiza estatísticas
        self.stats["total_interactions"] += 1
        if success:
            self.stats["positive_interactions"] += 1
        else:
            self.stats["negative_interactions"] += 1
        self.stats["last_update"] = datetime.now().isoformat()
        
        print(f"📊 [FeedbackModule] Score de {node_id}: {old_score:.3f} → {new_score:.3f} ({interaction_type})")
        
        return new_score

    def _record_interaction(self, node_id: str, interaction_type: str, success: bool, delta: float, old_score: float, new_score: float):
        """Registra detalhes da interação no histórico"""
        if node_id not in self.interactions:
            self.interactions[node_id] = []
        
        interaction_record = {
            "timestamp": datetime.now().isoformat(),
            "type": interaction_type,
            "success": success,
            "delta": delta,
            "score_before": old_score,
            "score_after": new_score
        }
        
        self.interactions[node_id].append(interaction_record)
        
        # Limita histórico a últimas 100 interações por nó
        if len(self.interactions[node_id]) > 100:
            self.interactions[node_id] = self.interactions[node_id][-100:]

    def get_node_reputation_analysis(self, node_id: str) -> Dict[str, Any]:
        """Análise detalhada da reputação de um nó"""
        if node_id not in self.scores:
            return {"error": "Node not found"}
        
        interactions = self.interactions.get(node_id, [])
        
        # Análise temporal (últimas 24h, 7 dias, etc.)
        now = datetime.now()
        recent_interactions = []
        
        for interaction in interactions:
            try:
                interaction_time = datetime.fromisoformat(interaction["timestamp"])
                hours_ago = (now - interaction_time).total_seconds() / 3600
                
                if hours_ago <= 24:
                    recent_interactions.append(interaction)
            except:
                continue
        
        # Estatísticas por tipo de interação
        interaction_stats = {}
        for interaction in interactions:
            interaction_type = interaction["type"]
            if interaction_type not in interaction_stats:
                interaction_stats[interaction_type] = {"total": 0, "success": 0, "failure": 0}
            
            interaction_stats[interaction_type]["total"] += 1
            if interaction["success"]:
                interaction_stats[interaction_type]["success"] += 1
            else:
                interaction_stats[interaction_type]["failure"] += 1
        
        # Tendência do score
        score_trend = "stable"
        if len(interactions) >= 5:
            recent_deltas = [i["delta"] for i in interactions[-5:]]
            avg_delta = sum(recent_deltas) / len(recent_deltas)
            
            if avg_delta > 0.01:
                score_trend = "improving"
            elif avg_delta < -0.01:
                score_trend = "declining"
        
        return {
            "node_id": node_id,
            "current_score": self.scores[node_id],
            "score_category": self._get_score_category(self.scores[node_id]),
            "total_interactions": len(interactions),
            "recent_interactions_24h": len(recent_interactions),
            "interaction_stats": interaction_stats,
            "score_trend": score_trend,
            "reliability_rating": self._calculate_reliability(node_id),
            "last_interaction": interactions[-1]["timestamp"] if interactions else None
        }

    def _get_score_category(self, score: float) -> str:
        """Categoriza o score em níveis descritivos"""
        if score >= 0.9:
            return "excellent"
        elif score >= 0.75:
            return "good"
        elif score >= 0.5:
            return "average"
        elif score >= 0.25:
            return "poor"
        else:
            return "critical"

    def _calculate_reliability(self, node_id: str) -> float:
        """Calcula índice de confiabilidade (0-100)"""
        interactions = self.interactions.get(node_id, [])
        
        if not interactions:
            return 50.0  # Neutro sem histórico
        
        # Fator 1: Taxa de sucesso
        success_rate = sum(1 for i in interactions if i["success"]) / len(interactions)
        
        # Fator 2: Consistência temporal
        consistency_factor = 1.0
        if len(interactions) >= 10:
            recent_success_rate = sum(1 for i in interactions[-10:] if i["success"]) / 10
            consistency_factor = 1 - abs(success_rate - recent_success_rate)
        
        # Fator 3: Volume de interações (mais interações = mais confiável)
        volume_factor = min(1.0, len(interactions) / 50.0)
        
        # Combina fatores
        reliability = (success_rate * 0.6 + consistency_factor * 0.25 + volume_factor * 0.15) * 100
        
        return round(reliability, 2)

    def apply_temporal_decay(self, decay_hours: int = 24):
        """Aplica decaimento temporal aos scores"""
        print(f"⏰ [FeedbackModule] Aplicando decaimento temporal ({decay_hours}h)")
        
        decay_factor = self.config["decay_rate"] ** (decay_hours / 24)
        decayed_nodes = 0
        
        for node_id in self.scores:
            old_score = self.scores[node_id]
            
            # Aplica decaimento em direção ao score padrão
            self.scores[node_id] = (old_score * decay_factor) + (self.default_score * (1 - decay_factor))
            
            if abs(old_score - self.scores[node_id]) > 0.001:  # Mudança significativa
                decayed_nodes += 1
        
        print(f"📉 [FeedbackModule] {decayed_nodes} nós tiveram scores ajustados pelo decaimento")

    def get_top_nodes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna nós com maior reputação"""
        sorted_nodes = sorted(
            [(node_id, score) for node_id, score in self.scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        top_nodes = []
        for node_id, score in sorted_nodes[:limit]:
            analysis = self.get_node_reputation_analysis(node_id)
            top_nodes.append({
                "node_id": node_id,
                "score": score,
                "category": analysis["score_category"],
                "reliability": analysis["reliability_rating"],
                "interactions": analysis["total_interactions"]
            })
        
        return top_nodes

    def get_network_health(self) -> Dict[str, Any]:
        """Análise da saúde geral da rede"""
        if not self.scores:
            return {"status": "no_data"}
        
        scores = list(self.scores.values())
        
        # Estatísticas básicas
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        # Distribuição por categoria
        categories = {"excellent": 0, "good": 0, "average": 0, "poor": 0, "critical": 0}
        for score in scores:
            category = self._get_score_category(score)
            categories[category] += 1
        
        # Health score geral
        health_score = (avg_score * 0.7) + (categories["excellent"] / len(scores) * 0.3)
        
        return {
            "total_nodes": len(self.scores),
            "average_score": round(avg_score, 3),
            "score_range": {"min": round(min_score, 3), "max": round(max_score, 3)},
            "distribution": categories,
            "network_health_score": round(health_score * 100, 1),
            "recommendation": self._get_network_recommendation(health_score)
        }

    def _get_network_recommendation(self, health_score: float) -> str:
        """Gera recomendação baseada na saúde da rede"""
        if health_score >= 0.8:
            return "Rede saudável - Manter monitoramento regular"
        elif health_score >= 0.6:
            return "Rede estável - Considerar incentivos para nós com baixa reputação"
        elif health_score >= 0.4:
            return "Rede com problemas - Implementar medidas de correção"
        else:
            return "Rede em estado crítico - Ação imediata necessária"

    def export_data(self) -> str:
        """Exporta dados do feedback em JSON"""
        export_data = {
            "scores": self.scores,
            "interactions": self.interactions,
            "config": self.config,
            "stats": self.stats,
            "export_timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(export_data, indent=2)

    def import_data(self, json_data: str) -> bool:
        """Importa dados do feedback de JSON"""
        try:
            data = json.loads(json_data)
            
            self.scores = data.get("scores", {})
            self.interactions = data.get("interactions", {})
            self.stats = data.get("stats", self.stats)
            
            print(f"📥 [FeedbackModule] Dados importados: {len(self.scores)} nós")
            return True
            
        except Exception as e:
            print(f"❌ [FeedbackModule] Erro ao importar dados: {e}")
            return False

def main():
    """Função de teste para FeedbackModule"""
    print("🧪 Testando FeedbackModule...")
    
    feedback = FeedbackModule()
    
    # Simula interações
    test_nodes = ["node_001", "node_002", "node_003"]
    
    for node in test_nodes:
        # Simula várias interações
        feedback.update_score(node, "validation", True)
        feedback.update_score(node, "connection", True)
        feedback.update_score(node, "broadcast", False)  # Uma falha
        feedback.update_score(node, "validation", True)
    
    # Mostra análises
    print("\n📊 Análises de Reputação:")
    for node in test_nodes:
        analysis = feedback.get_node_reputation_analysis(node)
        print(f"{node}: Score {analysis['current_score']:.3f} ({analysis['score_category']}) - Confiabilidade: {analysis['reliability_rating']}%")
    
    # Saúde da rede
    health = feedback.get_network_health()
    print(f"\n🌐 Saúde da Rede: {health['network_health_score']}%")
    print(f"Recomendação: {health['recommendation']}")
    
    # Top nós
    top = feedback.get_top_nodes(3)
    print(f"\n🏆 Top 3 Nós:")
    for i, node_info in enumerate(top, 1):
        print(f"{i}. {node_info['node_id']}: {node_info['score']:.3f} ({node_info['category']})")

if __name__ == "__main__":
    main()
