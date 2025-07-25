#!/usr/bin/env python3
"""
P2P Trading Demo - Demonstração do sistema P2P integrado
========================================================

Script para demonstrar o uso do nó P2P com análise fractal.
"""

import sys
import os
import time
import threading
import json
from datetime import datetime

# Adicionar paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai-core'))

try:
    from simple_p2p_node import SimpleP2PNode, TradingMessage
    print("✅ Módulo P2P carregado")
except ImportError as e:
    print(f"❌ Erro ao importar P2P: {e}")
    sys.exit(1)

# Tentar importar módulos de análise fractal
try:
    from fractal import FractalAnalyzer
    from utils import generate_fractal_series, calculate_fractal_metrics
    FRACTAL_AVAILABLE = True
    print("✅ Módulos fractais carregados")
except ImportError as e:
    print(f"⚠️  Módulos fractais não disponíveis: {e}")
    FRACTAL_AVAILABLE = False

try:
    from trading_ai import TradingAI, FractalPredictor
    AI_AVAILABLE = True
    print("✅ Módulos IA carregados")
except ImportError as e:
    print(f"⚠️  Módulos IA não disponíveis: {e}")
    AI_AVAILABLE = False


class FractalP2PTrader:
    """
    Trader que combina análise fractal com comunicação P2P.
    """
    
    def __init__(self, host='localhost', port=5000):
        self.node = SimpleP2PNode(host=host, port=port)
        
        # Componentes opcionais
        self.fractal_analyzer = None
        self.ai_predictor = None
        
        if FRACTAL_AVAILABLE:
            try:
                self.fractal_analyzer = FractalAnalyzer()
                print("✅ Analisador fractal inicializado")
            except Exception as e:
                print(f"⚠️  Erro ao inicializar analisador fractal: {e}")
        
        if AI_AVAILABLE:
            try:
                self.ai_predictor = FractalPredictor()
                print("✅ Preditor IA inicializado")
            except Exception as e:
                print(f"⚠️  Erro ao inicializar preditor IA: {e}")

    def start(self):
        """Iniciar trader P2P."""
        success = self.node.start_server()
        if success:
            print(f"🚀 Trader P2P iniciado: {self.node.node_id}")
            
            # Iniciar loop de análise automática
            analysis_thread = threading.Thread(target=self._analysis_loop, daemon=True)
            analysis_thread.start()
            
        return success

    def _analysis_loop(self):
        """Loop de análise automática."""
        symbols = ["BTCUSD", "ETHUSD", "ADAUSD", "SOLUSD"]
        
        while self.node.running:
            try:
                for symbol in symbols:
                    self.analyze_and_share(symbol)
                    time.sleep(30)  # Análise a cada 30 segundos por símbolo
                    
            except Exception as e:
                print(f"❌ Erro no loop de análise: {e}")
                time.sleep(60)

    def analyze_and_share(self, symbol: str):
        """Analisar símbolo e compartilhar resultados."""
        try:
            print(f"\n📊 Analisando {symbol}...")
            
            # Gerar dados de teste se módulos não disponíveis
            if FRACTAL_AVAILABLE and self.fractal_analyzer:
                # Usar análise fractal real
                analysis_result = self._real_fractal_analysis(symbol)
            else:
                # Usar dados simulados
                analysis_result = self._simulated_analysis(symbol)
            
            # Compartilhar padrão fractal
            if analysis_result.get('fractal_pattern'):
                self.node.send_fractal_pattern(symbol, analysis_result['fractal_pattern'])
            
            # Compartilhar sinal de trading
            if analysis_result.get('trading_signal'):
                signal = analysis_result['trading_signal']
                self.node.send_trading_signal(
                    symbol=symbol,
                    action=signal['action'],
                    confidence=signal['confidence'],
                    price_target=signal.get('price_target', 0),
                    reasoning=signal.get('reasoning', 'Análise fractal automatizada')
                )
            
            print(f"✅ Análise de {symbol} compartilhada com {len(self.node.peers)} peers")
            
        except Exception as e:
            print(f"❌ Erro ao analisar {symbol}: {e}")

    def _real_fractal_analysis(self, symbol: str) -> dict:
        """Análise fractal real usando os módulos disponíveis."""
        try:
            # Gerar série temporal de teste
            if FRACTAL_AVAILABLE:
                series = generate_fractal_series(length=200, hurst=0.7)
                metrics = calculate_fractal_metrics(series)
            else:
                # Fallback para dados simulados
                return self._simulated_analysis(symbol)
            
            # Análise fractal
            hurst = metrics.get('hurst_exponent', 0.5)
            box_dim = metrics.get('box_dimension', 1.5)
            volatility = metrics.get('volatility', 0.02)
            
            # Predição com IA se disponível
            prediction = []
            confidence = 0.5
            
            if AI_AVAILABLE and self.ai_predictor:
                try:
                    # Treinar predictor
                    self.ai_predictor.fit(series)
                    prediction = self.ai_predictor.predict_next(series, steps=10)
                    confidence = self.ai_predictor.predict_with_confidence(series)[1]
                except Exception as e:
                    print(f"⚠️  Erro na predição IA: {e}")
                    prediction = series[-10:].tolist()  # Usar últimos valores
            
            # Determinar sinal de trading
            if hurst > 0.6:
                action = "BUY" if series[-1] > series[-10] else "HOLD"
                reasoning = f"Série persistente (Hurst: {hurst:.3f}), tendência mantida"
            elif hurst < 0.4:
                action = "SELL" if series[-1] > series[-10] else "BUY"
                reasoning = f"Série anti-persistente (Hurst: {hurst:.3f}), reversão esperada"
            else:
                action = "HOLD"
                reasoning = f"Série aleatória (Hurst: {hurst:.3f}), aguardar padrão"
            
            return {
                'fractal_pattern': {
                    'pattern_type': 'hurst_analysis',
                    'hurst_exponent': hurst,
                    'box_dimension': box_dim,
                    'volatility': volatility,
                    'confidence': confidence,
                    'prediction': prediction if isinstance(prediction, list) else prediction.tolist(),
                    'analysis_time': time.time()
                },
                'trading_signal': {
                    'action': action,
                    'confidence': confidence,
                    'price_target': series[-1] * (1.05 if action == "BUY" else 0.95),
                    'reasoning': reasoning
                }
            }
            
        except Exception as e:
            print(f"❌ Erro na análise fractal real: {e}")
            return self._simulated_analysis(symbol)

    def _simulated_analysis(self, symbol: str) -> dict:
        """Análise simulada para demonstração."""
        import random
        
        # Simular métricas fractais
        hurst = random.uniform(0.3, 0.8)
        box_dim = random.uniform(1.2, 1.8)
        confidence = random.uniform(0.6, 0.9)
        
        # Simular preços
        base_price = {
            'BTCUSD': 45000,
            'ETHUSD': 3200,
            'ADAUSD': 0.65,
            'SOLUSD': 120
        }.get(symbol, 100)
        
        price_variation = random.uniform(0.95, 1.05)
        current_price = base_price * price_variation
        
        # Simular predição
        prediction = []
        for i in range(10):
            trend = random.uniform(0.998, 1.002)
            prediction.append(current_price * (trend ** (i + 1)))
        
        # Determinar ação
        if hurst > 0.6:
            action = "BUY"
            reasoning = f"Padrão persistente detectado (H={hurst:.3f})"
        elif hurst < 0.4:
            action = "SELL"
            reasoning = f"Padrão anti-persistente detectado (H={hurst:.3f})"
        else:
            action = "HOLD"
            reasoning = f"Movimento browniano (H={hurst:.3f})"
        
        return {
            'fractal_pattern': {
                'pattern_type': 'simulated_hurst',
                'hurst_exponent': hurst,
                'box_dimension': box_dim,
                'confidence': confidence,
                'prediction': prediction,
                'analysis_time': time.time()
            },
            'trading_signal': {
                'action': action,
                'confidence': confidence,
                'price_target': current_price * (1.03 if action == "BUY" else 0.97),
                'reasoning': reasoning
            }
        }

    def connect_to_peers(self, peer_addresses: list):
        """Conectar a lista de peers."""
        for address in peer_addresses:
            try:
                host, port = address.split(":")
                if self.node.add_peer_manual(host, int(port)):
                    print(f"✅ Conectado a {address}")
                else:
                    print(f"❌ Falha ao conectar a {address}")
            except ValueError:
                print(f"❌ Endereço inválido: {address}")

    def get_network_consensus(self, symbol: str) -> dict:
        """Obter consensus da rede sobre um símbolo."""
        recent_signals = [
            msg for msg in self.node.received_messages 
            if msg.symbol == symbol and msg.msg_type == 'trading_signal'
            and time.time() - msg.timestamp < 300  # Últimos 5 minutos
        ]
        
        if not recent_signals:
            return {"consensus": "NO_DATA", "confidence": 0}
        
        # Contar votos
        votes = {}
        total_confidence = 0
        
        for signal in recent_signals:
            action = signal.data.get('action', 'HOLD')
            confidence = signal.data.get('confidence', 0)
            
            votes[action] = votes.get(action, 0) + 1
            total_confidence += confidence
        
        # Determinar consensus
        if votes:
            consensus_action = max(votes, key=votes.get)
            avg_confidence = total_confidence / len(recent_signals)
            
            return {
                "consensus": consensus_action,
                "confidence": avg_confidence,
                "votes": votes,
                "participants": len(recent_signals)
            }
        
        return {"consensus": "HOLD", "confidence": 0}

    def stop(self):
        """Parar trader."""
        self.node.stop()


