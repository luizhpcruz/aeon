#!/usr/bin/env python3
"""
Enhanced P2P Node - Versão aprimorada do p2p_node.py
====================================================

Implementação robusta de nó P2P com todas as melhorias recomendadas:
- Tratamento de erros robusto
- Timeouts e retry logic
- Descoberta automática de peers
- Logging detalhado
- Threading seguro
- Graceful shutdown
"""

import socket
import threading
import pickle
import time
import logging
import json
from typing import Dict, Set, Any, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class P2PMessage:
    """Estrutura padronizada para mensagens P2P."""
    message_id: str
    message_type: str
    sender_id: str
    timestamp: float
    payload: Dict[str, Any]
    version: str = "1.0"


class EnhancedP2PNode:
    """
    Nó P2P aprimorado com recursos empresariais.
    
    Melhorias implementadas:
    - Sistema de timeouts e retries
    - Descoberta automática de peers
    - Heartbeat para verificar peers ativos
    - Logging estruturado
    - Threading thread-safe
    - Graceful shutdown
    - Validação de mensagens
    - Estatísticas de rede
    """
    
    def __init__(self, host='localhost', port=5000, node_id=None):
        # Configuração básica
        self.host = host
        self.port = port
        self.node_id = node_id or f"node_{uuid.uuid4().hex[:8]}"
        
        # Threading e controle
        self.running = False
        self.peers: Set[tuple] = set()  # Thread-safe set
        self.peers_lock = threading.RLock()
        self.connections_active = 0
        self.connections_lock = threading.Lock()
        
        # Socket configuration
        self.server_socket = None
        self.socket_timeout = 30.0
        self.retry_attempts = 3
        self.retry_delay = 2.0
        
        # Message handling
        self.message_handlers: Dict[str, Callable] = {}
        self.message_queue = []
        self.message_queue_lock = threading.Lock()
        
        # Statistics
        self.stats = {
            'messages_sent': 0,
            'messages_received': 0,
            'connections_accepted': 0,
            'connection_errors': 0,
            'peer_discoveries': 0,
            'start_time': None
        }
        
        # Setup logging
        self.setup_logging()
        
        # Register default message handlers
        self.register_message_handler('ping', self.handle_ping)
        self.register_message_handler('pong', self.handle_pong)
        self.register_message_handler('peer_discovery', self.handle_peer_discovery)
        
        self.logger.info(f"Enhanced P2P Node created: {self.node_id} on {self.host}:{self.port}")

    def setup_logging(self):
        """Configurar sistema de logging."""
        self.logger = logging.getLogger(f"P2PNode-{self.node_id}")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def register_message_handler(self, message_type: str, handler: Callable):
        """Registrar handler para tipo específico de mensagem."""
        self.message_handlers[message_type] = handler
        self.logger.debug(f"Registered handler for message type: {message_type}")

    def create_server_socket(self) -> bool:
        """Criar e configurar socket do servidor."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Configurar opções do socket
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.settimeout(self.socket_timeout)
            
            # Bind e listen
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)  # Increased backlog
            
            self.logger.info(f"Server socket created and listening on {self.host}:{self.port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create server socket: {e}")
            return False

    def start_server(self) -> bool:
        """Iniciar servidor P2P com todos os serviços."""
        if self.running:
            self.logger.warning("Server is already running")
            return True
            
        if not self.create_server_socket():
            return False
            
        self.running = True
        self.stats['start_time'] = time.time()
        
        try:
            # Thread principal do servidor
            self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
            self.server_thread.start()
            
            # Thread de descoberta de peers
            self.discovery_thread = threading.Thread(target=self._peer_discovery_loop, daemon=True)
            self.discovery_thread.start()
            
            # Thread de heartbeat
            self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
            self.heartbeat_thread.start()
            
            # Thread de limpeza
            self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
            self.cleanup_thread.start()
            
            self.logger.info("P2P Server started successfully with all services")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start server: {e}")
            self.running = False
            return False

    def _server_loop(self):
        """Loop principal do servidor."""
        self.logger.info("Server loop started")
        
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                self.stats['connections_accepted'] += 1
                
                # Adicionar peer automaticamente
                with self.peers_lock:
                    self.peers.add((addr[0], addr[1]))
                
                self.logger.debug(f"New connection from {addr}")
                
                # Thread para tratar cliente
                client_thread = threading.Thread(
                    target=self._handle_client_connection, 
                    args=(conn, addr), 
                    daemon=True
                )
                client_thread.start()
                
            except socket.timeout:
                continue  # Normal timeout, continue loop
            except Exception as e:
                if self.running:
                    self.logger.error(f"Error in server loop: {e}")
                    self.stats['connection_errors'] += 1

    def _handle_client_connection(self, conn, addr):
        """Tratar conexão de cliente com timeout e validação."""
        try:
            with self.connections_lock:
                self.connections_active += 1
                
            conn.settimeout(self.socket_timeout)
            
            # Receber dados
            data = self._receive_complete_message(conn)
            if not data:
                return
                
            # Deserializar mensagem
            try:
                message = pickle.loads(data)
                self.stats['messages_received'] += 1
                
                # Validar estrutura da mensagem
                if self._validate_message(message):
                    response = self._process_message(message, addr)
                else:
                    response = self._create_error_response("Invalid message format")
                    
            except (pickle.PickleError, Exception) as e:
                self.logger.warning(f"Failed to deserialize message from {addr}: {e}")
                response = self._create_error_response(f"Deserialization error: {str(e)}")
            
            # Enviar resposta
            try:
                response_data = pickle.dumps(response)
                conn.send(response_data)
                self.logger.debug(f"Response sent to {addr}")
            except Exception as e:
                self.logger.error(f"Failed to send response to {addr}: {e}")
                
        except socket.timeout:
            self.logger.warning(f"Connection timeout with {addr}")
        except Exception as e:
            self.logger.error(f"Error handling client {addr}: {e}")
        finally:
            with self.connections_lock:
                self.connections_active -= 1
            conn.close()

    def _receive_complete_message(self, conn) -> Optional[bytes]:
        """Receber mensagem completa, tratando mensagens grandes."""
        try:
            # Primeiro, receber o tamanho da mensagem (4 bytes)
            size_data = conn.recv(4)
            if len(size_data) < 4:
                return None
                
            message_size = int.from_bytes(size_data, byteorder='big')
            
            # Verificar tamanho máximo (proteção contra DoS)
            max_message_size = 1024 * 1024  # 1MB
            if message_size > max_message_size:
                self.logger.warning(f"Message too large: {message_size} bytes")
                return None
            
            # Receber mensagem completa
            received_data = b''
            while len(received_data) < message_size:
                chunk = conn.recv(min(4096, message_size - len(received_data)))
                if not chunk:
                    break
                received_data += chunk
                
            return received_data if len(received_data) == message_size else None
            
        except Exception as e:
            self.logger.error(f"Error receiving message: {e}")
            return None

    def _validate_message(self, message) -> bool:
        """Validar estrutura da mensagem."""
        if isinstance(message, P2PMessage):
            return all([
                hasattr(message, 'message_id'),
                hasattr(message, 'message_type'),
                hasattr(message, 'sender_id'),
                hasattr(message, 'timestamp'),
                hasattr(message, 'payload')
            ])
        elif isinstance(message, dict):
            # Compatibilidade com mensagens simples
            return True
        elif isinstance(message, str):
            # Mensagens de texto simples
            return True
        else:
            return False

    def _process_message(self, message, sender_addr) -> Any:
        """Processar mensagem recebida."""
        try:
            if isinstance(message, P2PMessage):
                # Mensagem estruturada
                handler = self.message_handlers.get(message.message_type)
                if handler:
                    return handler(message, sender_addr)
                else:
                    self.logger.debug(f"No handler for message type: {message.message_type}")
                    return self._create_ack_response(message.message_id)
            else:
                # Mensagem simples (compatibilidade)
                self.logger.info(f"Simple message from {sender_addr}: {message}")
                return f"ACK: {message}"
                
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return self._create_error_response(str(e))

    def _create_ack_response(self, message_id: str) -> P2PMessage:
        """Criar resposta de ACK."""
        return P2PMessage(
            message_id=str(uuid.uuid4()),
            message_type="ack",
            sender_id=self.node_id,
            timestamp=time.time(),
            payload={"ack_for": message_id, "status": "received"}
        )

    def _create_error_response(self, error_msg: str) -> P2PMessage:
        """Criar resposta de erro."""
        return P2PMessage(
            message_id=str(uuid.uuid4()),
            message_type="error",
            sender_id=self.node_id,
            timestamp=time.time(),
            payload={"error": error_msg}
        )

    def send_to_peer(self, peer_host: str, peer_port: int, message: Any) -> bool:
        """Enviar mensagem para peer com retry logic."""
        for attempt in range(self.retry_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(self.socket_timeout)
                    s.connect((peer_host, peer_port))
                    
                    # Serializar mensagem
                    if not isinstance(message, (P2PMessage, dict, str)):
                        message = str(message)
                        
                    message_data = pickle.dumps(message)
                    message_size = len(message_data)
                    
                    # Enviar tamanho primeiro, depois dados
                    s.send(message_size.to_bytes(4, byteorder='big'))
                    s.send(message_data)
                    
                    # Receber resposta
                    response_data = self._receive_complete_message(s)
                    if response_data:
                        response = pickle.loads(response_data)
                        self.logger.debug(f"Response from {peer_host}:{peer_port}: {response}")
                    
                    self.stats['messages_sent'] += 1
                    return True
                    
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed to send to {peer_host}:{peer_port}: {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.retry_delay)
                else:
                    # Remove peer after all attempts failed
                    with self.peers_lock:
                        self.peers.discard((peer_host, peer_port))
                    self.stats['connection_errors'] += 1
                    
        return False

    def broadcast_message(self, message: Any) -> Dict[str, bool]:
        """Enviar mensagem para todos os peers."""
        results = {}
        
        with self.peers_lock:
            peers_copy = self.peers.copy()
            
        for peer_host, peer_port in peers_copy:
            success = self.send_to_peer(peer_host, peer_port, message)
            results[f"{peer_host}:{peer_port}"] = success
            
        success_count = sum(results.values())
        self.logger.info(f"Broadcast sent to {len(peers_copy)} peers, {success_count} successful")
        
        return results

    def add_peer(self, host: str, port: int) -> bool:
        """Adicionar peer manualmente."""
        if (host, port) == (self.host, self.port):
            return False  # Don't add self
            
        # Test connection first
        test_message = P2PMessage(
            message_id=str(uuid.uuid4()),
            message_type="ping",
            sender_id=self.node_id,
            timestamp=time.time(),
            payload={"test": "connection"}
        )
        
        if self.send_to_peer(host, port, test_message):
            with self.peers_lock:
                self.peers.add((host, port))
            self.logger.info(f"Peer added: {host}:{port}")
            return True
        else:
            self.logger.warning(f"Failed to add peer: {host}:{port}")
            return False

    def _peer_discovery_loop(self):
        """Loop de descoberta automática de peers."""
        self.logger.info("Peer discovery loop started")
        
        while self.running:
            try:
                # Descobrir peers em portas próximas
                base_port = self.port
                for offset in [-2, -1, 1, 2]:
                    test_port = base_port + offset
                    if 1024 <= test_port <= 65535:
                        self._try_discover_peer(self.host, test_port)
                
                time.sleep(30)  # Discovery every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in peer discovery: {e}")
                time.sleep(60)

    def _try_discover_peer(self, host: str, port: int):
        """Tentar descobrir um peer específico."""
        if (host, port) not in self.peers and (host, port) != (self.host, self.port):
            discovery_message = P2PMessage(
                message_id=str(uuid.uuid4()),
                message_type="peer_discovery",
                sender_id=self.node_id,
                timestamp=time.time(),
                payload={"discovering": True}
            )
            
            if self.send_to_peer(host, port, discovery_message):
                with self.peers_lock:
                    self.peers.add((host, port))
                self.stats['peer_discoveries'] += 1
                self.logger.info(f"Discovered new peer: {host}:{port}")

    def _heartbeat_loop(self):
        """Loop de heartbeat para verificar peers ativos."""
        self.logger.info("Heartbeat loop started")
        
        while self.running:
            try:
                with self.peers_lock:
                    peers_to_check = self.peers.copy()
                
                for peer_host, peer_port in peers_to_check:
                    ping_message = P2PMessage(
                        message_id=str(uuid.uuid4()),
                        message_type="ping",
                        sender_id=self.node_id,
                        timestamp=time.time(),
                        payload={"heartbeat": True}
                    )
                    
                    if not self.send_to_peer(peer_host, peer_port, ping_message):
                        with self.peers_lock:
                            self.peers.discard((peer_host, peer_port))
                        self.logger.info(f"Removed inactive peer: {peer_host}:{peer_port}")
                
                time.sleep(60)  # Heartbeat every minute
                
            except Exception as e:
                self.logger.error(f"Error in heartbeat loop: {e}")
                time.sleep(120)

    def _cleanup_loop(self):
        """Loop de limpeza de recursos."""
        while self.running:
            try:
                # Limpar mensagens antigas da queue
                with self.message_queue_lock:
                    current_time = time.time()
                    self.message_queue = [
                        msg for msg in self.message_queue 
                        if current_time - msg.get('timestamp', 0) < 3600  # Keep for 1 hour
                    ]
                
                time.sleep(300)  # Cleanup every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
                time.sleep(600)

    # Message Handlers
    def handle_ping(self, message: P2PMessage, sender_addr) -> P2PMessage:
        """Tratar mensagem de ping."""
        self.logger.debug(f"Ping received from {sender_addr}")
        return P2PMessage(
            message_id=str(uuid.uuid4()),
            message_type="pong",
            sender_id=self.node_id,
            timestamp=time.time(),
            payload={"pong_for": message.message_id}
        )

    def handle_pong(self, message: P2PMessage, sender_addr) -> P2PMessage:
        """Tratar mensagem de pong."""
        self.logger.debug(f"Pong received from {sender_addr}")
        return self._create_ack_response(message.message_id)

    def handle_peer_discovery(self, message: P2PMessage, sender_addr) -> P2PMessage:
        """Tratar descoberta de peer."""
        self.logger.info(f"Peer discovery from {sender_addr}")
        
        # Add the discovering peer
        with self.peers_lock:
            self.peers.add((sender_addr[0], sender_addr[1]))
        
        return P2PMessage(
            message_id=str(uuid.uuid4()),
            message_type="peer_discovery_response",
            sender_id=self.node_id,
            timestamp=time.time(),
            payload={
                "peer_count": len(self.peers),
                "known_peers": list(self.peers)[:10]  # Limit response size
            }
        )

    def get_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do nó."""
        uptime = time.time() - self.stats['start_time'] if self.stats['start_time'] else 0
        
        return {
            'node_id': self.node_id,
            'address': f"{self.host}:{self.port}",
            'running': self.running,
            'uptime_seconds': uptime,
            'peer_count': len(self.peers),
            'active_connections': self.connections_active,
            'messages_sent': self.stats['messages_sent'],
            'messages_received': self.stats['messages_received'],
            'connections_accepted': self.stats['connections_accepted'],
            'connection_errors': self.stats['connection_errors'],
            'peer_discoveries': self.stats['peer_discoveries'],
            'peers': list(self.peers)
        }

    def stop(self):
        """Parar nó P2P com graceful shutdown."""
        self.logger.info("Stopping P2P Node...")
        self.running = False
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        # Wait for active connections to finish
        timeout = 10
        start_time = time.time()
        while self.connections_active > 0 and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        self.logger.info(f"P2P Node stopped. Final stats: {self.get_stats()}")


