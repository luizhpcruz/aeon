# aeoncosma/communication/p2p_interface.py
"""
🌐 AEONCOSMA P2P INTERFACE - O Meio de Comunicação
Sistema de comunicação segura e eficiente entre nós
Protocolo simbólico de alta level para troca de significados
Desenvolvido por Luiz Cruz - 2025
"""

import asyncio
import websockets
import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
import ssl
import logging

# Importações internas
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from aeoncosma.core.aeon_kernel import AeonKernel
    from security.aeoncosma_security_lock import AeonSecurityLock
    SECURITY_ENABLED = True
except ImportError:
    SECURITY_ENABLED = False
    print("⚠️ Dependências não disponíveis para P2P Interface")

@dataclass
class SymbolicMessage:
    """
    📨 Mensagem Simbólica AEONCOSMA
    Estrutura de alto nível para comunicação entre nós
    """
    action: str  # "QUERY", "RESPONSE", "BROADCAST", "VALIDATE", "KNOWLEDGE_SHARE"
    subject: str  # Assunto específico da mensagem
    target: str  # "SPECIFIC_NODE", "ALL_NODES", "FINANCE_NODES", etc
    content: Dict[str, Any]  # Conteúdo simbólico
    metadata: Dict[str, Any]  # Metadados de contexto
    timestamp: str
    sender_id: str
    message_id: str
    priority: int = 1  # 1-10, onde 10 é máxima prioridade
    ttl: int = 3600  # Time to live em segundos

@dataclass  
class HandshakeData:
    """
    🤝 Dados de handshake para validação
    """
    node_id: str
    node_type: str  # "cognitive", "guardian", "bridge", "specialized"
    capabilities: List[str]
    reputation_score: float
    timestamp: str
    challenge_response: str
    security_token: str

class SymbolicProtocol:
    """
    🧬 Protocolo Simbólico AEONCOSMA
    Define linguagem e gramática para comunicação de alto nível
    """
    
    def __init__(self):
        # Vocabulário simbólico básico
        self.action_vocabulary = {
            "QUERY": "Solicita informação ou processamento",
            "RESPONSE": "Resposta a uma query",
            "BROADCAST": "Dissemina informação para múltiplos nós",
            "VALIDATE": "Solicita validação de dados/decisão",
            "KNOWLEDGE_SHARE": "Compartilha conhecimento específico",
            "CONSENSUS_REQUEST": "Solicita consenso da rede",
            "REPUTATION_UPDATE": "Atualiza reputação de nó",
            "HEALTH_CHECK": "Verifica saúde da conexão",
            "HANDSHAKE": "Inicialização de conexão",
            "DISCONNECT": "Encerramento de conexão"
        }
        
        self.subject_categories = {
            "TRADING": ["PRICE_ANALYSIS", "MARKET_PREDICTION", "RISK_ASSESSMENT"],
            "AI_DECISION": ["VALIDATION_REQUEST", "PATTERN_RECOGNITION", "LEARNING_UPDATE"],
            "KNOWLEDGE": ["DATA_QUERY", "INSIGHT_SHARING", "EXPERTISE_REQUEST"],
            "NETWORK": ["PEER_DISCOVERY", "TOPOLOGY_UPDATE", "CONSENSUS_BUILDING"],
            "SECURITY": ["THREAT_ALERT", "REPUTATION_QUERY", "ACCESS_REQUEST"]
        }
        
        self.target_patterns = {
            "SELF": "Processamento local apenas",
            "DIRECT:node_id": "Nó específico",
            "BROADCAST:ALL": "Todos os nós conectados",
            "BROADCAST:CAPABILITY:capability": "Nós com capacidade específica",
            "CONSENSUS:QUORUM": "Maioria dos nós para consenso",
            "NEAREST:N": "N nós mais próximos/confiáveis"
        }
        
    def create_message(self, action: str, subject: str, target: str, 
                      content: Dict, sender_id: str, priority: int = 1) -> SymbolicMessage:
        """Cria mensagem simbólica estruturada"""
        message_id = hashlib.sha256(
            f"{sender_id}-{time.time()}-{action}-{subject}".encode()
        ).hexdigest()[:16]
        
        return SymbolicMessage(
            action=action,
            subject=subject,
            target=target,
            content=content,
            metadata={
                "protocol_version": "1.0",
                "encoding": "symbolic-aeon",
                "compression": "none",
                "encryption": "none"
            },
            timestamp=datetime.now().isoformat(),
            sender_id=sender_id,
            message_id=message_id,
            priority=priority
        )
        
    def validate_message(self, message: SymbolicMessage) -> tuple[bool, str]:
        """Valida estrutura e conteúdo da mensagem"""
        # Valida ação
        if message.action not in self.action_vocabulary:
            return False, f"Ação '{message.action}' não reconhecida"
            
        # Valida timestamp
        try:
            msg_time = datetime.fromisoformat(message.timestamp)
            age = (datetime.now() - msg_time).total_seconds()
            if age > message.ttl:
                return False, "Mensagem expirada (TTL)"
        except:
            return False, "Timestamp inválido"
            
        # Valida prioridade
        if not 1 <= message.priority <= 10:
            return False, "Prioridade deve estar entre 1-10"
            
        return True, "Mensagem válida"
        
    def serialize_message(self, message: SymbolicMessage) -> str:
        """Serializa mensagem para transmissão"""
        return json.dumps(asdict(message), ensure_ascii=False)
        
    def deserialize_message(self, data: str) -> Optional[SymbolicMessage]:
        """Deserializa mensagem recebida"""
        try:
            msg_dict = json.loads(data)
            return SymbolicMessage(**msg_dict)
        except Exception as e:
            logging.error(f"Erro ao deserializar mensagem: {e}")
            return None

