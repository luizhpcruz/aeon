#!/usr/bin/env python3
"""
🌌 AEON Quantum Entropy Analyzer
Sistema avançado de análise de entropia quântica para simulações cosmológicas
Integrado com monitoramento de recursos e otimização automática
"""

import numpy as np
import time
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional, Callable
import threading
import queue
from pathlib import Path
import math
import random

# Tentativa de importar bibliotecas científicas
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️ NumPy não disponível. Usando implementações nativas Python.")

try:
    import scipy.stats as stats
    import scipy.integrate as integrate
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("⚠️ SciPy não disponível. Usando implementações nativas.")

try:
    from aeon_resource_monitor import AeonResourceMonitor
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False
    print("ℹ️ Monitor de recursos não disponível. Funcionando no modo standalone.")

# Implementações nativas para quando numpy não está disponível
class NumpyCompat:
    """Implementações compatíveis com NumPy usando Python puro"""
    
    @staticmethod
    def mean(values):
        return sum(values) / len(values) if values else 0.0
    
    @staticmethod
    def std(values):
        if not values:
            return 0.0
        mean_val = NumpyCompat.mean(values)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
    
    @staticmethod
    def var(values):
        if not values:
            return 0.0
        mean_val = NumpyCompat.mean(values)
        return sum((x - mean_val) ** 2 for x in values) / len(values)
    
    @staticmethod
    def histogram(values, bins=10, density=False):
        if not values:
            return [0] * bins, [0] * (bins + 1)
        
        min_val, max_val = min(values), max(values)
        if min_val == max_val:
            hist = [len(values)] + [0] * (bins - 1)
            bin_edges = [min_val - 0.5, min_val + 0.5] + [min_val + 0.5] * (bins - 1)
            return hist, bin_edges
        
        bin_width = (max_val - min_val) / bins
        hist = [0] * bins
        bin_edges = [min_val + i * bin_width for i in range(bins + 1)]
        
        for value in values:
            bin_idx = min(int((value - min_val) / bin_width), bins - 1)
            hist[bin_idx] += 1
        
        if density:
            total = sum(hist)
            hist = [h / total if total > 0 else 0 for h in hist]
        
        return hist, bin_edges

# Usa numpy se disponível, senão usa implementação nativa
if NUMPY_AVAILABLE:
    np_mean = np.mean
    np_std = np.std
    np_var = np.var
    np_histogram = np.histogram
else:
    np_mean = NumpyCompat.mean
    np_std = NumpyCompat.std
    np_var = NumpyCompat.var
    np_histogram = NumpyCompat.histogram

@dataclass
class QuantumState:
    """Representa um estado quântico no sistema AEON"""
    amplitude: complex
    phase: float
    energy: float
    entropy: float
    timestamp: str
    coherence: float
    entanglement_degree: float

@dataclass
class EntropySnapshot:
    """Snapshot de análise de entropia em um momento específico"""
    timestamp: str
    total_entropy: float
    quantum_entropy: float
    classical_entropy: float
    entanglement_entropy: float
    complexity_index: float
    coherence_level: float
    system_temperature: float
    evolution_rate: float
    dimensional_analysis: Dict[str, float]

