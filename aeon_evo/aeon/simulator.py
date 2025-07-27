"""
AEON Simulator - Simulação Evolutiva
====================================

Módulo responsável pela simulação de cadeias evolutivas usando a equação AEON.
Inclui funcionalidades para múltiplas espécies, gerações e análise temporal.

Desenvolvido por Luiz Cruz - 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import logging
from typing import List, Dict, Tuple, Optional
from .engine import AeonEngine, analyze_stability, find_equilibrium_points

logger = logging.getLogger(__name__)

class AeonSimulator:
    """
    Simulador principal para evolução de sistemas usando equações AEON.
    """
    
    def __init__(self, output_dir: str = "aeon/output"):
        self.engine = AeonEngine()
        self.output_dir = output_dir
        self.simulation_results = {}
        self.time_range = None
        
    def simulate_chain(self, n_species: int, t_range: float, 
                      params_list: List[List[float]], 
                      chain_params: Optional[List[Dict]] = None,
                      n_points: int = 1000) -> Tuple[np.ndarray, List[np.ndarray]]:
        """
        Simula uma cadeia evolutiva de n espécies.
        
        Args:
            n_species: Número de espécies/gerações
            t_range: Intervalo de tempo total
            params_list: Lista de parâmetros [A, B, phi, C, lambd, D] para cada espécie
            chain_params: Parâmetros de ligação entre gerações
            n_points: Número de pontos na simulação
            
        Returns:
            Tupla (tempo, resultados) onde resultados é lista de arrays
        """
        logger.info(f"Iniciando simulação de cadeia com {n_species} espécies")
        
        # Criar array de tempo
        t = np.linspace(0.01, t_range, n_points)
        self.time_range = t
        
        # Converter parâmetros para formato do engine
        params_dicts = []
        for params in params_list[:n_species]:
            if len(params) >= 6:
                params_dict = {
                    'A': params[0],
                    'B': params[1], 
                    'phi': params[2],
                    'C': params[3],
                    'lambd': params[4],
                    'D': params[5]
                }
                params_dicts.append(params_dict)
            else:
                logger.warning(f"Parâmetros insuficientes: {params}. Usando defaults.")
                params_dicts.append({
                    'A': 1.0, 'B': 1.0, 'phi': 0.0,
                    'C': 1.0, 'lambd': 0.1, 'D': 1.0
                })
        
        # Executar simulação
        try:
            results = self.engine.compute_chain(t, params_dicts, chain_params)
            
            # Armazenar resultados
            self.simulation_results = {
                'time': t,
                'species_results': results,
                'parameters': params_dicts,
                'chain_parameters': chain_params,
                'statistics': self.engine.get_statistics(results)
            }
            
            logger.info("Simulação concluída com sucesso")
            return t, results
            
        except Exception as e:
            logger.error(f"Erro durante simulação: {e}")
            raise
    
    def simulate_single_species(self, t_range: float, params: List[float],
                               n_points: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simula uma única espécie.
        
        Args:
            t_range: Intervalo de tempo
            params: Parâmetros [A, B, phi, C, lambd, D]
            n_points: Número de pontos
            
        Returns:
            Tupla (tempo, resultado)
        """
        t = np.linspace(0.01, t_range, n_points)
        self.time_range = t
        
        params_dict = {
            'A': params[0] if len(params) > 0 else 1.0,
            'B': params[1] if len(params) > 1 else 1.0,
            'phi': params[2] if len(params) > 2 else 0.0,
            'C': params[3] if len(params) > 3 else 1.0,
            'lambd': params[4] if len(params) > 4 else 0.1,
            'D': params[5] if len(params) > 5 else 1.0
        }
        
        result = self.engine.compute_single(t, params_dict)
        return t, result
    
    def simulate_with_mutations(self, base_params: List[float], 
                               n_generations: int, mutation_rate: float = 0.1,
                               t_range: float = 50.0) -> Dict:
        """
        Simula evolução com mutações aleatórias.
        
        Args:
            base_params: Parâmetros base
            n_generations: Número de gerações
            mutation_rate: Taxa de mutação (0-1)
            t_range: Intervalo de tempo
            
        Returns:
            Dicionário com resultados da evolução
        """
        logger.info(f"Simulando {n_generations} gerações com mutação")
        
        generations = []
        params_evolution = []
        current_params = base_params.copy()
        
        for gen in range(n_generations):
            # Aplicar mutação
            if gen > 0:
                for i in range(len(current_params)):
                    if np.random.random() < mutation_rate:
                        # Mutação gaussiana
                        mutation = np.random.normal(0, abs(current_params[i]) * 0.1)
                        current_params[i] += mutation
            
            # Simular geração atual
            t, result = self.simulate_single_species(t_range, current_params)
            
            generations.append(result)
            params_evolution.append(current_params.copy())
            
            # Seleção natural: modifica parâmetros baseado no "fitness"
            fitness = self._calculate_fitness(result)
            if fitness > 0.5:  # Se fitness alto, preserve mais
                mutation_rate *= 0.95
            else:  # Se fitness baixo, mute mais
                mutation_rate *= 1.05
                
            mutation_rate = np.clip(mutation_rate, 0.01, 0.5)
        
        return {
            'time': t,
            'generations': generations,
            'parameters_evolution': params_evolution,
            'mutation_rates': mutation_rate,
            'final_fitness': self._calculate_fitness(generations[-1])
        }
    
    def _calculate_fitness(self, result: np.ndarray) -> float:
        """
        Calcula fitness de uma geração (simplicado).
        
        Args:
            result: Array com resultados da geração
            
        Returns:
            Valor de fitness (0-1)
        """
        # Fitness baseado em estabilidade e crescimento
        stability = 1.0 / (1.0 + np.std(result[-100:]))  # Mais estável = melhor
        growth = np.tanh(np.mean(result[-100:]))  # Crescimento moderado = melhor
        
        return (stability + growth) / 2.0
    
    def analyze_results(self) -> Dict:
        """
        Analisa os resultados da última simulação.
        
        Returns:
            Dicionário com análises detalhadas
        """
        if not self.simulation_results:
            raise ValueError("Nenhuma simulação executada ainda")
        
        results = self.simulation_results['species_results']
        t = self.simulation_results['time']
        
        analysis = {
            'stability_analysis': [],
            'equilibrium_points': [],
            'cross_correlations': [],
            'dominant_frequencies': [],
            'evolution_summary': {}
        }
        
        # Análise para cada espécie
        for i, result in enumerate(results):
            # Análise de estabilidade
            stability = analyze_stability(t, result)
            analysis['stability_analysis'].append(stability)
            
            # Pontos de equilíbrio
            equilibrium = find_equilibrium_points(t, result)
            analysis['equilibrium_points'].append(equilibrium)
            
            # Análise de frequência (FFT)
            fft = np.fft.fft(result)
            frequencies = np.fft.fftfreq(len(result))
            dominant_freq_idx = np.argmax(np.abs(fft[1:len(fft)//2])) + 1
            dominant_freq = frequencies[dominant_freq_idx]
            analysis['dominant_frequencies'].append(dominant_freq)
        
        # Correlações cruzadas entre espécies
        for i in range(len(results)):
            for j in range(i+1, len(results)):
                correlation = np.corrcoef(results[i], results[j])[0, 1]
                analysis['cross_correlations'].append({
                    'species_pair': (i, j),
                    'correlation': correlation
                })
        
        # Resumo da evolução
        stats = self.simulation_results['statistics']
        analysis['evolution_summary'] = {
            'total_generations': stats['generations'],
            'evolution_trends': stats['evolution_trend'],
            'final_diversity': np.std(stats['mean_values']),
            'convergence': all(abs(trend) < 0.1 for trend in stats['evolution_trend'][-3:])
        }
        
        return analysis
    
    def save_results(self, filename: str = "results.txt"):
        """
        Salva os resultados em arquivo texto.
        
        Args:
            filename: Nome do arquivo
        """
        if not self.simulation_results:
            raise ValueError("Nenhuma simulação executada ainda")
        
        filepath = f"{self.output_dir}/{filename}"
        
        try:
            with open(filepath, "w", encoding='utf-8') as f:
                f.write("# SIMULAÇÃO AEON - RESULTADOS\n")
                f.write(f"# Desenvolvido por Luiz Cruz - 2025\n")
                f.write(f"# Gerações: {len(self.simulation_results['species_results'])}\n")
                f.write(f"# Pontos temporais: {len(self.simulation_results['time'])}\n\n")
                
                # Salvar dados de tempo
                f.write("# TEMPO\n")
                for t_val in self.simulation_results['time']:
                    f.write(f"{t_val:.6f}\n")
                f.write("\n")
                
                # Salvar resultados de cada espécie
                for i, result in enumerate(self.simulation_results['species_results']):
                    f.write(f"# ESPÉCIE {i+1}\n")
                    for val in result:
                        f.write(f"{val:.6f}\n")
                    f.write("\n")
                
                # Salvar estatísticas
                stats = self.simulation_results['statistics']
                f.write("# ESTATÍSTICAS\n")
                f.write(f"# Médias: {stats['mean_values']}\n")
                f.write(f"# Desvios: {stats['std_values']}\n")
                f.write(f"# Tendências: {stats['evolution_trend']}\n")
            
            logger.info(f"Resultados salvos em {filepath}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar resultados: {e}")
            raise
    
    def save_logs(self, filename: str = "logs.txt"):
        """
        Salva logs da simulação.
        
        Args:
            filename: Nome do arquivo de logs
        """
        filepath = f"{self.output_dir}/{filename}"
        
        try:
            with open(filepath, "w", encoding='utf-8') as f:
                f.write("# LOGS DA SIMULAÇÃO AEON\n")
                f.write(f"# Desenvolvido por Luiz Cruz - 2025\n\n")
                
                if self.simulation_results:
                    f.write("# PARÂMETROS UTILIZADOS\n")
                    for i, params in enumerate(self.simulation_results['parameters']):
                        f.write(f"Espécie {i+1}: {params}\n")
                    
                    f.write("\n# ANÁLISE DOS RESULTADOS\n")
                    analysis = self.analyze_results()
                    
                    for i, stability in enumerate(analysis['stability_analysis']):
                        f.write(f"Espécie {i+1} - Estável: {stability['is_stable']}\n")
                        f.write(f"  Valor final: {stability['final_value']:.6f}\n")
                        f.write(f"  Taxa convergência: {stability['convergence_rate']:.6f}\n")
                    
                    f.write(f"\n# RESUMO EVOLUTIVO\n")
                    summary = analysis['evolution_summary']
                    f.write(f"Gerações: {summary['total_generations']}\n")
                    f.write(f"Diversidade final: {summary['final_diversity']:.6f}\n")
                    f.write(f"Convergiu: {summary['convergence']}\n")
            
            logger.info(f"Logs salvos em {filepath}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar logs: {e}")
            raise
    
    def plot_results(self, save_plot: bool = True, filename: str = "evolution_plot.png"):
        """
        Plota os resultados da simulação.
        
        Args:
            save_plot: Se deve salvar o gráfico
            filename: Nome do arquivo da imagem
        """
        if not self.simulation_results:
            raise ValueError("Nenhuma simulação executada ainda")
        
        t = self.simulation_results['time']
        results = self.simulation_results['species_results']
        
        plt.figure(figsize=(12, 8))
        
        # Plot principal
        plt.subplot(2, 2, 1)
        for i, result in enumerate(results):
            plt.plot(t, result, label=f'Espécie {i+1}', linewidth=2)
        plt.xlabel('Tempo')
        plt.ylabel('Valor F(t)')
        plt.title('Evolução das Espécies AEON')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot de fases
        plt.subplot(2, 2, 2)
        if len(results) >= 2:
            plt.plot(results[0], results[1], 'b-', alpha=0.7)
            plt.xlabel('Espécie 1')
            plt.ylabel('Espécie 2')
            plt.title('Diagrama de Fase')
            plt.grid(True, alpha=0.3)
        
        # Plot de estatísticas
        plt.subplot(2, 2, 3)
        stats = self.simulation_results['statistics']
        generations = range(1, len(stats['mean_values']) + 1)
        plt.bar(generations, stats['mean_values'], alpha=0.7)
        plt.xlabel('Geração')
        plt.ylabel('Valor Médio')
        plt.title('Valores Médios por Geração')
        plt.grid(True, alpha=0.3)
        
        # Plot de tendências
        plt.subplot(2, 2, 4)
        if stats['evolution_trend']:
            trend_gens = range(2, len(stats['evolution_trend']) + 2)
            plt.plot(trend_gens, stats['evolution_trend'], 'ro-')
            plt.axhline(y=0, color='k', linestyle='--', alpha=0.5)
            plt.xlabel('Geração')
            plt.ylabel('Tendência de Mudança')
            plt.title('Evolução das Tendências')
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_plot:
            filepath = f"{self.output_dir}/{filename}"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em {filepath}")
        
        plt.show()
    
    def reset(self):
        """Reset do simulador."""
        self.engine.reset()
        self.simulation_results.clear()
        self.time_range = None
