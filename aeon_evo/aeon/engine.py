"""
AEON Engine - Implementação da Equação AEON
==========================================

Módulo principal que implementa a equação matemática do AEON:
F(t) = A * sin(Bt + φ) + C * e^(-λt) + D * log(t + 1)

Desenvolvido por Luiz Cruz - 2025
"""

import numpy as np
import logging
from typing import Union, List, Tuple

logger = logging.getLogger(__name__)

def aeon_equation(t: Union[float, np.ndarray], A: float, B: float, phi: float, 
                  C: float, lambd: float, D: float) -> Union[float, np.ndarray]:
    """
    Equação principal do AEON que modela crescimento, interação e mutação.
    
    Args:
        t: Tempo (pode ser escalar ou array)
        A: Amplitude da oscilação
        B: Frequência da oscilação  
        phi: Fase da oscilação
        C: Amplitude do decaimento exponencial
        lambd: Taxa de decaimento
        D: Influência logarítmica (memória acumulativa)
        
    Returns:
        Valor da função AEON no tempo t
        
    Formula:
        F(t) = A * sin(Bt + φ) + C * e^(-λt) + D * log(t + 1)
    """
    try:
        # Componente oscilatório (fatores externos)
        oscillatory = A * np.sin(B * t + phi)
        
        # Componente de decaimento/estabilidade estrutural
        decay = C * np.exp(-lambd * t)
        
        # Componente de memória/influência acumulativa
        memory = D * np.log(t + 1)
        
        return oscillatory + decay + memory
        
    except Exception as e:
        logger.error(f"Erro no cálculo da equação AEON: {e}")
        raise

def aeon_chain_equation(prev_value: float, prev_derivative: float, 
                       alpha: float, beta: float, gamma: float) -> float:
    """
    Equação AEON para cadeia ligada entre espécies/gerações.
    
    Args:
        prev_value: Valor da geração anterior F(n-1)
        prev_derivative: Derivada da geração anterior dF(n-1)/dt
        alpha: Coeficiente de herança
        beta: Coeficiente de mudança
        gamma: Offset/mutação
        
    Returns:
        Novo valor da cadeia
        
    Formula:
        Fₙ(t) = Fₙ₋₁(t) * αₙ + βₙ * dFₙ₋₁/dt + γₙ
    """
    try:
        return prev_value * alpha + beta * prev_derivative + gamma
    except Exception as e:
        logger.error(f"Erro no cálculo da cadeia AEON: {e}")
        raise

def calculate_derivative(t: np.ndarray, values: np.ndarray) -> np.ndarray:
    """
    Calcula a derivada numérica de uma função.
    
    Args:
        t: Array de tempo
        values: Array de valores da função
        
    Returns:
        Array com as derivadas
    """
    try:
        return np.gradient(values, t)
    except Exception as e:
        logger.error(f"Erro no cálculo da derivada: {e}")
        raise

