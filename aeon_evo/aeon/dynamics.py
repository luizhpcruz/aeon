"""
AEON Dynamics - Lógicas de Cadeias e Interações
===============================================

Módulo responsável pela implementação de dinâmicas complexas entre
espécies, interações ecológicas e padrões emergentes.

Desenvolvido por Luiz Cruz - 2025
"""

import numpy as np
import logging
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
@dataclass
class SpeciesParameters:
    """Parâmetros de uma espécie no sistema AEON."""
    A: float = 1.0      # Amplitude oscilação
    B: float = 1.0      # Frequência oscilação
    phi: float = 0.0    # Fase oscilação
    C: float = 1.0      # Amplitude decaimento
    lambd: float = 0.1  # Taxa decaimento
    D: float = 1.0      # Influência logarítmica
    id: str = ""        # Identificador da espécie
    fitness: float = 1.0
    population: float = 1.0

@dataclass
class InteractionRule:
    """Regra de interação entre espécies."""
    species_a: str
    species_b: str
    interaction_type: str  # 'competition', 'predation', 'symbiosis', 'neutral'
    strength: float
    effect_function: Optional[Callable] = None

class ChainDynamics:
    """
    Gerenciador principal das dinâmicas de cadeia AEON.
    """
    
    def __init__(self):
        self.species = {}
        self.interactions = []
        self.network_topology = {}
        self.history = []
        
    def add_species(self, species: SpeciesParameters):
        """
        Adiciona uma nova espécie ao sistema.
        
        Args:
            species: Parâmetros da espécie
        """
        self.species[species.id] = species
        self.network_topology[species.id] = []
        logger.info(f"Espécie {species.id} adicionada ao sistema")
    
    def add_interaction(self, rule: InteractionRule):
        """
        Adiciona uma regra de interação entre espécies.
        
        Args:
            rule: Regra de interação
        """
        self.interactions.append(rule)
        
        # Atualizar topologia da rede
        if rule.species_a in self.network_topology:
            self.network_topology[rule.species_a].append(rule.species_b)
        if rule.species_b in self.network_topology:
            self.network_topology[rule.species_b].append(rule.species_a)
            
        logger.info(f"Interação {rule.interaction_type} adicionada: {rule.species_a} <-> {rule.species_b}")
    
    def compute_interaction_effects(self, species_id: str, t: float, 
                                  current_values: Dict[str, float]) -> float:
        """
        Computa efeitos de interação para uma espécie.
        
        Args:
            species_id: ID da espécie
            t: Tempo atual
            current_values: Valores atuais de todas as espécies
            
        Returns:
            Efeito total das interações
        """
        total_effect = 0.0
        
        for interaction in self.interactions:
            if interaction.species_a == species_id:
                partner_id = interaction.species_b
                effect = self._calculate_interaction_effect(
                    interaction, current_values.get(species_id, 0.0),
                    current_values.get(partner_id, 0.0), t
                )
                total_effect += effect
                
            elif interaction.species_b == species_id:
                partner_id = interaction.species_a
                effect = self._calculate_interaction_effect(
                    interaction, current_values.get(species_id, 0.0),
                    current_values.get(partner_id, 0.0), t
                )
                total_effect += effect
        
        return total_effect
    
    def _calculate_interaction_effect(self, interaction: InteractionRule,
                                    value_a: float, value_b: float, t: float) -> float:
        """
        Calcula o efeito específico de uma interação.
        
        Args:
            interaction: Regra de interação
            value_a: Valor da espécie A
            value_b: Valor da espécie B
            t: Tempo atual
            
        Returns:
            Efeito da interação
        """
        if interaction.effect_function:
            return interaction.effect_function(value_a, value_b, t) * interaction.strength
        
        # Efeitos padrão baseados no tipo de interação
        if interaction.interaction_type == 'competition':
            # Competição: reduz crescimento baseado na população do competidor
            return -interaction.strength * value_b * value_a * 0.1
            
        elif interaction.interaction_type == 'predation':
            # Predação: aumenta predador, diminui presa
            if interaction.species_a in self.species:  # A é predador
                return interaction.strength * value_b * 0.1
            else:  # B é predador
                return -interaction.strength * value_b * 0.1
                
        elif interaction.interaction_type == 'symbiosis':
            # Simbiose: benefício mútuo
            return interaction.strength * value_b * 0.05
            
        elif interaction.interaction_type == 'neutral':
            # Interação neutra
            return 0.0
            
        return 0.0
    
    def evolve_parameters(self, species_id: str, fitness: float, 
                         mutation_rate: float = 0.01):
        """
        Evolui os parâmetros de uma espécie baseado no fitness.
        
        Args:
            species_id: ID da espécie
            fitness: Fitness atual
            mutation_rate: Taxa de mutação
        """
        if species_id not in self.species:
            return
        
        species = self.species[species_id]
        species.fitness = fitness
        
        # Mutação adaptativa: maior fitness = menor mutação
        effective_mutation = mutation_rate * (2.0 - fitness)
        
        # Aplicar mutações nos parâmetros
        if np.random.random() < effective_mutation:
            species.A += np.random.normal(0, abs(species.A) * 0.1)
        if np.random.random() < effective_mutation:
            species.B += np.random.normal(0, abs(species.B) * 0.1)
        if np.random.random() < effective_mutation:
            species.phi += np.random.normal(0, 0.1)
        if np.random.random() < effective_mutation:
            species.C += np.random.normal(0, abs(species.C) * 0.1)
        if np.random.random() < effective_mutation:
            species.lambd = max(0.001, species.lambd + np.random.normal(0, species.lambd * 0.1))
        if np.random.random() < effective_mutation:
            species.D += np.random.normal(0, abs(species.D) * 0.1)
            
        # Manter parâmetros em faixas válidas
        species.A = np.clip(species.A, 0.1, 10.0)
        species.B = np.clip(species.B, 0.1, 10.0)
        species.phi = np.clip(species.phi, -np.pi, np.pi)
        species.C = np.clip(species.C, 0.1, 10.0)
        species.lambd = np.clip(species.lambd, 0.001, 1.0)
        species.D = np.clip(species.D, 0.1, 10.0)
    
    def simulate_ecosystem(self, t_range: float, n_points: int = 1000) -> Dict:
        """
        Simula todo o ecossistema com interações.
        
        Args:
            t_range: Intervalo de tempo
            n_points: Número de pontos temporais
            
        Returns:
            Dicionário com resultados da simulação
        """
        from .engine import aeon_equation
        
        t = np.linspace(0.01, t_range, n_points)
        results = {}
        interaction_effects = {}
        
        # Inicializar resultados
        for species_id in self.species:
            results[species_id] = np.zeros(n_points)
            interaction_effects[species_id] = np.zeros(n_points)
        
        # Simular passo a passo para considerar interações
        for i, time_point in enumerate(t):
            current_values = {}
            
            # Primeiro, calcular valores base sem interações
            for species_id, species in self.species.items():
                base_value = aeon_equation(
                    time_point, species.A, species.B, species.phi,
                    species.C, species.lambd, species.D
                )
                current_values[species_id] = base_value
            
            # Depois, aplicar efeitos de interação
            for species_id in self.species:
                interaction_effect = self.compute_interaction_effects(
                    species_id, time_point, current_values
                )
                interaction_effects[species_id][i] = interaction_effect
                
                # Valor final com interações
                final_value = current_values[species_id] + interaction_effect
                results[species_id][i] = final_value
        
        # Calcular fitness de cada espécie
        fitness_values = {}
        for species_id, result in results.items():
            fitness_values[species_id] = self._calculate_ecosystem_fitness(result)
            
        return {
            'time': t,
            'species_results': results,
            'interaction_effects': interaction_effects,
            'fitness_values': fitness_values,
            'network_topology': self.network_topology.copy()
        }
    
    def _calculate_ecosystem_fitness(self, result: np.ndarray) -> float:
        """
        Calcula fitness de uma espécie no contexto do ecossistema.
        
        Args:
            result: Array com valores da espécie ao longo do tempo
            
        Returns:
            Valor de fitness
        """
        # Fitness baseado em múltiplos critérios
        stability = 1.0 / (1.0 + np.std(result[-100:]))
        sustainability = 1.0 / (1.0 + abs(np.mean(result[-50:]) - np.mean(result[:50])))
        growth = np.tanh(np.mean(result[-100:]))
        
        # Penalizar valores extremos
        extreme_penalty = 1.0 / (1.0 + np.sum(np.abs(result) > 100) / len(result))
        
        return (stability + sustainability + growth + extreme_penalty) / 4.0
    
    def analyze_network_properties(self) -> Dict:
        """
        Analisa propriedades da rede de interações.
        
        Returns:
            Dicionário com propriedades da rede
        """
        n_species = len(self.species)
        n_interactions = len(self.interactions)
        
        # Calcular grau de cada nó
        degrees = {}
        for species_id in self.species:
            degrees[species_id] = len(self.network_topology[species_id])
        
        # Calcular centralidade
        centrality = {}
        for species_id in self.species:
            centrality[species_id] = degrees[species_id] / max(1, n_species - 1)
        
        # Densidade da rede
        max_connections = n_species * (n_species - 1) / 2
        density = n_interactions / max_connections if max_connections > 0 else 0
        
        # Tipos de interação
        interaction_types = {}
        for interaction in self.interactions:
            itype = interaction.interaction_type
            interaction_types[itype] = interaction_types.get(itype, 0) + 1
        
        return {
            'n_species': n_species,
            'n_interactions': n_interactions,
            'density': density,
            'degrees': degrees,
            'centrality': centrality,
            'interaction_types': interaction_types,
            'most_connected': max(degrees.items(), key=lambda x: x[1]) if degrees else None
        }
    
    def run_evolutionary_simulation(self, generations: int, t_range: float,
                                   mutation_rate: float = 0.01) -> Dict:
        """
        Executa simulação evolutiva com múltiplas gerações.
        
        Args:
            generations: Número de gerações
            t_range: Intervalo de tempo por geração
            mutation_rate: Taxa de mutação
            
        Returns:
            Resultados da evolução
        """
        evolution_history = []
        fitness_history = []
        
        for gen in range(generations):
            logger.info(f"Simulando geração {gen + 1}/{generations}")
            
            # Simular ecossistema atual
            sim_results = self.simulate_ecosystem(t_range)
            
            # Armazenar histórico
            evolution_history.append({
                'generation': gen,
                'species_params': {sid: vars(species.copy() if hasattr(species, 'copy') else species) 
                                 for sid, species in self.species.items()},
                'results': sim_results
            })
            
            # Evoluir parâmetros baseado no fitness
            generation_fitness = {}
            for species_id, fitness in sim_results['fitness_values'].items():
                generation_fitness[species_id] = fitness
                self.evolve_parameters(species_id, fitness, mutation_rate)
            
            fitness_history.append(generation_fitness)
            
            # Adaptação da taxa de mutação
            avg_fitness = np.mean(list(generation_fitness.values()))
            if avg_fitness > 0.7:
                mutation_rate *= 0.95  # Reduzir mutação se fitness alto
            elif avg_fitness < 0.3:
                mutation_rate *= 1.05  # Aumentar mutação se fitness baixo
                
            mutation_rate = np.clip(mutation_rate, 0.001, 0.1)
        
        return {
            'evolution_history': evolution_history,
            'fitness_history': fitness_history,
            'final_mutation_rate': mutation_rate,
            'network_properties': self.analyze_network_properties()
        }
    
    def create_default_ecosystem(self, n_species: int = 3) -> None:
        """
        Cria um ecossistema padrão para testes.
        
        Args:
            n_species: Número de espécies
        """
        self.species.clear()
        self.interactions.clear()
        self.network_topology.clear()
        
        # Criar espécies
        for i in range(n_species):
            species = SpeciesParameters(
                id=f"species_{i+1}",
                A=1.0 + np.random.normal(0, 0.2),
                B=1.0 + np.random.normal(0, 0.3),
                phi=np.random.uniform(-np.pi/4, np.pi/4),
                C=0.5 + np.random.normal(0, 0.1),
                lambd=0.01 + np.random.uniform(0, 0.05),
                D=1.0 + np.random.normal(0, 0.2)
            )
            self.add_species(species)
        
        # Criar interações aleatórias
        species_list = list(self.species.keys())
        for i in range(len(species_list)):
            for j in range(i+1, len(species_list)):
                if np.random.random() < 0.5:  # 50% chance de interação
                    interaction_types = ['competition', 'predation', 'symbiosis', 'neutral']
                    itype = np.random.choice(interaction_types)
                    strength = np.random.uniform(0.1, 0.5)
                    
                    rule = InteractionRule(
                        species_a=species_list[i],
                        species_b=species_list[j],
                        interaction_type=itype,
                        strength=strength
                    )
                    self.add_interaction(rule)
        
        logger.info(f"Ecossistema padrão criado com {n_species} espécies")


