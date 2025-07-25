"""
P2P Network - Peer-to-Peer Trading Network
==========================================

Sistema de rede peer-to-peer para trading descentralizado,
permitindo comunicação direta entre traders sem intermediários.
"""

import asyncio
import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Callable
import websockets
import logging
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet
import uuid

logger = logging.getLogger(__name__)

@dataclass
class PeerInfo:
    """Informações de um peer na rede."""
    peer_id: str
    address: str
    port: int
    public_key: str
    last_seen: datetime
    reputation: float = 0.0
    trades_completed: int = 0

@dataclass
class TradeOffer:
    """Oferta de trade na rede P2P."""
    offer_id: str
    peer_id: str
    symbol: str
    amount: float
    price: float
    trade_type: str  # "buy" or "sell"
    timestamp: datetime
    expires_at: datetime
    signature: str

@dataclass
class NetworkMessage:
    """Mensagem na rede P2P."""
    message_id: str
    message_type: str
    sender_id: str
    payload: Dict
    timestamp: datetime
    signature: Optional[str] = None

class P2PNode:
    """
    Nó individual na rede P2P.
    """
    
    def __init__(self, port: int = 8080):
        self.peer_id = str(uuid.uuid4())
        self.port = port
        self.peers: Dict[str, PeerInfo] = {}
        self.active_offers: Dict[str, TradeOffer] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.running = False
        
        # Registrar handlers de mensagem
        self._register_message_handlers()
        
    def _register_message_handlers(self):
        """Registrar handlers para diferentes tipos de mensagem."""
        self.message_handlers.update({
            "peer_discovery": self._handle_peer_discovery,
            "trade_offer": self._handle_trade_offer,
            "trade_accept": self._handle_trade_accept,
            "trade_complete": self._handle_trade_complete,
            "heartbeat": self._handle_heartbeat
        })
    
    async def start_node(self):
        """Iniciar o nó P2P."""
        try:
            self.running = True
            logger.info(f"Iniciando nó P2P {self.peer_id} na porta {self.port}")
            
            # Iniciar servidor WebSocket
            start_server = websockets.serve(
                self._handle_connection,
                "localhost",
                self.port
            )
            
            # Iniciar discovery de peers
            discovery_task = asyncio.create_task(self._peer_discovery_loop())
            
            # Iniciar limpeza de ofertas expiradas
            cleanup_task = asyncio.create_task(self._cleanup_expired_offers())
            
            await start_server
            logger.info(f"Nó P2P ativo em ws://localhost:{self.port}")
            
            # Manter tasks rodando
            await asyncio.gather(discovery_task, cleanup_task)
            
        except Exception as e:
            logger.error(f"Erro ao iniciar nó P2P: {e}")
            self.running = False
    
    async def stop_node(self):
        """Parar o nó P2P."""
        self.running = False
        logger.info("Nó P2P parado")
    
    async def _handle_connection(self, websocket, path):
        """Lidar com conexões WebSocket de outros peers."""
        peer_address = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"Nova conexão de {peer_address}")
        
        try:
            async for message in websocket:
                await self._process_message(json.loads(message), websocket)
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Conexão fechada: {peer_address}")
        except Exception as e:
            logger.error(f"Erro na conexão {peer_address}: {e}")
    
    async def _process_message(self, message_data: Dict, websocket):
        """Processar mensagem recebida."""
        try:
            message = NetworkMessage(**message_data)
            handler = self.message_handlers.get(message.message_type)
            
            if handler:
                await handler(message, websocket)
            else:
                logger.warning(f"Tipo de mensagem desconhecida: {message.message_type}")
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
    
    async def _handle_peer_discovery(self, message: NetworkMessage, websocket):
        """Lidar com descoberta de peers."""
        peer_info = PeerInfo(**message.payload)
        self.peers[peer_info.peer_id] = peer_info
        logger.info(f"Peer descoberto: {peer_info.peer_id}")
        
        # Responder com nossas informações
        our_info = PeerInfo(
            peer_id=self.peer_id,
            address="localhost",
            port=self.port,
            public_key="mock_public_key",
            last_seen=datetime.now()
        )
        
        response = NetworkMessage(
            message_id=str(uuid.uuid4()),
            message_type="peer_info",
            sender_id=self.peer_id,
            payload=asdict(our_info),
            timestamp=datetime.now()
        )
        
        await websocket.send(json.dumps(asdict(response), default=str))
    
    async def _handle_trade_offer(self, message: NetworkMessage, websocket):
        """Lidar com ofertas de trade."""
        offer = TradeOffer(**message.payload)
        self.active_offers[offer.offer_id] = offer
        logger.info(f"Nova oferta recebida: {offer.symbol} {offer.amount} @ {offer.price}")
        
        # Notificar aplicação sobre nova oferta
        await self._notify_new_offer(offer)
    
    async def _handle_trade_accept(self, message: NetworkMessage, websocket):
        """Lidar com aceitação de trade."""
        offer_id = message.payload.get("offer_id")
        if offer_id in self.active_offers:
            offer = self.active_offers[offer_id]
            logger.info(f"Trade aceito: {offer_id}")
            
            # Processar execução do trade
            await self._execute_trade(offer, message.sender_id)
    
    async def _handle_trade_complete(self, message: NetworkMessage, websocket):
        """Lidar com conclusão de trade."""
        trade_id = message.payload.get("trade_id")
        logger.info(f"Trade concluído: {trade_id}")
        
        # Atualizar reputação do peer
        if message.sender_id in self.peers:
            self.peers[message.sender_id].trades_completed += 1
            self.peers[message.sender_id].reputation += 0.1
    
    async def _handle_heartbeat(self, message: NetworkMessage, websocket):
        """Lidar com heartbeat de peers."""
        if message.sender_id in self.peers:
            self.peers[message.sender_id].last_seen = datetime.now()
    
    async def create_trade_offer(self, symbol: str, amount: float, price: float, trade_type: str) -> str:
        """Criar uma nova oferta de trade."""
        offer_id = str(uuid.uuid4())
        
        offer = TradeOffer(
            offer_id=offer_id,
            peer_id=self.peer_id,
            symbol=symbol,
            amount=amount,
            price=price,
            trade_type=trade_type,
            timestamp=datetime.now(),
            expires_at=datetime.now().replace(hour=datetime.now().hour + 1),  # Expira em 1h
            signature="mock_signature"
        )
        
        self.active_offers[offer_id] = offer
        
        # Broadcast para todos os peers
        await self._broadcast_message("trade_offer", asdict(offer))
        
        logger.info(f"Oferta criada: {offer_id}")
        return offer_id
    
    async def accept_trade_offer(self, offer_id: str) -> bool:
        """Aceitar uma oferta de trade."""
        if offer_id not in self.active_offers:
            return False
        
        offer = self.active_offers[offer_id]
        
        # Enviar aceitação para o peer que criou a oferta
        message = NetworkMessage(
            message_id=str(uuid.uuid4()),
            message_type="trade_accept",
            sender_id=self.peer_id,
            payload={"offer_id": offer_id},
            timestamp=datetime.now()
        )
        
        # Encontrar e enviar para o peer correto
        target_peer = self.peers.get(offer.peer_id)
        if target_peer:
            await self._send_message_to_peer(target_peer, message)
            logger.info(f"Oferta aceita: {offer_id}")
            return True
        
        return False
    
    async def _broadcast_message(self, message_type: str, payload: Dict):
        """Broadcast mensagem para todos os peers."""
        message = NetworkMessage(
            message_id=str(uuid.uuid4()),
            message_type=message_type,
            sender_id=self.peer_id,
            payload=payload,
            timestamp=datetime.now()
        )
        
        # Enviar para todos os peers conectados
        for peer in self.peers.values():
            try:
                await self._send_message_to_peer(peer, message)
            except Exception as e:
                logger.error(f"Erro ao enviar para peer {peer.peer_id}: {e}")
    
    async def _send_message_to_peer(self, peer: PeerInfo, message: NetworkMessage):
        """Enviar mensagem para um peer específico."""
        try:
            uri = f"ws://{peer.address}:{peer.port}"
            async with websockets.connect(uri) as websocket:
                await websocket.send(json.dumps(asdict(message), default=str))
        except Exception as e:
            logger.error(f"Erro ao conectar com peer {peer.peer_id}: {e}")
    
    async def _peer_discovery_loop(self):
        """Loop de descoberta de peers."""
        while self.running:
            try:
                # Tentar conectar com peers conhecidos
                known_peers = ["8081", "8082", "8083"]  # Portas de exemplo
                
                for port in known_peers:
                    if port != str(self.port):
                        try:
                            uri = f"ws://localhost:{port}"
                            async with websockets.connect(uri, timeout=5) as websocket:
                                discovery_message = NetworkMessage(
                                    message_id=str(uuid.uuid4()),
                                    message_type="peer_discovery",
                                    sender_id=self.peer_id,
                                    payload={
                                        "peer_id": self.peer_id,
                                        "address": "localhost",
                                        "port": self.port,
                                        "public_key": "mock_public_key",
                                        "last_seen": datetime.now()
                                    },
                                    timestamp=datetime.now()
                                )
                                await websocket.send(json.dumps(asdict(discovery_message), default=str))
                        except:
                            pass  # Peer não disponível
                
                await asyncio.sleep(30)  # Descoberta a cada 30 segundos
                
            except Exception as e:
                logger.error(f"Erro no discovery loop: {e}")
                await asyncio.sleep(60)
    
    async def _cleanup_expired_offers(self):
        """Limpar ofertas expiradas."""
        while self.running:
            try:
                now = datetime.now()
                expired_offers = [
                    offer_id for offer_id, offer in self.active_offers.items()
                    if offer.expires_at < now
                ]
                
                for offer_id in expired_offers:
                    del self.active_offers[offer_id]
                    logger.info(f"Oferta expirada removida: {offer_id}")
                
                await asyncio.sleep(60)  # Limpeza a cada minuto
                
            except Exception as e:
                logger.error(f"Erro na limpeza de ofertas: {e}")
                await asyncio.sleep(300)
    
    async def _notify_new_offer(self, offer: TradeOffer):
        """Notificar aplicação sobre nova oferta."""
        # Implementar notificação para UI ou sistema de callbacks
        pass
    
    async def _execute_trade(self, offer: TradeOffer, acceptor_id: str):
        """Executar trade aceito."""
        # Implementar lógica de execução de trade
        logger.info(f"Executando trade {offer.offer_id} entre {offer.peer_id} e {acceptor_id}")
        
        # Simular execução
        trade_complete_message = NetworkMessage(
            message_id=str(uuid.uuid4()),
            message_type="trade_complete",
            sender_id=self.peer_id,
            payload={
                "trade_id": offer.offer_id,
                "status": "completed",
                "timestamp": datetime.now()
            },
            timestamp=datetime.now()
        )
        
        # Notificar conclusão
        await self._broadcast_message("trade_complete", trade_complete_message.payload)
    
    def get_network_status(self) -> Dict:
        """Obter status da rede."""
        return {
            "peer_id": self.peer_id,
            "connected_peers": len(self.peers),
            "active_offers": len(self.active_offers),
            "peers": [asdict(peer) for peer in self.peers.values()],
            "offers": [asdict(offer) for offer in self.active_offers.values()],
            "timestamp": datetime.now()
        }


# Instância global do nó P2P
p2p_node = P2PNode()