class AeonEngine:
    """
    Engine principal para computação das equações AEON.
    """
    
    def __init__(self):
        self.history = []
        self.parameters_history = []
        
    def compute_single(self, t: Union[float, np.ndarray], 
                      params: dict) -> Union[float, np.ndarray]:
        """
        Computa a equação AEON para um conjunto de parâmetros.
        
        Args:
            t: Tempo
            params: Dicionário com parâmetros {A, B, phi, C, lambd, D}
            
        Returns:
            Resultado da equação
        """
        result = aeon_equation(
            t=t,
            A=params.get('A', 1.0),
            B=params.get('B', 1.0),
            phi=params.get('phi', 0.0),
            C=params.get('C', 1.0),
            lambd=params.get('lambd', 0.1),
            D=params.get('D', 1.0)
        )
        
        # Armazenar no histórico
        self.history.append(result)
        self.parameters_history.append(params.copy())
        
        return result
    
    def compute_chain(self, t: np.ndarray, params_list: List[dict], 
                     chain_params: List[dict] = None) -> List[np.ndarray]:
        """
        Computa uma cadeia evolutiva de equações AEON.
        
        Args:
            t: Array de tempo
            params_list: Lista de parâmetros para cada espécie/geração
            chain_params: Parâmetros de ligação da cadeia (alpha, beta, gamma)
            
        Returns:
            Lista com resultados de cada geração
        """
        results = []
        
        # Primeira geração - computação padrão
        first_result = self.compute_single(t, params_list[0])
        results.append(first_result)
        
        # Gerações subsequentes - influenciadas pela anterior
        for i in range(1, len(params_list)):
            # Pegar resultado anterior
            prev_result = results[-1]
            prev_derivative = calculate_derivative(t, prev_result)
            
            # Parâmetros de cadeia (usar defaults se não fornecidos)
            if chain_params and i-1 < len(chain_params):
                alpha = chain_params[i-1].get('alpha', 1.0)
                beta = chain_params[i-1].get('beta', 0.1)
                gamma = chain_params[i-1].get('gamma', 0.0)
            else:
                alpha, beta, gamma = 1.0, 0.1, 0.0
            
            # Modificar parâmetros baseado na geração anterior
            modified_params = params_list[i].copy()
            
            # Influência da geração anterior nos parâmetros
            influence_factor = np.mean(prev_result) / 10.0
            modified_params['A'] *= (1 + influence_factor * alpha)
            modified_params['C'] *= (1 + np.std(prev_result) * beta)
            modified_params['D'] += gamma
            
            # Computar nova geração
            current_result = self.compute_single(t, modified_params)
            
            # Aplicar equação de cadeia se necessário
            if chain_params:
                chain_influence = aeon_chain_equation(
                    prev_value=np.mean(prev_result),
                    prev_derivative=np.mean(prev_derivative),
                    alpha=alpha,
                    beta=beta,
                    gamma=gamma
                )
                current_result += chain_influence * 0.1  # Fator de escala
            
            results.append(current_result)
        
        return results
    
    def get_statistics(self, results: List[np.ndarray]) -> dict:
        """
        Calcula estatísticas dos resultados.
        
        Args:
            results: Lista de resultados das gerações
            
        Returns:
            Dicionário com estatísticas
        """
        stats = {
            'generations': len(results),
            'mean_values': [np.mean(r) for r in results],
            'std_values': [np.std(r) for r in results],
            'min_values': [np.min(r) for r in results],
            'max_values': [np.max(r) for r in results],
            'evolution_trend': []
        }
        
        # Calcular tendência de evolução
        for i in range(1, len(results)):
            trend = np.mean(results[i]) - np.mean(results[i-1])
            stats['evolution_trend'].append(trend)
        
        return stats
    
    def reset(self):
        """Reset do engine."""
        self.history.clear()
        self.parameters_history.clear()


# Funções auxiliares para análise
def analyze_stability(t: np.ndarray, values: np.ndarray, 
                     threshold: float = 0.1) -> dict:
    """
    Analisa a estabilidade de uma série temporal.
    
    Args:
        t: Array de tempo
        values: Array de valores
        threshold: Limiar para determinar estabilidade
        
    Returns:
        Dicionário com análise de estabilidade
    """
    derivative = calculate_derivative(t, values)
    
    return {
        'is_stable': np.all(np.abs(derivative[-100:]) < threshold),
        'final_value': values[-1],
        'convergence_rate': np.mean(np.abs(derivative[-100:])),
        'oscillation_amplitude': np.std(values[-100:])
    }

def find_equilibrium_points(t: np.ndarray, values: np.ndarray) -> List[int]:
    """
    Encontra pontos de equilíbrio na série temporal.
    
    Args:
        t: Array de tempo
        values: Array de valores
        
    Returns:
        Lista de índices dos pontos de equilíbrio
    """
    derivative = calculate_derivative(t, values)
    
    # Pontos onde a derivada cruza zero
    equilibrium_indices = []
    for i in range(1, len(derivative)):
        if derivative[i-1] * derivative[i] <= 0:  # Mudança de sinal
            equilibrium_indices.append(i)
    
    return equilibrium_indices
