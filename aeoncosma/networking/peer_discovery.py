# aeoncosma/networking/peer_discovery.py
"""
🔍 PEER DISCOVERY - Descoberta Automática de Nós
Sistema de descoberta e anúncio de peers na rede AEONCOSMA
Desenvolvido por Luiz Cruz - 2025
"""

import socket
import threading
import json
import time
from datetime import datetime
from typing import Callable, Dict, Any, List, Tuple

class PeerDiscovery:
    """
    Sistema de descoberta automática de peers na rede P2P
    """
    
    def __init__(self, node_id: str, port: int, broadcast_port: int = 5001):
        self.node_id = node_id
        self.port = port
        self.broadcast_port = broadcast_port
        self.discovered_peers = {}  # {node_id: (ip, port, last_seen)}
        self.running = False
        
        # Estatísticas
        self.stats = {
            "announcements_sent": 0,
            "peers_discovered": 0,
            "broadcast_errors": 0,
            "last_announcement": None,
            "discovery_start": None
        }
        
        print(f"🔍 [PeerDiscovery] Inicializado para {node_id}")
        print(f"📡 Porta de broadcast: {broadcast_port}")

    def announce_presence(self, additional_data: Dict[str, Any] = None) -> bool:
        """Anuncia presença na rede via broadcast"""
        try:
            # Prepara mensagem de anúncio
            announcement = {
                "type": "peer_announce",
                "node_id": self.node_id,
                "port": self.port,
                "timestamp": datetime.now().isoformat(),
                "announcement_version": "1.0"
            }
            
            # Adiciona dados extras se fornecidos
            if additional_data:
                announcement["additional_data"] = additional_data
            
            message_data = json.dumps(announcement).encode('utf-8')
            
            # Envia broadcast UDP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(message_data, ('<broadcast>', self.broadcast_port))
                
                self.stats["announcements_sent"] += 1
                self.stats["last_announcement"] = datetime.now().isoformat()
                
                print(f"📢 [PeerDiscovery] Presença anunciada via broadcast")
                return True
                
        except Exception as e:
            print(f"❌ [PeerDiscovery] Erro ao anunciar presença: {e}")
            self.stats["broadcast_errors"] += 1
            return False

    def listen_for_peers(self, callback: Callable[[Dict[str, Any], Tuple[str, int]], None]):
        """Escuta anúncios de outros peers"""
        def listen():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind(('', self.broadcast_port))
                    sock.settimeout(1.0)  # Timeout para permitir parada
                    
                    self.running = True
                    self.stats["discovery_start"] = datetime.now()
                    
                    print(f"👂 [PeerDiscovery] Escutando peers na porta {self.broadcast_port}")
                    
                    while self.running:
                        try:
                            data, addr = sock.recvfrom(2048)
                            
                            # Ignora mensagens de si mesmo
                            if addr[0] == '127.0.0.1' or addr[0] == socket.gethostbyname(socket.gethostname()):
                                continue
                            
                            try:
                                message = json.loads(data.decode('utf-8'))
                                
                                # Verifica se é anúncio válido
                                if (message.get("type") == "peer_announce" and 
                                    message.get("node_id") and 
                                    message.get("node_id") != self.node_id):
                                    
                                    peer_node_id = message["node_id"]
                                    peer_port = message.get("port", 9000)
                                    
                                    # Atualiza lista de peers descobertos
                                    self.discovered_peers[peer_node_id] = (
                                        addr[0],  # IP
                                        peer_port,  # Porta
                                        datetime.now().isoformat()  # Última vez visto
                                    )
                                    
                                    self.stats["peers_discovered"] += 1
                                    
                                    print(f"🎯 [PeerDiscovery] Peer descoberto: {peer_node_id} ({addr[0]}:{peer_port})")
                                    
                                    # Chama callback se fornecido
                                    if callback:
                                        try:
                                            callback(message, addr)
                                        except Exception as e:
                                            print(f"❌ [PeerDiscovery] Erro no callback: {e}")
                                            
                            except json.JSONDecodeError:
                                print(f"⚠️ [PeerDiscovery] JSON inválido de {addr}")
                                
                        except socket.timeout:
                            # Timeout normal, continua loop
                            continue
                        except Exception as e:
                            if self.running:
                                print(f"❌ [PeerDiscovery] Erro ao receber: {e}")
                                
            except Exception as e:
                print(f"❌ [PeerDiscovery] Erro crítico no listener: {e}")
            finally:
                self.running = False
                print(f"🛑 [PeerDiscovery] Listener parado")

        # Inicia listener em thread separada
        listener_thread = threading.Thread(target=listen, daemon=True, name="peer_discovery_listener")
        listener_thread.start()
        
        return listener_thread

    def start_auto_announce(self, interval_seconds: int = 30, additional_data: Dict[str, Any] = None):
        """Inicia anúncios automáticos periódicos"""
        def auto_announce():
            while self.running:
                self.announce_presence(additional_data)
                time.sleep(interval_seconds)
        
        # Thread para anúncios automáticos
        announce_thread = threading.Thread(target=auto_announce, daemon=True, name="auto_announce")
        announce_thread.start()
        
        print(f"⏰ [PeerDiscovery] Auto-anúncio iniciado (intervalo: {interval_seconds}s)")
        
        return announce_thread

    def get_discovered_peers(self, max_age_minutes: int = 10) -> Dict[str, Tuple[str, int]]:
        """Retorna peers descobertos recentemente"""
        current_time = datetime.now()
        active_peers = {}
        
        for node_id, (ip, port, last_seen) in self.discovered_peers.items():
            try:
                last_seen_time = datetime.fromisoformat(last_seen)
                age_minutes = (current_time - last_seen_time).total_seconds() / 60
                
                if age_minutes <= max_age_minutes:
                    active_peers[node_id] = (ip, port)
                    
            except Exception as e:
                print(f"⚠️ [PeerDiscovery] Erro ao processar peer {node_id}: {e}")
        
        return active_peers

    def cleanup_old_peers(self, max_age_minutes: int = 30):
        """Remove peers que não foram vistos há muito tempo"""
        current_time = datetime.now()
        peers_to_remove = []
        
        for node_id, (ip, port, last_seen) in self.discovered_peers.items():
            try:
                last_seen_time = datetime.fromisoformat(last_seen)
                age_minutes = (current_time - last_seen_time).total_seconds() / 60
                
                if age_minutes > max_age_minutes:
                    peers_to_remove.append(node_id)
                    
            except Exception:
                peers_to_remove.append(node_id)  # Remove peers com timestamp inválido
        
        # Remove peers antigos
        for node_id in peers_to_remove:
            del self.discovered_peers[node_id]
            
        if peers_to_remove:
            print(f"🧹 [PeerDiscovery] {len(peers_to_remove)} peers antigos removidos")

    def request_peer_list(self, target_ip: str, target_port: int) -> List[Dict[str, Any]]:
        """Solicita lista de peers de outro nó"""
        try:
            request_message = {
                "type": "peer_list_request",
                "requester": self.node_id,
                "timestamp": datetime.now().isoformat()
            }
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)
                sock.connect((target_ip, target_port))
                
                # Envia solicitação
                sock.send(json.dumps(request_message).encode('utf-8'))
                
                # Recebe resposta
                response_data = sock.recv(4096)
                if response_data:
                    response = json.loads(response_data.decode('utf-8'))
                    
                    if response.get("type") == "peer_list_response":
                        peer_list = response.get("peers", [])
                        print(f"📋 [PeerDiscovery] Recebida lista de {len(peer_list)} peers de {target_ip}:{target_port}")
                        return peer_list
                        
        except Exception as e:
            print(f"❌ [PeerDiscovery] Erro ao solicitar lista de peers: {e}")
            
        return []

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do peer discovery"""
        uptime = 0
        if self.stats["discovery_start"]:
            uptime = (datetime.now() - self.stats["discovery_start"]).total_seconds()
        
        return {
            **self.stats,
            "uptime_seconds": uptime,
            "total_discovered": len(self.discovered_peers),
            "active_peers": len(self.get_discovered_peers()),
            "is_running": self.running
        }

    def stop(self):
        """Para o sistema de descoberta"""
        print(f"🛑 [PeerDiscovery] Parando sistema de descoberta...")
        self.running = False
        
        # Cleanup final
        self.cleanup_old_peers(0)  # Remove todos os peers

def main():
    """Função de teste para PeerDiscovery"""
    def peer_discovered(message, addr):
        print(f"🧪 Peer descoberto: {message['node_id']} de {addr}")
    
    # Cria sistema de descoberta
    discovery = PeerDiscovery("test_discovery_node", 9998, 5555)
    
    try:
        # Inicia listener
        discovery.listen_for_peers(peer_discovered)
        
        # Inicia anúncios automáticos
        discovery.start_auto_announce(10, {"test_mode": True})
        
        print("🚀 PeerDiscovery em teste. Pressione Ctrl+C para parar.")
        
        # Loop principal
        while discovery.running:
            time.sleep(5)
            
            # Mostra peers descobertos
            peers = discovery.get_discovered_peers()
            if peers:
                print(f"📊 Peers ativos: {list(peers.keys())}")
            
            # Cleanup periódico
            discovery.cleanup_old_peers()
            
    except KeyboardInterrupt:
        print("\n🛑 Teste interrompido")
    finally:
        discovery.stop()

if __name__ == "__main__":
    main()