class QuantumEntropyAnalyzer:
    """Analisador avançado de entropia quântica para AEON"""
    
    def __init__(self, dimensions: int = 4, system_size: int = 1000):
        self.dimensions = dimensions
        self.system_size = system_size
        self.quantum_states: List[QuantumState] = []
        self.entropy_history: List[EntropySnapshot] = []
        self.is_running = False
        self.evolution_thread: Optional[threading.Thread] = None
        
        # Constantes físicas (unidades naturais)
        self.planck_constant = 1.0  # ℏ = 1 em unidades naturais
        self.boltzmann_constant = 1.0  # kB = 1 em unidades naturais
        self.speed_of_light = 1.0  # c = 1 em unidades naturais
        
        # Parâmetros do sistema quântico
        self.coherence_decay_rate = 0.01
        self.entanglement_threshold = 0.5
        self.thermal_noise_level = 0.05
        
        # Integração com monitoramento de recursos
        self.resource_monitor = AeonResourceMonitor() if MONITORING_AVAILABLE else None
        self.performance_data = []
        
        # Inicialização do sistema
        self._initialize_quantum_system()
        
    def _initialize_quantum_system(self):
        """Inicializa o sistema quântico com estados aleatórios"""
        print("🌌 Inicializando sistema quântico AEON...")
        
        for i in range(self.system_size):
            # Gera estado quântico aleatório normalizado
            amplitude = complex(
                random.gauss(0, 1), 
                random.gauss(0, 1)
            )
            # Normalização
            amplitude = amplitude / abs(amplitude) if abs(amplitude) > 0 else complex(1, 0)
            
            phase = random.uniform(0, 2 * math.pi)
            energy = random.exponential(1.0)  # Distribuição de Boltzmann
            entropy = self._calculate_von_neumann_entropy(amplitude)
            coherence = random.uniform(0.5, 1.0)
            entanglement = random.uniform(0, 1.0)
            
            state = QuantumState(
                amplitude=amplitude,
                phase=phase,
                energy=energy,
                entropy=entropy,
                timestamp=datetime.now().isoformat(),
                coherence=coherence,
                entanglement_degree=entanglement
            )
            
            self.quantum_states.append(state)
        
        print(f"✅ Sistema inicializado com {len(self.quantum_states)} estados quânticos")
        
    def _calculate_von_neumann_entropy(self, amplitude: complex) -> float:
        """Calcula entropia de von Neumann para um estado quântico"""
        # Densidade de probabilidade do estado
        prob = abs(amplitude) ** 2
        
        # Evita log(0)
        if prob <= 1e-15:
            return 0.0
        
        # Entropia de von Neumann: S = -Tr(ρ ln ρ)
        return -prob * math.log(prob)
    
    def calculate_system_entropy(self) -> EntropySnapshot:
        """Calcula snapshot completo de entropia do sistema"""
        start_time = time.time()
        
        # Coleta dados dos estados quânticos
        entropies = [state.entropy for state in self.quantum_states]
        energies = [state.energy for state in self.quantum_states]
        coherences = [state.coherence for state in self.quantum_states]
        entanglements = [state.entanglement_degree for state in self.quantum_states]
        
        # Entropia quântica total (von Neumann)
        quantum_entropy = sum(entropies)
        
        # Entropia clássica (Shannon)
        classical_entropy = self._calculate_shannon_entropy(energies)
        
        # Entropia de emaranhamento
        entanglement_entropy = self._calculate_entanglement_entropy(entanglements)
        
        # Entropia total do sistema
        total_entropy = quantum_entropy + classical_entropy + entanglement_entropy
        
        # Índice de complexidade (baseado na distribuição de estados)
        complexity_index = self._calculate_complexity_index(entropies, energies)
        
        # Nível de coerência médio
        coherence_level = np_mean(coherences) if coherences else 0.0
        
        # Temperatura efetiva do sistema
        system_temperature = self._calculate_effective_temperature(energies)
        
        # Taxa de evolução (mudança temporal)
        evolution_rate = self._calculate_evolution_rate()
        
        # Análise dimensional
        dimensional_analysis = self._perform_dimensional_analysis()
        
        # Tempo de processamento
        processing_time = time.time() - start_time
        
        snapshot = EntropySnapshot(
            timestamp=datetime.now().isoformat(),
            total_entropy=total_entropy,
            quantum_entropy=quantum_entropy,
            classical_entropy=classical_entropy,
            entanglement_entropy=entanglement_entropy,
            complexity_index=complexity_index,
            coherence_level=coherence_level,
            system_temperature=system_temperature,
            evolution_rate=evolution_rate,
            dimensional_analysis=dimensional_analysis
        )
        
        # Armazena dados de performance
        if MONITORING_AVAILABLE:
            self.performance_data.append({
                'timestamp': snapshot.timestamp,
                'processing_time_ms': processing_time * 1000,
                'system_size': len(self.quantum_states),
                'memory_efficient': len(self.quantum_states) < 10000
            })
        
        return snapshot
    
    def _calculate_shannon_entropy(self, values: List[float]) -> float:
        """Calcula entropia de Shannon para distribuição clássica"""
        if not values:
            return 0.0
        
        # Cria histograma para probabilidades
        hist, _ = np_histogram(values, bins=50, density=True)
        
        # Normaliza para obter probabilidades
        hist_sum = sum(hist)
        probabilities = [h / hist_sum for h in hist] if hist_sum > 0 else hist
        
        # Calcula entropia de Shannon
        entropy = 0.0
        for p in probabilities:
            if p > 1e-15:
                entropy -= p * math.log2(p)
        
        return entropy
    
    def _calculate_entanglement_entropy(self, entanglements: List[float]) -> float:
        """Calcula entropia de emaranhamento do sistema"""
        if not entanglements:
            return 0.0
        
        # Entropia baseada no grau médio de emaranhamento
        avg_entanglement = np_mean(entanglements)
        
        # Modelo simplificado de entropia de emaranhamento
        # S_ent = -∑ λi log λi onde λi são autovalores da matriz densidade reduzida
        if avg_entanglement > self.entanglement_threshold:
            return -avg_entanglement * math.log(avg_entanglement) - (1 - avg_entanglement) * math.log(1 - avg_entanglement)
        else:
            return 0.1 * avg_entanglement  # Emaranhamento fraco
    
    def _calculate_complexity_index(self, entropies: List[float], energies: List[float]) -> float:
        """Calcula índice de complexidade do sistema"""
        if not entropies or not energies:
            return 0.0
        
        # Complexidade baseada na correlação entre entropia e energia
        if SCIPY_AVAILABLE:
            correlation, _ = stats.pearsonr(entropies, energies)
            complexity = abs(correlation) * np_std(entropies) * np_std(energies)
        else:
            # Implementação nativa
            entropy_std = np_std(entropies)
            energy_std = np_std(energies)
            complexity = entropy_std * energy_std
        
        return min(complexity, 10.0)  # Normaliza entre 0-10
    
    def _calculate_effective_temperature(self, energies: List[float]) -> float:
        """Calcula temperatura efetiva do sistema"""
        if not energies:
            return 0.0
        
        # Temperatura relacionada à energia média: T = <E> / kB
        avg_energy = np_mean(energies)
        temperature = avg_energy / self.boltzmann_constant
        
        return temperature
    
    def _calculate_evolution_rate(self) -> float:
        """Calcula taxa de evolução temporal do sistema"""
        if len(self.entropy_history) < 2:
            return 0.0
        
        # Taxa baseada na mudança de entropia total
        current = self.entropy_history[-1]
        previous = self.entropy_history[-2]
        
        time_diff = (datetime.fromisoformat(current.timestamp) - 
                    datetime.fromisoformat(previous.timestamp)).total_seconds()
        
        if time_diff > 0:
            entropy_change = current.total_entropy - previous.total_entropy
            return entropy_change / time_diff
        
        return 0.0
    
    def _perform_dimensional_analysis(self) -> Dict[str, float]:
        """Realiza análise dimensional do sistema"""
        analysis = {}
        
        # Dimensão fractal baseada na distribuição de estados
        energies = [state.energy for state in self.quantum_states]
        if energies:
            # Estimativa de dimensão fractal usando box-counting simplificado
            analysis['fractal_dimension'] = self._estimate_fractal_dimension(energies)
        
        # Dimensão de emaranhamento
        entanglements = [state.entanglement_degree for state in self.quantum_states]
        if entanglements:
            high_entanglement = sum(1 for e in entanglements if e > self.entanglement_threshold)
            analysis['entanglement_dimension'] = high_entanglement / len(entanglements)
        
        # Dimensão espectral (baseada na distribuição de energia)
        if energies:
            analysis['spectral_dimension'] = self._calculate_spectral_dimension(energies)
        
        # Dimensão informacional
        total_info = sum(state.entropy for state in self.quantum_states)
        analysis['information_dimension'] = min(total_info / len(self.quantum_states), self.dimensions)
        
        return analysis
    
    def _estimate_fractal_dimension(self, values: List[float]) -> float:
        """Estima dimensão fractal usando método box-counting simplificado"""
        if len(values) < 10:
            return 1.0
        
        # Normaliza valores entre 0 e 1
        min_val, max_val = min(values), max(values)
        if max_val - min_val == 0:
            return 1.0
        
        normalized = [(v - min_val) / (max_val - min_val) for v in values]
        
        # Box-counting com diferentes escalas
        scales = [0.1, 0.05, 0.02, 0.01]
        counts = []
        
        for scale in scales:
            boxes = set()
            for val in normalized:
                box_id = int(val / scale)
                boxes.add(box_id)
            counts.append(len(boxes))
        
        # Calcula dimensão pela inclinação log-log
        if len(counts) >= 2 and counts[0] > 0 and counts[-1] > 0:
            log_scales = [math.log(1/s) for s in scales]
            log_counts = [math.log(c) for c in counts]
            
            # Regressão linear simples
            n = len(log_scales)
            slope = (n * sum(x*y for x,y in zip(log_scales, log_counts)) - 
                    sum(log_scales) * sum(log_counts)) / (n * sum(x*x for x in log_scales) - sum(log_scales)**2)
            
            return max(0.1, min(slope, 3.0))  # Limita entre 0.1 e 3.0
        
        return 1.5  # Valor padrão
    
    def _calculate_spectral_dimension(self, energies: List[float]) -> float:
        """Calcula dimensão espectral baseada na distribuição de energia"""
        if not energies:
            return 2.0
        
        # Análise da densidade espectral de estados
        hist, bins = np_histogram(energies, bins=20)
        
        # Dimensão espectral relacionada à distribuição de densidade
        non_zero_bins = sum(1 for count in hist if count > 0)
        spectral_dim = non_zero_bins / len(hist) * self.dimensions
        
        return max(1.0, min(spectral_dim, self.dimensions))
    
    def evolve_system(self, time_step: float = 0.1):
        """Evolui o sistema quântico por um passo temporal"""
        for i, state in enumerate(self.quantum_states):
            # Evolução unitária: |ψ(t+dt)⟩ = U(dt)|ψ(t)⟩
            # U(dt) = exp(-iHdt/ℏ) ≈ 1 - iHdt/ℏ para dt pequeno
            
            # Evolução da fase
            phase_evolution = state.energy * time_step / self.planck_constant
            new_phase = (state.phase + phase_evolution) % (2 * math.pi)
            
            # Evolução da amplitude (incluindo decoerência)
            decoherence_factor = math.exp(-self.coherence_decay_rate * time_step)
            new_amplitude = state.amplitude * decoherence_factor
            
            # Evolução da coerência
            new_coherence = state.coherence * decoherence_factor + random.gauss(0, self.thermal_noise_level)
            new_coherence = max(0.0, min(new_coherence, 1.0))
            
            # Evolução do emaranhamento (dinâmica complexa)
            entanglement_drift = random.gauss(0, 0.01)
            new_entanglement = state.entanglement_degree + entanglement_drift
            new_entanglement = max(0.0, min(new_entanglement, 1.0))
            
            # Recalcula entropia
            new_entropy = self._calculate_von_neumann_entropy(new_amplitude)
            
            # Atualiza estado
            self.quantum_states[i] = QuantumState(
                amplitude=new_amplitude,
                phase=new_phase,
                energy=state.energy,  # Energia conservada
                entropy=new_entropy,
                timestamp=datetime.now().isoformat(),
                coherence=new_coherence,
                entanglement_degree=new_entanglement
            )
    
    def start_continuous_evolution(self, time_step: float = 0.1, analysis_interval: int = 10):
        """Inicia evolução contínua do sistema com análise periódica"""
        if self.is_running:
            print("⚠️ Sistema já está em execução")
            return
        
        self.is_running = True
        print(f"🚀 Iniciando evolução contínua (dt={time_step}, análise a cada {analysis_interval}s)")
        
        def evolution_loop():
            step_count = 0
            last_analysis = time.time()
            
            while self.is_running:
                try:
                    # Evolui sistema
                    self.evolve_system(time_step)
                    step_count += 1
                    
                    # Análise periódica
                    current_time = time.time()
                    if current_time - last_analysis >= analysis_interval:
                        snapshot = self.calculate_system_entropy()
                        self.entropy_history.append(snapshot)
                        
                        # Limita histórico
                        if len(self.entropy_history) > 1000:
                            self.entropy_history = self.entropy_history[-1000:]
                        
                        # Log de progresso
                        print(f"📊 Step {step_count}: S_total={snapshot.total_entropy:.3f}, "
                              f"T_eff={snapshot.system_temperature:.3f}, "
                              f"Coherence={snapshot.coherence_level:.3f}")
                        
                        last_analysis = current_time
                    
                    # Pequena pausa para não sobrecarregar
                    time.sleep(time_step / 10)
                    
                except KeyboardInterrupt:
                    print("\n🛑 Evolução interrompida pelo usuário")
                    break
                except Exception as e:
                    print(f"❌ Erro na evolução: {e}")
                    time.sleep(1)
        
        self.evolution_thread = threading.Thread(target=evolution_loop, daemon=True)
        self.evolution_thread.start()
    
    def stop_evolution(self):
        """Para a evolução contínua"""
        self.is_running = False
        if self.evolution_thread:
            self.evolution_thread.join(timeout=5)
        print("🔄 Evolução parada")
    
    def generate_analysis_report(self) -> Dict:
        """Gera relatório completo de análise"""
        if not self.entropy_history:
            current_snapshot = self.calculate_system_entropy()
            self.entropy_history.append(current_snapshot)
        
        latest = self.entropy_history[-1]
        
        # Estatísticas temporais
        if len(self.entropy_history) > 1:
            entropies = [s.total_entropy for s in self.entropy_history]
            temps = [s.system_temperature for s in self.entropy_history]
            coherences = [s.coherence_level for s in self.entropy_history]
            
            temporal_stats = {
                'entropy_trend': {
                    'mean': np_mean(entropies),
                    'std': np_std(entropies),
                    'min': min(entropies),
                    'max': max(entropies),
                    'current': entropies[-1]
                },
                'temperature_evolution': {
                    'mean': np_mean(temps),
                    'current': temps[-1],
                    'stability': 1.0 - (np_std(temps) / np_mean(temps) if np_mean(temps) > 0 else 0)
                },
                'coherence_dynamics': {
                    'mean': np_mean(coherences),
                    'current': coherences[-1],
                    'decay_rate': self._estimate_decay_rate(coherences)
                }
            }
        else:
            temporal_stats = {'note': 'Dados insuficientes para análise temporal'}
        
        # Análise de estabilidade
        stability_analysis = self._analyze_system_stability()
        
        # Previsões
        predictions = self._generate_predictions()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_overview': {
                'total_states': len(self.quantum_states),
                'dimensions': self.dimensions,
                'evolution_steps': len(self.entropy_history),
                'current_entropy': latest.total_entropy,
                'system_health': self._assess_system_health(latest)
            },
            'current_state': asdict(latest),
            'temporal_analysis': temporal_stats,
            'stability_analysis': stability_analysis,
            'predictions': predictions,
            'performance_metrics': self._analyze_performance(),
            'recommendations': self._generate_recommendations(latest)
        }
        
        return report
    
    def _estimate_decay_rate(self, values: List[float]) -> float:
        """Estima taxa de decaimento de uma série temporal"""
        if len(values) < 3:
            return 0.0
        
        # Ajuste exponencial simples
        times = list(range(len(values)))
        try:
            # ln(y) = ln(A) - λt
            log_values = [math.log(max(v, 1e-10)) for v in values]
            
            # Regressão linear
            n = len(times)
            sum_t = sum(times)
            sum_ln_y = sum(log_values)
            sum_t2 = sum(t*t for t in times)
            sum_t_ln_y = sum(t*ln_y for t, ln_y in zip(times, log_values))
            
            slope = (n * sum_t_ln_y - sum_t * sum_ln_y) / (n * sum_t2 - sum_t * sum_t)
            return -slope  # Taxa de decaimento
            
        except (ValueError, ZeroDivisionError):
            return 0.0
    
    def _analyze_system_stability(self) -> Dict:
        """Analisa estabilidade do sistema quântico"""
        if len(self.entropy_history) < 10:
            return {'status': 'insufficient_data'}
        
        recent_entropies = [s.total_entropy for s in self.entropy_history[-10:]]
        recent_temps = [s.system_temperature for s in self.entropy_history[-10:]]
        
        entropy_variance = np_var(recent_entropies)
        temp_variance = np_var(recent_temps)
        
        # Critérios de estabilidade
        entropy_stable = entropy_variance < 0.1
        temp_stable = temp_variance < 0.5
        
        stability_score = (
            (0.5 if entropy_stable else 0) +
            (0.5 if temp_stable else 0)
        )
        
        return {
            'overall_stability': stability_score,
            'entropy_stable': entropy_stable,
            'temperature_stable': temp_stable,
            'entropy_variance': entropy_variance,
            'temperature_variance': temp_variance,
            'status': 'stable' if stability_score > 0.7 else 'unstable' if stability_score < 0.3 else 'moderate'
        }
    
    def _generate_predictions(self) -> Dict:
        """Gera previsões baseadas na evolução do sistema"""
        if len(self.entropy_history) < 5:
            return {'note': 'Dados insuficientes para previsões'}
        
        # Previsão simples baseada em tendência linear
        recent_entropies = [s.total_entropy for s in self.entropy_history[-5:]]
        times = list(range(len(recent_entropies)))
        
        # Regressão linear
        n = len(times)
        sum_t = sum(times)
        sum_s = sum(recent_entropies)
        sum_t2 = sum(t*t for t in times)
        sum_ts = sum(t*s for t, s in zip(times, recent_entropies))
        
        if n * sum_t2 - sum_t * sum_t != 0:
            slope = (n * sum_ts - sum_t * sum_s) / (n * sum_t2 - sum_t * sum_t)
            intercept = (sum_s - slope * sum_t) / n
            
            # Previsão para próximos passos
            future_steps = [5, 10, 20]
            predictions = {}
            
            for step in future_steps:
                predicted_entropy = intercept + slope * (len(recent_entropies) + step)
                predictions[f'entropy_in_{step}_steps'] = predicted_entropy
            
            predictions['trend'] = 'increasing' if slope > 0.01 else 'decreasing' if slope < -0.01 else 'stable'
            predictions['trend_strength'] = abs(slope)
            
            return predictions
        
        return {'note': 'Previsão não disponível'}
    
    def _analyze_performance(self) -> Dict:
        """Analisa performance computacional"""
        if not self.performance_data:
            return {'note': 'Dados de performance não disponíveis'}
        
        processing_times = [d['processing_time_ms'] for d in self.performance_data]
        
        return {
            'average_processing_time_ms': np_mean(processing_times),
            'max_processing_time_ms': max(processing_times),
            'min_processing_time_ms': min(processing_times),
            'total_analyses': len(self.performance_data),
            'performance_trend': 'improving' if len(processing_times) > 1 and processing_times[-1] < processing_times[0] else 'stable'
        }
    
    def _assess_system_health(self, snapshot: EntropySnapshot) -> str:
        """Avalia saúde geral do sistema"""
        health_score = 0
        max_score = 5
        
        # Critério 1: Entropia não divergente
        if 0.1 < snapshot.total_entropy < 100:
            health_score += 1
        
        # Critério 2: Coerência adequada
        if snapshot.coherence_level > 0.3:
            health_score += 1
        
        # Critério 3: Temperatura controlada
        if 0.1 < snapshot.system_temperature < 10:
            health_score += 1
        
        # Critério 4: Complexidade moderada
        if 0.1 < snapshot.complexity_index < 5:
            health_score += 1
        
        # Critério 5: Evolução estável
        if abs(snapshot.evolution_rate) < 1.0:
            health_score += 1
        
        health_ratio = health_score / max_score
        
        if health_ratio >= 0.8:
            return 'excellent'
        elif health_ratio >= 0.6:
            return 'good'
        elif health_ratio >= 0.4:
            return 'moderate'
        else:
            return 'poor'
    
    def _generate_recommendations(self, snapshot: EntropySnapshot) -> List[str]:
        """Gera recomendações baseadas no estado atual"""
        recommendations = []
        
        # Análise de entropia
        if snapshot.total_entropy > 50:
            recommendations.append("🔥 Entropia muito alta. Considere reduzir temperatura ou tamanho do sistema")
        elif snapshot.total_entropy < 0.1:
            recommendations.append("❄️ Entropia muito baixa. Sistema pode estar super-resfriado")
        
        # Análise de coerência
        if snapshot.coherence_level < 0.2:
            recommendations.append("🌪️ Coerência muito baixa. Reduza ruído térmico ou aumente isolamento")
        elif snapshot.coherence_level > 0.9:
            recommendations.append("🔒 Coerência muito alta. Sistema pode estar artificialmente isolado")
        
        # Análise de complexidade
        if snapshot.complexity_index > 8:
            recommendations.append("🧩 Sistema muito complexo. Considere simplificar interações")
        elif snapshot.complexity_index < 0.5:
            recommendations.append("📐 Sistema muito simples. Adicione mais interações ou aumentar dimensionalidade")
        
        # Análise dimensional
        if 'fractal_dimension' in snapshot.dimensional_analysis:
            fractal_dim = snapshot.dimensional_analysis['fractal_dimension']
            if fractal_dim > 2.5:
                recommendations.append("🌀 Estrutura fractal complexa detectada. Monitor para auto-organização")
        
        # Análise temporal
        if abs(snapshot.evolution_rate) > 2.0:
            recommendations.append("⚡ Evolução muito rápida. Reduza passo temporal ou força de interação")
        
        # Performance
        if len(self.quantum_states) > 5000:
            recommendations.append("💾 Sistema grande detectado. Monitor uso de RAM com aeon_resource_monitor.py")
        
        # Padrão geral
        if not recommendations:
            recommendations.append("✅ Sistema operando dentro dos parâmetros normais")
        
        return recommendations
    
    def export_data(self, filepath: Optional[str] = None) -> str:
        """Exporta dados completos para análise externa"""
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"aeon_quantum_entropy_{timestamp}.json"
        
        # Prepara dados para export
        export_data = {
            'metadata': {
                'export_timestamp': datetime.now().isoformat(),
                'system_parameters': {
                    'dimensions': self.dimensions,
                    'system_size': self.system_size,
                    'coherence_decay_rate': self.coherence_decay_rate,
                    'entanglement_threshold': self.entanglement_threshold,
                    'thermal_noise_level': self.thermal_noise_level
                },
                'total_snapshots': len(self.entropy_history),
                'total_states': len(self.quantum_states)
            },
            'entropy_evolution': [asdict(snapshot) for snapshot in self.entropy_history],
            'final_analysis': self.generate_analysis_report(),
            'performance_data': self.performance_data[-100:] if self.performance_data else []  # Últimos 100 registros
        }
        
        # Salva arquivo
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        file_size = Path(filepath).stat().st_size / 1024  # KB
        print(f"💾 Dados exportados para {filepath} ({file_size:.1f} KB)")
        
        return filepath

