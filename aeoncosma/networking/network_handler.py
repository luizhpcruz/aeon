# aeoncosma/networking/network_handler.py
"""
🌐 NETWORK HANDLER - Controlador de Conexões e Roteamento
Gerencia conexões P2P e roteamento de mensagens na rede AEONCOSMA
Desenvolvido por Luiz Cruz - 2025
"""

import socket
import threading
import json
import time
from datetime import datetime
from typing import Dict, Callable, Tuple, Any

class NetworkHandler:
    """
    Controlador principal de rede P2P para AEONCOSMA
    """
    
    def __init__(self, node_id: str, port: int, message_callback: Callable):
        self.node_id = node_id
        self.port = port
        self.message_callback = message_callback
        self.peers = {}  # {id: (ip, port)}
        self.running = False
        self.server_socket = None
        self.connection_count = 0
        
        # Estatísticas
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "peers_connected": 0,
            "connection_errors": 0,
            "start_time": None
        }
        
        print(f"🌐 [NetworkHandler] Inicializado para {node_id} na porta {port}")

    def start_server(self):
        """Inicia o servidor P2P para escutar conexões"""
        def listen():
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server_socket.bind(('', self.port))
                self.server_socket.listen(10)  # Aumentado para mais conexões
                
                self.running = True
                self.stats["start_time"] = datetime.now()
                
                print(f"✅ [NetworkHandler] Servidor P2P ativo na porta {self.port}")

                while self.running:
                    try:
                        conn, addr = self.server_socket.accept()
                        self.connection_count += 1
                        
                        # Processa cada conexão em thread separada
                        threading.Thread(
                            target=self.handle_peer, 
                            args=(conn, addr), 
                            daemon=True,
                            name=f"peer_handler_{self.connection_count}"
                        ).start()
                        
                    except socket.error as e:
                        if self.running:  # Só mostra erro se ainda estiver rodando
                            print(f"⚠️ [NetworkHandler] Erro ao aceitar conexão: {e}")
                            
            except Exception as e:
                print(f"❌ [NetworkHandler] Erro crítico no servidor: {e}")
            finally:
                self.stop_server()

        # Inicia servidor em thread separada
        server_thread = threading.Thread(target=listen, daemon=True, name=f"server_{self.node_id}")
        server_thread.start()
        
        return server_thread

    def handle_peer(self, conn: socket.socket, addr: Tuple[str, int]):
        """Processa conexão de um peer"""
        peer_info = f"{addr[0]}:{addr[1]}"
        
        try:
            print(f"🤝 [NetworkHandler] Nova conexão de {peer_info}")
            
            # Timeout para receber dados
            conn.settimeout(30)
            
            # Recebe dados do peer
            data = conn.recv(8192)  # Aumentado buffer
            if not data:
                print(f"⚠️ [NetworkHandler] Dados vazios de {peer_info}")
                return
            
            # Decodifica mensagem
            try:
                message = json.loads(data.decode('utf-8'))
                self.stats["messages_received"] += 1
                
                print(f"📨 [NetworkHandler] Mensagem de {peer_info}: {message.get('type', 'unknown')}")
                
                # Adiciona informações de contexto à mensagem
                message["_network_context"] = {
                    "sender_address": addr,
                    "received_at": datetime.now().isoformat(),
                    "connection_id": self.connection_count
                }
                
                # Chama callback para processar mensagem
                if self.message_callback:
                    try:
                        response = self.message_callback(message, addr)
                        
                        # Se callback retorna resposta, envia de volta
                        if response:
                            response_data = json.dumps(response).encode('utf-8')
                            conn.send(response_data)
                            self.stats["messages_sent"] += 1
                            print(f"📤 [NetworkHandler] Resposta enviada para {peer_info}")
                            
                    except Exception as e:
                        print(f"❌ [NetworkHandler] Erro no callback: {e}")
                        
                        # Envia resposta de erro
                        error_response = {
                            "status": "error",
                            "message": "Callback processing failed",
                            "timestamp": datetime.now().isoformat()
                        }
                        conn.send(json.dumps(error_response).encode('utf-8'))
                
            except json.JSONDecodeError as e:
                print(f"❌ [NetworkHandler] JSON inválido de {peer_info}: {e}")
                self.stats["connection_errors"] += 1
                
                # Envia erro JSON
                error_response = {
                    "status": "error", 
                    "message": "Invalid JSON format"
                }
                conn.send(json.dumps(error_response).encode('utf-8'))
                
        except socket.timeout:
            print(f"⏰ [NetworkHandler] Timeout na conexão com {peer_info}")
            self.stats["connection_errors"] += 1
            
        except Exception as e:
            print(f"❌ [NetworkHandler] Erro ao processar peer {peer_info}: {e}")
            self.stats["connection_errors"] += 1
            
        finally:
            try:
                conn.close()
                print(f"🔚 [NetworkHandler] Conexão com {peer_info} encerrada")
            except:
                pass

    def send_to_peer(self, ip: str, port: int, message: Dict[str, Any], timeout: int = 10) -> bool:
        """Envia mensagem para um peer específico"""
        peer_address = f"{ip}:{port}"
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                sock.connect((ip, port))
                
                # Adiciona metadados à mensagem
                message["_sender"] = self.node_id
                message["_timestamp"] = datetime.now().isoformat()
                
                # Envia mensagem
                message_data = json.dumps(message).encode('utf-8')
                sock.send(message_data)
                
                self.stats["messages_sent"] += 1
                print(f"📤 [NetworkHandler] Mensagem enviada para {peer_address}")
                
                # Tenta receber resposta
                try:
                    sock.settimeout(5)  # Timeout menor para resposta
                    response_data = sock.recv(4096)
                    if response_data:
                        response = json.loads(response_data.decode('utf-8'))
                        self.stats["messages_received"] += 1
                        print(f"📨 [NetworkHandler] Resposta de {peer_address}: {response.get('status', 'OK')}")
                        return True
                except socket.timeout:
                    print(f"⏰ [NetworkHandler] Sem resposta de {peer_address}")
                    return True  # Enviou com sucesso mesmo sem resposta
                    
                return True
                
        except ConnectionRefusedError:
            print(f"🚫 [NetworkHandler] Conexão recusada por {peer_address}")
            self.stats["connection_errors"] += 1
            return False
            
        except socket.timeout:
            print(f"⏰ [NetworkHandler] Timeout ao conectar com {peer_address}")
            self.stats["connection_errors"] += 1
            return False
            
        except Exception as e:
            print(f"❌ [NetworkHandler] Erro ao enviar para {peer_address}: {e}")
            self.stats["connection_errors"] += 1
            return False

    def broadcast(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Envia mensagem para todos os peers conhecidos"""
        print(f"📢 [NetworkHandler] Broadcasting mensagem para {len(self.peers)} peers")
        
        broadcast_results = {
            "total_peers": len(self.peers),
            "successful": [],
            "failed": [],
            "start_time": datetime.now().isoformat()
        }
        
        # Broadcast paralelo usando threads
        def send_to_single_peer(peer_id: str, ip: str, port: int):
            success = self.send_to_peer(ip, port, message.copy())
            
            if success:
                broadcast_results["successful"].append(peer_id)
            else:
                broadcast_results["failed"].append(peer_id)
        
        # Cria threads para envio paralelo
        threads = []
        for peer_id, (ip, port) in self.peers.items():
            thread = threading.Thread(
                target=send_to_single_peer,
                args=(peer_id, ip, port),
                daemon=True
            )
            thread.start()
            threads.append(thread)
        
        # Aguarda todas as threads terminarem
        for thread in threads:
            thread.join(timeout=15)  # Timeout para evitar travamento
        
        # Calcula resultados
        broadcast_results["success_rate"] = (
            len(broadcast_results["successful"]) / broadcast_results["total_peers"] * 100
            if broadcast_results["total_peers"] > 0 else 0
        )
        broadcast_results["end_time"] = datetime.now().isoformat()
        
        print(f"📊 [NetworkHandler] Broadcast concluído: {broadcast_results['success_rate']:.1f}% sucesso")
        
        return broadcast_results

    def add_peer(self, peer_id: str, ip: str, port: int):
        """Adiciona um novo peer à lista"""
        if peer_id not in self.peers:
            self.peers[peer_id] = (ip, port)
            self.stats["peers_connected"] += 1
            print(f"✅ [NetworkHandler] Novo peer adicionado: {peer_id} ({ip}:{port})")
        else:
            # Atualiza endereço se já existe
            self.peers[peer_id] = (ip, port)
            print(f"🔄 [NetworkHandler] Peer atualizado: {peer_id} ({ip}:{port})")

    def remove_peer(self, peer_id: str):
        """Remove peer da lista"""
        if peer_id in self.peers:
            del self.peers[peer_id]
            print(f"🗑️ [NetworkHandler] Peer removido: {peer_id}")

    def get_peer_list(self) -> Dict[str, Tuple[str, int]]:
        """Retorna lista de peers"""
        return self.peers.copy()

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do network handler"""
        uptime = 0
        if self.stats["start_time"]:
            uptime = (datetime.now() - self.stats["start_time"]).total_seconds()
        
        return {
            **self.stats,
            "uptime_seconds": uptime,
            "total_peers": len(self.peers),
            "is_running": self.running,
            "connection_count": self.connection_count
        }

    def stop_server(self):
        """Para o servidor de rede"""
        print(f"🛑 [NetworkHandler] Parando servidor...")
        self.running = False
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print(f"✅ [NetworkHandler] Servidor parado")

def main():
    """Função de teste para NetworkHandler"""
    def test_callback(message, addr):
        print(f"🧪 Callback teste - Mensagem: {message}, Endereço: {addr}")
        return {"status": "received", "node_id": "test_handler"}
    
    # Cria handler de teste
    handler = NetworkHandler("test_node", 9999, test_callback)
    
    try:
        # Inicia servidor
        handler.start_server()
        
        print("🚀 NetworkHandler em teste. Pressione Ctrl+C para parar.")
        
        # Mantém rodando
        while handler.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Teste interrompido")
    finally:
        handler.stop_server()

if __name__ == "__main__":
    main()
