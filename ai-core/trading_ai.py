"""
AI Core - Trading Intelligence Engine
=====================================

Módulo principal de inteligência artificial para análise de mercado,
predição de preços e otimização de estratégias de trading.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler # type: ignore
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple, Optional
import joblib

logger = logging.getLogger(__name__)

class TradingAI:
    """
    Engine principal de IA para trading.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.fractal_predictor = FractalPredictor(window_size=30)
        
    def prepare_features(self, market_data: pd.DataFrame) -> np.ndarray:
        """
        Preparar features para o modelo de IA.
        
        Args:
            market_data: DataFrame com dados de mercado
            
        Returns:
            Array numpy com features preparadas
        """
        features = []
        
        # Features técnicas básicas
        if 'close' in market_data.columns:
            # Moving averages
            market_data['ma_5'] = market_data['close'].rolling(5).mean()
            market_data['ma_20'] = market_data['close'].rolling(20).mean()
            
            # RSI simplificado
            delta = market_data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            market_data['rsi'] = 100 - (100 / (1 + rs))
            
            # Volatilidade
            market_data['volatility'] = market_data['close'].rolling(20).std()
            
            # Features adicionais
            features = [
                'ma_5', 'ma_20', 'rsi', 'volatility'
            ]
            
            if 'volume' in market_data.columns:
                features.append('volume')
                
        return market_data[features].fillna(0).values
    
    def train_model(self, historical_data: pd.DataFrame) -> Dict:
        """
        Treinar o modelo de IA com dados históricos.
        
        Args:
            historical_data: DataFrame com dados históricos
            
        Returns:
            Métricas de treinamento
        """
        try:
            logger.info("Iniciando treinamento do modelo de IA...")
            
            # Preparar features
            X = self.prepare_features(historical_data)
            
            # Target: próximo preço de fechamento
            y = historical_data['close'].shift(-1).fillna(method='ffill')
            
            # Remover NaN
            mask = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
            X = X[mask]
            y = y[mask]
            
            # Normalizar features
            X_scaled = self.scaler.fit_transform(X)
            
            # Split train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42
            )
            
            # Treinar modelo
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.model.fit(X_train, y_train)
            
            # Avaliar modelo
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
            
            self.is_trained = True
            
            metrics = {
                "train_score": train_score,
                "test_score": test_score,
                "samples_trained": len(X_train),
                "timestamp": datetime.now()
            }
            
            logger.info(f"Modelo treinado com sucesso. Score: {test_score:.4f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Erro no treinamento: {e}")
            raise
    
    def predict_price(self, current_data: pd.DataFrame) -> Dict:
        """
        Prever próximo preço baseado nos dados atuais.
        
        Args:
            current_data: DataFrame com dados atuais
            
        Returns:
            Predição e metadados
        """
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado ainda")
            
        try:
            # Preparar features
            X = self.prepare_features(current_data)
            X_scaled = self.scaler.transform(X[-1:])  # Usar último ponto
            
            # Fazer predição
            prediction = self.model.predict(X_scaled)[0]
            
            # Calcular confiança (simplificado)
            feature_importance = self.model.feature_importances_
            confidence = min(np.mean(feature_importance), 1.0)
            
            return {
                "predicted_price": prediction,
                "confidence": confidence,
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Erro na predição: {e}")
            raise
    
    def generate_signal(self, market_data: pd.DataFrame) -> Dict:
        """
        Gerar sinal de trading baseado na análise de IA.
        
        Args:
            market_data: DataFrame com dados de mercado
            
        Returns:
            Sinal de trading
        """
        try:
            if not self.is_trained:
                return {
                    "signal": "hold",
                    "confidence": 0.0,
                    "reason": "Modelo não treinado"
                }
            
            # Fazer predição tradicional
            prediction_data = self.predict_price(market_data)
            predicted_price = prediction_data["predicted_price"]
            current_price = market_data['close'].iloc[-1]
            
            # Gerar sinal baseado na predição
            price_change = (predicted_price - current_price) / current_price
            
            if price_change > 0.02:  # > 2% de alta
                signal = "buy"
                confidence = min(prediction_data["confidence"] * abs(price_change) * 10, 1.0)
            elif price_change < -0.02:  # > 2% de queda
                signal = "sell"
                confidence = min(prediction_data["confidence"] * abs(price_change) * 10, 1.0)
            else:
                signal = "hold"
                confidence = 0.5
            
            return {
                "signal": signal,
                "confidence": confidence,
                "predicted_price": predicted_price,
                "current_price": current_price,
                "expected_change": price_change,
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Erro na geração de sinal: {e}")
            return {
                "signal": "hold",
                "confidence": 0.0,
                "reason": f"Erro: {str(e)}"
            }
    
    def generate_fractal_signal(self, market_data: pd.DataFrame, prediction_steps: int = 10) -> Dict:
        """
        Gerar sinal de trading usando preditor fractal.
        
        Args:
            market_data: DataFrame com dados de mercado
            prediction_steps: Número de passos para predição
            
        Returns:
            Sinal de trading baseado em análise fractal
        """
        try:
            prices = market_data['close'].values
            
            # Treinar predictor fractal se necessário
            if not self.fractal_predictor.is_fitted and len(prices) >= 50:
                self.fractal_predictor.fit(prices)
            
            if not self.fractal_predictor.is_fitted:
                return {
                    "signal": "hold",
                    "confidence": 0.0,
                    "reason": "Dados insuficientes para análise fractal"
                }
            
            # Fazer predição fractal com confiança
            fractal_prediction = self.fractal_predictor.predict_with_confidence(
                prices, steps=prediction_steps
            )
            
            if not fractal_prediction["predictions"]:
                return {
                    "signal": "hold",
                    "confidence": 0.0,
                    "reason": "Erro na predição fractal"
                }
            
            # Analisar tendência das predições
            predictions = fractal_prediction["predictions"]
            current_price = prices[-1]
            
            # Calcular mudança prevista nos próximos passos
            short_term_change = (predictions[2] - current_price) / current_price  # 3 passos à frente
            medium_term_change = (predictions[5] - current_price) / current_price if len(predictions) > 5 else short_term_change
            
            # Calcular tendência geral
            if len(predictions) >= 5:
                trend = np.polyfit(range(5), predictions[:5], 1)[0]
                trend_strength = abs(trend) / current_price
            else:
                trend = predictions[-1] - predictions[0]
                trend_strength = abs(trend) / current_price
            
            # Gerar sinal baseado na análise fractal
            confidence = fractal_prediction["confidence_mean"]
            
            if short_term_change > 0.015 and medium_term_change > 0.01:  # Alta consistente
                signal = "buy"
                confidence *= (1 + trend_strength)
            elif short_term_change < -0.015 and medium_term_change < -0.01:  # Baixa consistente
                signal = "sell"
                confidence *= (1 + trend_strength)
            elif trend_strength > 0.02:  # Tendência forte
                signal = "buy" if trend > 0 else "sell"
                confidence *= 0.8  # Menor confiança para sinais baseados só em tendência
            else:
                signal = "hold"
                confidence = 0.5
            
            return {
                "signal": signal,
                "confidence": min(confidence, 1.0),
                "predicted_prices": predictions,
                "short_term_change": short_term_change,
                "medium_term_change": medium_term_change,
                "trend_strength": trend_strength,
                "confidence_interval": {
                    "lower": fractal_prediction["confidence_lower"],
                    "upper": fractal_prediction["confidence_upper"]
                },
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Erro na geração de sinal fractal: {e}")
            return {
                "signal": "hold",
                "confidence": 0.0,
                "reason": f"Erro fractal: {str(e)}"
            }
    
    def generate_combined_signal(self, market_data: pd.DataFrame) -> Dict:
        """
        Gerar sinal combinado usando modelo tradicional e fractal.
        
        Args:
            market_data: DataFrame com dados de mercado
            
        Returns:
            Sinal de trading combinado
        """
        try:
            # Obter sinais individuais
            traditional_signal = self.generate_signal(market_data)
            fractal_signal = self.generate_fractal_signal(market_data)
            
            # Pesos para combinação (podem ser ajustados)
            traditional_weight = 0.4
            fractal_weight = 0.6
            
            # Combinar sinais
            signals = []
            weights = []
            
            if traditional_signal["signal"] != "hold":
                signals.append(traditional_signal["signal"])
                weights.append(traditional_signal["confidence"] * traditional_weight)
            
            if fractal_signal["signal"] != "hold":
                signals.append(fractal_signal["signal"])
                weights.append(fractal_signal["confidence"] * fractal_weight)
            
            if not signals:
                return {
                    "signal": "hold",
                    "confidence": 0.5,
                    "reason": "Nenhum sinal forte detectado",
                    "components": {
                        "traditional": traditional_signal,
                        "fractal": fractal_signal
                    }
                }
            
            # Votação ponderada
            buy_weight = sum(w for s, w in zip(signals, weights) if s == "buy")
            sell_weight = sum(w for s, w in zip(signals, weights) if s == "sell")
            
            if buy_weight > sell_weight and buy_weight > 0.3:
                final_signal = "buy"
                confidence = buy_weight
            elif sell_weight > buy_weight and sell_weight > 0.3:
                final_signal = "sell"
                confidence = sell_weight
            else:
                final_signal = "hold"
                confidence = 0.5
            
            return {
                "signal": final_signal,
                "confidence": min(confidence, 1.0),
                "reason": f"Sinal combinado - Traditional: {traditional_signal['signal']}, Fractal: {fractal_signal['signal']}",
                "components": {
                    "traditional": traditional_signal,
                    "fractal": fractal_signal
                },
                "weights": {
                    "traditional": traditional_weight,
                    "fractal": fractal_weight
                },
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Erro na geração de sinal combinado: {e}")
            return {
                "signal": "hold",
                "confidence": 0.0,
                "reason": f"Erro combinado: {str(e)}"
            }
    
    def save_model(self, filepath: str):
        """Salvar modelo treinado."""
        if self.is_trained:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler
            }, filepath)
            logger.info(f"Modelo salvo em {filepath}")
    
    def load_model(self, filepath: str):
        """Carregar modelo salvo."""
        try:
            saved_data = joblib.load(filepath)
            self.model = saved_data['model']
            self.scaler = saved_data['scaler']
            self.is_trained = True
            logger.info(f"Modelo carregado de {filepath}")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")


class MarketAnalyzer:
    """
    Analisador de mercado com indicadores técnicos.
    """
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Calcular RSI."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """Calcular MACD."""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        
        return {
            'macd': macd,
            'signal': signal_line,
            'histogram': histogram
        }
    
    @staticmethod
    def detect_patterns(market_data: pd.DataFrame) -> List[str]:
        """Detectar padrões de mercado."""
        patterns = []
        
        if len(market_data) < 20:
            return patterns
        
        # Padrão de alta
        recent_trend = market_data['close'].iloc[-5:].pct_change().mean()
        if recent_trend > 0.01:
            patterns.append("Tendência de alta")
        elif recent_trend < -0.01:
            patterns.append("Tendência de baixa")
        
        # Volume análise
        if 'volume' in market_data.columns:
            avg_volume = market_data['volume'].rolling(20).mean().iloc[-1]
            current_volume = market_data['volume'].iloc[-1]
            if current_volume > avg_volume * 1.5:
                patterns.append("Volume acima da média")
        
        return patterns


class FractalPredictor:
    """
    Preditor fractal avançado para séries temporais financeiras.
    Usa janelas deslizantes e Random Forest para capturar padrões fractais.
    """
    
    def __init__(self, window_size: int = 30):
        self.window_size = window_size
        self.model = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])
        self.is_fitted = False
        
    def _create_features(self, series: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Criar features de janela deslizante para treinamento.
        
        Args:
            series: Série temporal de entrada
            
        Returns:
            Tupla (X, y) com features e targets
        """
        X, y = [], []
        for i in range(len(series) - self.window_size):
            X.append(series[i:i+self.window_size])
            y.append(series[i+self.window_size])
        return np.array(X), np.array(y)
    
    def _create_fractal_features(self, window: np.ndarray) -> np.ndarray:
        """
        Criar features fractais adicionais para uma janela.
        
        Args:
            window: Janela de dados
            
        Returns:
            Array com features fractais
        """
        features = []
        
        # Features básicas da janela
        features.extend(window)
        
        # Features estatísticas
        features.append(np.mean(window))
        features.append(np.std(window))
        features.append(np.min(window))
        features.append(np.max(window))
        
        # Features de tendência
        if len(window) > 1:
            # Slope da regressão linear
            x = np.arange(len(window))
            slope = np.polyfit(x, window, 1)[0]
            features.append(slope)
            
            # Correlação com tendência linear
            linear_trend = slope * x + window[0]
            correlation = np.corrcoef(window, linear_trend)[0, 1]
            features.append(correlation if not np.isnan(correlation) else 0.0)
        else:
            features.extend([0.0, 0.0])
        
        # Features de volatilidade
        if len(window) > 1:
            returns = np.diff(window) / window[:-1]
            features.append(np.std(returns))
            features.append(np.mean(np.abs(returns)))
        else:
            features.extend([0.0, 0.0])
        
        # Features fractais simplificadas
        # Medida de rugosidade (roughness)
        if len(window) > 2:
            second_diff = np.diff(window, n=2)
            roughness = np.sum(np.abs(second_diff))
            features.append(roughness)
        else:
            features.append(0.0)
        
        # Auto-correlação de lag 1
        if len(window) > 1:
            lag1_corr = np.corrcoef(window[:-1], window[1:])[0, 1]
            features.append(lag1_corr if not np.isnan(lag1_corr) else 0.0)
        else:
            features.append(0.0)
        
        return np.array(features)
    
    def fit(self, series: np.ndarray):
        """
        Treinar o modelo com uma série temporal.
        
        Args:
            series: Série temporal para treinamento
        """
        try:
            # Criar features básicas
            X_basic, y = self._create_features(series)
            
            if len(X_basic) == 0:
                raise ValueError("Série muito curta para criar features")
            
            # Criar features fractais avançadas
            X_fractal = []
            for window in X_basic:
                fractal_features = self._create_fractal_features(window)
                X_fractal.append(fractal_features)
            
            X_fractal = np.array(X_fractal)
            
            # Treinar modelo
            self.model.fit(X_fractal, y)
            self.is_fitted = True
            
            logger.info(f"FractalPredictor treinado com {len(X_fractal)} amostras")
            
        except Exception as e:
            logger.error(f"Erro no treinamento do FractalPredictor: {e}")
            raise
    
    def predict_next(self, series: np.ndarray, steps: int = 10) -> List[float]:
        """
        Prever próximos valores da série temporal.
        
        Args:
            series: Série temporal atual
            steps: Número de passos a prever
            
        Returns:
            Lista com predições
        """
        if not self.is_fitted:
            raise ValueError("Modelo não foi treinado ainda")
        
        try:
            predictions = []
            current_window = list(series[-self.window_size:])
            
            for _ in range(steps):
                # Criar features fractais para a janela atual
                window_array = np.array(current_window)
                fractal_features = self._create_fractal_features(window_array)
                
                # Fazer predição
                next_val = self.model.predict([fractal_features])[0]
                predictions.append(float(next_val))
                
                # Atualizar janela deslizante
                current_window = current_window[1:] + [next_val]
            
            return predictions
            
        except Exception as e:
            logger.error(f"Erro na predição: {e}")
            return []
    
    def predict_with_confidence(self, series: np.ndarray, steps: int = 10) -> Dict:
        """
        Prever com estimativa de confiança usando ensemble.
        
        Args:
            series: Série temporal atual
            steps: Número de passos a prever
            
        Returns:
            Dicionário com predições e intervalo de confiança
        """
        if not self.is_fitted:
            raise ValueError("Modelo não foi treinado ainda")
        
        try:
            # Fazer múltiplas predições com pequenas variações
            n_predictions = 50
            all_predictions = []
            
            for _ in range(n_predictions):
                # Adicionar pequeno ruído para criar ensemble
                noisy_series = series + np.random.normal(0, np.std(series) * 0.01, len(series))
                predictions = self.predict_next(noisy_series, steps)
                if predictions:
                    all_predictions.append(predictions)
            
            if not all_predictions:
                return {
                    "predictions": [],
                    "confidence_lower": [],
                    "confidence_upper": [],
                    "confidence_mean": 0.0
                }
            
            # Calcular estatísticas
            all_predictions = np.array(all_predictions)
            mean_predictions = np.mean(all_predictions, axis=0)
            std_predictions = np.std(all_predictions, axis=0)
            
            # Intervalo de confiança (95%)
            confidence_lower = mean_predictions - 1.96 * std_predictions
            confidence_upper = mean_predictions + 1.96 * std_predictions
            
            # Confiança média baseada na variabilidade
            confidence_mean = 1.0 / (1.0 + np.mean(std_predictions))
            
            return {
                "predictions": mean_predictions.tolist(),
                "confidence_lower": confidence_lower.tolist(),
                "confidence_upper": confidence_upper.tolist(),
                "confidence_mean": float(confidence_mean),
                "ensemble_size": len(all_predictions)
            }
            
        except Exception as e:
            logger.error(f"Erro na predição com confiança: {e}")
            return {
                "predictions": [],
                "confidence_lower": [],
                "confidence_upper": [],
                "confidence_mean": 0.0
            }
    
    def get_feature_importance(self) -> Dict:
        """Obter importância das features fractais."""
        if not self.is_fitted:
            return {}
        
        try:
            # Obter importâncias do Random Forest
            regressor = self.model.named_steps['regressor']
            importances = regressor.feature_importances_
            
            # Mapear para nomes de features
            feature_names = (
                [f"price_t-{i}" for i in range(self.window_size, 0, -1)] +
                ["mean", "std", "min", "max", "slope", "trend_corr", 
                 "volatility", "abs_returns", "roughness", "autocorr"]
            )
            
            feature_importance = dict(zip(feature_names[:len(importances)], importances))
            
            return {
                "feature_importance": feature_importance,
                "top_features": sorted(feature_importance.items(), 
                                     key=lambda x: x[1], reverse=True)[:5]
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter importância das features: {e}")
            return {}


# Instância global do motor de IA
trading_ai = TradingAI()
market_analyzer = MarketAnalyzer()
fractal_predictor = FractalPredictor()
