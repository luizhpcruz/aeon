# aeoncosma/core/aeon_kernel.py
"""
👑 AEONCOSMA KERNEL - O Guardião da Identidade
Núcleo de segurança, identidade e ética do nó
Sistema imunológico e córtex pré-frontal do AEONCOSMA
Desenvolvido por Luiz Cruz - 2025
"""

import os
import json
import yaml
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import sqlite3
import logging

# Configuração opcional de segurança
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from security.aeoncosma_security_lock import AeonSecurityLock
    SECURITY_ENABLED = True
except ImportError:
    SECURITY_ENABLED = False
    print("⚠️ Security lock não disponível para AEON Kernel")

@dataclass
class ReputationScore:
    """Estrutura de pontuação de reputação"""
    node_id: str
    current_score: float  # 0.0 a 1.0
    interactions_count: int
    last_interaction: str
    trust_level: str  # "untrusted", "neutral", "trusted", "highly_trusted"
    history: List[Dict]
    decay_factor: float = 0.99  # Decay temporal da reputação

@dataclass
class SecurityPolicy:
    """Política de segurança do nó"""
    min_trust_threshold: float = 0.5
    max_connections: int = 100
    quarantine_threshold: float = 0.2
    auto_ban_threshold: float = 0.1
    reputation_decay_hours: int = 24
    interaction_weight: float = 0.1
    validation_weight: float = 0.3
    contribution_weight: float = 0.4
    consistency_weight: float = 0.2

