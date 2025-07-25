"""
Fractal Analysis Engine
======================

Módulo principal para análise fractal de séries temporais financeiras.
Implementa algoritmos avançados para detecção de padrões fractais em dados de mercado.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import yfinance as yf
import warnings
from typing import Dict, List, Tuple, Optional, Union
from datetime import datetime, timedelta
import logging

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class FractalAnalyzer:
    """
    Analisador principal de padrões fractais em séries temporais financeiras.
    """
    
    def __init__(self):
        self.data = None
        self.fractals = {}
        self.patterns = []
        
    def load_market_data(self, symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Carregar dados de mercado usando Yahoo Finance.
        
        Args:
            symbol: Símbolo do ativo (ex: "AAPL", "TSLA")
            period: Período dos dados ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
            interval: Intervalo dos dados ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")
            
        Returns:
            DataFrame com dados OHLCV
        """
        try:
            logger.info(f"Carregando dados para {symbol} - período: {period}")
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                raise ValueError(f"Nenhum dado encontrado para {symbol}")
            
            # Adicionar colunas calculadas
            data['Returns'] = data['Close'].pct_change()
            data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
            data['Volatility'] = data['Returns'].rolling(window=20).std()
            
            self.data = data
            logger.info(f"Dados carregados: {len(data)} registros")
            return data
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def calculate_box_dimension(self, prices: np.array, max_box_size: int = None) -> float:
        """
        Calcular dimensão fractal usando algoritmo Box Counting.
        
        Args:
            prices: Array de preços
            max_box_size: Tamanho máximo da caixa
            
        Returns:
            Dimensão fractal estimada
        """
        if max_box_size is None:
            max_box_size = len(prices) // 4
            
        # Normalizar preços
        prices_norm = (prices - np.min(prices)) / (np.max(prices) - np.min(prices))
        
        box_sizes = np.logspace(0.5, np.log10(max_box_size), 20).astype(int)
        box_counts = []
        
        for box_size in box_sizes:
            # Dividir em caixas
            n_boxes_x = len(prices_norm) // box_size
            n_boxes_y = int(1.0 / (1.0 / box_size))
            
            if n_boxes_x == 0 or n_boxes_y == 0:
                continue
                
            # Contar caixas ocupadas
            occupied_boxes = set()
            
            for i in range(0, len(prices_norm) - box_size, box_size):
                for j in range(i, min(i + box_size, len(prices_norm))):
                    box_x = j // box_size
                    box_y = int(prices_norm[j] * n_boxes_y)
                    occupied_boxes.add((box_x, box_y))
            
            box_counts.append(len(occupied_boxes))
        
        if len(box_counts) < 2:
            return 1.0
        
        # Regressão linear em escala log-log
        log_box_sizes = np.log(box_sizes[:len(box_counts)])
        log_box_counts = np.log(box_counts)
        
        slope, _, r_value, _, _ = stats.linregress(log_box_sizes, log_box_counts)
        
        # Dimensão fractal é o negativo da inclinação
        fractal_dimension = -slope
        
        return max(1.0, min(2.0, fractal_dimension))
    
    def calculate_hurst_exponent(self, prices: np.array) -> float:
        """
        Calcular expoente de Hurst para medir persistência da série.
        
        Args:
            prices: Array de preços
            
        Returns:
            Expoente de Hurst (0.5 = random walk, >0.5 = persistente, <0.5 = anti-persistente)
        """
        try:
            # Calcular log returns
            log_returns = np.diff(np.log(prices))
            n = len(log_returns)
            
            # Diferentes tamanhos de janela
            lags = np.logspace(0.5, np.log10(n//4), 20).astype(int)
            rs_values = []
            
            for lag in lags:
                if lag >= n:
                    continue
                    
                # Dividir série em segmentos
                n_segments = n // lag
                segments = log_returns[:n_segments * lag].reshape(n_segments, lag)
                
                rs_segment = []
                for segment in segments:
                    # Calcular mean
                    mean_segment = np.mean(segment)
                    
                    # Calcular desvios cumulativos
                    deviations = np.cumsum(segment - mean_segment)
                    
                    # Range
                    R = np.max(deviations) - np.min(deviations)
                    
                    # Standard deviation
                    S = np.std(segment)
                    
                    # R/S ratio
                    if S > 0:
                        rs_segment.append(R / S)
                
                if rs_segment:
                    rs_values.append(np.mean(rs_segment))
            
            if len(rs_values) < 2:
                return 0.5
            
            # Regressão linear
            log_lags = np.log(lags[:len(rs_values)])
            log_rs = np.log(rs_values)
            
            slope, _, _, _, _ = stats.linregress(log_lags, log_rs)
            
            return max(0.0, min(1.0, slope))
            
        except Exception as e:
            logger.error(f"Erro no cálculo do expoente de Hurst: {e}")
            return 0.5
    
    def detect_fractal_patterns(self, window: int = 5) -> List[Dict]:
        """
        Detectar padrões fractais nos dados (fractais de Williams).
        
        Args:
            window: Tamanho da janela para detecção
            
        Returns:
            Lista de padrões fractais detectados
        """
        if self.data is None:
            raise ValueError("Carregue dados primeiro usando load_market_data()")
        
        high = self.data['High'].values
        low = self.data['Low'].values
        
        fractals = []
        
        # Detectar fractais de alta (máximos locais)
        for i in range(window, len(high) - window):
            is_high_fractal = True
            for j in range(i - window, i + window + 1):
                if j != i and high[j] >= high[i]:
                    is_high_fractal = False
                    break
            
            if is_high_fractal:
                fractals.append({
                    'type': 'high',
                    'index': i,
                    'price': high[i],
                    'timestamp': self.data.index[i],
                    'strength': self._calculate_fractal_strength(high, i, window)
                })
        
        # Detectar fractais de baixa (mínimos locais)
        for i in range(window, len(low) - window):
            is_low_fractal = True
            for j in range(i - window, i + window + 1):
                if j != i and low[j] <= low[i]:
                    is_low_fractal = False
                    break
            
            if is_low_fractal:
                fractals.append({
                    'type': 'low',
                    'index': i,
                    'price': low[i],
                    'timestamp': self.data.index[i],
                    'strength': self._calculate_fractal_strength(low, i, window, fractal_type='low')
                })
        
        self.patterns = fractals
        return fractals
    
    def _calculate_fractal_strength(self, prices: np.array, index: int, window: int, fractal_type: str = 'high') -> float:
        """Calcular força do fractal baseado na diferença com pontos adjacentes."""
        try:
            center_price = prices[index]
            surrounding_prices = []
            
            for j in range(index - window, index + window + 1):
                if j != index and 0 <= j < len(prices):
                    surrounding_prices.append(prices[j])
            
            if not surrounding_prices:
                return 0.0
            
            if fractal_type == 'high':
                # Para fractais de alta, força é a diferença com o maior preço adjacente
                max_surrounding = max(surrounding_prices)
                strength = (center_price - max_surrounding) / center_price
            else:
                # Para fractais de baixa, força é a diferença com o menor preço adjacente
                min_surrounding = min(surrounding_prices)
                strength = (min_surrounding - center_price) / center_price
            
            return max(0.0, strength)
            
        except Exception:
            return 0.0
    
    def analyze_fractals(self, data: pd.DataFrame = None) -> Dict:
        """
        Análise completa de fractais nos dados.
        
        Args:
            data: DataFrame opcional, usa self.data se não fornecido
            
        Returns:
            Dicionário com resultados da análise fractal
        """
        if data is not None:
            self.data = data
        
        if self.data is None:
            raise ValueError("Nenhum dado disponível para análise")
        
        logger.info("Iniciando análise fractal completa...")
        
        prices = self.data['Close'].values
        
        # Cálculos fractais
        results = {
            'symbol': getattr(self.data, 'symbol', 'Unknown'),
            'timestamp': datetime.now(),
            'data_points': len(prices),
            'fractals': {}
        }
        
        # Dimensão fractal
        results['fractals']['box_dimension'] = self.calculate_box_dimension(prices)
        
        # Expoente de Hurst
        results['fractals']['hurst_exponent'] = self.calculate_hurst_exponent(prices)
        
        # Padrões fractais
        fractal_patterns = self.detect_fractal_patterns()
        results['fractals']['patterns'] = fractal_patterns
        results['fractals']['pattern_count'] = len(fractal_patterns)
        
        # Análise de persistência
        hurst = results['fractals']['hurst_exponent']
        if hurst > 0.6:
            results['fractals']['trend_type'] = 'persistent'
            results['fractals']['trend_description'] = 'Tendência persistente - movimentos passados indicam direção futura'
        elif hurst < 0.4:
            results['fractals']['trend_type'] = 'anti-persistent'
            results['fractals']['trend_description'] = 'Tendência anti-persistente - reversões são mais prováveis'
        else:
            results['fractals']['trend_type'] = 'random'
            results['fractals']['trend_description'] = 'Movimento aleatório - sem tendência clara'
        
        # Complexidade da série
        box_dim = results['fractals']['box_dimension']
        if box_dim > 1.7:
            results['fractals']['complexity'] = 'high'
            results['fractals']['complexity_description'] = 'Alta complexidade - padrões fractais complexos'
        elif box_dim > 1.3:
            results['fractals']['complexity'] = 'medium'
            results['fractals']['complexity_description'] = 'Complexidade média - alguns padrões fractais'
        else:
            results['fractals']['complexity'] = 'low'
            results['fractals']['complexity_description'] = 'Baixa complexidade - padrões simples'
        
        self.fractals = results
        logger.info("Análise fractal concluída")
        return results
    
    def generate_signals(self, fractals: Dict = None) -> List[Dict]:
        """
        Gerar sinais de trading baseados na análise fractal.
        
        Args:
            fractals: Resultados da análise fractal
            
        Returns:
            Lista de sinais de trading
        """
        if fractals is None:
            fractals = self.fractals
        
        if not fractals:
            raise ValueError("Execute analyze_fractals() primeiro")
        
        signals = []
        
        # Sinais baseados no expoente de Hurst
        hurst = fractals['fractals']['hurst_exponent']
        trend_type = fractals['fractals']['trend_type']
        
        # Sinais baseados em padrões fractais recentes
        patterns = fractals['fractals']['patterns']
        if patterns:
            # Ordenar por timestamp
            recent_patterns = sorted(patterns, key=lambda x: x['index'])[-5:]
            
            for pattern in recent_patterns:
                if pattern['type'] == 'high' and pattern['strength'] > 0.02:
                    signals.append({
                        'type': 'sell',
                        'reason': f'Fractal de alta detectado com força {pattern["strength"]:.3f}',
                        'confidence': min(pattern['strength'] * 10, 1.0),
                        'timestamp': pattern['timestamp'],
                        'price': pattern['price']
                    })
                elif pattern['type'] == 'low' and pattern['strength'] > 0.02:
                    signals.append({
                        'type': 'buy',
                        'reason': f'Fractal de baixa detectado com força {pattern["strength"]:.3f}',
                        'confidence': min(pattern['strength'] * 10, 1.0),
                        'timestamp': pattern['timestamp'],
                        'price': pattern['price']
                    })
        
        # Sinais baseados na tendência
        if trend_type == 'persistent' and hurst > 0.7:
            recent_return = self.data['Returns'].iloc[-1] if self.data is not None else 0
            if recent_return > 0.01:
                signals.append({
                    'type': 'buy',
                    'reason': f'Tendência persistente (H={hurst:.3f}) com movimento positivo',
                    'confidence': (hurst - 0.5) * 2,
                    'timestamp': datetime.now(),
                    'price': self.data['Close'].iloc[-1] if self.data is not None else 0
                })
            elif recent_return < -0.01:
                signals.append({
                    'type': 'sell',
                    'reason': f'Tendência persistente (H={hurst:.3f}) com movimento negativo',
                    'confidence': (hurst - 0.5) * 2,
                    'timestamp': datetime.now(),
                    'price': self.data['Close'].iloc[-1] if self.data is not None else 0
                })
        
        elif trend_type == 'anti-persistent' and hurst < 0.3:
            recent_return = self.data['Returns'].iloc[-1] if self.data is not None else 0
            if recent_return > 0.02:
                signals.append({
                    'type': 'sell',
                    'reason': f'Tendência anti-persistente (H={hurst:.3f}) - reversão provável',
                    'confidence': (0.5 - hurst) * 2,
                    'timestamp': datetime.now(),
                    'price': self.data['Close'].iloc[-1] if self.data is not None else 0
                })
            elif recent_return < -0.02:
                signals.append({
                    'type': 'buy',
                    'reason': f'Tendência anti-persistente (H={hurst:.3f}) - reversão provável',
                    'confidence': (0.5 - hurst) * 2,
                    'timestamp': datetime.now(),
                    'price': self.data['Close'].iloc[-1] if self.data is not None else 0
                })
        
        return signals
    
    def save_analysis(self, filename: str):
        """Salvar análise fractal em arquivo JSON."""
        import json
        
        if not self.fractals:
            raise ValueError("Nenhuma análise para salvar")
        
        # Converter datetime para string para serialização JSON
        fractals_copy = self.fractals.copy()
        fractals_copy['timestamp'] = fractals_copy['timestamp'].isoformat()
        
        for pattern in fractals_copy['fractals']['patterns']:
            pattern['timestamp'] = pattern['timestamp'].isoformat()
        
        with open(filename, 'w') as f:
            json.dump(fractals_copy, f, indent=2, default=str)
        
        logger.info(f"Análise salva em {filename}")
    
    def load_analysis(self, filename: str):
        """Carregar análise fractal de arquivo JSON."""
        import json
        from datetime import datetime
        
        with open(filename, 'r') as f:
            fractals = json.load(f)
        
        # Converter strings de volta para datetime
        fractals['timestamp'] = datetime.fromisoformat(fractals['timestamp'])
        
        for pattern in fractals['fractals']['patterns']:
            pattern['timestamp'] = datetime.fromisoformat(pattern['timestamp'])
        
        self.fractals = fractals
        logger.info(f"Análise carregada de {filename}")
        return fractals


# Instância global
fractal_analyzer = FractalAnalyzer()