# Funções auxiliares para criação de interações específicas

def create_predator_prey_system(predator_params: List[float], 
                               prey_params: List[float]) -> ChainDynamics:
    """
    Cria um sistema predador-presa simples.
    
    Args:
        predator_params: Parâmetros do predador [A, B, phi, C, lambd, D]
        prey_params: Parâmetros da presa [A, B, phi, C, lambd, D]
        
    Returns:
        Sistema de dinâmica configurado
    """
    dynamics = ChainDynamics()
    
    # Criar espécies
    predator = SpeciesParameters(A=predator_params[0], B=predator_params[1], 
                                phi=predator_params[2], C=predator_params[3],
                                lambd=predator_params[4], D=predator_params[5], 
                                id="predator")
    prey = SpeciesParameters(A=prey_params[0], B=prey_params[1], 
                           phi=prey_params[2], C=prey_params[3],
                           lambd=prey_params[4], D=prey_params[5], 
                           id="prey")
    
    dynamics.add_species(predator)
    dynamics.add_species(prey)
    
    # Criar interação de predação
    rule = InteractionRule(
        species_a="predator",
        species_b="prey", 
        interaction_type="predation",
        strength=0.3
    )
    dynamics.add_interaction(rule)
    
    return dynamics

def create_competitive_system(species_params: List[List[float]]) -> ChainDynamics:
    """
    Cria um sistema competitivo com múltiplas espécies.
    
    Args:
        species_params: Lista de parâmetros para cada espécie
        
    Returns:
        Sistema de dinâmica configurado
    """
    dynamics = ChainDynamics()
    
    # Criar espécies
    for i, params in enumerate(species_params):
        species = SpeciesParameters(A=params[0], B=params[1], phi=params[2], 
                                  C=params[3], lambd=params[4], D=params[5],
                                  id=f"competitor_{i+1}")
        dynamics.add_species(species)
    
    # Criar competição entre todas as espécies
    species_ids = list(dynamics.species.keys())
    for i in range(len(species_ids)):
        for j in range(i+1, len(species_ids)):
            rule = InteractionRule(
                species_a=species_ids[i],
                species_b=species_ids[j],
                interaction_type="competition",
                strength=0.2
            )
            dynamics.add_interaction(rule)
    
    return dynamics
