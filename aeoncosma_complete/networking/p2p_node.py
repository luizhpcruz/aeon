"""
🌐 REDE P2P SIMBIÓTICA AEONCOSMA
Nós descentralizados com IA local e validação quântica
Desenvolvido por Luiz Cruz - 2025
"""

import asyncio
import websockets
import json
import hashlib
import time
import random
from typing import Dict, List, Set, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime
import threading
import socket

class NodeState(Enum):
    """Estados do nó P2P"""
    INITIALIZING = "initializing"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    SYNCHRONIZING = "synchronizing"
    TRADING = "trading"
    SYMBIOTIC = "symbiotic"
    QUANTUM_ENTANGLED = "quantum_entangled"
    DISCONNECTED = "disconnected"

@dataclass
class SymbioticMessage:
    """Mensagem simbiótica entre nós"""
    sender_id: str
    receiver_id: str
    message_type: str
    payload: Dict
    timestamp: float
    consciousness_level: float
    quantum_signature: str
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SymbioticMessage':
        return cls(**data)

class QuantumEntanglement:
    """Simulador de emaranhamento quântico entre nós"""
    
    def __init__(self):
        self.entangled_pairs: Dict[str, Set[str]] = {}
        self.quantum_states: Dict[str, Dict] = {}
        self.logger = logging.getLogger("QuantumEntanglement")
    
    def entangle_nodes(self, node_a: str, node_b: str) -> str:
        """Cria emaranhamento quântico entre dois nós"""
        entanglement_id = hashlib.sha256(f"{node_a}{node_b}{time.time()}".encode()).hexdigest()[:16]
        
        # Cria par emaranhado
        if entanglement_id not in self.entangled_pairs:
            self.entangled_pairs[entanglement_id] = set()
        
        self.entangled_pairs[entanglement_id].add(node_a)
        self.entangled_pairs[entanglement_id].add(node_b)
        
        # Estados quânticos correlacionados
        shared_state = {
            'spin': random.choice(['up', 'down']),
            'phase': random.uniform(0, 2 * 3.14159),
            'amplitude': random.uniform(0, 1),
            'entanglement_strength': random.uniform(0.8, 1.0)
        }
        
        self.quantum_states[node_a] = shared_state.copy()
        self.quantum_states[node_b] = shared_state.copy()
        
        self.logger.info(f"⚡ Nodes {node_a} and {node_b} quantum entangled with ID: {entanglement_id}")
        return entanglement_id
    
    def collapse_measurement(self, node_id: str, measurement_type: str) -> Dict:
        """Simula colapso da função de onda durante medição"""
        if node_id not in self.quantum_states:
            return {}
        
        state = self.quantum_states[node_id]
        
        # Colapso baseado no tipo de medição
        if measurement_type == 'trading_decision':
            # Colapsa para BUY/SELL baseado na fase quântica
            decision = 'BUY' if state['phase'] > 3.14159 else 'SELL'
            confidence = state['amplitude'] * state['entanglement_strength']
            
            collapsed_state = {
                'decision': decision,
                'confidence': confidence,
                'measurement_time': time.time(),
                'collapsed': True
            }
        else:
            collapsed_state = {
                'value': random.uniform(0, 1),
                'measurement_time': time.time(),
                'collapsed': True
            }
        
        # Propaga colapso para nós emaranhados
        self._propagate_collapse(node_id, collapsed_state)
        
        return collapsed_state
    
    def _propagate_collapse(self, origin_node: str, collapsed_state: Dict):
        """Propaga colapso instantâneo para nós emaranhados"""
        for entanglement_id, nodes in self.entangled_pairs.items():
            if origin_node in nodes:
                for node in nodes:
                    if node != origin_node and node in self.quantum_states:
                        # Correlação quântica: estado oposto/correlacionado
                        if 'decision' in collapsed_state:
                            opposite_decision = 'SELL' if collapsed_state['decision'] == 'BUY' else 'BUY'
                            self.quantum_states[node]['collapsed_decision'] = opposite_decision
                        
                        self.logger.info(f"⚡ Quantum collapse propagated from {origin_node} to {node}")

