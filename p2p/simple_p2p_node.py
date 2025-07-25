#!/usr/bin/env python3
"""
Simple P2P Node - Versão melhorada do sistema original
=====================================================

Implementação simples e robusta de nó P2P baseada no código fornecido,
com melhorias para integração com o sistema de trading fractal.
"""

import socket
import threading
import pickle
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict


@dataclass
class TradingMessage:
    """Mensagem de trading para troca entre nós."""
    msg_type: str  # 'fractal_pattern', 'trading_signal', 'market_data'
    sender_id: str
    timestamp: float
    symbol: str
    data: Dict[str, Any]
    message_id: str = None
    
    def __post_init__(self):
        if self.message_id is None:
            self.message_id = f"{self.sender_id}_{int(time.time() * 1000)}"


class SimpleP2PNode:
    """
    Nó P2P simples e melhorado para sistema de trading fractal.
    
    Baseado no código original com as seguintes melhorias:
    - Descoberta automática de peers
    - Tratamento robusto de erros
    - Sistema de mensagens estruturadas
    - Logging detalhado
    - Tolerance a falhas de rede
    """
    
    def __init__(self, host='localhost', port=5000, node_id=None):
        # Configuração básica
        self.host = host
        self.port = port
        self.node_id = node_id or f"trader_{port}_{int(time.time() % 10000)}"
        
        # Networking
        self.peers = set()  # (host, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
        
        # Data storage
        self.received_messages: List[TradingMessage] = []
        self.fractal_patterns: List[Dict] = []
        self.trading_signals: List[Dict] = []
        
        # Threading
        self.server_thread = None
        self.discovery_thread = None
        
        # Logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(f"P2PNode-{self.node_id}")
        
        # Bind do socket
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            self.logger.info(f"Nó P2P criado: {self.node_id} em {self.host}:{self.port}")
        except Exception as e:
            self.logger.error(f"Erro ao criar nó: {e}")
            raise

    def handle_client(self, conn, addr):
        """Tratar cliente conectado - versão melhorada."""
        try:
            # Receber dados com timeout
            conn.settimeout(30)
            raw_data = conn.recv(8192)  # Buffer maior
            
            if raw_data:
                try:
                    # Tentar deserializar como TradingMessage primeiro
                    message = pickle.loads(raw_data)
                    
                    if isinstance(message, TradingMessage):
                        self.process_trading_message(message, addr)
                        response = f"ACK_TRADING: {message.message_id}"
                    else:
                        # Compatibilidade com mensagens simples
                        self.logger.info(f"Mensagem simples de {addr}: {message}")
                        response = f"ACK: {message}"
                    
                    # Enviar resposta
                    conn.send(pickle.dumps(response))
                    
                except Exception as e:
                    self.logger.error(f"Erro ao processar mensagem de {addr}: {e}")
                    conn.send(pickle.dumps(f"ERROR: {str(e)}"))
            
            # Adicionar peer se não conhecido
            if addr[0] != self.host or addr[1] != self.port:
                self.peers.add((addr[0], addr[1]))
                self.logger.info(f"Peer adicionado: {addr[0]}:{addr[1]}")
                
        except socket.timeout:
            self.logger.warning(f"Timeout na conexão com {addr}")
        except Exception as e:
            self.logger.error(f"Erro no handle_client: {e}")
        finally:
            conn.close()

    def process_trading_message(self, message: TradingMessage, sender_addr):
        """Processar mensagem de trading estruturada."""
        try:
            self.received_messages.append(message)
            
            # Processar baseado no tipo
            if message.msg_type == 'fractal_pattern':
                self.fractal_patterns.append(message.data)
                self.logger.info(f"Padrão fractal recebido: {message.symbol} - {message.data.get('pattern_type', 'unknown')}")
                
            elif message.msg_type == 'trading_signal':
                self.trading_signals.append(message.data)
                action = message.data.get('action', 'UNKNOWN')
                confidence = message.data.get('confidence', 0)
                self.logger.info(f"Sinal de trading: {message.symbol} - {action} (confiança: {confidence:.2f})")
                
            elif message.msg_type == 'market_data':
                self.logger.info(f"Dados de mercado: {message.symbol} - {len(message.data)} pontos")
                
            else:
                self.logger.warning(f"Tipo de mensagem desconhecido: {message.msg_type}")
                
        except Exception as e:
            self.logger.error(f"Erro ao processar trading message: {e}")

    def start_server(self):
        """Iniciar servidor - versão melhorada."""
        if self.running:
            self.logger.warning("Servidor já está rodando")
            return True
        
        try:
            self.running = True
            
            # Thread do servidor
            self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
            self.server_thread.start()
            
            # Thread de descoberta automática
            self.discovery_thread = threading.Thread(target=self._discovery_loop, daemon=True)
            self.discovery_thread.start()
            
            self.logger.info(f"Servidor P2P iniciado em {self.host}:{self.port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao iniciar servidor: {e}")
            self.running = False
            return False

    def _server_loop(self):
        """Loop principal do servidor."""
        while self.running:
            try:
                conn, addr = self.server.accept()
                self.logger.debug(f"Nova conexão de {addr}")
                
                # Thread para cada cliente
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(conn, addr), 
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    self.logger.error(f"Erro no server loop: {e}")

    def _discovery_loop(self):
        """Loop de descoberta automática de peers."""
        while self.running:
            try:
                # Tentar conectar com portas próximas
                base_port = self.port
                for offset in [-2, -1, 1, 2]:
                    test_port = base_port + offset
                    if 1024 <= test_port <= 65535 and test_port != self.port:
                        self.try_connect_peer(self.host, test_port)
                
                # Tentar outros IPs na rede local (opcional)
                # for ip_suffix in range(2, 10):
                #     test_ip = f"192.168.1.{ip_suffix}"
                #     self.try_connect_peer(test_ip, self.port)
                
                time.sleep(30)  # Descoberta a cada 30 segundos
                
            except Exception as e:
                self.logger.error(f"Erro na descoberta de peers: {e}")

    def try_connect_peer(self, peer_host: str, peer_port: int) -> bool:
        """Tentar conectar com um peer."""
        if (peer_host, peer_port) in self.peers:
            return True
            
        try:
            # Ping simples
            ping_msg = TradingMessage(
                msg_type='ping',
                sender_id=self.node_id,
                timestamp=time.time(),
                symbol='SYSTEM',
                data={'message': 'discovery_ping'}
            )
            
            success = self.send_to_peer(peer_host, peer_port, ping_msg)
            if success:
                self.peers.add((peer_host, peer_port))
                self.logger.info(f"Peer descoberto e adicionado: {peer_host}:{peer_port}")
                return True
                
        except Exception as e:
            self.logger.debug(f"Falha ao conectar com {peer_host}:{peer_port}: {e}")
            
        return False

    def send_to_peer(self, peer_host: str, peer_port: int, message) -> bool:
        """Enviar mensagem para peer específico - versão robusta."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)  # Timeout de 10 segundos
                s.connect((peer_host, peer_port))
                
                # Serializar e enviar
                serialized = pickle.dumps(message)
                s.send(serialized)
                
                # Receber ACK
                ack_data = s.recv(4096)
                ack = pickle.loads(ack_data)
                
                self.logger.debug(f"ACK de {peer_host}:{peer_port}: {ack}")
                return True
                
        except Exception as e:
            self.logger.warning(f"Erro ao enviar para {peer_host}:{peer_port}: {e}")
            # Remover peer se falhou
            self.peers.discard((peer_host, peer_port))
            return False

    def broadcast_message(self, message) -> Dict[str, bool]:
        """Enviar mensagem para todos os peers."""
        results = {}
        
        if not self.peers:
            self.logger.warning("Nenhum peer conectado para broadcast")
            return results
        
        for peer_host, peer_port in self.peers.copy():
            success = self.send_to_peer(peer_host, peer_port, message)
            results[f"{peer_host}:{peer_port}"] = success
            
        success_count = sum(results.values())
        self.logger.info(f"Broadcast: {success_count}/{len(self.peers)} peers alcançados")
        
        return results

    def send_fractal_pattern(self, symbol: str, pattern_data: Dict[str, Any]) -> Dict[str, bool]:
        """Enviar padrão fractal para a rede."""
        message = TradingMessage(
            msg_type='fractal_pattern',
            sender_id=self.node_id,
            timestamp=time.time(),
            symbol=symbol,
            data=pattern_data
        )
        
        self.logger.info(f"Enviando padrão fractal: {symbol}")
        return self.broadcast_message(message)

    def send_trading_signal(self, symbol: str, action: str, confidence: float, 
                          price_target: float = 0, reasoning: str = "") -> Dict[str, bool]:
        """Enviar sinal de trading para a rede."""
        signal_data = {
            'action': action,
            'confidence': confidence,
            'price_target': price_target,
            'reasoning': reasoning,
            'timestamp': time.time()
        }
        
        message = TradingMessage(
            msg_type='trading_signal',
            sender_id=self.node_id,
            timestamp=time.time(),
            symbol=symbol,
            data=signal_data
        )
        
        self.logger.info(f"Enviando sinal: {symbol} - {action}")
        return self.broadcast_message(message)

    def send_market_data(self, symbol: str, price_data: List[float]) -> Dict[str, bool]:
        """Enviar dados de mercado para a rede."""
        market_data = {
            'prices': price_data,
            'count': len(price_data),
            'timestamp': time.time()
        }
        
        message = TradingMessage(
            msg_type='market_data',
            sender_id=self.node_id,
            timestamp=time.time(),
            symbol=symbol,
            data=market_data
        )
        
        self.logger.info(f"Enviando dados de mercado: {symbol} ({len(price_data)} pontos)")
        return self.broadcast_message(message)

    def add_peer_manual(self, host: str, port: int) -> bool:
        """Adicionar peer manualmente."""
        return self.try_connect_peer(host, port)

    def get_peer_stats(self) -> Dict[str, Any]:
        """Obter estatísticas dos peers."""
        return {
            'node_id': self.node_id,
            'address': f"{self.host}:{self.port}",
            'peer_count': len(self.peers),
            'peers': list(self.peers),
            'messages_received': len(self.received_messages),
            'fractal_patterns': len(self.fractal_patterns),
            'trading_signals': len(self.trading_signals),
            'running': self.running
        }

    def get_recent_fractals(self, limit: int = 10) -> List[Dict]:
        """Obter padrões fractais recentes."""
        return self.fractal_patterns[-limit:]

    def get_recent_signals(self, limit: int = 10) -> List[Dict]:
        """Obter sinais de trading recentes."""
        return self.trading_signals[-limit:]

    def stop(self):
        """Parar o nó P2P."""
        self.logger.info("Parando nó P2P...")
        self.running = False
        
        try:
            self.server.close()
        except:
            pass
            
        self.logger.info("Nó P2P parado")


def main():
    """Exemplo de uso do nó P2P simples."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Nó P2P Simples para Trading")
    parser.add_argument("--host", default="localhost", help="Host do nó")
    parser.add_argument("--port", type=int, default=5000, help="Porta do nó")
    parser.add_argument("--connect", help="Conectar a peer (host:port)")
    
    args = parser.parse_args()
    
    # Criar nó
    try:
        node = SimpleP2PNode(host=args.host, port=args.port)
    except Exception as e:
        print(f"Erro ao criar nó: {e}")
        sys.exit(1)
    
    # Iniciar servidor
    if not node.start_server():
        print("Erro ao iniciar servidor")
        sys.exit(1)
    
    # Conectar a peer se especificado
    if args.connect:
        try:
            host, port = args.connect.split(":")
            if node.add_peer_manual(host, int(port)):
                print(f"Conectado ao peer: {host}:{port}")
            else:
                print(f"Falha ao conectar com: {host}:{port}")
        except ValueError:
            print("Formato inválido para --connect. Use host:port")
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                   🔗 NÓ P2P SIMPLES 🔗                      ║
║                                                              ║
║  Node ID: {node.node_id:49} ║
║  Endereço: {args.host}:{args.port:43} ║
║                                                              ║
║  Comandos:                                                   ║
║  stats    - Ver estatísticas                                ║
║  peers    - Listar peers                                    ║
║  connect  - Conectar a peer                                 ║
║  fractal  - Enviar padrão fractal de teste                 ║
║  signal   - Enviar sinal de trading de teste               ║
║  quit     - Sair                                            ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        while True:
            cmd = input("\n> ").strip().lower()
            
            if cmd == "quit":
                break
                
            elif cmd == "stats":
                stats = node.get_peer_stats()
                print(json.dumps(stats, indent=2))
                
            elif cmd == "peers":
                print(f"\nPeers conectados ({len(node.peers)}):")
                for i, (host, port) in enumerate(node.peers, 1):
                    print(f"  {i}. {host}:{port}")
                    
            elif cmd == "connect":
                peer = input("Peer (host:port): ").strip()
                try:
                    host, port = peer.split(":")
                    if node.add_peer_manual(host, int(port)):
                        print(f"✅ Conectado: {host}:{port}")
                    else:
                        print(f"❌ Falha ao conectar: {host}:{port}")
                except ValueError:
                    print("❌ Formato inválido. Use host:port")
                    
            elif cmd == "fractal":
                # Enviar padrão fractal de teste
                pattern = {
                    'pattern_type': 'triangle_ascending',
                    'confidence': 0.85,
                    'hurst_exponent': 0.72,
                    'box_dimension': 1.35,
                    'prediction': [100, 102, 105, 108, 110]
                }
                
                results = node.send_fractal_pattern("BTCUSD", pattern)
                print(f"✅ Padrão fractal enviado para {sum(results.values())} peers")
                
            elif cmd == "signal":
                # Enviar sinal de trading de teste
                results = node.send_trading_signal(
                    symbol="BTCUSD",
                    action="BUY",
                    confidence=0.78,
                    price_target=45000,
                    reasoning="Padrão fractal ascendente detectado"
                )
                print(f"✅ Sinal enviado para {sum(results.values())} peers")
                
            else:
                print("❌ Comando não reconhecido")
                
    except KeyboardInterrupt:
        print("\n")
    finally:
        node.stop()
        print("👋 Nó finalizado")


if __name__ == "__main__":
    main()