def main():
    """Demonstração do sistema P2P fractal."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Demo P2P Fractal Trading")
    parser.add_argument("--host", default="localhost", help="Host do trader")
    parser.add_argument("--port", type=int, default=5000, help="Porta do trader")
    parser.add_argument("--peers", nargs="*", help="Peers para conectar")
    parser.add_argument("--auto", action="store_true", help="Modo automático")
    
    args = parser.parse_args()
    
    # Criar trader
    trader = FractalP2PTrader(host=args.host, port=args.port)
    
    if not trader.start():
        print("❌ Erro ao iniciar trader")
        return
    
    # Conectar a peers
    if args.peers:
        trader.connect_to_peers(args.peers)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                  🤖 FRACTAL P2P TRADER 🤖                   ║
║                                                              ║
║  Trader ID: {trader.node.node_id:48} ║
║  Endereço: {args.host}:{args.port:44} ║
║  Análise Fractal: {'✅ Disponível' if FRACTAL_AVAILABLE else '⚠️  Simulada':50} ║
║  IA Preditiva: {'✅ Disponível' if AI_AVAILABLE else '⚠️  Simulada':53} ║
║                                                              ║
║  Comandos:                                                   ║
║  analyze <symbol> - Analisar símbolo específico             ║
║  consensus <symbol> - Ver consensus da rede                 ║
║  stats - Ver estatísticas                                   ║
║  peers - Listar peers                                       ║
║  signals - Ver sinais recentes                              ║
║  fractals - Ver padrões fractais                            ║
║  quit - Sair                                                ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    if args.auto:
        print("🤖 Modo automático ativado - análises contínuas em execução")
        print("   Pressione Ctrl+C para parar...")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando modo automático...")
    else:
        # Modo interativo
        try:
            while True:
                cmd = input("\n🤖 > ").strip().split()
                
                if not cmd:
                    continue
                    
                command = cmd[0].lower()
                
                if command == "quit":
                    break
                    
                elif command == "analyze":
                    symbol = cmd[1] if len(cmd) > 1 else "BTCUSD"
                    trader.analyze_and_share(symbol)
                    
                elif command == "consensus":
                    symbol = cmd[1] if len(cmd) > 1 else "BTCUSD"
                    consensus = trader.get_network_consensus(symbol)
                    print(f"Consensus para {symbol}:")
                    print(json.dumps(consensus, indent=2))
                    
                elif command == "stats":
                    stats = trader.node.get_peer_stats()
                    print(json.dumps(stats, indent=2))
                    
                elif command == "peers":
                    peers = trader.node.peers
                    print(f"Peers conectados ({len(peers)}):")
                    for i, (host, port) in enumerate(peers, 1):
                        print(f"  {i}. {host}:{port}")
                        
                elif command == "signals":
                    signals = trader.node.get_recent_signals(5)
                    print("Sinais recentes:")
                    for signal in signals:
                        print(f"  • {signal.get('action', 'N/A')} - Confiança: {signal.get('confidence', 0):.2f}")
                        
                elif command == "fractals":
                    fractals = trader.node.get_recent_fractals(5)
                    print("Padrões fractais recentes:")
                    for fractal in fractals:
                        print(f"  • {fractal.get('pattern_type', 'N/A')} - H: {fractal.get('hurst_exponent', 0):.3f}")
                        
                else:
                    print("❌ Comando não reconhecido")
                    
        except KeyboardInterrupt:
            print("\n")
    
    trader.stop()
    print("👋 Trader finalizado")


if __name__ == "__main__":
    main()
