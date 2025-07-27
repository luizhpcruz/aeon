# aeoncosma/reasoning/interaction_engine.py
"""
🧠⚡ AEONCOSMA INTERACTION ENGINE - O Motor de Raciocínio
Orquestra o pensamento, traduz linguagem humana em ações simbólicas
Distribui raciocínio pela rede e cria auditoria imutável
Desenvolvido por Luiz Cruz - 2025
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
import asyncio
import sqlite3
import os

# Importações internas
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from aeoncosma.cognitive.gpt_node import GPTNode
    from aeoncosma.communication.p2p_interface import P2PInterface, SymbolicMessage
    from aeoncosma.core.aeon_kernel import AeonKernel
    from security.aeoncosma_security_lock import AeonSecurityLock
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    print(f"⚠️ Dependências parciais para Interaction Engine: {e}")

@dataclass
class ReasoningStep:
    """
    🔍 Passo individual no processo de raciocínio
    """
    step_id: str
    step_type: str  # "translate", "local_query", "distributed_query", "synthesis", "validation"
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    processing_node: str
    timestamp: str
    confidence: float
    execution_time: float
    metadata: Dict[str, Any]

@dataclass
class ReasoningTrail:
    """
    🛤️ Trilha completa de raciocínio para auditoria
    """
    trail_id: str
    human_request: str
    symbolic_request: Dict[str, Any]
    reasoning_steps: List[ReasoningStep]
    final_result: Dict[str, Any]
    participating_nodes: List[str]
    total_execution_time: float
    confidence_score: float
    start_timestamp: str
    end_timestamp: str
    trail_hash: str

class SymbolicTranslator:
    """
    🔄 Tradutor de Linguagem Natural para Protocolo Simbólico
    """
    
    def __init__(self):
        # Padrões de tradução de linguagem natural para simbólico
        self.translation_patterns = {
            # Consultas de trading
            r"(?i)(preço|price|valor).*(bitcoin|btc|crypto)": {
                "action": "QUERY",
                "subject": "PRICE_ANALYSIS",
                "category": "TRADING"
            },
            r"(?i)(análise|analysis).*(mercado|market)": {
                "action": "QUERY", 
                "subject": "MARKET_ANALYSIS",
                "category": "TRADING"
            },
            r"(?i)(previsão|prediction|forecast)": {
                "action": "QUERY",
                "subject": "MARKET_PREDICTION", 
                "category": "AI_DECISION"
            },
            
            # Consultas de conhecimento
            r"(?i)(como|how|o que|what).*(funciona|works?)": {
                "action": "QUERY",
                "subject": "KNOWLEDGE_REQUEST",
                "category": "KNOWLEDGE"
            },
            r"(?i)(explicar|explain|definir|define)": {
                "action": "QUERY",
                "subject": "EXPLANATION_REQUEST",
                "category": "KNOWLEDGE"
            },
            
            # Comandos de rede
            r"(?i)(conectar|connect).*(nó|node|peer)": {
                "action": "NETWORK_COMMAND",
                "subject": "PEER_CONNECTION",
                "category": "NETWORK"
            },
            r"(?i)(status|estado).*(rede|network)": {
                "action": "QUERY",
                "subject": "NETWORK_STATUS",
                "category": "NETWORK"
            },
            
            # Validações e consenso
            r"(?i)(validar|validate|verificar|verify)": {
                "action": "VALIDATE",
                "subject": "VALIDATION_REQUEST",
                "category": "AI_DECISION"
            },
            r"(?i)(consenso|consensus|acordo|agreement)": {
                "action": "CONSENSUS_REQUEST",
                "subject": "CONSENSUS_BUILDING",
                "category": "NETWORK"
            }
        }
        
        # Estratégias de distribuição
        self.distribution_strategies = {
            "SELF": "Processamento local apenas",
            "NEAREST": "Nós mais próximos/confiáveis",
            "SPECIALIZED": "Nós com expertise específica",
            "CONSENSUS": "Maioria para consenso",
            "BROADCAST": "Todos os nós disponíveis"
        }
        
    def translate_to_symbolic(self, human_text: str, context: Dict = None) -> Dict[str, Any]:
        """
        Traduz texto humano para protocolo simbólico
        """
        import re
        
        context = context or {}
        
        # Analisa padrões na entrada
        matched_pattern = None
        for pattern, symbolic_data in self.translation_patterns.items():
            if re.search(pattern, human_text):
                matched_pattern = symbolic_data
                break
        
        if not matched_pattern:
            # Fallback para consulta genérica
            matched_pattern = {
                "action": "QUERY",
                "subject": "GENERAL_INQUIRY",
                "category": "KNOWLEDGE"
            }
        
        # Determina estratégia de distribuição
        distribution_strategy = self._determine_distribution_strategy(
            matched_pattern["category"], human_text, context
        )
        
        # Constrói requisição simbólica
        symbolic_request = {
            "action": matched_pattern["action"],
            "subject": matched_pattern["subject"],
            "category": matched_pattern["category"],
            "target": distribution_strategy,
            "original_text": human_text,
            "context": context,
            "processing_hints": self._extract_processing_hints(human_text),
            "priority": self._calculate_priority(matched_pattern["category"], context),
            "expected_response_type": self._determine_response_type(matched_pattern["subject"])
        }
        
        return symbolic_request
        
    def _determine_distribution_strategy(self, category: str, text: str, context: Dict) -> str:
        """Determina como distribuir o processamento"""
        # Lógica simples de distribuição
        if "rápido" in text.lower() or "urgente" in text.lower():
            return "NEAREST"
        elif category == "TRADING" and ("consenso" in text.lower() or "validação" in text.lower()):
            return "CONSENSUS"
        elif category == "KNOWLEDGE" and any(word in text.lower() for word in ["complexo", "difícil", "análise"]):
            return "SPECIALIZED"
        elif "todos" in text.lower() or "rede" in text.lower():
            return "BROADCAST"
        else:
            return "SELF"
            
    def _extract_processing_hints(self, text: str) -> List[str]:
        """Extrai dicas de processamento do texto"""
        hints = []
        
        if any(word in text.lower() for word in ["rápido", "urgente", "agora"]):
            hints.append("high_priority")
        if any(word in text.lower() for word in ["detalhado", "completo", "análise"]):
            hints.append("detailed_analysis")
        if any(word in text.lower() for word in ["simples", "resumo", "básico"]):
            hints.append("simplified_response")
        if any(word in text.lower() for word in ["dados", "números", "estatísticas"]):
            hints.append("data_heavy")
            
        return hints
        
    def _calculate_priority(self, category: str, context: Dict) -> int:
        """Calcula prioridade da requisição (1-10)"""
        base_priority = {
            "TRADING": 7,
            "AI_DECISION": 6, 
            "SECURITY": 9,
            "NETWORK": 5,
            "KNOWLEDGE": 3
        }.get(category, 3)
        
        # Ajustes baseados no contexto
        if context.get("urgent", False):
            base_priority += 2
        if context.get("user_priority") == "high":
            base_priority += 1
            
        return min(10, max(1, base_priority))
        
    def _determine_response_type(self, subject: str) -> str:
        """Determina tipo de resposta esperada"""
        response_types = {
            "PRICE_ANALYSIS": "structured_data",
            "MARKET_PREDICTION": "prediction_with_confidence",
            "KNOWLEDGE_REQUEST": "explanatory_text",
            "NETWORK_STATUS": "status_report",
            "VALIDATION_REQUEST": "validation_result"
        }
        
        return response_types.get(subject, "general_response")

class AuditTrailManager:
    """
    📋 Gerenciador de Trilha de Auditoria
    Mantém registro imutável de todos os processos de raciocínio
    """
    
    def __init__(self, db_path: str = "data/audit_trails.db"):
        self.db_path = db_path
        self.ensure_directory()
        self.init_database()
        
    def ensure_directory(self):
        """Garante que o diretório existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
    def init_database(self):
        """Inicializa base de dados de auditoria"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reasoning_trails (
                trail_id TEXT PRIMARY KEY,
                human_request TEXT NOT NULL,
                symbolic_request TEXT NOT NULL,
                final_result TEXT NOT NULL,
                participating_nodes TEXT NOT NULL,
                total_execution_time REAL NOT NULL,
                confidence_score REAL NOT NULL,
                start_timestamp TEXT NOT NULL,
                end_timestamp TEXT NOT NULL,
                trail_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reasoning_steps (
                step_id TEXT PRIMARY KEY,
                trail_id TEXT NOT NULL,
                step_type TEXT NOT NULL,
                input_data TEXT NOT NULL,
                output_data TEXT NOT NULL,
                processing_node TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                confidence REAL NOT NULL,
                execution_time REAL NOT NULL,
                metadata TEXT NOT NULL,
                FOREIGN KEY (trail_id) REFERENCES reasoning_trails (trail_id)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_trail_timestamp ON reasoning_trails(start_timestamp DESC);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_step_trail ON reasoning_steps(trail_id, timestamp);
        """)
        
        conn.commit()
        conn.close()
        
    def create_trail(self, human_request: str, symbolic_request: Dict) -> str:
        """Cria nova trilha de raciocínio"""
        trail_id = hashlib.sha256(
            f"{human_request}-{time.time()}".encode()
        ).hexdigest()[:16]
        
        # Placeholder para dados que serão atualizados
        initial_trail = ReasoningTrail(
            trail_id=trail_id,
            human_request=human_request,
            symbolic_request=symbolic_request,
            reasoning_steps=[],
            final_result={},
            participating_nodes=[],
            total_execution_time=0.0,
            confidence_score=0.0,
            start_timestamp=datetime.now().isoformat(),
            end_timestamp="",
            trail_hash=""
        )
        
        return trail_id
        
    def add_reasoning_step(self, trail_id: str, step: ReasoningStep):
        """Adiciona passo ao trail de raciocínio"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO reasoning_steps 
            (step_id, trail_id, step_type, input_data, output_data, 
             processing_node, timestamp, confidence, execution_time, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            step.step_id, trail_id, step.step_type,
            json.dumps(step.input_data), json.dumps(step.output_data),
            step.processing_node, step.timestamp, step.confidence,
            step.execution_time, json.dumps(step.metadata)
        ))
        
        conn.commit()
        conn.close()
        
    def finalize_trail(self, trail_id: str, trail: ReasoningTrail):
        """Finaliza trilha de raciocínio com hash de integridade"""
        # Calcula hash da trilha completa
        trail_content = f"{trail.human_request}-{json.dumps(trail.symbolic_request)}-{json.dumps(trail.final_result)}-{trail.start_timestamp}-{trail.end_timestamp}"
        trail_hash = hashlib.sha256(trail_content.encode()).hexdigest()
        
        trail.trail_hash = trail_hash
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO reasoning_trails 
            (trail_id, human_request, symbolic_request, final_result,
             participating_nodes, total_execution_time, confidence_score,
             start_timestamp, end_timestamp, trail_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trail.trail_id, trail.human_request,
            json.dumps(trail.symbolic_request), json.dumps(trail.final_result),
            json.dumps(trail.participating_nodes), trail.total_execution_time,
            trail.confidence_score, trail.start_timestamp,
            trail.end_timestamp, trail.trail_hash
        ))
        
        conn.commit()
        conn.close()
        
    def get_trail(self, trail_id: str) -> Optional[ReasoningTrail]:
        """Recupera trilha completa de raciocínio"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca dados da trilha
        cursor.execute("""
            SELECT human_request, symbolic_request, final_result,
                   participating_nodes, total_execution_time, confidence_score,
                   start_timestamp, end_timestamp, trail_hash
            FROM reasoning_trails WHERE trail_id = ?
        """, (trail_id,))
        
        trail_data = cursor.fetchone()
        if not trail_data:
            conn.close()
            return None
            
        # Busca passos do raciocínio
        cursor.execute("""
            SELECT step_id, step_type, input_data, output_data,
                   processing_node, timestamp, confidence, execution_time, metadata
            FROM reasoning_steps WHERE trail_id = ?
            ORDER BY timestamp ASC
        """, (trail_id,))
        
        steps_data = cursor.fetchall()
        conn.close()
        
        # Reconstrói objetos
        reasoning_steps = []
        for step_row in steps_data:
            step = ReasoningStep(
                step_id=step_row[0],
                step_type=step_row[1],
                input_data=json.loads(step_row[2]),
                output_data=json.loads(step_row[3]),
                processing_node=step_row[4],
                timestamp=step_row[5],
                confidence=step_row[6],
                execution_time=step_row[7],
                metadata=json.loads(step_row[8])
            )
            reasoning_steps.append(step)
            
        trail = ReasoningTrail(
            trail_id=trail_id,
            human_request=trail_data[0],
            symbolic_request=json.loads(trail_data[1]),
            final_result=json.loads(trail_data[2]),
            participating_nodes=json.loads(trail_data[3]),
            total_execution_time=trail_data[4],
            confidence_score=trail_data[5],
            start_timestamp=trail_data[6],
            end_timestamp=trail_data[7],
            trail_hash=trail_data[8],
            reasoning_steps=reasoning_steps
        )
        
        return trail