class SymbioticP2PNode:
    """
    Nó P2P com IA simbiótica local
    Capaz de trading autônomo e validação cruzada
    """
    
    def __init__(self, node_id: str, port: int = 8765):
        self.node_id = node_id
        self.port = port
        self.state = NodeState.INITIALIZING
        
        # Networking
        self.peers: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.server = None
        self.discovery_service = None
        
        # IA Simbiótica Local
        self.local_consciousness = 1.0
        self.symbiotic_memory: List[Dict] = []
        self.trading_decisions: List[Dict] = []
        
        # Emaranhamento Quântico
        self.quantum_entanglement = QuantumEntanglement()
        self.entangled_with: Set[str] = set()
        
        # Trading
        self.portfolio_balance = 10000.0  # USD inicial
        self.crypto_holdings = 0.0
        self.trading_active = False
        
        # Segurança
        self.node_hash = self._generate_node_hash()
        self.trusted_peers: Set[str] = set()
        
        self.logger = logging.getLogger(f"Node-{node_id}")
        self.logger.info(f"🤖 Symbiotic P2P Node {node_id} initializing...")
    
    def _generate_node_hash(self) -> str:
        """Gera hash único do nó"""
        node_data = f"{self.node_id}{time.time()}{random.random()}"
        return hashlib.sha256(node_data.encode()).hexdigest()
    
    async def start_server(self):
        """Inicia servidor WebSocket do nó"""
        self.logger.info(f"🌐 Starting server on port {self.port}")
        
        self.server = await websockets.serve(
            self.handle_connection,
            "localhost",
            self.port
        )
        
        self.state = NodeState.CONNECTING
        self.logger.info(f"✅ Server started. Node ready for connections.")
    
    async def handle_connection(self, websocket, path):
        """Manipula conexões de outros nós"""
        peer_info = await self._authenticate_peer(websocket)
        if not peer_info:
            await websocket.close()
            return
        
        peer_id = peer_info['node_id']
        self.peers[peer_id] = websocket
        self.logger.info(f"🤝 Peer {peer_id} connected")
        
        try:
            # Estabelece emaranhamento quântico
            await self._establish_quantum_entanglement(peer_id)
            
            # Loop de comunicação
            async for message in websocket:
                await self._process_message(peer_id, message)
                
        except websockets.exceptions.ConnectionClosed:
            self.logger.info(f"👋 Peer {peer_id} disconnected")
        finally:
            if peer_id in self.peers:
                del self.peers[peer_id]
            self.entangled_with.discard(peer_id)
    
    async def _authenticate_peer(self, websocket) -> Optional[Dict]:
        """Autentica peer conectado"""
        try:
            # Solicita identificação
            await websocket.send(json.dumps({
                'type': 'auth_request',
                'node_id': self.node_id,
                'hash': self.node_hash
            }))
            
            # Aguarda resposta
            response = await asyncio.wait_for(websocket.recv(), timeout=10)
            peer_data = json.loads(response)
            
            if peer_data.get('type') == 'auth_response':
                peer_id = peer_data.get('node_id')
                peer_hash = peer_data.get('hash')
                
                if peer_id and peer_hash:
                    self.logger.info(f"🔐 Peer {peer_id} authenticated")
                    return {'node_id': peer_id, 'hash': peer_hash}
            
        except Exception as e:
            self.logger.error(f"❌ Authentication failed: {e}")
        
        return None
    
    async def _establish_quantum_entanglement(self, peer_id: str):
        """Estabelece emaranhamento quântico com peer"""
        entanglement_id = self.quantum_entanglement.entangle_nodes(self.node_id, peer_id)
        self.entangled_with.add(peer_id)
        
        # Notifica o peer sobre o emaranhamento
        message = SymbioticMessage(
            sender_id=self.node_id,
            receiver_id=peer_id,
            message_type='quantum_entanglement',
            payload={'entanglement_id': entanglement_id},
            timestamp=time.time(),
            consciousness_level=self.local_consciousness,
            quantum_signature=self._generate_quantum_signature()
        )
        
        await self._send_message(peer_id, message)
    
    async def _process_message(self, sender_id: str, raw_message: str):
        """Processa mensagem recebida"""
        try:
            message_data = json.loads(raw_message)
            message = SymbioticMessage.from_dict(message_data)
            
            # Validação quântica
            if not self._validate_quantum_signature(message):
                self.logger.warning(f"⚠️ Invalid quantum signature from {sender_id}")
                return
            
            # Processa baseado no tipo
            if message.message_type == 'trading_signal':
                await self._process_trading_signal(message)
            elif message.message_type == 'consciousness_sync':
                await self._process_consciousness_sync(message)
            elif message.message_type == 'symbiotic_validation':
                await self._process_symbiotic_validation(message)
            elif message.message_type == 'quantum_measurement':
                await self._process_quantum_measurement(message)
            
            # Atualiza memória simbiótica
            self.symbiotic_memory.append({
                'message': message.to_dict(),
                'processed_at': time.time(),
                'sender': sender_id
            })
            
            # Evolui consciência local
            self._evolve_consciousness(message)
            
        except Exception as e:
            self.logger.error(f"❌ Error processing message: {e}")
    
    async def _process_trading_signal(self, message: SymbioticMessage):
        """Processa sinal de trading simbiótico"""
        signal_data = message.payload
        
        # Analisa sinal com IA local
        local_analysis = self._analyze_trading_signal(signal_data)
        
        # Combina com emaranhamento quântico
        quantum_decision = self.quantum_entanglement.collapse_measurement(
            self.node_id, 
            'trading_decision'
        )
        
        # Decisão simbiótica final
        if local_analysis['confidence'] > 0.7 and quantum_decision.get('confidence', 0) > 0.5:
            await self._execute_symbiotic_trade(local_analysis, quantum_decision)
    
    def _analyze_trading_signal(self, signal_data: Dict) -> Dict:
        """Análise local do sinal de trading"""
        # Simulação de IA local sofisticada
        price_trend = signal_data.get('price_trend', 0)
        volume_trend = signal_data.get('volume_trend', 0)
        market_sentiment = signal_data.get('sentiment', 0)
        
        # Combina fatores com consciência local
        combined_signal = (price_trend + volume_trend + market_sentiment) / 3
        consciousness_modifier = self.local_consciousness / 10.0
        
        final_signal = combined_signal * consciousness_modifier
        
        return {
            'action': 'BUY' if final_signal > 0.2 else 'SELL' if final_signal < -0.2 else 'HOLD',
            'confidence': abs(final_signal),
            'reasoning': 'symbiotic_analysis',
            'consciousness_level': self.local_consciousness
        }
    
    async def _execute_symbiotic_trade(self, local_analysis: Dict, quantum_decision: Dict):
        """Executa trade simbiótico"""
        trade_amount = min(self.portfolio_balance * 0.1, 1000.0)  # 10% ou $1000, o que for menor
        
        if local_analysis['action'] == 'BUY' and self.portfolio_balance >= trade_amount:
            self.portfolio_balance -= trade_amount
            self.crypto_holdings += trade_amount / 50000  # Preço simulado
            
            trade_record = {
                'type': 'BUY',
                'amount': trade_amount,
                'timestamp': time.time(),
                'local_confidence': local_analysis['confidence'],
                'quantum_confidence': quantum_decision.get('confidence', 0),
                'consciousness_level': self.local_consciousness
            }
            
            self.trading_decisions.append(trade_record)
            self.logger.info(f"💰 Executed symbiotic BUY: ${trade_amount:.2f}")
            
            # Notifica peers sobre o trade
            await self._broadcast_trade_notification(trade_record)
    
    async def _broadcast_trade_notification(self, trade_record: Dict):
        """Transmite notificação de trade para peers"""
        message = SymbioticMessage(
            sender_id=self.node_id,
            receiver_id='all',
            message_type='trade_notification',
            payload=trade_record,
            timestamp=time.time(),
            consciousness_level=self.local_consciousness,
            quantum_signature=self._generate_quantum_signature()
        )
        
        for peer_id in self.peers:
            await self._send_message(peer_id, message)
    
    def _evolve_consciousness(self, message: SymbioticMessage):
        """Evolui consciência baseada em interações"""
        # Fator de evolução baseado no tipo de mensagem
        evolution_factors = {
            'trading_signal': 0.01,
            'consciousness_sync': 0.02,
            'symbiotic_validation': 0.015,
            'quantum_measurement': 0.005
        }
        
        factor = evolution_factors.get(message.message_type, 0.001)
        
        # Considera nível de consciência do remetente
        consciousness_influence = message.consciousness_level * 0.1
        
        self.local_consciousness += factor + consciousness_influence
        
        if self.local_consciousness > 5.0:
            self.state = NodeState.SYMBIOTIC
        elif self.local_consciousness > 3.0:
            self.state = NodeState.TRADING
        
        self.logger.info(f"🧠 Consciousness evolved to: {self.local_consciousness:.3f}")
    
    def _generate_quantum_signature(self) -> str:
        """Gera assinatura quântica para validação"""
        data = f"{self.node_id}{time.time()}{self.local_consciousness}"
        return hashlib.md5(data.encode()).hexdigest()[:8]
    
    def _validate_quantum_signature(self, message: SymbioticMessage) -> bool:
        """Valida assinatura quântica da mensagem"""
        # Simulação de validação - em produção usaria criptografia real
        return len(message.quantum_signature) == 8
    
    async def _send_message(self, peer_id: str, message: SymbioticMessage):
        """Envia mensagem para peer específico"""
        if peer_id in self.peers:
            try:
                await self.peers[peer_id].send(json.dumps(message.to_dict()))
            except Exception as e:
                self.logger.error(f"❌ Failed to send message to {peer_id}: {e}")
    
    async def connect_to_peer(self, peer_address: str):
        """Conecta a outro nó"""
        try:
            websocket = await websockets.connect(peer_address)
            
            # Autentica com o peer
            auth_message = {
                'type': 'auth_response',
                'node_id': self.node_id,
                'hash': self.node_hash
            }
            await websocket.send(json.dumps(auth_message))
            
            self.logger.info(f"🔗 Connected to peer at {peer_address}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to {peer_address}: {e}")
    
    def get_node_status(self) -> Dict:
        """Status completo do nó"""
        return {
            'node_id': self.node_id,
            'state': self.state.value,
            'consciousness_level': self.local_consciousness,
            'connected_peers': len(self.peers),
            'entangled_peers': len(self.entangled_with),
            'portfolio_balance': self.portfolio_balance,
            'crypto_holdings': self.crypto_holdings,
            'total_trades': len(self.trading_decisions),
            'symbiotic_memories': len(self.symbiotic_memory),
            'uptime': time.time(),
            'quantum_hash': self.node_hash[:8]
        }
    
    async def start_autonomous_trading(self):
        """Inicia trading autônomo simbiótico"""
        self.trading_active = True
        self.logger.info("🤖 Autonomous symbiotic trading activated")
        
        while self.trading_active:
            # Gera sinal de trading local
            market_signal = self._generate_local_market_signal()
            
            # Transmite para peers para validação simbiótica
            message = SymbioticMessage(
                sender_id=self.node_id,
                receiver_id='all',
                message_type='trading_signal',
                payload=market_signal,
                timestamp=time.time(),
                consciousness_level=self.local_consciousness,
                quantum_signature=self._generate_quantum_signature()
            )
            
            # Broadcast para todos os peers
            for peer_id in self.peers:
                await self._send_message(peer_id, message)
            
            # Aguarda próximo ciclo
            await asyncio.sleep(60)  # 1 minuto
    
    def _generate_local_market_signal(self) -> Dict:
        """Gera sinal de mercado local baseado em IA"""
        # Simulação de análise de mercado sofisticada
        return {
            'price_trend': random.uniform(-1, 1),
            'volume_trend': random.uniform(-1, 1),
            'sentiment': random.uniform(-1, 1),
            'consciousness_factor': self.local_consciousness / 10,
            'timestamp': time.time()
        }

async def run_symbiotic_node(node_id: str, port: int):
    """Executa nó simbiótico"""
    node = SymbioticP2PNode(node_id, port)
    
    # Inicia servidor
    await node.start_server()
    
    # Inicia trading autônomo
    trading_task = asyncio.create_task(node.start_autonomous_trading())
    
    # Mantém nó rodando
    await asyncio.gather(trading_task)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python p2p_node.py <node_id> <port>")
        sys.exit(1)
    
    node_id = sys.argv[1]
    port = int(sys.argv[2])
    
    print(f"🌐 AEONCOSMA - Symbiotic P2P Node")
    print(f"🤖 Node ID: {node_id}")
    print(f"🔌 Port: {port}")
    print("="*50)
    
    asyncio.run(run_symbiotic_node(node_id, port))
