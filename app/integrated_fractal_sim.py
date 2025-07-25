"""
Fractal P2P Simulator Integrado
==============================

Integração dos simuladores fractais com sistema P2P avançado.
Combina análise fractal, projections adaptativas e rede distribuída.
"""

import asyncio
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import logging
import threading
from dataclasses import dataclass, asdict
import uuid

# Importar módulos locais
from fractal import FractalAnalyzer
from trading_ai import TradingAI

logger = logging.getLogger(__name__)

@dataclass
class FractalPattern:
    """Padrão fractal detectado."""
    pattern_id: str
    pattern_type: str  # "self_similar", "scaling", "recursive"
    complexity: float
    dimension: float
    confidence: float
    timestamp: datetime
    data_points: List[float]
    prediction: Optional[List[float]] = None

@dataclass
class P2PFractalNode:
    """Nó na rede P2P com capacidades fractais."""
    node_id: str
    address: str
    port: int
    fractal_patterns: List[FractalPattern]
    consensus_weight: float
    last_active: datetime

class FractalProjector:
    """
    Projetor de padrões fractais para predição de séries temporais.
    """
    
    def __init__(self):
        self.patterns = []
        self.dimension_cache = {}
        
    def extract_patterns(self, data: np.ndarray, window_size: int = 50) -> List[FractalPattern]:
        """
        Extrair padrões fractais auto-similares dos dados.
        
        Args:
            data: Array de dados de série temporal
            window_size: Tamanho da janela para análise
            
        Returns:
            Lista de padrões fractais detectados
        """
        patterns = []
        
        for i in range(0, len(data) - window_size, window_size // 2):
            window = data[i:i + window_size]
            
            # Calcular dimensão fractal da janela
            dimension = self._calculate_box_dimension(window)
            
            # Detectar auto-similaridade
            similarity_score = self._detect_self_similarity(window)
            
            # Calcular complexidade
            complexity = self._calculate_complexity(window)
            
            if similarity_score > 0.6 and dimension > 1.1:  # Thresholds
                pattern = FractalPattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=self._classify_pattern(window),
                    complexity=complexity,
                    dimension=dimension,
                    confidence=similarity_score,
                    timestamp=datetime.now(),
                    data_points=window.tolist()
                )
                patterns.append(pattern)
        
        self.patterns = patterns
        return patterns
    
    def _calculate_box_dimension(self, data: np.ndarray) -> float:
        """Calcular dimensão fractal usando box counting."""
        if len(data) < 10:
            return 1.0
            
        # Normalizar dados
        data_norm = (data - np.min(data)) / (np.max(data) - np.min(data) + 1e-8)
        
        box_sizes = np.logspace(0.5, np.log10(len(data)//4), 10).astype(int)
        box_counts = []
        
        for box_size in box_sizes:
            if box_size >= len(data):
                continue
                
            # Contar caixas ocupadas
            n_boxes = len(data) // box_size
            occupied = set()
            
            for j in range(0, len(data), box_size):
                end_idx = min(j + box_size, len(data))
                box_data = data_norm[j:end_idx]
                if len(box_data) > 0:
                    box_id = (j // box_size, int(np.mean(box_data) * 10))
                    occupied.add(box_id)
            
            box_counts.append(len(occupied))
        
        if len(box_counts) < 2:
            return 1.0
        
        # Regressão linear em escala log
        log_sizes = np.log(box_sizes[:len(box_counts)])
        log_counts = np.log(np.array(box_counts) + 1e-8)
        
        if len(log_sizes) > 1:
            slope = np.polyfit(log_sizes, log_counts, 1)[0]
            return max(1.0, min(2.0, -slope))
        
        return 1.0
    
    def _detect_self_similarity(self, data: np.ndarray) -> float:
        """Detectar auto-similaridade em diferentes escalas."""
        if len(data) < 20:
            return 0.0
            
        # Dividir em sub-sequências de diferentes tamanhos
        scales = [len(data)//4, len(data)//2, len(data)//8]
        similarities = []
        
        for scale in scales:
            if scale < 5:
                continue
                
            # Extrair subsequências
            n_subs = len(data) // scale
            subsequences = []
            
            for i in range(n_subs):
                start = i * scale
                end = min(start + scale, len(data))
                if end - start >= scale:
                    subsequences.append(data[start:end])
            
            if len(subsequences) < 2:
                continue
            
            # Calcular correlações entre subsequências
            correlations = []
            for i in range(len(subsequences)):
                for j in range(i+1, len(subsequences)):
                    if len(subsequences[i]) == len(subsequences[j]):
                        corr = np.corrcoef(subsequences[i], subsequences[j])[0, 1]
                        if not np.isnan(corr):
                            correlations.append(abs(corr))
            
            if correlations:
                similarities.append(np.mean(correlations))
        
        return np.mean(similarities) if similarities else 0.0
    
    def _calculate_complexity(self, data: np.ndarray) -> float:
        """Calcular complexidade usando entropia aproximada."""
        if len(data) < 10:
            return 0.0
            
        m = 2  # Pattern length
        r = 0.2 * np.std(data)  # Tolerance
        
        def _maxdist(xi, xj, m):
            return max([abs(ua - va) for ua, va in zip(xi, xj)])
        
        def _phi(m):
            patterns = np.array([data[i:i+m] for i in range(len(data) - m + 1)])
            C = np.zeros(len(patterns))
            
            for i in range(len(patterns)):
                template = patterns[i]
                matches = sum(1 for pattern in patterns if _maxdist(template, pattern, m) <= r)
                C[i] = matches / len(patterns)
            
            phi = np.mean(np.log(C + 1e-8))
            return phi
        
        try:
            return _phi(m) - _phi(m + 1)
        except:
            return 0.0
    
    def _classify_pattern(self, data: np.ndarray) -> str:
        """Classificar tipo de padrão fractal."""
        # Análise de tendência
        trend = np.polyfit(range(len(data)), data, 1)[0]
        
        # Análise de periodicidade
        fft = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(data))
        dominant_freq = freqs[np.argmax(np.abs(fft[1:len(fft)//2])) + 1]
        
        if abs(trend) > np.std(data) * 0.1:
            if trend > 0:
                return "trending_up"
            else:
                return "trending_down"
        elif abs(dominant_freq) > 0.1:
            return "cyclical"
        else:
            return "self_similar"
    
    def project_future(self, n_steps: int = 20) -> np.ndarray:
        """
        Projetar valores futuros baseado nos padrões fractais.
        
        Args:
            n_steps: Número de passos futuros para projetar
            
        Returns:
            Array com valores projetados
        """
        if not self.patterns:
            return np.array([])
        
        # Usar padrão com maior confiança
        best_pattern = max(self.patterns, key=lambda p: p.confidence)
        data = np.array(best_pattern.data_points)
        
        # Projeção baseada na auto-similaridade
        projection = []
        
        # Identificar período característico
        if len(data) > 10:
            # Usar correlação para encontrar período
            autocorr = np.correlate(data, data, mode='full')
            autocorr = autocorr[len(autocorr)//2:]
            
            # Encontrar primeiro máximo local (período)
            period = 1
            for i in range(2, min(len(autocorr)//2, len(data)//2)):
                if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1]:
                    period = i
                    break
            
            # Gerar projeção usando periodicidade detectada
            for i in range(n_steps):
                # Repetir padrão com variação baseada na dimensão fractal
                base_idx = i % period if period > 1 else i % len(data)
                base_value = data[base_idx] if base_idx < len(data) else data[-1]
                
                # Adicionar variação fractal
                noise_scale = 0.1 * (best_pattern.dimension - 1.0)
                noise = np.random.normal(0, noise_scale) * np.std(data)
                
                projection.append(base_value + noise)
        else:
            # Fallback: tendência linear com ruído
            trend = np.polyfit(range(len(data)), data, 1)[0]
            last_value = data[-1]
            
            for i in range(n_steps):
                noise = np.random.normal(0, 0.05 * np.std(data))
                projection.append(last_value + trend * (i + 1) + noise)
        
        return np.array(projection)


class FractalP2PNetwork:
    """
    Rede P2P especializada em análise fractal distribuída.
    """
    
    def __init__(self, node_id: str = None):
        self.node_id = node_id or str(uuid.uuid4())
        self.nodes: Dict[str, P2PFractalNode] = {}
        self.local_patterns: List[FractalPattern] = []
        self.consensus_patterns: List[FractalPattern] = []
        self.fractal_projector = FractalProjector()
        self.running = False
        
    async def start_network(self, port: int = 8080):
        """Iniciar rede P2P fractal."""
        self.running = True
        logger.info(f"Iniciando rede P2P fractal - Node {self.node_id} na porta {port}")
        
        # Simular descoberta de nós
        await self._simulate_node_discovery()
        
        # Iniciar loop de consensus
        asyncio.create_task(self._consensus_loop())
        
    def add_local_pattern(self, pattern: FractalPattern):
        """Adicionar padrão fractal local."""
        self.local_patterns.append(pattern)
        logger.info(f"Padrão fractal adicionado: {pattern.pattern_type}")
        
    async def broadcast_pattern(self, pattern: FractalPattern):
        """Broadcast padrão fractal para a rede."""
        message = {
            "type": "fractal_pattern",
            "node_id": self.node_id,
            "pattern": asdict(pattern),
            "timestamp": datetime.now().isoformat()
        }
        
        # Simular broadcast para todos os nós
        for node in self.nodes.values():
            await self._send_to_node(node, message)
        
        logger.info(f"Pattern {pattern.pattern_id} broadcasted to {len(self.nodes)} nodes")
    
    async def _simulate_node_discovery(self):
        """Simular descoberta de nós na rede."""
        # Adicionar nós simulados
        for i in range(3):
            node = P2PFractalNode(
                node_id=f"node_{i}",
                address="localhost",
                port=8080 + i + 1,
                fractal_patterns=[],
                consensus_weight=np.random.uniform(0.5, 1.0),
                last_active=datetime.now()
            )
            self.nodes[node.node_id] = node
        
        logger.info(f"Descobertos {len(self.nodes)} nós na rede")
    
    async def _send_to_node(self, node: P2PFractalNode, message: Dict):
        """Enviar mensagem para um nó específico."""
        # Simular envio de mensagem
        await asyncio.sleep(0.1)  # Simular latência de rede
        
    async def _consensus_loop(self):
        """Loop de consensus para padrões fractais."""
        while self.running:
            try:
                await self._run_consensus()
                await asyncio.sleep(30)  # Consensus a cada 30 segundos
            except Exception as e:
                logger.error(f"Erro no consensus loop: {e}")
                await asyncio.sleep(60)
    
    async def _run_consensus(self):
        """Executar algoritmo de consensus para padrões fractais."""
        if not self.local_patterns:
            return
        
        # Simular votação de padrões
        pattern_votes = {}
        
        for pattern in self.local_patterns:
            pattern_votes[pattern.pattern_id] = {
                "pattern": pattern,
                "votes": 0,
                "total_weight": 0.0
            }
            
            # Simular votos dos nós
            for node in self.nodes.values():
                # Probabilidade de voto baseada na confiança do padrão
                if np.random.random() < pattern.confidence:
                    pattern_votes[pattern.pattern_id]["votes"] += 1
                    pattern_votes[pattern.pattern_id]["total_weight"] += node.consensus_weight
        
        # Determinar padrões consensuais
        self.consensus_patterns = []
        min_votes = max(1, len(self.nodes) // 2)  # Maioria simples
        
        for pattern_id, votes_data in pattern_votes.items():
            if votes_data["votes"] >= min_votes:
                pattern = votes_data["pattern"]
                pattern.confidence = votes_data["total_weight"] / len(self.nodes)
                self.consensus_patterns.append(pattern)
        
        logger.info(f"Consensus: {len(self.consensus_patterns)} padrões aprovados")
    
    def get_network_prediction(self, symbol: str, n_steps: int = 20) -> Dict:
        """Obter predição baseada no consensus da rede."""
        if not self.consensus_patterns:
            return {
                "symbol": symbol,
                "prediction": [],
                "confidence": 0.0,
                "patterns_used": 0,
                "timestamp": datetime.now()
            }
        
        # Usar padrões consensuais para projeção
        projections = []
        weights = []
        
        for pattern in self.consensus_patterns:
            self.fractal_projector.patterns = [pattern]
            projection = self.fractal_projector.project_future(n_steps)
            if len(projection) > 0:
                projections.append(projection)
                weights.append(pattern.confidence)
        
        if not projections:
            return {
                "symbol": symbol,
                "prediction": [],
                "confidence": 0.0,
                "patterns_used": 0,
                "timestamp": datetime.now()
            }
        
        # Média ponderada das projeções
        weights = np.array(weights)
        weights = weights / np.sum(weights)  # Normalizar
        
        ensemble_prediction = np.zeros(n_steps)
        for projection, weight in zip(projections, weights):
            ensemble_prediction += projection * weight
        
        return {
            "symbol": symbol,
            "prediction": ensemble_prediction.tolist(),
            "confidence": np.mean(weights),
            "patterns_used": len(projections),
            "network_nodes": len(self.nodes),
            "timestamp": datetime.now()
        }


class IntegratedFractalTrader:
    """
    Sistema integrado que combina análise fractal, IA e rede P2P.
    """
    
    def __init__(self):
        self.fractal_analyzer = FractalAnalyzer()
        self.trading_ai = TradingAI()
        self.fractal_projector = FractalProjector()
        self.p2p_network = FractalP2PNetwork()
        
    async def analyze_and_trade(self, symbol: str, period: str = "1y") -> Dict:
        """
        Análise completa e geração de sinais de trading.
        
        Args:
            symbol: Símbolo do ativo
            period: Período dos dados
            
        Returns:
            Análise completa com sinais de trading
        """
        try:
            logger.info(f"Iniciando análise integrada para {symbol}")
            
            # 1. Carregar dados de mercado
            market_data = self.fractal_analyzer.load_market_data(symbol, period)
            prices = market_data['Close'].values
            
            # 2. Análise fractal local
            fractal_results = self.fractal_analyzer.analyze_fractals(market_data)
            
            # 3. Extrair padrões fractais para P2P
            patterns = self.fractal_projector.extract_patterns(prices)
            
            # 4. Adicionar padrões à rede P2P
            for pattern in patterns:
                self.p2p_network.add_local_pattern(pattern)
                await self.p2p_network.broadcast_pattern(pattern)
            
            # 5. Obter predição da rede P2P
            network_prediction = self.p2p_network.get_network_prediction(symbol)
            
            # 6. Análise de IA
            ai_signal = self.trading_ai.generate_signal(market_data)
            
            # 7. Combinar resultados
            combined_analysis = {
                "symbol": symbol,
                "timestamp": datetime.now(),
                "fractal_analysis": fractal_results,
                "ai_analysis": ai_signal,
                "p2p_prediction": network_prediction,
                "patterns_detected": len(patterns),
                "trading_recommendation": self._generate_combined_signal(
                    fractal_results, ai_signal, network_prediction
                )
            }
            
            logger.info(f"Análise integrada concluída para {symbol}")
            return combined_analysis
            
        except Exception as e:
            logger.error(f"Erro na análise integrada: {e}")
            raise
    
    def _generate_combined_signal(self, fractal_results: Dict, ai_signal: Dict, network_prediction: Dict) -> Dict:
        """Gerar sinal combinado baseado em todas as análises."""
        signals = []
        weights = []
        
        # Sinal fractal
        fractal_signals = self.fractal_analyzer.generate_signals(fractal_results)
        if fractal_signals:
            recent_fractal = fractal_signals[-1]
            signals.append(recent_fractal['type'])
            weights.append(recent_fractal['confidence'] * 0.3)  # 30% peso
        
        # Sinal IA
        if ai_signal['signal'] != 'hold':
            signals.append(ai_signal['signal'])
            weights.append(ai_signal['confidence'] * 0.4)  # 40% peso
        
        # Sinal rede P2P
        if network_prediction['confidence'] > 0.5:
            # Analisar tendência da predição
            prediction = network_prediction['prediction']
            if len(prediction) > 5:
                trend = np.polyfit(range(len(prediction[:5])), prediction[:5], 1)[0]
                if trend > 0.01:
                    signals.append('buy')
                    weights.append(network_prediction['confidence'] * 0.3)  # 30% peso
                elif trend < -0.01:
                    signals.append('sell')
                    weights.append(network_prediction['confidence'] * 0.3)
        
        # Determinar sinal final
        if not signals:
            return {
                "signal": "hold",
                "confidence": 0.0,
                "reason": "Sinais insuficientes"
            }
        
        # Votação ponderada
        buy_weight = sum(w for s, w in zip(signals, weights) if s == 'buy')
        sell_weight = sum(w for s, w in zip(signals, weights) if s == 'sell')
        
        if buy_weight > sell_weight and buy_weight > 0.5:
            final_signal = "buy"
            confidence = buy_weight
        elif sell_weight > buy_weight and sell_weight > 0.5:
            final_signal = "sell"
            confidence = sell_weight
        else:
            final_signal = "hold"
            confidence = 0.5
        
        return {
            "signal": final_signal,
            "confidence": confidence,
            "components": {
                "fractal": len([s for s in signals if fractal_signals and s == fractal_signals[-1]['type']]),
                "ai": 1 if ai_signal['signal'] != 'hold' else 0,
                "p2p": 1 if network_prediction['confidence'] > 0.5 else 0
            },
            "reason": f"Sinal combinado de {len(signals)} componentes"
        }


# Instância global
integrated_trader = IntegratedFractalTrader()