class InteractionEngine:
    """
    🧠⚡ Motor de Interação Principal
    Orquestra todo o processo de raciocínio distribuído
    """
    
    def __init__(self, node_id: str, gpt_node: Optional[GPTNode] = None, 
                 p2p_interface: Optional[P2PInterface] = None,
                 kernel: Optional[AeonKernel] = None):
        self.node_id = node_id
        self.gpt_node = gpt_node
        self.p2p_interface = p2p_interface
        self.kernel = kernel
        
        # Componentes do motor
        self.translator = SymbolicTranslator()
        self.audit_manager = AuditTrailManager(f"data/{node_id}_audit.db")
        
        # 🛡️ Segurança
        if DEPENDENCIES_AVAILABLE:
            try:
                self.security_lock = AeonSecurityLock()
                self.security_lock.log_execution("interaction_engine_init", {
                    "node_id": node_id,
                    "has_gpt_node": gpt_node is not None,
                    "has_p2p_interface": p2p_interface is not None,
                    "has_kernel": kernel is not None
                })
                print(f"🔒 [{node_id}] Interaction Engine com segurança ativa")
            except:
                print(f"⚠️ [{node_id}] Segurança não disponível")
        
        # Estado do motor
        self.active_reasonings = {}
        self.reasoning_queue = asyncio.Queue()
        
        # Estatísticas
        self.stats = {
            "human_requests_processed": 0,
            "symbolic_translations": 0,
            "local_reasonings": 0,
            "distributed_reasonings": 0,
            "consensus_operations": 0,
            "audit_trails_created": 0,
            "average_execution_time": 0.0,
            "average_confidence": 0.0,
            "engine_start_time": datetime.now().isoformat()
        }
        
        print(f"🧠⚡ [{node_id}] Interaction Engine inicializado")
        
    async def process_human_request(self, text: str, context: Dict = None, 
                                   user_id: str = "anonymous") -> Dict[str, Any]:
        """
        Ponto de entrada principal para requisições humanas
        """
        start_time = time.time()
        context = context or {}
        
        print(f"👤 [{self.node_id}] Processando requisição humana: {text[:100]}...")
        
        try:
            # 1. Traduz para protocolo simbólico
            translation_start = time.time()
            symbolic_request = self.translator.translate_to_symbolic(text, context)
            translation_time = time.time() - translation_start
            
            self.stats["symbolic_translations"] += 1
            
            # 2. Cria trilha de auditoria
            trail_id = self.audit_manager.create_trail(text, symbolic_request)
            self.stats["audit_trails_created"] += 1
            
            # 3. Adiciona passo de tradução ao audit trail
            translation_step = ReasoningStep(
                step_id=f"{trail_id}_translate",
                step_type="translate",
                input_data={"human_text": text, "context": context},
                output_data={"symbolic_request": symbolic_request},
                processing_node=self.node_id,
                timestamp=datetime.now().isoformat(),
                confidence=0.9,  # Alta confiança na tradução
                execution_time=translation_time,
                metadata={"user_id": user_id, "translation_patterns_used": 1}
            )
            
            self.audit_manager.add_reasoning_step(trail_id, translation_step)
            
            # 4. Executa raciocínio baseado na estratégia
            if symbolic_request["target"] == "SELF":
                result = await self._execute_local_reasoning(trail_id, symbolic_request)
                self.stats["local_reasonings"] += 1
            elif symbolic_request["target"] == "CONSENSUS":
                result = await self._execute_consensus_reasoning(trail_id, symbolic_request)
                self.stats["consensus_operations"] += 1
            else:
                result = await self._execute_distributed_reasoning(trail_id, symbolic_request)
                self.stats["distributed_reasonings"] += 1
                
            # 5. Finaliza trilha de auditoria
            total_time = time.time() - start_time
            
            final_trail = ReasoningTrail(
                trail_id=trail_id,
                human_request=text,
                symbolic_request=symbolic_request,
                reasoning_steps=[],  # Será carregado do banco
                final_result=result,
                participating_nodes=[self.node_id] + result.get("participating_nodes", []),
                total_execution_time=total_time,
                confidence_score=result.get("confidence", 0.5),
                start_timestamp=datetime.fromtimestamp(start_time).isoformat(),
                end_timestamp=datetime.now().isoformat(),
                trail_hash=""  # Será calculado pelo audit manager
            )
            
            self.audit_manager.finalize_trail(trail_id, final_trail)
            
            # 6. Atualiza estatísticas
            self.stats["human_requests_processed"] += 1
            self._update_average_stats(total_time, result.get("confidence", 0.5))
            
            # 7. Prepara resposta final
            response = {
                "status": "success",
                "trail_id": trail_id,
                "symbolic_request": symbolic_request,
                "result": result,
                "execution_time": total_time,
                "confidence": result.get("confidence", 0.5),
                "participating_nodes": final_trail.participating_nodes,
                "reasoning_type": symbolic_request["target"]
            }
            
            print(f"✅ [{self.node_id}] Requisição processada em {total_time:.2f}s (confiança: {result.get('confidence', 0.5):.2f})")
            
            return response
            
        except Exception as e:
            error_time = time.time() - start_time
            print(f"❌ [{self.node_id}] Erro ao processar requisição: {e}")
            
            return {
                "status": "error",
                "error": str(e),
                "execution_time": error_time,
                "trail_id": locals().get("trail_id", "unknown"),
                "partial_result": locals().get("symbolic_request", {})
            }
            
    async def _execute_local_reasoning(self, trail_id: str, symbolic_request: Dict) -> Dict[str, Any]:
        """Executa raciocínio local usando GPT Node"""
        step_start = time.time()
        
        if not self.gpt_node:
            return {
                "response": "GPT Node não disponível para processamento local",
                "confidence": 0.1,
                "reasoning_type": "local_fallback"
            }
            
        # Constrói prompt baseado na requisição simbólica
        prompt = self._build_gpt_prompt(symbolic_request)
        
        # Consulta GPT Node
        gpt_result = self.gpt_node.query(prompt, include_context=True)
        
        # Adiciona passo ao audit trail
        reasoning_step = ReasoningStep(
            step_id=f"{trail_id}_local_gpt",
            step_type="local_query",
            input_data={"prompt": prompt, "symbolic_request": symbolic_request},
            output_data={"gpt_result": gpt_result},
            processing_node=self.node_id,
            timestamp=datetime.now().isoformat(),
            confidence=0.8 if gpt_result["status"] == "success" else 0.3,
            execution_time=time.time() - step_start,
            metadata={"gpt_node_stats": self.gpt_node.get_stats()}
        )
        
        self.audit_manager.add_reasoning_step(trail_id, reasoning_step)
        
        return {
            "response": gpt_result["response"],
            "confidence": reasoning_step.confidence,
            "reasoning_type": "local_gpt",
            "context_used": gpt_result.get("context_used", []),
            "gpt_status": gpt_result["status"]
        }
        
    async def _execute_distributed_reasoning(self, trail_id: str, symbolic_request: Dict) -> Dict[str, Any]:
        """Executa raciocínio distribuído via P2P"""
        step_start = time.time()
        
        if not self.p2p_interface:
            # Fallback para raciocínio local
            return await self._execute_local_reasoning(trail_id, symbolic_request)
            
        # Envia consulta para peers relevantes
        distributed_results = []
        participating_nodes = []
        
        try:
            # Broadcast da consulta simbólica
            sent_count = await self.p2p_interface.broadcast_message(
                action=symbolic_request["action"],
                subject=symbolic_request["subject"],
                content={
                    "symbolic_request": symbolic_request,
                    "trail_id": trail_id,
                    "requesting_node": self.node_id
                },
                priority=symbolic_request["priority"]
            )
            
            # TODO: Implementar coleta de respostas (necessita handler específico)
            # Por enquanto, simula resposta distribuída
            distributed_results = [
                {"node": "simulated_peer_1", "response": "Análise distribuída simulada", "confidence": 0.7},
                {"node": "simulated_peer_2", "response": "Segunda opinião simulada", "confidence": 0.6}
            ]
            participating_nodes = ["simulated_peer_1", "simulated_peer_2"]
            
        except Exception as e:
            print(f"⚠️ [{self.node_id}] Erro no raciocínio distribuído: {e}")
            
        # Adiciona passo ao audit trail
        reasoning_step = ReasoningStep(
            step_id=f"{trail_id}_distributed",
            step_type="distributed_query",
            input_data={"symbolic_request": symbolic_request, "peers_contacted": sent_count},
            output_data={"distributed_results": distributed_results},
            processing_node=self.node_id,
            timestamp=datetime.now().isoformat(),
            confidence=0.7 if distributed_results else 0.2,
            execution_time=time.time() - step_start,
            metadata={"peers_responded": len(distributed_results)}
        )
        
        self.audit_manager.add_reasoning_step(trail_id, reasoning_step)
        
        # Síntese das respostas distribuídas
        if distributed_results:
            combined_response = self._synthesize_distributed_responses(distributed_results)
        else:
            combined_response = "Nenhuma resposta da rede distribuída"
            
        return {
            "response": combined_response,
            "confidence": reasoning_step.confidence,
            "reasoning_type": "distributed",
            "participating_nodes": participating_nodes,
            "individual_responses": distributed_results
        }
        
    async def _execute_consensus_reasoning(self, trail_id: str, symbolic_request: Dict) -> Dict[str, Any]:
        """Executa raciocínio por consenso da rede"""
        step_start = time.time()
        
        # Por enquanto, simula consenso
        # TODO: Implementar algoritmo de consenso real
        
        consensus_results = [
            {"node": "consensus_node_1", "vote": "approve", "confidence": 0.8},
            {"node": "consensus_node_2", "vote": "approve", "confidence": 0.7},
            {"node": "consensus_node_3", "vote": "reject", "confidence": 0.6}
        ]
        
        # Calcula consenso
        approve_votes = sum(1 for r in consensus_results if r["vote"] == "approve")
        total_votes = len(consensus_results)
        consensus_reached = approve_votes > total_votes / 2
        
        # Adiciona passo ao audit trail
        reasoning_step = ReasoningStep(
            step_id=f"{trail_id}_consensus",
            step_type="consensus_query",
            input_data={"symbolic_request": symbolic_request},
            output_data={"consensus_results": consensus_results, "consensus_reached": consensus_reached},
            processing_node=self.node_id,
            timestamp=datetime.now().isoformat(),
            confidence=0.9 if consensus_reached else 0.4,
            execution_time=time.time() - step_start,
            metadata={"votes_approve": approve_votes, "votes_total": total_votes}
        )
        
        self.audit_manager.add_reasoning_step(trail_id, reasoning_step)
        
        return {
            "response": f"Consenso {'alcançado' if consensus_reached else 'não alcançado'}: {approve_votes}/{total_votes} votos de aprovação",
            "confidence": reasoning_step.confidence,
            "reasoning_type": "consensus",
            "consensus_reached": consensus_reached,
            "vote_details": consensus_results
        }
        
    def _build_gpt_prompt(self, symbolic_request: Dict) -> str:
        """Constrói prompt para GPT baseado na requisição simbólica"""
        base_prompt = f"""
Requisição Simbólica AEONCOSMA:
- Ação: {symbolic_request['action']}
- Assunto: {symbolic_request['subject']}
- Categoria: {symbolic_request['category']}

Texto Original: {symbolic_request['original_text']}

Contexto: {json.dumps(symbolic_request.get('context', {}), indent=2)}

Dicas de Processamento: {', '.join(symbolic_request.get('processing_hints', []))}

Responda de forma clara e estruturada, considerando o tipo de resposta esperada: {symbolic_request.get('expected_response_type', 'geral')}.
"""
        return base_prompt
        
    def _synthesize_distributed_responses(self, responses: List[Dict]) -> str:
        """Sintetiza múltiplas respostas distribuídas"""
        if not responses:
            return "Nenhuma resposta para sintetizar"
            
        # Síntese simples - pode ser melhorada com IA
        synthesis = "Síntese de respostas distribuídas:\n\n"
        
        for i, response in enumerate(responses, 1):
            synthesis += f"{i}. {response['node']} (confiança: {response['confidence']:.2f}):\n"
            synthesis += f"   {response['response']}\n\n"
            
        # Calcula confiança média
        avg_confidence = sum(r['confidence'] for r in responses) / len(responses)
        synthesis += f"Confiança média: {avg_confidence:.2f}"
        
        return synthesis
        
    def _update_average_stats(self, execution_time: float, confidence: float):
        """Atualiza estatísticas médias"""
        total_requests = self.stats["human_requests_processed"]
        
        # Média móvel simples
        if total_requests == 1:
            self.stats["average_execution_time"] = execution_time
            self.stats["average_confidence"] = confidence
        else:
            self.stats["average_execution_time"] = (
                (self.stats["average_execution_time"] * (total_requests - 1) + execution_time) / total_requests
            )
            self.stats["average_confidence"] = (
                (self.stats["average_confidence"] * (total_requests - 1) + confidence) / total_requests
            )
            
    def get_engine_status(self) -> Dict[str, Any]:
        """Retorna status completo do motor"""
        return {
            "node_id": self.node_id,
            "stats": self.stats,
            "components_status": {
                "gpt_node": self.gpt_node is not None,
                "p2p_interface": self.p2p_interface is not None,
                "kernel": self.kernel is not None
            },
            "active_reasonings": len(self.active_reasonings),
            "dependencies_available": DEPENDENCIES_AVAILABLE
        }
        
    def export_audit_ledger(self, limit: int = 100) -> str:
        """Exporta ledger de auditoria em JSON"""
        conn = sqlite3.connect(self.audit_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT trail_id, human_request, symbolic_request, final_result,
                   participating_nodes, total_execution_time, confidence_score,
                   start_timestamp, end_timestamp, trail_hash
            FROM reasoning_trails
            ORDER BY start_timestamp DESC
            LIMIT ?
        """, (limit,))
        
        trails = []
        for row in cursor.fetchall():
            trails.append({
                "trail_id": row[0],
                "human_request": row[1],
                "symbolic_request": json.loads(row[2]),
                "final_result": json.loads(row[3]),
                "participating_nodes": json.loads(row[4]),
                "total_execution_time": row[5],
                "confidence_score": row[6],
                "start_timestamp": row[7],
                "end_timestamp": row[8],
                "trail_hash": row[9]
            })
            
        conn.close()
        
        ledger = {
            "export_timestamp": datetime.now().isoformat(),
            "engine_node_id": self.node_id,
            "total_trails": len(trails),
            "trails": trails,
            "engine_stats": self.stats
        }
        
        return json.dumps(ledger, indent=2, ensure_ascii=False)

# Exemplo de uso
async def main():
    """Teste do Interaction Engine"""
    print("🧠⚡ TESTANDO INTERACTION ENGINE")
    print("=" * 50)
    
    # Cria motor de interação básico
    engine = InteractionEngine("test_reasoning_node")
    
    # Testa requisições humanas
    test_requests = [
        "Qual é o preço do Bitcoin hoje?",
        "Como funciona o sistema AEONCOSMA?",
        "Valide esta transação de trading",
        "Conecte com nós especializados em análise de mercado",
        "Preciso de um consenso da rede sobre essa decisão"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n🔍 TESTE {i}: {request}")
        
        result = await engine.process_human_request(
            request, 
            context={"user_priority": "normal", "test_case": i}
        )
        
        print(f"✅ Status: {result['status']}")
        print(f"🎯 Tipo de raciocínio: {result.get('reasoning_type', 'unknown')}")
        print(f"⏱️ Tempo: {result['execution_time']:.2f}s")
        print(f"🎲 Confiança: {result.get('confidence', 0):.2f}")
        
        if result['status'] == 'success':
            print(f"💬 Resposta: {result['result']['response'][:100]}...")
    
    # Status final do motor
    status = engine.get_engine_status()
    print(f"\n📊 STATUS DO MOTOR:")
    print(f"   Requisições processadas: {status['stats']['human_requests_processed']}")
    print(f"   Traduções simbólicas: {status['stats']['symbolic_translations']}")
    print(f"   Raciocínios locais: {status['stats']['local_reasonings']}")
    print(f"   Tempo médio: {status['stats']['average_execution_time']:.2f}s")
    print(f"   Confiança média: {status['stats']['average_confidence']:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