def main():
    """Função principal - demonstração do sistema"""
    print("🌌 AEON Quantum Entropy Analyzer")
    print("=" * 50)
    
    # Inicializa analisador
    analyzer = QuantumEntropyAnalyzer(dimensions=4, system_size=500)
    
    # Análise inicial
    print("\n📊 Análise inicial do sistema...")
    initial_snapshot = analyzer.calculate_system_entropy()
    analyzer.entropy_history.append(initial_snapshot)
    
    print(f"🔬 Entropia total: {initial_snapshot.total_entropy:.3f}")
    print(f"🌡️ Temperatura efetiva: {initial_snapshot.system_temperature:.3f}")
    print(f"✨ Coerência: {initial_snapshot.coherence_level:.3f}")
    print(f"🧩 Complexidade: {initial_snapshot.complexity_index:.3f}")
    
    # Simulação de evolução
    print("\n🚀 Iniciando simulação de evolução temporal...")
    for i in range(10):
        analyzer.evolve_system(time_step=0.1)
        
        if i % 3 == 0:  # Análise a cada 3 passos
            snapshot = analyzer.calculate_system_entropy()
            analyzer.entropy_history.append(snapshot)
            print(f"  Step {i+1}: S={snapshot.total_entropy:.3f}, T={snapshot.system_temperature:.3f}")
    
    # Relatório final
    print("\n📋 Gerando relatório final...")
    report = analyzer.generate_analysis_report()
    
    print(f"\n🎯 Saúde do sistema: {report['system_overview']['system_health'].upper()}")
    print(f"📈 Evolução: {report.get('temporal_analysis', {}).get('entropy_trend', {}).get('current', 'N/A')}")
    
    # Recomendações
    print("\n💡 Recomendações:")
    for rec in report['recommendations']:
        print(f"  {rec}")
    
    # Export de dados
    export_file = analyzer.export_data()
    print(f"\n💾 Dados completos exportados para: {export_file}")
    
    # Integração com monitoramento de recursos
    if MONITORING_AVAILABLE:
        print("\n🔧 Análise de recursos:")
        resource_health = analyzer.resource_monitor.generate_health_report()
        print(f"  Sistema: {resource_health['overall_health']}")
        if 'current_resources' in resource_health:
            ram_usage = resource_health['current_resources']['current_status']['ram_usage_percent']
            print(f"  RAM: {ram_usage}%")
    
    print("\n✅ Análise concluída! Sistema AEON funcionando perfeitamente.")

if __name__ == "__main__":
    main()
