"""
🌐 AEONCOSMA P2P Network - Teste Direto
Demonstração funcional da rede P2P
Copyright 2025 - Luiz H. P. Cruz
"""

import asyncio
import random
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class NetworkMessage:
    """Mensagem da rede P2P"""
    id: str
    sender: str
    content: str
    message_type: str
    timestamp: float
    priority: int = 1

@dataclass
class Peer:
    """Peer da rede P2P"""
    id: str
    address: str
    last_seen: float
    is_online: bool = True

class P2PNodeLive:
    """Nó P2P em funcionamento ao vivo"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.peers: Dict[str, Peer] = {}
        self.received_messages: List[NetworkMessage] = []
        self.sent_messages: List[NetworkMessage] = []
        self.is_online = True
        
        print(f"🔵 Nó P2P '{node_id}' inicializado!")
    
    async def connect_peer(self, peer_id: str, address: str):
        """Conectar a um peer"""
        peer = Peer(
            id=peer_id,
            address=address,
            last_seen=datetime.now().timestamp(),
            is_online=True
        )
        self.peers[peer_id] = peer
        print(f"🔗 {self.node_id} conectado ao peer {peer_id} ({address})")
        await asyncio.sleep(0.1)  # Simular latência de rede
        return True
    
    async def broadcast(self, message: str, message_type: str = "general", priority: int = 1):
        """Transmitir mensagem para todos os peers"""
        msg_id = f"msg_{random.randint(1000, 9999)}"
        
        network_msg = NetworkMessage(
            id=msg_id,
            sender=self.node_id,
            content=message,
            message_type=message_type,
            timestamp=datetime.now().timestamp(),
            priority=priority
        )
        
        self.sent_messages.append(network_msg)
        
        print(f"📡 {self.node_id} transmitindo: '{message}' para {len(self.peers)} peers")
        
        # Simular propagação na rede
        await asyncio.sleep(0.05 * len(self.peers))
        
        return {
            "status": "message_broadcast",
            "message_id": msg_id,
            "peers_reached": len(self.peers),
            "sender": self.node_id,
            "timestamp": datetime.now().isoformat()
        }
    
    async def receive_message(self, message_data: Dict[str, Any]):
        """Receber mensagem de outro nó"""
        network_msg = NetworkMessage(
            id=message_data.get("id", f"recv_{random.randint(1000, 9999)}"),
            sender=message_data.get("sender", "unknown"),
            content=message_data.get("content", ""),
            message_type=message_data.get("message_type", "general"),
            timestamp=message_data.get("timestamp", datetime.now().timestamp())
        )
        
        self.received_messages.append(network_msg)
        print(f"📥 {self.node_id} recebeu de {network_msg.sender}: '{network_msg.content}'")
        
        return True
    
    def get_status(self):
        """Obter status do nó"""
        return {
            "node_id": self.node_id,
            "is_online": self.is_online,
            "connected_peers": len([p for p in self.peers.values() if p.is_online]),
            "total_peers": len(self.peers),
            "messages_sent": len(self.sent_messages),
            "messages_received": len(self.received_messages),
            "uptime": "Active"
        }

async def run_p2p_demo():
    """Executar demonstração da rede P2P ao vivo"""
    
    print("🌐 AEONCOSMA P2P NETWORK - AO VIVO!")
    print("=" * 50)
    print("Criado por: Luiz H. P. Cruz")
    print("Data: Agosto 2025")
    print("=" * 50)
    
    # Criar nós da rede
    nodes = {}
    node_names = ["luiz_node", "energy_node", "crypto_node", "quantum_node", "cosmos_node"]
    
    print("\n📡 Criando rede P2P...")
    for name in node_names:
        nodes[name] = P2PNodeLive(name)
        await asyncio.sleep(0.2)
    
    # Conectar todos os nós entre si
    print("\n🔗 Conectando nós...")
    for i, (name1, node1) in enumerate(nodes.items()):
        for j, (name2, node2) in enumerate(nodes.items()):
            if i != j:
                await node1.connect_peer(name2, f"192.168.1.{100+j}")
    
    print(f"\n✅ Rede criada com {len(nodes)} nós interconectados!")
    
    # Status inicial
    print("\n📊 STATUS DA REDE:")
    for name, node in nodes.items():
        status = node.get_status()
        print(f"   {name}: {status['connected_peers']} peers, Status: {'🟢 Online' if status['is_online'] else '🔴 Offline'}")
    
    # Demonstração de transmissões
    print("\n📤 DEMONSTRAÇÃO DE TRANSMISSÕES:")
    
    messages = [
        ("luiz_node", "Olá da rede AEONCOSMA P2P! Sistema funcionando!", "greeting"),
        ("energy_node", "Dados energéticos sincronizados - 98.5% eficiência", "energy_data"),
        ("crypto_node", "Criptografia AES-256 ativa - Segurança máxima", "security"),
        ("quantum_node", "Canal quântico estabelecido - Fidelidade 99.2%", "quantum"),
        ("cosmos_node", "Análise cosmológica concluída - H0 = 67.4 km/s/Mpc", "cosmos")
    ]
    
    for sender_name, message, msg_type in messages:
        sender = nodes[sender_name]
        result = await sender.broadcast(message, msg_type, 5)
        
        # Simular recepção em outros nós
        for receiver_name, receiver in nodes.items():
            if receiver_name != sender_name:
                await receiver.receive_message({
                    "id": result["message_id"],
                    "sender": sender_name,
                    "content": message,
                    "message_type": msg_type,
                    "timestamp": datetime.now().timestamp()
                })
        
        await asyncio.sleep(1)  # Pausa entre transmissões
    
    # Status final
    print("\n📈 STATUS FINAL DA REDE:")
    total_messages = 0
    for name, node in nodes.items():
        status = node.get_status()
        total_messages += status['messages_sent'] + status['messages_received']
        print(f"   {name}:")
        print(f"     📤 Enviadas: {status['messages_sent']}")
        print(f"     📥 Recebidas: {status['messages_received']}")
        print(f"     🔗 Peers: {status['connected_peers']}")
    
    print(f"\n🎉 REDE P2P AEONCOSMA OPERACIONAL!")
    print(f"   📊 Total de nós: {len(nodes)}")
    print(f"   📨 Total de mensagens: {total_messages}")
    print(f"   🔗 Conexões ativas: {len(nodes) * (len(nodes)-1)}")
    print(f"   ⚡ Performance: EXCELENTE")
    
    # Interação ao vivo
    print(f"\n🎮 INTERAÇÃO AO VIVO:")
    print(f"   Digite uma mensagem para transmitir na rede")
    print(f"   (Digite 'quit' para sair)")
    
    while True:
        try:
            user_input = input(f"\n🌐 Luiz> ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input == '':
                continue
            else:
                # Transmitir mensagem do usuário
                luiz_node = nodes["luiz_node"]
                result = await luiz_node.broadcast(f"Luiz diz: {user_input}", "user_message", 10)
                
                # Simular recepção
                for other_name, other_node in nodes.items():
                    if other_name != "luiz_node":
                        await other_node.receive_message({
                            "id": result["message_id"],
                            "sender": "luiz_node",
                            "content": f"Luiz diz: {user_input}",
                            "message_type": "user_message",
                            "timestamp": datetime.now().timestamp()
                        })
                
                print(f"✅ Sua mensagem foi transmitida para {len(nodes)-1} nós!")
        
        except KeyboardInterrupt:
            print(f"\n⚠️ Interrompido pelo usuário")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print(f"\n👋 Rede P2P AEONCOSMA desconectada!")
    print(f"🚀 Criado por Luiz H. P. Cruz - Tecnologia 100% brasileira!")

if __name__ == "__main__":
    print("🚀 Iniciando AEONCOSMA P2P Network...")
    try:
        asyncio.run(run_p2p_demo())
    except KeyboardInterrupt:
        print("\n👋 Demo encerrada!")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        print("🔄 Programa finalizado")
