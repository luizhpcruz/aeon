"""
🌌 AEON TRADING NETWORK - MINI-AEON MOBILE
Desenvolvido por Luiz Cruz - 2025

Sistema distribuído de trading evolutivo para dispositivos móveis
"""

import asyncio
import json
import time
import uuid
import hashlib
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
import websockets
import numpy as np
from datetime import datetime, timedelta

@dataclass
class DeviceProfile:
    """Perfil único do dispositivo móvel"""
    device_id: str
    device_type: str  # 'ios', 'android', 'other'
    cpu_cores: int
    ram_gb: float
    battery_level: float
    network_type: str  # '4g', '5g', 'wifi'
    location_timezone: str
    user_risk_tolerance: float  # 0.0 (conservador) a 1.0 (agressivo)

@dataclass
class TradingSignal:
    """Sinal de trading gerado pelo mini-AEON"""
    signal_id: str
    timestamp: datetime
    symbol: str
    action: str  # 'buy', 'sell', 'hold'
    confidence: float  # 0.0 a 1.0
    price_target: float
    stop_loss: float
    device_id: str
    fitness_score: float

class MiniAEON:
    """
    Mini-AEON otimizado para dispositivos móveis
    Implementa a equação AEON adaptada para trading
    """
    
    def __init__(self, device_profile: DeviceProfile):
        self.device_profile = device_profile
        self.device_id = device_profile.device_id
        
        # Parâmetros AEON adaptados ao device
        self.aeon_params = self._initialize_device_params()
        
        # Estado evolutivo
        self.fitness_score = 1.0
        self.generation = 0
        self.trading_history = []
        self.market_memory = []
        
        # Conectividade
        self.peer_connections = set()
        self.master_connection = None
        self.is_online = False
        
    def _initialize_device_params(self) -> Dict[str, float]:
        """Inicializa parâmetros AEON baseados no perfil do device"""
        
        # Parâmetros base da equação F(t) = A*sin(Bt+φ) + C*e^(-λt) + D*log(t+1)
        base_params = {
            'A': 1.0,    # Amplitude oscilação
            'B': 1.0,    # Frequência oscilação  
            'phi': 0.0,  # Fase oscilação
            'C': 1.0,    # Amplitude decaimento
            'lambda': 0.1,  # Taxa decaimento
            'D': 1.0     # Influência logarítmica
        }
        
        # Adaptação baseada no tipo de device
        if self.device_profile.device_type == 'ios':
            # iOS: Mais conservador, estável
            base_params.update({
                'A': 0.8,
                'B': 1.2,
                'lambda': 0.05,
                'D': 0.9
            })
        elif self.device_profile.device_type == 'android':
            # Android: Mais agressivo, adaptável
            base_params.update({
                'A': 1.3,
                'B': 2.1,
                'lambda': 0.08,
                'D': 1.2
            })
        
        # Ajuste baseado na tolerância ao risco do usuário
        risk_factor = self.device_profile.user_risk_tolerance
        base_params['A'] *= (0.5 + risk_factor)
        base_params['B'] *= (0.8 + 0.4 * risk_factor)
        
        return base_params
    
    def calculate_aeon_value(self, t: float) -> float:
        """
        Calcula valor da equação AEON no tempo t
        F(t) = A*sin(Bt+φ) + C*e^(-λt) + D*log(t+1)
        """
        A = self.aeon_params['A']
        B = self.aeon_params['B']
        phi = self.aeon_params['phi']
        C = self.aeon_params['C']
        lambda_val = self.aeon_params['lambda']
        D = self.aeon_params['D']
        
        # Componentes da equação
        oscillation = A * np.sin(B * t + phi)
        decay = C * np.exp(-lambda_val * t)
        logarithmic = D * np.log(t + 1)
        
        return oscillation + decay + logarithmic
    
    def analyze_market_pattern(self, market_data: List[float]) -> TradingSignal:
        """Analisa padrões de mercado usando AEON"""
        
        if len(market_data) < 10:
            return self._generate_hold_signal()
        
        # Calcula valores AEON para diferentes janelas temporais
        current_time = time.time()
        aeon_values = []
        
        for i, price in enumerate(market_data[-20:]):  # Últimos 20 pontos
            t = i * 0.1  # Intervalo de tempo
            aeon_val = self.calculate_aeon_value(t)
            aeon_values.append(aeon_val)
        
        # Análise de tendência
        trend = self._calculate_trend(aeon_values)
        
        # Análise de volatilidade
        volatility = np.std(market_data[-10:])
        
        # Geração do sinal
        signal = self._generate_trading_signal(trend, volatility, market_data[-1])
        
        # Atualiza histórico
        self.trading_history.append(signal)
        
        return signal
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calcula tendência dos valores AEON"""
        if len(values) < 2:
            return 0.0
        
        # Regressão linear simples
        x = np.arange(len(values))
        y = np.array(values)
        
        slope = np.polyfit(x, y, 1)[0]
        return slope
    
    def _generate_trading_signal(self, trend: float, volatility: float, 
                                current_price: float) -> TradingSignal:
        """Gera sinal de trading baseado na análise AEON"""
        
        # Lógica de decisão baseada em AEON
        confidence = min(abs(trend) / volatility, 1.0) if volatility > 0 else 0.5
        
        # Ajusta confiança baseada no fitness do device
        confidence *= self.fitness_score
        
        # Determina ação
        if trend > 0.01 and confidence > 0.6:
            action = 'buy'
            price_target = current_price * (1 + trend * 0.1)
            stop_loss = current_price * 0.98
        elif trend < -0.01 and confidence > 0.6:
            action = 'sell'
            price_target = current_price * (1 + trend * 0.1)
            stop_loss = current_price * 1.02
        else:
            action = 'hold'
            price_target = current_price
            stop_loss = current_price
        
        return TradingSignal(
            signal_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            symbol='BTC/USDT',  # Exemplo
            action=action,
            confidence=confidence,
            price_target=price_target,
            stop_loss=stop_loss,
            device_id=self.device_id,
            fitness_score=self.fitness_score
        )
    
    def _generate_hold_signal(self) -> TradingSignal:
        """Gera sinal de manter posição"""
        return TradingSignal(
            signal_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            symbol='BTC/USDT',
            action='hold',
            confidence=0.5,
            price_target=0.0,
            stop_loss=0.0,
            device_id=self.device_id,
            fitness_score=self.fitness_score
        )
    
    def evolve_parameters(self, performance_feedback: float):
        """Evolui parâmetros AEON baseado no desempenho"""
        
        self.generation += 1
        
        # Taxa de mutação baseada no desempenho
        mutation_rate = 0.05 if performance_feedback > 0 else 0.1
        
        # Mutação dos parâmetros
        for param in self.aeon_params:
            if np.random.random() < mutation_rate:
                # Mutação gaussiana
                mutation = np.random.normal(0, 0.1)
                self.aeon_params[param] *= (1 + mutation)
                
                # Limites para evitar valores extremos
                self.aeon_params[param] = np.clip(
                    self.aeon_params[param], 0.1, 10.0
                )
        
        # Atualiza fitness
        self.fitness_score = max(0.1, self.fitness_score + performance_feedback * 0.1)
        self.fitness_score = min(2.0, self.fitness_score)  # Limite superior
    
    async def connect_to_network(self, master_url: str):
        """Conecta ao AEON Master e à rede P2P"""
        try:
            self.master_connection = await websockets.connect(master_url)
            self.is_online = True
            
            # Registra device na rede
            registration = {
                'type': 'register',
                'device_id': self.device_id,
                'profile': asdict(self.device_profile),
                'aeon_params': self.aeon_params,
                'fitness_score': self.fitness_score
            }
            
            await self.master_connection.send(json.dumps(registration))
            print(f"📱 Mini-AEON {self.device_id} conectado à rede!")
            
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            self.is_online = False
    
    async def sync_with_hive(self, market_insight: Dict):
        """Sincroniza com a mente coletiva AEON"""
        if not self.is_online or not self.master_connection:
            return
        
        try:
            sync_message = {
                'type': 'sync',
                'device_id': self.device_id,
                'insight': market_insight,
                'fitness_score': self.fitness_score,
                'generation': self.generation
            }
            
            await self.master_connection.send(json.dumps(sync_message))
            
        except Exception as e:
            print(f"❌ Erro na sincronização: {e}")
    
    def get_device_stats(self) -> Dict:
        """Retorna estatísticas do mini-AEON"""
        return {
            'device_id': self.device_id,
            'device_type': self.device_profile.device_type,
            'fitness_score': self.fitness_score,
            'generation': self.generation,
            'total_signals': len(self.trading_history),
            'is_online': self.is_online,
            'aeon_params': self.aeon_params,
            'battery_level': self.device_profile.battery_level,
            'last_active': datetime.now().isoformat()
        }

# Exemplo de uso
if __name__ == "__main__":
    # Simula perfil de device iOS
    ios_profile = DeviceProfile(
        device_id=f"ios_{uuid.uuid4().hex[:8]}",
        device_type="ios",
        cpu_cores=6,
        ram_gb=4.0,
        battery_level=0.85,
        network_type="5g",
        location_timezone="America/Sao_Paulo",
        user_risk_tolerance=0.3  # Conservador
    )
    
    # Cria mini-AEON
    mini_aeon = MiniAEON(ios_profile)
    
    # Simula dados de mercado
    market_data = [100 + np.sin(i*0.1) * 5 + np.random.normal(0, 1) 
                   for i in range(50)]
    
    # Analisa padrão e gera sinal
    signal = mini_aeon.analyze_market_pattern(market_data)
    
    print("📊 MINI-AEON TRADING SIGNAL")
    print("=" * 40)
    print(f"Device: {signal.device_id}")
    print(f"Action: {signal.action.upper()}")
    print(f"Confidence: {signal.confidence:.2%}")
    print(f"Target: ${signal.price_target:.2f}")
    print(f"Stop Loss: ${signal.stop_loss:.2f}")
    print(f"Fitness: {signal.fitness_score:.3f}")
    print("\n📱 Device Stats:")
    stats = mini_aeon.get_device_stats()
    for key, value in stats.items():
        if key != 'aeon_params':
            print(f"  {key}: {value}")