def main():
    """Exemplo de uso do nó P2P aprimorado."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Enhanced P2P Node")
    parser.add_argument("--host", default="localhost", help="Host address")
    parser.add_argument("--port", type=int, default=5000, help="Port number")
    parser.add_argument("--peers", nargs="*", help="Initial peers (host:port)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create and start node
    node = EnhancedP2PNode(host=args.host, port=args.port)
    
    if not node.start_server():
        print("Failed to start P2P node")
        sys.exit(1)
    
    # Add initial peers
    if args.peers:
        for peer in args.peers:
            try:
                host, port = peer.split(":")
                node.add_peer(host, int(port))
            except ValueError:
                print(f"Invalid peer format: {peer}")
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                 🚀 ENHANCED P2P NODE 🚀                     ║
║                                                              ║
║  Node ID: {node.node_id:49} ║
║  Address: {args.host}:{args.port:44} ║
║  Features: Auto-discovery, Heartbeat, Retry Logic           ║
║                                                              ║
║  Commands:                                                   ║
║  stats    - Show node statistics                            ║
║  peers    - List connected peers                            ║
║  send     - Send test message                               ║
║  broadcast - Broadcast test message                         ║
║  quit     - Stop node                                       ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        while True:
            cmd = input("\n> ").strip().lower()
            
            if cmd == "quit":
                break
            elif cmd == "stats":
                stats = node.get_stats()
                print(json.dumps(stats, indent=2))
            elif cmd == "peers":
                with node.peers_lock:
                    peers = list(node.peers)
                print(f"Connected peers ({len(peers)}):")
                for i, (host, port) in enumerate(peers, 1):
                    print(f"  {i}. {host}:{port}")
            elif cmd == "send":
                if node.peers:
                    peer = list(node.peers)[0]
                    test_msg = P2PMessage(
                        message_id=str(uuid.uuid4()),
                        message_type="test",
                        sender_id=node.node_id,
                        timestamp=time.time(),
                        payload={"message": "Hello from enhanced node!"}
                    )
                    success = node.send_to_peer(peer[0], peer[1], test_msg)
                    print(f"Message sent: {'✅' if success else '❌'}")
                else:
                    print("No peers available")
            elif cmd == "broadcast":
                test_msg = P2PMessage(
                    message_id=str(uuid.uuid4()),
                    message_type="broadcast_test",
                    sender_id=node.node_id,
                    timestamp=time.time(),
                    payload={"message": "Broadcast from enhanced node!"}
                )
                results = node.broadcast_message(test_msg)
                print(f"Broadcast results: {results}")
            else:
                print("Unknown command")
                
    except KeyboardInterrupt:
        print("\n")
    finally:
        node.stop()
        print("Enhanced P2P Node stopped")


if __name__ == "__main__":
    main()
