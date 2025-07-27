# aeoncosma/core/aeon_core_simplified.py
"""
🧠 AEON CORE SIMPLIFIED - Motor de Decisão Inteligente
Núcleo simplificado do AEON para arquitetura modular
Desenvolvido por Luiz Cruz - 2025
"""

import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class AeonCoreSimplified:
    """
    Motor de decisão AEON simplificado para arquitetura modular
    """
    
    def __init__(self, node_id: str = "aeon_node"):
        self.node_id = node_id
        self.decisions = []  # Histórico de decisões
        self.rules = {}  # Regras de aprovação
        self.pattern_memory = {}  # Memória de padrões
        
        # Configuração de decisão
        self.config = {
            "approval_threshold": 0.7,  # Limiar de aprovação
            "max_decisions": 1000,      # Máximo de decisões em memória
            "learning_rate": 0.1,       # Taxa de aprendizado
            "pattern_retention": 100    # Retenção de padrões
        }
        
        # Estatísticas
        self.stats = {
            "decisions_made": 0,
            "approvals": 0,
            "rejections": 0,
            "patterns_learned": 0,
            "accuracy_rate": 0.0
        }
        
        print(f"🧠 [AeonCore] Motor de decisão inicializado para {node_id}")
        self._initialize_base_rules()

    def _initialize_base_rules(self):
        """Inicializa regras básicas de aprovação"""
        self.rules = {
            "node_structure": {
                "required_fields": ["node_id", "host", "port", "timestamp"],
                "weight": 0.3
            },
            "temporal_validity": {
                "max_age_seconds": 300,  # 5 minutos
                "weight": 0.2
            },
            "network_reputation": {
                "min_score": 0.3,
                "weight": 0.3
            },
            "pattern_consistency": {
                "similarity_threshold": 0.8,
                "weight": 0.2
            }
        }
        
        print(f"⚙️ [AeonCore] Regras básicas configuradas: {len(self.rules)} critérios")

    def make_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Toma decisão baseada no contexto fornecido
        """
        decision_id = self._generate_decision_id()
        timestamp = datetime.now().isoformat()
        
        # Avalia cada critério
        scores = {}
        total_weight = 0
        weighted_score = 0
        
        for rule_name, rule_config in self.rules.items():
            score = self._evaluate_rule(rule_name, rule_config, context)
            weight = rule_config["weight"]
            
            scores[rule_name] = score
            weighted_score += score * weight
            total_weight += weight
        
        # Calcula score final
        final_score = weighted_score / total_weight if total_weight > 0 else 0
        
        # Decisão baseada no threshold
        approved = final_score >= self.config["approval_threshold"]
        
        # Cria registro da decisão
        decision_record = {
            "id": decision_id,
            "timestamp": timestamp,
            "context": context,
            "scores": scores,
            "final_score": final_score,
            "approved": approved,
            "reasoning": self._generate_reasoning(scores, approved),
            "confidence": self._calculate_confidence(scores)
        }
        
        # Armazena decisão
        self.decisions.append(decision_record)
        
        # Limita histórico
        if len(self.decisions) > self.config["max_decisions"]:
            self.decisions = self.decisions[-self.config["max_decisions"]:]
        
        # Atualiza estatísticas
        self._update_stats(approved)
        
        # Aprende com o padrão
        self._learn_pattern(context, final_score)
        
        print(f"🎯 [AeonCore] Decisão {decision_id}: {'✅ APROVADO' if approved else '❌ REJEITADO'} (Score: {final_score:.3f})")
        
        return decision_record

    def _evaluate_rule(self, rule_name: str, rule_config: Dict, context: Dict) -> float:
        """Avalia uma regra específica"""
        try:
            if rule_name == "node_structure":
                return self._evaluate_node_structure(rule_config, context)
            elif rule_name == "temporal_validity":
                return self._evaluate_temporal_validity(rule_config, context)
            elif rule_name == "network_reputation":
                return self._evaluate_network_reputation(rule_config, context)
            elif rule_name == "pattern_consistency":
                return self._evaluate_pattern_consistency(rule_config, context)
            else:
                return 0.5  # Neutro para regras desconhecidas
                
        except Exception as e:
            print(f"⚠️ [AeonCore] Erro ao avaliar regra {rule_name}: {e}")
            return 0.0

    def _evaluate_node_structure(self, rule_config: Dict, context: Dict) -> float:
        """Avalia estrutura do nó"""
        required_fields = rule_config["required_fields"]
        present_fields = 0
        
        for field in required_fields:
            if field in context and context[field] is not None:
                present_fields += 1
        
        return present_fields / len(required_fields)

    def _evaluate_temporal_validity(self, rule_config: Dict, context: Dict) -> float:
        """Avalia validade temporal"""
        if "timestamp" not in context:
            return 0.0
        
        try:
            timestamp = datetime.fromisoformat(context["timestamp"])
            age_seconds = (datetime.now() - timestamp).total_seconds()
            max_age = rule_config["max_age_seconds"]
            
            if age_seconds < 0:  # Timestamp futuro
                return 0.0
            elif age_seconds > max_age:
                return 0.0
            else:
                return 1.0 - (age_seconds / max_age)
                
        except Exception:
            return 0.0

    def _evaluate_network_reputation(self, rule_config: Dict, context: Dict) -> float:
        """Avalia reputação na rede"""
        reputation_score = context.get("reputation_score", rule_config["min_score"])
        min_score = rule_config["min_score"]
        
        if reputation_score < min_score:
            return 0.0
        else:
            return min(1.0, reputation_score)

    def _evaluate_pattern_consistency(self, rule_config: Dict, context: Dict) -> float:
        """Avalia consistência com padrões conhecidos"""
        if not self.pattern_memory:
            return 0.8  # Neutro positivo sem histórico
        
        # Gera fingerprint do contexto
        context_fingerprint = self._generate_context_fingerprint(context)
        
        # Busca padrões similares
        max_similarity = 0.0
        for pattern_id, pattern_data in self.pattern_memory.items():
            similarity = self._calculate_similarity(context_fingerprint, pattern_data["fingerprint"])
            max_similarity = max(max_similarity, similarity)
        
        return max_similarity

    def _generate_context_fingerprint(self, context: Dict) -> str:
        """Gera fingerprint do contexto"""
        relevant_fields = ["node_id", "host", "port"]
        fingerprint_data = {}
        
        for field in relevant_fields:
            if field in context:
                fingerprint_data[field] = str(context[field])
        
        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.md5(fingerprint_str.encode()).hexdigest()

    def _calculate_similarity(self, fingerprint1: str, fingerprint2: str) -> float:
        """Calcula similaridade entre fingerprints"""
        # Similaridade simples baseada em caracteres comuns
        common_chars = sum(c1 == c2 for c1, c2 in zip(fingerprint1, fingerprint2))
        return common_chars / max(len(fingerprint1), len(fingerprint2))

    def _learn_pattern(self, context: Dict, score: float):
        """Aprende padrão do contexto"""
        fingerprint = self._generate_context_fingerprint(context)
        pattern_id = f"pattern_{len(self.pattern_memory)}"
        
        pattern_data = {
            "fingerprint": fingerprint,
            "context": context,
            "score": score,
            "timestamp": datetime.now().isoformat(),
            "usage_count": 1
        }
        
        # Verifica se padrão similar já existe
        existing_pattern = None
        for pid, pdata in self.pattern_memory.items():
            if self._calculate_similarity(fingerprint, pdata["fingerprint"]) > 0.9:
                existing_pattern = pid
                break
        
        if existing_pattern:
            # Atualiza padrão existente
            self.pattern_memory[existing_pattern]["usage_count"] += 1
            self.pattern_memory[existing_pattern]["score"] = (
                self.pattern_memory[existing_pattern]["score"] * 0.9 + score * 0.1
            )
        else:
            # Novo padrão
            self.pattern_memory[pattern_id] = pattern_data
            self.stats["patterns_learned"] += 1
        
        # Limita memória de padrões
        if len(self.pattern_memory) > self.config["pattern_retention"]:
            # Remove padrão menos usado
            least_used = min(self.pattern_memory.keys(), 
                           key=lambda k: self.pattern_memory[k]["usage_count"])
            del self.pattern_memory[least_used]

    def _generate_reasoning(self, scores: Dict[str, float], approved: bool) -> str:
        """Gera explicação da decisão"""
        reasoning_parts = []
        
        for rule_name, score in scores.items():
            if score >= 0.8:
                reasoning_parts.append(f"{rule_name}: excelente ({score:.2f})")
            elif score >= 0.6:
                reasoning_parts.append(f"{rule_name}: bom ({score:.2f})")
            elif score >= 0.4:
                reasoning_parts.append(f"{rule_name}: médio ({score:.2f})")
            else:
                reasoning_parts.append(f"{rule_name}: baixo ({score:.2f})")
        
        result = "Aprovado" if approved else "Rejeitado"
        return f"{result}. Critérios: {', '.join(reasoning_parts)}"

    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """Calcula confiança na decisão"""
        score_values = list(scores.values())
        if not score_values:
            return 0.5
        
        # Confiança baseada na consistência dos scores
        avg_score = sum(score_values) / len(score_values)
        variance = sum((s - avg_score) ** 2 for s in score_values) / len(score_values)
        
        # Menos variância = mais confiança
        confidence = 1.0 - min(1.0, variance)
        return confidence

    def _update_stats(self, approved: bool):
        """Atualiza estatísticas"""
        self.stats["decisions_made"] += 1
        
        if approved:
            self.stats["approvals"] += 1
        else:
            self.stats["rejections"] += 1
        
        # Calcula taxa de aprovação como proxy de acurácia
        if self.stats["decisions_made"] > 0:
            self.stats["accuracy_rate"] = self.stats["approvals"] / self.stats["decisions_made"]

    def _generate_decision_id(self) -> str:
        """Gera ID único para decisão"""
        timestamp = str(int(time.time() * 1000))
        return f"decision_{self.node_id}_{timestamp}"

    def get_decision_history(self, limit: int = 10) -> List[Dict]:
        """Retorna histórico de decisões"""
        return self.decisions[-limit:]

    def get_pattern_analysis(self) -> Dict[str, Any]:
        """Análise dos padrões aprendidos"""
        if not self.pattern_memory:
            return {"status": "no_patterns"}
        
        patterns_by_score = sorted(
            self.pattern_memory.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        return {
            "total_patterns": len(self.pattern_memory),
            "best_pattern": patterns_by_score[0] if patterns_by_score else None,
            "worst_pattern": patterns_by_score[-1] if patterns_by_score else None,
            "average_score": sum(p["score"] for p in self.pattern_memory.values()) / len(self.pattern_memory)
        }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Métricas de performance"""
        return {
            "stats": self.stats,
            "config": self.config,
            "pattern_analysis": self.get_pattern_analysis(),
            "recent_decisions": len([d for d in self.decisions[-10:] if d["approved"]]),
            "memory_usage": {
                "decisions": len(self.decisions),
                "patterns": len(self.pattern_memory)
            }
        }

    def export_knowledge(self) -> str:
        """Exporta conhecimento em JSON"""
        export_data = {
            "node_id": self.node_id,
            "config": self.config,
            "rules": self.rules,
            "pattern_memory": self.pattern_memory,
            "stats": self.stats,
            "recent_decisions": self.decisions[-50:],  # Últimas 50 decisões
            "export_timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(export_data, indent=2)

def main():
    """Teste do AeonCoreSimplified"""
    print("🧪 Testando AeonCoreSimplified...")
    
    aeon = AeonCoreSimplified("test_node")
    
    # Testa decisões
    test_contexts = [
        {
            "node_id": "node_001",
            "host": "192.168.1.100",
            "port": 9000,
            "timestamp": datetime.now().isoformat(),
            "reputation_score": 0.8
        },
        {
            "node_id": "node_002",
            "host": "192.168.1.101",
            "port": 9001,
            "timestamp": datetime.now().isoformat(),
            "reputation_score": 0.3
        },
        {
            "node_id": "node_003",
            "port": 9002,  # Faltando host
            "timestamp": datetime.now().isoformat(),
            "reputation_score": 0.9
        }
    ]
    
    for i, context in enumerate(test_contexts, 1):
        print(f"\n🔍 Teste {i}:")
        decision = aeon.make_decision(context)
        print(f"Resultado: {decision['reasoning']}")
    
    # Métricas finais
    print("\n📊 Métricas Finais:")
    metrics = aeon.get_performance_metrics()
    print(f"Decisões: {metrics['stats']['decisions_made']}")
    print(f"Taxa de aprovação: {metrics['stats']['accuracy_rate']:.1%}")
    print(f"Padrões aprendidos: {metrics['stats']['patterns_learned']}")

if __name__ == "__main__":
    main()