class P2PInterface:
    """
    🌐 Interface P2P Principal
    Gerencia comunicação segura entre nós usando protocolo simbólico
    """
    
    def __init__(self, node_id: str, kernel: Optional[AeonKernel] = None, 
                 host: str = "127.0.0.1", port: int = 8765):
        self.node_id = node_id
        self.kernel = kernel
        self.host = host
        self.port = port
        
        # Protocolo simbólico
        self.protocol = SymbolicProtocol()
        
        # 🛡️ Segurança
        if SECURITY_ENABLED:
            self.security_lock = AeonSecurityLock()
            self.security_lock.log_execution("p2p_interface_init", {
                "node_id": node_id,
                "host": host,
                "port": port
            })
            print(f"🔒 [{node_id}] P2P Interface com segurança ativa")
        
        # Estado da interface
        self.active_connections = {}
        self.message_handlers = {}
        self.server = None
        self.running = False
        
        # Filas de mensagens
        self.incoming_queue = asyncio.Queue()
        self.outgoing_queue = asyncio.Queue()
        self.priority_queue = asyncio.PriorityQueue()
        
        # Estatísticas
        self.stats = {
            "connections_established": 0,
            "connections_rejected": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "handshakes_successful": 0,
            "handshakes_failed": 0,
            "protocol_errors": 0,
            "start_time": None
        }
        
        # Registra handlers padrão
        self._register_default_handlers()
        
        print(f"🌐 [{node_id}] P2P Interface inicializada em {host}:{port}")
        
    def _register_default_handlers(self):
        """Registra handlers padrão para mensagens"""
        self.register_handler("HANDSHAKE", self._handle_handshake)
        self.register_handler("HEALTH_CHECK", self._handle_health_check)
        self.register_handler("DISCONNECT", self._handle_disconnect)
        
    def register_handler(self, action: str, handler: Callable):
        """Registra handler para tipo específico de mensagem"""
        self.message_handlers[action] = handler
        print(f"📝 [{self.node_id}] Handler registrado para ação '{action}'")
        
    async def start_server(self):
        """Inicia servidor WebSocket"""
        self.running = True
        self.stats["start_time"] = datetime.now().isoformat()
        
        # Inicia servidor WebSocket
        self.server = await websockets.serve(
            self.handle_connection,
            self.host,
            self.port,
            ping_interval=30,
            ping_timeout=10
        )
        
        # Inicia processadores de fila
        asyncio.create_task(self._process_incoming_queue())
        asyncio.create_task(self._process_outgoing_queue())
        
        print(f"🚀 [{self.node_id}] Servidor P2P iniciado em ws://{self.host}:{self.port}")
        
    async def handle_connection(self, websocket, path):
        """Handler principal para conexões WebSocket"""
        peer_id = None
        
        try:
            # Aguarda handshake
            handshake_data = await self._perform_handshake(websocket)
            
            if not handshake_data:
                await websocket.close(code=4001, reason="Handshake failed")
                self.stats["connections_rejected"] += 1
                return
                
            peer_id = handshake_data.node_id
            
            # Valida com kernel se disponível
            if self.kernel:
                allowed, reason, metadata = self.kernel.validate_incoming_request(
                    peer_id, "websocket_connection", {
                        "handshake_data": asdict(handshake_data),
                        "websocket_path": path
                    }
                )
                
                if not allowed:
                    await websocket.close(code=4003, reason=f"Kernel denied: {reason}")
                    self.stats["connections_rejected"] += 1
                    return
            
            # Registra conexão ativa
            self.active_connections[peer_id] = {
                "websocket": websocket,
                "handshake_data": handshake_data,
                "connected_at": datetime.now().isoformat(),
                "messages_exchanged": 0
            }
            
            self.stats["connections_established"] += 1
            self.stats["handshakes_successful"] += 1
            
            print(f"🤝 [{self.node_id}] Conexão estabelecida com {peer_id}")
            
            # Loop principal de comunicação
            await self._communication_loop(websocket, peer_id)
            
        except websockets.exceptions.ConnectionClosed:
            print(f"📡 [{self.node_id}] Conexão com {peer_id} encerrada")
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro na conexão com {peer_id}: {e}")
            self.stats["protocol_errors"] += 1
        finally:
            # Limpeza
            if peer_id and peer_id in self.active_connections:
                del self.active_connections[peer_id]
                
            if self.kernel and peer_id:
                self.kernel.close_connection(peer_id, "websocket_disconnect")
                
    async def _perform_handshake(self, websocket) -> Optional[HandshakeData]:
        """Realiza handshake de segurança"""
        try:
            # Envia challenge
            challenge = hashlib.sha256(f"{self.node_id}-{time.time()}".encode()).hexdigest()[:16]
            
            challenge_msg = self.protocol.create_message(
                action="HANDSHAKE",
                subject="CHALLENGE",
                target="DIRECT",
                content={"challenge": challenge},
                sender_id=self.node_id
            )
            
            await websocket.send(self.protocol.serialize_message(challenge_msg))
            
            # Aguarda resposta
            response_data = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            response_msg = self.protocol.deserialize_message(response_data)
            
            if not response_msg or response_msg.action != "HANDSHAKE":
                return None
                
            # Valida resposta
            expected_response = hashlib.sha256(f"{challenge}-{response_msg.sender_id}".encode()).hexdigest()[:16]
            
            if response_msg.content.get("challenge_response") != expected_response:
                return None
                
            # Cria dados de handshake
            handshake_data = HandshakeData(
                node_id=response_msg.sender_id,
                node_type=response_msg.content.get("node_type", "unknown"),
                capabilities=response_msg.content.get("capabilities", []),
                reputation_score=response_msg.content.get("reputation_score", 0.5),
                timestamp=response_msg.timestamp,
                challenge_response=response_msg.content.get("challenge_response"),
                security_token=response_msg.content.get("security_token", "")
            )
            
            return handshake_data
            
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro no handshake: {e}")
            self.stats["handshakes_failed"] += 1
            return None
            
    async def _communication_loop(self, websocket, peer_id: str):
        """Loop principal de comunicação com um peer"""
        try:
            async for message_data in websocket:
                # Deserializa mensagem
                message = self.protocol.deserialize_message(message_data)
                
                if not message:
                    self.stats["protocol_errors"] += 1
                    continue
                    
                # Valida mensagem
                valid, reason = self.protocol.validate_message(message)
                if not valid:
                    print(f"⚠️ [{self.node_id}] Mensagem inválida de {peer_id}: {reason}")
                    self.stats["protocol_errors"] += 1
                    continue
                    
                # Adiciona à fila de entrada com prioridade
                await self.priority_queue.put((10 - message.priority, message, peer_id))
                self.stats["messages_received"] += 1
                
                # Atualiza contador de mensagens da conexão
                if peer_id in self.active_connections:
                    self.active_connections[peer_id]["messages_exchanged"] += 1
                    
        except websockets.exceptions.ConnectionClosed:
            print(f"📡 [{self.node_id}] {peer_id} desconectou")
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro no loop de comunicação com {peer_id}: {e}")
            
    async def _process_incoming_queue(self):
        """Processa fila de mensagens recebidas"""
        while self.running:
            try:
                # Pega mensagem com prioridade
                priority, message, sender_id = await self.priority_queue.get()
                
                # Processa mensagem
                await self._process_message(message, sender_id)
                
            except Exception as e:
                print(f"❌ [{self.node_id}] Erro ao processar mensagem recebida: {e}")
                
    async def _process_message(self, message: SymbolicMessage, sender_id: str):
        """Processa mensagem individual"""
        # Verifica se existe handler específico
        if message.action in self.message_handlers:
            try:
                handler = self.message_handlers[message.action]
                await handler(message, sender_id)
            except Exception as e:
                print(f"❌ [{self.node_id}] Erro no handler para {message.action}: {e}")
        else:
            print(f"⚠️ [{self.node_id}] Nenhum handler para ação '{message.action}'")
            
    async def _process_outgoing_queue(self):
        """Processa fila de mensagens para envio"""
        while self.running:
            try:
                # Aguarda mensagem para envio
                target_id, message = await self.outgoing_queue.get()
                
                # Envia mensagem
                await self._send_message_to_peer(target_id, message)
                
            except Exception as e:
                print(f"❌ [{self.node_id}] Erro ao processar fila de envio: {e}")
                
    async def _send_message_to_peer(self, target_id: str, message: SymbolicMessage):
        """Envia mensagem para peer específico"""
        if target_id not in self.active_connections:
            print(f"⚠️ [{self.node_id}] Peer {target_id} não conectado")
            return False
            
        try:
            websocket = self.active_connections[target_id]["websocket"]
            serialized = self.protocol.serialize_message(message)
            
            await websocket.send(serialized)
            self.stats["messages_sent"] += 1
            
            return True
            
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro ao enviar mensagem para {target_id}: {e}")
            return False
            
    # Handlers padrão
    async def _handle_handshake(self, message: SymbolicMessage, sender_id: str):
        """Handler para mensagens de handshake"""
        print(f"🤝 [{self.node_id}] Processando handshake de {sender_id}")
        
    async def _handle_health_check(self, message: SymbolicMessage, sender_id: str):
        """Handler para health checks"""
        response = self.protocol.create_message(
            action="RESPONSE",
            subject="HEALTH_STATUS",
            target=f"DIRECT:{sender_id}",
            content={
                "status": "healthy",
                "uptime": time.time() - time.mktime(datetime.fromisoformat(self.stats["start_time"]).timetuple()) if self.stats["start_time"] else 0,
                "connections": len(self.active_connections),
                "load": "normal"
            },
            sender_id=self.node_id
        )
        
        await self.outgoing_queue.put((sender_id, response))
        
    async def _handle_disconnect(self, message: SymbolicMessage, sender_id: str):
        """Handler para desconexões"""
        print(f"👋 [{self.node_id}] {sender_id} solicitou desconexão")
        
        if sender_id in self.active_connections:
            websocket = self.active_connections[sender_id]["websocket"]
            await websocket.close(code=1000, reason="Disconnect requested")
            
    # API pública
    async def send_message(self, target_id: str, action: str, subject: str, 
                          content: Dict, priority: int = 1) -> bool:
        """Envia mensagem simbólica para peer específico"""
        message = self.protocol.create_message(
            action=action,
            subject=subject,
            target=f"DIRECT:{target_id}",
            content=content,
            sender_id=self.node_id,
            priority=priority
        )
        
        await self.outgoing_queue.put((target_id, message))
        return True
        
    async def broadcast_message(self, action: str, subject: str, 
                               content: Dict, priority: int = 1) -> int:
        """Broadcast mensagem para todos os peers conectados"""
        message = self.protocol.create_message(
            action=action,
            subject=subject,
            target="BROADCAST:ALL",
            content=content,
            sender_id=self.node_id,
            priority=priority
        )
        
        sent_count = 0
        for peer_id in self.active_connections.keys():
            await self.outgoing_queue.put((peer_id, message))
            sent_count += 1
            
        return sent_count
        
    def get_interface_status(self) -> Dict[str, Any]:
        """Retorna status da interface P2P"""
        return {
            "node_id": self.node_id,
            "address": f"ws://{self.host}:{self.port}",
            "running": self.running,
            "active_connections": len(self.active_connections),
            "connected_peers": list(self.active_connections.keys()),
            "stats": self.stats,
            "protocol_version": "1.0",
            "security_enabled": SECURITY_ENABLED
        }
        
    async def stop(self):
        """Para o servidor P2P"""
        self.running = False
        
        # Notifica peers sobre desconexão
        if self.active_connections:
            await self.broadcast_message(
                action="DISCONNECT",
                subject="SERVER_SHUTDOWN",
                content={"reason": "Server stopping gracefully"}
            )
            
        # Fecha servidor
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            
        print(f"🛑 [{self.node_id}] Servidor P2P parado")

# Exemplo de uso
async def main():
    """Teste da P2P Interface"""
    print("🌐 TESTANDO P2P INTERFACE")
    print("=" * 50)
    
    # Cria interface
    interface = P2PInterface("test_communication_node", port=8765)
    
    # Registra handler personalizado
    async def handle_custom_query(message, sender_id):
        print(f"🔍 Query recebida de {sender_id}: {message.content}")
        
    interface.register_handler("QUERY", handle_custom_query)
    
    # Inicia servidor
    await interface.start_server()
    
    print("✅ Interface P2P ativa - pressione Ctrl+C para parar")
    
    try:
        # Mantém servidor rodando
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        print("\n🛑 Parando interface...")
        await interface.stop()

if __name__ == "__main__":
    asyncio.run(main())
