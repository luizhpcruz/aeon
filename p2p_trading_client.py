#!/usr/bin/env python3
"""
P2P Trading Client - Cliente para conectar ao servidor P2P
=========================================================

Cliente que se conecta ao servidor P2P de trading e:
- Envia dados de análise fractal
- Recebe sinais da rede
- Mantém conexão persistente
- Contribui para a rede distribuída
"""

import socket
import pickle
import time
import threading
import json
import random
from datetime import datetime
from typing import Dict, List, Optional
import uuid


class P2PTradingClient:
    """Cliente P2P para conectar ao servidor de trading."""
    
    def __init__(self, server_host='localhost', server_port=8888, client_id=None):
        self.server_host = server_host
        self.server_port = server_port
        self.client_id = client_id or f"client_{uuid.uuid4().hex[:8]}"
        
        self.connected = False
        self.running = False
        self.socket = None
        
        # Threads
        self.heartbeat_thread = None
        self.data_sender_thread = None
        
        print(f"Cliente P2P criado: {self.client_id}")
    
    def connect_to_server(self) -> bool:
        """Conectar ao servidor P2P."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(30)
            self.socket.connect((self.server_host, self.server_port))
            
            # Registrar no servidor
            registration_msg = {
                'type': 'register',
                'node_id': self.client_id,
                'capabilities': ['fractal_analysis', 'trading_signals'],
                'version': '1.0',
                'timestamp': time.time()
            }
            
            response = self.send_message(registration_msg)
            if response and response.get('status') == 'registered':
                self.connected = True
                self.running = True
                
                print(f"✅ Conectado ao servidor {self.server_host}:{self.server_port}")
                print(f"📊 {response.get('welcome_message', 'Bem-vindo!')}")
                
                # Iniciar threads de serviço
                self.start_background_services()
                return True
            else:
                print(f"❌ Falha no registro: {response}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def send_message(self, message: Dict) -> Optional[Dict]:
        """Enviar mensagem para o servidor."""
        try:
            if not self.socket:
                return None
                
            # Enviar mensagem
            data = pickle.dumps(message)
            self.socket.send(data)
            
            # Receber resposta
            response_data = self.socket.recv(8192)
            response = pickle.loads(response_data)
            
            return response
            
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            self.connected = False
            return None
    
    def send_trading_signal(self, symbol: str, action: str, confidence: float, reasoning: str = ""):
        """Enviar sinal de trading para a rede."""
        signal_msg = {
            'type': 'trading_signal',
            'node_id': self.client_id,
            'symbol': symbol,
            'confidence': confidence,
            'data': {
                'action': action,
                'reasoning': reasoning,
                'timestamp': time.time(),
                'source': 'fractal_analysis'
            }
        }
        
        response = self.send_message(signal_msg)
        if response and response.get('status') == 'stored':
            print(f"📤 Sinal enviado: {symbol} - {action} (ID: {response.get('signal_id')})")
            return True
        else:
            print(f"❌ Falha ao enviar sinal: {response}")
            return False
    
    def send_fractal_pattern(self, symbol: str, pattern_type: str, hurst: float, box_dim: float):
        """Enviar padrão fractal para a rede."""
        pattern_msg = {
            'type': 'fractal_pattern',
            'node_id': self.client_id,
            'symbol': symbol,
            'confidence': min(abs(hurst - 0.5) * 2, 1.0),  # Converter Hurst para confiança
            'data': {
                'pattern_type': pattern_type,
                'hurst_exponent': hurst,
                'box_dimension': box_dim,
                'analysis_time': time.time(),
                'timeframe': '1h'
            }
        }
        
        response = self.send_message(pattern_msg)
        if response and response.get('status') == 'stored':
            print(f"🔮 Padrão fractal enviado: {symbol} - {pattern_type} (ID: {response.get('pattern_id')})")
            return True
        else:
            print(f"❌ Falha ao enviar padrão: {response}")
            return False
    
    def send_market_data(self, symbol: str, prices: List[float]):
        """Enviar dados de mercado para a rede."""
        market_msg = {
            'type': 'market_data',
            'node_id': self.client_id,
            'symbol': symbol,
            'data': {
                'prices': prices,
                'count': len(prices),
                'timestamp': time.time(),
                'source': 'manual_input'
            }
        }
        
        response = self.send_message(market_msg)
        if response and response.get('status') == 'stored':
            print(f"📊 Dados de mercado enviados: {symbol} ({len(prices)} pontos)")
            return True
        else:
            print(f"❌ Falha ao enviar dados: {response}")
            return False
    
    def get_network_stats(self) -> Optional[Dict]:
        """Obter estatísticas da rede."""
        stats_msg = {
            'type': 'get_stats',
            'node_id': self.client_id
        }
        
        response = self.send_message(stats_msg)
        if response and response.get('status') == 'success':
            return response
        else:
            print(f"❌ Falha ao obter estatísticas: {response}")
            return None
    
    def start_background_services(self):
        """Iniciar serviços em background."""
        # Thread de heartbeat
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
        
        # Thread de envio automático de dados
        self.data_sender_thread = threading.Thread(target=self._auto_data_sender, daemon=True)
        self.data_sender_thread.start()
    
    def _heartbeat_loop(self):
        """Loop de heartbeat para manter conexão."""
        while self.running and self.connected:
            try:
                # Ping simples
                ping_msg = {
                    'type': 'ping',
                    'node_id': self.client_id,
                    'timestamp': time.time()
                }
                
                response = self.send_message(ping_msg)
                if not response:
                    print("⚠️ Heartbeat falhou - conexão perdida")
                    self.connected = False
                    break
                
                time.sleep(60)  # Heartbeat a cada minuto
                
            except Exception as e:
                print(f"❌ Erro no heartbeat: {e}")
                self.connected = False
                break
    
    def _auto_data_sender(self):
        """Envio automático de dados simulados."""
        symbols = ['BTCUSD', 'ETHUSD', 'ADAUSD', 'SOLUSD', 'DOTUSD']
        
        while self.running and self.connected:
            try:
                # Simular análise fractal
                symbol = random.choice(symbols)
                
                # Gerar dados fractais simulados
                hurst = random.uniform(0.3, 0.8)
                box_dim = random.uniform(1.2, 1.8)
                
                pattern_types = ['trend_continuation', 'reversal_pattern', 'breakout', 'consolidation']
                pattern_type = random.choice(pattern_types)
                
                # Enviar padrão fractal
                self.send_fractal_pattern(symbol, pattern_type, hurst, box_dim)
                
                # Gerar sinal de trading baseado no Hurst
                if hurst > 0.6:
                    action = 'BUY'
                    reasoning = f"Tendência persistente detectada (H={hurst:.3f})"
                elif hurst < 0.4:
                    action = 'SELL'
                    reasoning = f"Reversão provável (H={hurst:.3f})"
                else:
                    action = 'HOLD'
                    reasoning = f"Movimento lateral (H={hurst:.3f})"
                
                confidence = min(abs(hurst - 0.5) * 2, 1.0)
                
                # Enviar sinal
                self.send_trading_signal(symbol, action, confidence, reasoning)
                
                # Aguardar antes do próximo envio
                time.sleep(random.randint(30, 120))  # 30s a 2min
                
            except Exception as e:
                print(f"❌ Erro no envio automático: {e}")
                time.sleep(60)
    
    def disconnect(self):
        """Desconectar do servidor."""
        self.running = False
        self.connected = False
        
        if self.socket:
            try:
                # Enviar mensagem de desconexão
                disconnect_msg = {
                    'type': 'disconnect',
                    'node_id': self.client_id,
                    'timestamp': time.time()
                }
                self.send_message(disconnect_msg)
            except:
                pass
            
            self.socket.close()
        
        print(f"🔌 Cliente {self.client_id} desconectado")


def run_interactive_client():
    """Executar cliente em modo interativo."""
    print("🔗 Iniciando cliente P2P interativo...")
    
    # Conectar ao servidor
    client = P2PTradingClient()
    
    if not client.connect_to_server():
        print("❌ Falha ao conectar ao servidor")
        return
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                🤖 CLIENTE P2P CONECTADO 🤖                  ║
║                                                              ║
║  Cliente ID: {client.client_id:47} ║
║  Servidor: {client.server_host}:{client.server_port:42} ║
║                                                              ║
║  Comandos disponíveis:                                       ║
║  signal <symbol> <action> <confidence> - Enviar sinal       ║
║  pattern <symbol> <type> <hurst> - Enviar padrão           ║
║  market <symbol> <prices...> - Enviar dados mercado        ║
║  stats - Ver estatísticas da rede                          ║
║  auto - Alternar envio automático                          ║
║  quit - Sair                                               ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    auto_mode = True
    print("🤖 Modo automático ATIVADO - enviando dados simulados...")
    
    try:
        while client.connected:
            try:
                cmd = input("\n> ").strip().split()
                
                if not cmd:
                    continue
                
                command = cmd[0].lower()
                
                if command == "quit":
                    break
                    
                elif command == "signal" and len(cmd) >= 4:
                    symbol = cmd[1].upper()
                    action = cmd[2].upper()
                    confidence = float(cmd[3])
                    reasoning = " ".join(cmd[4:]) if len(cmd) > 4 else "Manual input"
                    
                    client.send_trading_signal(symbol, action, confidence, reasoning)
                    
                elif command == "pattern" and len(cmd) >= 4:
                    symbol = cmd[1].upper()
                    pattern_type = cmd[2]
                    hurst = float(cmd[3])
                    box_dim = float(cmd[4]) if len(cmd) > 4 else 1.5
                    
                    client.send_fractal_pattern(symbol, pattern_type, hurst, box_dim)
                    
                elif command == "market" and len(cmd) >= 3:
                    symbol = cmd[1].upper()
                    prices = [float(p) for p in cmd[2:]]
                    
                    client.send_market_data(symbol, prices)
                    
                elif command == "stats":
                    stats = client.get_network_stats()
                    if stats:
                        print("\n📊 ESTATÍSTICAS DA REDE:")
                        network_stats = stats.get('network_stats', {})
                        print(f"   Total de nós: {network_stats.get('total_nodes', 0)}")
                        print(f"   Conexões ativas: {network_stats.get('active_connections', 0)}")
                        print(f"   Sinais hoje: {network_stats.get('trading_signals_today', 0)}")
                        print(f"   Padrões hoje: {network_stats.get('fractal_patterns_today', 0)}")
                        
                        top_symbols = stats.get('top_symbols', [])
                        if top_symbols:
                            print("\n🔥 Top Símbolos:")
                            for i, symbol_data in enumerate(top_symbols[:5], 1):
                                print(f"   {i}. {symbol_data['symbol']} - "
                                      f"{symbol_data['activity_count']} atividades "
                                      f"(conf: {symbol_data['avg_confidence']:.2f})")
                    
                elif command == "auto":
                    auto_mode = not auto_mode
                    status = "ATIVADO" if auto_mode else "DESATIVADO"
                    print(f"🤖 Modo automático {status}")
                    
                else:
                    print("❌ Comando inválido ou parâmetros insuficientes")
                    print("💡 Exemplos:")
                    print("   signal BTCUSD BUY 0.85 Strong uptrend")
                    print("   pattern ETHUSD breakout 0.72")
                    print("   market ADAUSD 0.45 0.46 0.47 0.45")
                    
            except ValueError as e:
                print(f"❌ Erro nos parâmetros: {e}")
            except KeyboardInterrupt:
                break
                
    except KeyboardInterrupt:
        print("\n")
    finally:
        client.disconnect()
        print("👋 Cliente finalizado")


def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description="P2P Trading Client")
    parser.add_argument("--server", default="localhost", help="Servidor P2P")
    parser.add_argument("--port", type=int, default=8888, help="Porta do servidor")
    parser.add_argument("--client-id", help="ID do cliente")
    parser.add_argument("--auto-only", action="store_true", help="Apenas modo automático")
    
    args = parser.parse_args()
    
    if args.auto_only:
        # Modo apenas automático (para deployment)
        client = P2PTradingClient(args.server, args.port, args.client_id)
        
        if client.connect_to_server():
            print(f"🤖 Cliente automático ativo: {client.client_id}")
            try:
                while client.connected:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            finally:
                client.disconnect()
        else:
            print("❌ Falha ao conectar")
    else:
        # Modo interativo
        run_interactive_client()


if __name__ == "__main__":
    main()