class ReputationEngine:
    """
    🎯 Motor de Reputação Evolutiva
    Calcula e mantém scores de confiança dinâmicos
    """
    
    def __init__(self, db_path: str = "data/reputation.db"):
        self.db_path = db_path
        self.ensure_directory()
        self.init_database()
        self.reputation_cache = {}
        self.decay_interval = 3600  # 1 hora em segundos
        self.last_decay = time.time()
        
    def ensure_directory(self):
        """Garante que o diretório existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
    def init_database(self):
        """Inicializa base de dados de reputação"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reputation_scores (
                node_id TEXT PRIMARY KEY,
                current_score REAL DEFAULT 0.5,
                interactions_count INTEGER DEFAULT 0,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                trust_level TEXT DEFAULT 'neutral',
                history TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reputation_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                feedback_value REAL NOT NULL,
                context TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (node_id) REFERENCES reputation_scores (node_id)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_node_reputation ON reputation_scores(node_id, current_score);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_timestamp ON reputation_events(timestamp DESC);
        """)
        
        conn.commit()
        conn.close()
        
    def get_reputation(self, node_id: str) -> ReputationScore:
        """Obtém reputação de um nó"""
        # Aplica decay temporal se necessário
        self._apply_temporal_decay()
        
        if node_id in self.reputation_cache:
            return self.reputation_cache[node_id]
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT current_score, interactions_count, last_interaction, 
                   trust_level, history 
            FROM reputation_scores WHERE node_id = ?
        """, (node_id,))
        
        result = cursor.fetchone()
        
        if result:
            score, interactions, last_interaction, trust_level, history_json = result
            history = json.loads(history_json)
        else:
            # Nó novo - reputação neutra
            score = 0.5
            interactions = 0
            last_interaction = datetime.now().isoformat()
            trust_level = "neutral"
            history = []
            
            # Insere novo nó na base
            cursor.execute("""
                INSERT INTO reputation_scores 
                (node_id, current_score, trust_level) 
                VALUES (?, ?, ?)
            """, (node_id, score, trust_level))
            conn.commit()
        
        conn.close()
        
        reputation = ReputationScore(
            node_id=node_id,
            current_score=score,
            interactions_count=interactions,
            last_interaction=last_interaction,
            trust_level=trust_level,
            history=history
        )
        
        self.reputation_cache[node_id] = reputation
        return reputation
        
    def update_reputation(self, node_id: str, feedback: float, 
                         event_type: str, context: Dict = None) -> ReputationScore:
        """
        Atualiza reputação de um nó com feedback (-1.0 a 1.0)
        """
        current_rep = self.get_reputation(node_id)
        
        # Calcula novo score usando fator de aprendizado adaptativo
        learning_rate = self._calculate_learning_rate(current_rep)
        delta = feedback * learning_rate
        new_score = max(0.0, min(1.0, current_rep.current_score + delta))
        
        # Atualiza trust level baseado no novo score
        new_trust_level = self._calculate_trust_level(new_score)
        
        # Adiciona evento ao histórico
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "feedback": feedback,
            "delta": delta,
            "old_score": current_rep.current_score,
            "new_score": new_score,
            "context": context or {}
        }
        
        new_history = current_rep.history.copy()
        new_history.append(event)
        
        # Mantém apenas últimos 100 eventos
        if len(new_history) > 100:
            new_history = new_history[-100:]
        
        # Salva na base de dados
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE reputation_scores 
            SET current_score = ?, interactions_count = ?, 
                last_interaction = ?, trust_level = ?, 
                history = ?, updated_at = CURRENT_TIMESTAMP
            WHERE node_id = ?
        """, (new_score, current_rep.interactions_count + 1,
              datetime.now().isoformat(), new_trust_level,
              json.dumps(new_history), node_id))
        
        # Registra evento
        cursor.execute("""
            INSERT INTO reputation_events 
            (node_id, event_type, feedback_value, context)
            VALUES (?, ?, ?, ?)
        """, (node_id, event_type, feedback, json.dumps(context or {})))
        
        conn.commit()
        conn.close()
        
        # Atualiza cache
        updated_rep = ReputationScore(
            node_id=node_id,
            current_score=new_score,
            interactions_count=current_rep.interactions_count + 1,
            last_interaction=datetime.now().isoformat(),
            trust_level=new_trust_level,
            history=new_history
        )
        
        self.reputation_cache[node_id] = updated_rep
        return updated_rep
        
    def _calculate_learning_rate(self, reputation: ReputationScore) -> float:
        """Calcula taxa de aprendizado adaptativa"""
        # Novos nós aprendem mais rápido
        if reputation.interactions_count < 10:
            return 0.2
        elif reputation.interactions_count < 50:
            return 0.1
        else:
            return 0.05
            
    def _calculate_trust_level(self, score: float) -> str:
        """Determina nível de confiança baseado no score"""
        if score >= 0.8:
            return "highly_trusted"
        elif score >= 0.6:
            return "trusted"
        elif score >= 0.4:
            return "neutral"
        elif score >= 0.2:
            return "low_trust"
        else:
            return "untrusted"
            
    def _apply_temporal_decay(self):
        """Aplica decay temporal nas reputações"""
        current_time = time.time()
        
        if current_time - self.last_decay < self.decay_interval:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Aplica decay gradual para nós inativos
        decay_hours = 24
        cutoff_time = datetime.now() - timedelta(hours=decay_hours)
        
        cursor.execute("""
            UPDATE reputation_scores 
            SET current_score = current_score * 0.99
            WHERE last_interaction < ? AND current_score > 0.5
        """, (cutoff_time.isoformat(),))
        
        cursor.execute("""
            UPDATE reputation_scores 
            SET current_score = current_score * 1.001
            WHERE last_interaction < ? AND current_score < 0.5
        """, (cutoff_time.isoformat(),))
        
        conn.commit()
        conn.close()
        
        self.last_decay = current_time
        self.reputation_cache.clear()  # Limpa cache para forçar reload
        
    def get_network_reputation_stats(self) -> Dict[str, Any]:
        """Estatísticas da rede de reputação"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_nodes,
                AVG(current_score) as avg_score,
                COUNT(CASE WHEN trust_level = 'highly_trusted' THEN 1 END) as highly_trusted,
                COUNT(CASE WHEN trust_level = 'trusted' THEN 1 END) as trusted,
                COUNT(CASE WHEN trust_level = 'neutral' THEN 1 END) as neutral,
                COUNT(CASE WHEN trust_level = 'low_trust' THEN 1 END) as low_trust,
                COUNT(CASE WHEN trust_level = 'untrusted' THEN 1 END) as untrusted
            FROM reputation_scores
        """)
        
        stats = cursor.fetchone()
        conn.close()
        
        return {
            "total_nodes": stats[0],
            "average_score": round(stats[1] or 0.5, 3),
            "trust_distribution": {
                "highly_trusted": stats[2],
                "trusted": stats[3],
                "neutral": stats[4],
                "low_trust": stats[5],
                "untrusted": stats[6]
            }
        }

class AeonKernel:
    """
    👑 Kernel AEON - Guardião da Identidade
    Controla acesso, reputação e políticas de segurança
    """
    
    def __init__(self, node_id: str, config_path: str = "config/security.yml"):
        self.node_id = node_id
        self.config_path = config_path
        
        # 🛡️ Inicialização com segurança
        if SECURITY_ENABLED:
            self.security_lock = AeonSecurityLock()
            self.security_lock.log_execution("aeon_kernel_init", {
                "node_id": node_id,
                "config_path": config_path
            })
            print(f"🔒 [{node_id}] AEON Kernel com segurança ativa")
        
        # Carrega políticas de segurança
        self.security_policy = self._load_security_policy()
        
        # Inicializa motor de reputação
        self.reputation_engine = ReputationEngine(f"data/{node_id}_reputation.db")
        
        # Estado interno do kernel
        self.active_connections = {}
        self.quarantined_nodes = set()
        self.banned_nodes = set()
        self.connection_attempts = {}
        
        # Estatísticas
        self.stats = {
            "connections_allowed": 0,
            "connections_denied": 0,
            "reputation_updates": 0,
            "security_violations": 0,
            "quarantine_actions": 0,
            "kernel_start_time": datetime.now().isoformat()
        }
        
        print(f"👑 [{node_id}] AEON Kernel inicializado")
        print(f"🎯 Threshold de confiança: {self.security_policy.min_trust_threshold}")
        
    def _load_security_policy(self) -> SecurityPolicy:
        """Carrega política de segurança do arquivo de configuração"""
        default_policy = SecurityPolicy()
        
        if not os.path.exists(self.config_path):
            # Cria configuração padrão
            self._create_default_config()
            return default_policy
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            security_config = config.get('security', {})
            
            return SecurityPolicy(
                min_trust_threshold=security_config.get('min_trust_threshold', 0.5),
                max_connections=security_config.get('max_connections', 100),
                quarantine_threshold=security_config.get('quarantine_threshold', 0.2),
                auto_ban_threshold=security_config.get('auto_ban_threshold', 0.1),
                reputation_decay_hours=security_config.get('reputation_decay_hours', 24),
                interaction_weight=security_config.get('interaction_weight', 0.1),
                validation_weight=security_config.get('validation_weight', 0.3),
                contribution_weight=security_config.get('contribution_weight', 0.4),
                consistency_weight=security_config.get('consistency_weight', 0.2)
            )
            
        except Exception as e:
            logging.error(f"Erro ao carregar configuração: {e}")
            return default_policy
            
    def _create_default_config(self):
        """Cria arquivo de configuração padrão"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        default_config = {
            'security': {
                'min_trust_threshold': 0.5,
                'max_connections': 100,
                'quarantine_threshold': 0.2,
                'auto_ban_threshold': 0.1,
                'reputation_decay_hours': 24,
                'interaction_weight': 0.1,
                'validation_weight': 0.3,
                'contribution_weight': 0.4,
                'consistency_weight': 0.2
            },
            'node': {
                'identity': f"AEON-{self.node_id}",
                'capabilities': ["validation", "trading", "ai_decisions"],
                'max_knowledge_entries': 10000
            }
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
            
        print(f"📝 [{self.node_id}] Configuração padrão criada em {self.config_path}")
        
    def validate_incoming_request(self, source_node_id: str, 
                                request_type: str = "connection",
                                context: Dict = None) -> Tuple[bool, str, Dict]:
        """
        Valida se uma requisição de um nó é permitida
        Retorna: (permitido, razão, metadata)
        """
        context = context or {}
        
        # 🛡️ Log de segurança
        if SECURITY_ENABLED:
            self.security_lock.log_execution("validate_request", {
                "source_node": source_node_id,
                "request_type": request_type,
                "context": context
            })
        
        # Verifica se nó está banido
        if source_node_id in self.banned_nodes:
            self.stats["connections_denied"] += 1
            return False, "Nó banido permanentemente", {"action": "banned"}
            
        # Verifica se nó está em quarentena
        if source_node_id in self.quarantined_nodes:
            self.stats["connections_denied"] += 1
            return False, "Nó em quarentena", {"action": "quarantined"}
            
        # Verifica limite de conexões
        if len(self.active_connections) >= self.security_policy.max_connections:
            self.stats["connections_denied"] += 1
            return False, "Limite de conexões atingido", {"action": "limit_reached"}
            
        # Obtém reputação do nó
        reputation = self.reputation_engine.get_reputation(source_node_id)
        
        # Verifica threshold de confiança
        if reputation.current_score < self.security_policy.min_trust_threshold:
            self.stats["connections_denied"] += 1
            
            # Coloca em quarentena se score muito baixo
            if reputation.current_score <= self.security_policy.quarantine_threshold:
                self.quarantined_nodes.add(source_node_id)
                self.stats["quarantine_actions"] += 1
                
            return False, f"Reputação insuficiente: {reputation.current_score:.3f}", {
                "action": "reputation_denied",
                "required_score": self.security_policy.min_trust_threshold,
                "current_score": reputation.current_score,
                "trust_level": reputation.trust_level
            }
            
        # Verifica padrões suspeitos
        if self._detect_suspicious_patterns(source_node_id, request_type, context):
            self.stats["security_violations"] += 1
            return False, "Padrão suspeito detectado", {"action": "suspicious_pattern"}
            
        # Conexão aprovada
        self.active_connections[source_node_id] = {
            "start_time": datetime.now().isoformat(),
            "request_type": request_type,
            "reputation_score": reputation.current_score,
            "trust_level": reputation.trust_level
        }
        
        self.stats["connections_allowed"] += 1
        
        return True, "Conexão autorizada", {
            "action": "approved",
            "reputation_score": reputation.current_score,
            "trust_level": reputation.trust_level,
            "connection_id": hashlib.md5(f"{source_node_id}-{time.time()}".encode()).hexdigest()[:8]
        }
        
    def update_reputation(self, target_node_id: str, feedback: float, 
                         event_type: str, context: Dict = None) -> ReputationScore:
        """
        Atualiza reputação de um nó
        feedback: -1.0 (muito negativo) a 1.0 (muito positivo)
        """
        self.stats["reputation_updates"] += 1
        
        updated_rep = self.reputation_engine.update_reputation(
            target_node_id, feedback, event_type, context
        )
        
        # Ações automáticas baseadas na nova reputação
        if updated_rep.current_score <= self.security_policy.auto_ban_threshold:
            self.banned_nodes.add(target_node_id)
            if target_node_id in self.active_connections:
                del self.active_connections[target_node_id]
            print(f"🚫 [{self.node_id}] Nó {target_node_id} banido automaticamente (score: {updated_rep.current_score:.3f})")
            
        elif updated_rep.current_score <= self.security_policy.quarantine_threshold:
            self.quarantined_nodes.add(target_node_id)
            print(f"⚠️ [{self.node_id}] Nó {target_node_id} colocado em quarentena (score: {updated_rep.current_score:.3f})")
            
        elif target_node_id in self.quarantined_nodes and updated_rep.current_score > self.security_policy.min_trust_threshold:
            self.quarantined_nodes.discard(target_node_id)
            print(f"✅ [{self.node_id}] Nó {target_node_id} removido da quarentena (score: {updated_rep.current_score:.3f})")
            
        return updated_rep
        
    def _detect_suspicious_patterns(self, node_id: str, request_type: str, context: Dict) -> bool:
        """Detecta padrões suspeitos de comportamento"""
        # Rate limiting - muitas tentativas de conexão
        current_time = time.time()
        if node_id not in self.connection_attempts:
            self.connection_attempts[node_id] = []
            
        # Remove tentativas antigas (últimos 5 minutos)
        self.connection_attempts[node_id] = [
            attempt for attempt in self.connection_attempts[node_id]
            if current_time - attempt < 300
        ]
        
        self.connection_attempts[node_id].append(current_time)
        
        # Mais de 10 tentativas em 5 minutos é suspeito
        if len(self.connection_attempts[node_id]) > 10:
            return True
            
        # Padrões suspeitos no contexto
        suspicious_keywords = ['hack', 'exploit', 'bypass', 'override', 'admin']
        context_str = json.dumps(context).lower()
        
        for keyword in suspicious_keywords:
            if keyword in context_str:
                return True
                
        return False
        
    def close_connection(self, node_id: str, reason: str = "normal_close"):
        """Fecha conexão com um nó"""
        if node_id in self.active_connections:
            connection_duration = time.time() - time.mktime(
                datetime.fromisoformat(self.active_connections[node_id]["start_time"]).timetuple()
            )
            
            # Feedback baseado na duração da conexão
            if reason == "normal_close" and connection_duration > 60:
                # Conexão longa e normal - feedback positivo
                self.update_reputation(node_id, 0.1, "connection_duration", {
                    "duration": connection_duration,
                    "reason": reason
                })
            elif reason == "error" or reason == "timeout":
                # Conexão com problemas - feedback negativo
                self.update_reputation(node_id, -0.2, "connection_error", {
                    "duration": connection_duration,
                    "reason": reason
                })
                
            del self.active_connections[node_id]
            
    def get_kernel_status(self) -> Dict[str, Any]:
        """Retorna status completo do kernel"""
        reputation_stats = self.reputation_engine.get_network_reputation_stats()
        
        return {
            "node_id": self.node_id,
            "kernel_stats": self.stats,
            "active_connections": len(self.active_connections),
            "quarantined_nodes": len(self.quarantined_nodes),
            "banned_nodes": len(self.banned_nodes),
            "security_policy": {
                "min_trust_threshold": self.security_policy.min_trust_threshold,
                "max_connections": self.security_policy.max_connections,
                "quarantine_threshold": self.security_policy.quarantine_threshold
            },
            "reputation_network": reputation_stats,
            "security_enabled": SECURITY_ENABLED
        }
        
    def export_reputation_ledger(self) -> str:
        """Exporta ledger completo de reputações"""
        conn = sqlite3.connect(self.reputation_engine.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT node_id, current_score, interactions_count, 
                   last_interaction, trust_level, history
            FROM reputation_scores
            ORDER BY current_score DESC
        """)
        
        ledger = {
            "export_timestamp": datetime.now().isoformat(),
            "kernel_node_id": self.node_id,
            "reputation_entries": []
        }
        
        for row in cursor.fetchall():
            node_id, score, interactions, last_interaction, trust_level, history_json = row
            
            ledger["reputation_entries"].append({
                "node_id": node_id,
                "current_score": score,
                "interactions_count": interactions,
                "last_interaction": last_interaction,
                "trust_level": trust_level,
                "history": json.loads(history_json)
            })
            
        conn.close()
        
        return json.dumps(ledger, indent=2, ensure_ascii=False)

def main():
    """Teste do AEON Kernel"""
    # Exemplo de uso
    kernel = AeonKernel("test_guardian_node")
    
    print("\n👑 TESTANDO AEON KERNEL")
    print("=" * 50)
    
    # Testa validação de conexões
    test_nodes = ["node_002", "node_003", "suspicious_node", "trusted_node"]
    
    for node in test_nodes:
        allowed, reason, metadata = kernel.validate_incoming_request(node, "connection")
        print(f"📡 {node}: {'✅ PERMITIDO' if allowed else '❌ NEGADO'} - {reason}")
        
        if allowed:
            # Simula feedback baseado no nome do nó
            if "suspicious" in node:
                kernel.update_reputation(node, -0.5, "suspicious_behavior")
            elif "trusted" in node:
                kernel.update_reputation(node, 0.3, "good_behavior")
            else:
                kernel.update_reputation(node, 0.1, "normal_interaction")
                
            kernel.close_connection(node, "normal_close")
    
    # Status final
    status = kernel.get_kernel_status()
    print(f"\n📊 STATUS DO KERNEL:")
    print(f"   Conexões permitidas: {status['kernel_stats']['connections_allowed']}")
    print(f"   Conexões negadas: {status['kernel_stats']['connections_denied']}")
    print(f"   Updates de reputação: {status['kernel_stats']['reputation_updates']}")
    print(f"   Nós em quarentena: {status['quarantined_nodes']}")
    
    print(f"\n🌐 REDE DE REPUTAÇÃO:")
    rep_stats = status['reputation_network']
    print(f"   Total de nós: {rep_stats['total_nodes']}")
    print(f"   Score médio: {rep_stats['average_score']}")
    print(f"   Distribuição de confiança: {rep_stats['trust_distribution']}")

if __name__ == "__main__":
    main()
