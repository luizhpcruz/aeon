"""
🌐 AEONCOSMA P2P Network Node
Rede peer-to-peer descentralizada com capacidade offline
Copyright 2025 - Luiz H. P. Cruz
"""

import asyncio
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict

@dataclass
class NetworkMessage:
    """Mensagem da rede P2P"""
    id: str
    sender_id: str
    content: Dict[str, Any]
    timestamp: float
    signature: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NetworkMessage':
        return cls(**data)

@dataclass
class Peer:
    """Peer da rede"""
    id: str
    address: str
    port: int
    last_seen: float
    is_online: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class P2PNode:
    """🌐 Nó da rede P2P descentralizada"""
    
    def __init__(self, node_id: Optional[str] = None, port: int = 8888):
        self.node_id = node_id or str(uuid.uuid4())[:8]
        self.port = port
        self.version = "1.0.0"
        self.author = "Luiz H. P. Cruz"
        
        # Estado da rede
        self.peers: Dict[str, Peer] = {}
        self.message_history: List[NetworkMessage] = []
        self.offline_messages: List[NetworkMessage] = []
        self.is_running = False
        self.max_peers = 100
        self.max_messages = 1000
        
        # Estatísticas
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "peers_connected": 0,
            "uptime_start": time.time()
        }
    
    async def start(self):
        """Iniciar o nó P2P"""
        self.is_running = True
        self.stats["uptime_start"] = time.time()
        print(f"🌐 P2P Node {self.node_id} iniciado na porta {self.port}")
        
        # Simular descoberta de peers
        await self._discover_peers()
    
    async def _discover_peers(self):
        """Descobrir peers na rede (simulado)"""
        # Simular peers conhecidos na rede AEONCOSMA
        known_peers = [
            {"id": "aeon001", "address": "192.168.1.100", "port": 8888},
            {"id": "aeon002", "address": "192.168.1.101", "port": 8889},
            {"id": "aeon003", "address": "192.168.1.102", "port": 8890},
            {"id": "cosma01", "address": "10.0.1.50", "port": 8888},
            {"id": "cosma02", "address": "10.0.1.51", "port": 8889},
        ]
        
        for peer_data in known_peers:
            if peer_data["id"] != self.node_id:
                peer = Peer(
                    id=peer_data["id"],
                    address=peer_data["address"],
                    port=peer_data["port"],
                    last_seen=time.time(),
                    is_online=True
                )
                self.peers[peer.id] = peer
        
        self.stats["peers_connected"] = len(self.peers)
        print(f"✅ Descobertos {len(self.peers)} peers na rede")
    
    async def broadcast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Fazer broadcast de dados na rede"""
        message = NetworkMessage(
            id=str(uuid.uuid4())[:12],
            sender_id=self.node_id,
            content=data,
            timestamp=time.time()
        )
        
        # Adicionar à história local
        self.message_history.append(message)
        self._cleanup_old_messages()
        
        # Simular envio para todos os peers
        successful_sends = 0
        failed_sends = 0
        
        for peer_id, peer in self.peers.items():
            try:
                # Simular latência de rede
                await asyncio.sleep(0.01)
                
                if peer.is_online:
                    successful_sends += 1
                    print(f"📤 Mensagem {message.id} enviada para {peer_id}")
                else:
                    # Armazenar para envio quando peer voltar online
                    self.offline_messages.append(message)
                    failed_sends += 1
                    
            except Exception as e:
                failed_sends += 1
                print(f"❌ Falha ao enviar para {peer_id}: {e}")
        
        self.stats["messages_sent"] += 1
        
        result = {
            "status": "broadcast_completed",
            "message_id": message.id,
            "sender": self.node_id,
            "peers_reached": successful_sends,
            "peers_failed": failed_sends,
            "total_peers": len(self.peers),
            "timestamp": datetime.now().isoformat(),
            "content_hash": hash(str(data))
        }
        
        return result
    
    async def receive_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Receber mensagem de outro peer"""
        try:
            message = NetworkMessage.from_dict(message_data)
            
            # Verificar se já recebemos esta mensagem
            if any(m.id == message.id for m in self.message_history):
                return {"status": "duplicate", "message_id": message.id}
            
            # Adicionar à história
            self.message_history.append(message)
            self._cleanup_old_messages()
            
            # Atualizar estatísticas
            self.stats["messages_received"] += 1
            
            # Simular validação da mensagem
            await asyncio.sleep(0.01)
            
            result = {
                "status": "message_received",
                "message_id": message.id,
                "sender": message.sender_id,
                "receiver": self.node_id,
                "timestamp": datetime.now().isoformat(),
                "validated": True
            }
            
            print(f"📥 Mensagem {message.id} recebida de {message.sender_id}")
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _cleanup_old_messages(self):
        """Limpar mensagens antigas para economizar memória"""
        if len(self.message_history) > self.max_messages:
            # Manter apenas as mensagens mais recentes
            self.message_history = self.message_history[-self.max_messages:]
    
    async def sync_with_peer(self, peer_id: str) -> Dict[str, Any]:
        """Sincronizar dados com um peer específico"""
        if peer_id not in self.peers:
            return {"status": "error", "error": "Peer não encontrado"}
        
        peer = self.peers[peer_id]
        
        # Simular sincronização
        await asyncio.sleep(0.5)
        
        # Enviar mensagens offline se houver
        offline_sent = 0
        if self.offline_messages:
            for message in self.offline_messages[:]:
                if message.sender_id == self.node_id:
                    # Tentar reenviar
                    self.offline_messages.remove(message)
                    offline_sent += 1
        
        peer.last_seen = time.time()
        peer.is_online = True
        
        result = {
            "status": "sync_completed",
            "peer_id": peer_id,
            "peer_address": f"{peer.address}:{peer.port}",
            "offline_messages_sent": offline_sent,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def get_network_status(self) -> Dict[str, Any]:
        """Obter status da rede"""
        online_peers = sum(1 for p in self.peers.values() if p.is_online)
        uptime = time.time() - self.stats["uptime_start"]
        
        return {
            "node_id": self.node_id,
            "version": self.version,
            "author": self.author,
            "is_running": self.is_running,
            "port": self.port,
            "total_peers": len(self.peers),
            "online_peers": online_peers,
            "offline_peers": len(self.peers) - online_peers,
            "messages_in_history": len(self.message_history),
            "offline_messages": len(self.offline_messages),
            "uptime_seconds": uptime,
            "stats": self.stats
        }
    
    def get_peers_list(self) -> List[Dict[str, Any]]:
        """Obter lista de peers"""
        return [peer.to_dict() for peer in self.peers.values()]
    
    def shutdown(self):
        """Desligar o nó"""
        self.is_running = False
        
        # Notificar peers sobre desconexão (simulado)
        print(f"🔄 Notificando {len(self.peers)} peers sobre desconexão...")
        
        # Limpar dados
        self.message_history.clear()
        self.offline_messages.clear()
        
        print(f"🛑 P2P Node {self.node_id} desligado")
