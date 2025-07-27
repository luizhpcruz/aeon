"""
🎓 AEON EDUCATIONAL MODULE - Sistema Educacional Evolutivo
Transformando AEON em ferramenta de ensino para evolução, ecologia e algoritmos genéticos
Desenvolvido por Luiz Cruz - 2025
"""

import math
import random
import time
from datetime import datetime

class EvolutionEducator:
    """Sistema educacional para ensinar evolução"""
    
    def __init__(self):
        self.population = []
        self.generation = 1
        self.environment_pressure = 0.5
        self.mutation_rate = 0.1
        self.lesson_data = {}
        
    def create_organism(self, traits=None):
        """Cria um organismo com características"""
        if not traits:
            traits = {
                'size': random.uniform(0.1, 2.0),
                'speed': random.uniform(0.1, 1.5),
                'intelligence': random.uniform(0.1, 1.0),
                'adaptability': random.uniform(0.1, 1.0),
                'energy_efficiency': random.uniform(0.1, 1.0)
            }
        
        return {
            'id': len(self.population) + 1,
            'traits': traits,
            'fitness': 0,
            'age': 0,
            'offspring': 0,
            'survival_time': 0
        }
    
    def calculate_fitness(self, organism):
        """Calcula fitness baseado no ambiente"""
        traits = organism['traits']
        
        # Fitness é influenciado pelo ambiente
        if self.environment_pressure < 0.3:  # Ambiente favorável
            fitness = (traits['size'] * 0.3 + 
                      traits['energy_efficiency'] * 0.4 + 
                      traits['intelligence'] * 0.3)
        elif self.environment_pressure > 0.7:  # Ambiente hostil
            fitness = (traits['speed'] * 0.4 + 
                      traits['adaptability'] * 0.4 + 
                      traits['intelligence'] * 0.2)
        else:  # Ambiente neutro
            fitness = sum(traits.values()) / len(traits)
            
        organism['fitness'] = fitness
        return fitness
    
    def natural_selection(self):
        """Seleciona organismos para reprodução"""
        # Calcula fitness de todos
        for organism in self.population:
            self.calculate_fitness(organism)
        
        # Ordena por fitness
        self.population.sort(key=lambda x: x['fitness'], reverse=True)
        
        # Mantém top 50%
        survivors = self.population[:len(self.population)//2]
        
        return survivors
    
    def reproduce(self, parent1, parent2):
        """Reprodução com crossover e mutação"""
        child_traits = {}
        
        for trait in parent1['traits']:
            # Crossover: mistura traits dos pais
            if random.random() < 0.5:
                child_traits[trait] = parent1['traits'][trait]
            else:
                child_traits[trait] = parent2['traits'][trait]
            
            # Mutação
            if random.random() < self.mutation_rate:
                mutation = random.uniform(-0.2, 0.2)
                child_traits[trait] = max(0.1, min(2.0, child_traits[trait] + mutation))
        
        return self.create_organism(child_traits)
    
    def evolve_generation(self):
        """Evolui uma geração completa"""
        if len(self.population) < 4:
            return
        
        # Seleção natural
        survivors = self.natural_selection()
        
        # Nova população com reprodução
        new_population = survivors.copy()
        
        while len(new_population) < len(self.population):
            parent1 = random.choice(survivors)
            parent2 = random.choice(survivors)
            child = self.reproduce(parent1, parent2)
            new_population.append(child)
        
        self.population = new_population
        self.generation += 1
        
        # Atualiza dados da lição
        self.update_lesson_data()
    
    def update_lesson_data(self):
        """Atualiza dados para ensino"""
        if not self.population:
            return
            
        avg_traits = {}
        for trait in self.population[0]['traits']:
            avg_traits[trait] = sum(org['traits'][trait] for org in self.population) / len(self.population)
        
        self.lesson_data = {
            'generation': self.generation,
            'population_size': len(self.population),
            'avg_fitness': sum(org['fitness'] for org in self.population) / len(self.population),
            'avg_traits': avg_traits,
            'best_organism': max(self.population, key=lambda x: x['fitness']),
            'diversity': self.calculate_diversity(),
            'environment_pressure': self.environment_pressure
        }
    
    def calculate_diversity(self):
        """Calcula diversidade genética"""
        if len(self.population) < 2:
            return 0
        
        trait_variances = []
        for trait in self.population[0]['traits']:
            values = [org['traits'][trait] for org in self.population]
            variance = sum((x - sum(values)/len(values))**2 for x in values) / len(values)
            trait_variances.append(variance)
        
        return sum(trait_variances) / len(trait_variances)

class EcologySimulator:
    """Simulador de ecossistemas"""
    
    def __init__(self):
        self.ecosystem = {
            'predators': [],
            'herbivores': [],
            'plants': [],
            'resources': 1000,
            'carrying_capacity': 100,
            'time': 0
        }
        self.food_chain = []
        
    def add_species(self, species_type, count=10):
        """Adiciona espécie ao ecossistema"""
        for i in range(count):
            organism = {
                'id': f"{species_type}_{i}",
                'type': species_type,
                'energy': 100,
                'age': 0,
                'reproduction_ready': False
            }
            
            if species_type == 'predator':
                organism.update({
                    'hunt_success': random.uniform(0.3, 0.8),
                    'energy_consumption': random.uniform(15, 25)
                })
            elif species_type == 'herbivore':
                organism.update({
                    'foraging_efficiency': random.uniform(0.4, 0.9),
                    'energy_consumption': random.uniform(8, 15)
                })
            elif species_type == 'plant':
                organism.update({
                    'growth_rate': random.uniform(0.5, 1.5),
                    'energy_production': random.uniform(20, 40)
                })
            
            self.ecosystem[f"{species_type}s"].append(organism)
    
    def simulate_step(self):
        """Simula um passo do ecossistema"""
        self.time += 1
        
        # Plantas crescem
        self.grow_plants()
        
        # Herbívoros se alimentam
        self.herbivores_feed()
        
        # Predadores caçam
        self.predators_hunt()
        
        # Envelhecimento e morte
        self.age_and_death()
        
        # Reprodução
        self.reproduction()
        
        # Atualiza recursos
        self.update_resources()
    
    def grow_plants(self):
        """Crescimento das plantas"""
        for plant in self.ecosystem['plants']:
            if self.ecosystem['resources'] > 0:
                growth = plant['growth_rate'] * min(1.0, self.ecosystem['resources'] / 500)
                plant['energy'] += growth * plant['energy_production']
                self.ecosystem['resources'] -= growth
    
    def herbivores_feed(self):
        """Herbívoros se alimentam de plantas"""
        for herbivore in self.ecosystem['herbivores']:
            if self.ecosystem['plants']:
                plant = random.choice(self.ecosystem['plants'])
                energy_gained = herbivore['foraging_efficiency'] * min(plant['energy'], 30)
                herbivore['energy'] += energy_gained
                plant['energy'] -= energy_gained
                
                if plant['energy'] <= 0:
                    self.ecosystem['plants'].remove(plant)
            
            herbivore['energy'] -= herbivore['energy_consumption']
    
    def predators_hunt(self):
        """Predadores caçam herbívoros"""
        for predator in self.ecosystem['predators']:
            if self.ecosystem['herbivores'] and random.random() < predator['hunt_success']:
                prey = random.choice(self.ecosystem['herbivores'])
                predator['energy'] += 80
                self.ecosystem['herbivores'].remove(prey)
            
            predator['energy'] -= predator['energy_consumption']
    
    def age_and_death(self):
        """Envelhecimento e morte natural"""
        for species_type in ['predators', 'herbivores', 'plants']:
            species_list = self.ecosystem[species_type]
            for organism in species_list[:]:  # Cópia para modificação segura
                organism['age'] += 1
                
                # Morte por energia baixa
                if organism['energy'] <= 0:
                    species_list.remove(organism)
                # Morte por idade
                elif organism['age'] > 100:
                    species_list.remove(organism)
                # Pronto para reprodução
                elif organism['age'] > 20 and organism['energy'] > 150:
                    organism['reproduction_ready'] = True
    
    def reproduction(self):
        """Reprodução das espécies"""
        for species_type in ['predators', 'herbivores', 'plants']:
            ready_organisms = [org for org in self.ecosystem[f"{species_type}"] 
                             if org.get('reproduction_ready', False)]
            
            while len(ready_organisms) >= 2:
                parent1 = ready_organisms.pop()
                parent2 = ready_organisms.pop()
                
                # Cria offspring
                if len(self.ecosystem[f"{species_type}"]) < self.ecosystem['carrying_capacity']:
                    self.add_species(species_type[:-1], 1)  # Remove 's' do final
                
                # Remove energia dos pais
                parent1['energy'] -= 50
                parent2['energy'] -= 50
                parent1['reproduction_ready'] = False
                parent2['reproduction_ready'] = False
    
    def update_resources(self):
        """Atualiza recursos do ambiente"""
        # Regeneração natural de recursos
        if self.ecosystem['resources'] < 1000:
            self.ecosystem['resources'] += 10
    
    def get_ecosystem_stats(self):
        """Retorna estatísticas do ecossistema"""
        return {
            'time': self.time,
            'predator_count': len(self.ecosystem['predators']),
            'herbivore_count': len(self.ecosystem['herbivores']),
            'plant_count': len(self.ecosystem['plants']),
            'resources': self.ecosystem['resources'],
            'total_biomass': sum(org['energy'] for species in ['predators', 'herbivores', 'plants'] 
                               for org in self.ecosystem[species])
        }

class GeneticAlgorithmTeacher:
    """Ensina algoritmos genéticos através de exemplos práticos"""
    
    def __init__(self):
        self.problem_type = "optimization"
        self.population_size = 50
        self.chromosome_length = 10
        self.population = []
        self.generation = 0
        self.target = None
        
    def create_chromosome(self):
        """Cria um cromossomo (solução candidata)"""
        if self.problem_type == "binary":
            return [random.randint(0, 1) for _ in range(self.chromosome_length)]
        elif self.problem_type == "numeric":
            return [random.uniform(-10, 10) for _ in range(self.chromosome_length)]
        else:  # optimization
            return [random.random() for _ in range(self.chromosome_length)]
    
    def fitness_function(self, chromosome):
        """Função de fitness dependendo do problema"""
        if self.problem_type == "binary":
            # Problema: maximizar número de 1s
            return sum(chromosome)
        elif self.problem_type == "numeric":
            # Problema: minimizar soma dos quadrados
            return 1 / (1 + sum(x**2 for x in chromosome))
        else:  # optimization
            # Problema: encontrar máximo de função complexa
            x = sum(chromosome) / len(chromosome)
            return abs(math.sin(x * math.pi) * math.cos(x * 2 * math.pi))
    
    def selection(self):
        """Seleção por torneio"""
        selected = []
        for _ in range(self.population_size):
            tournament = random.sample(self.population, 3)
            winner = max(tournament, key=lambda x: x['fitness'])
            selected.append(winner)
        return selected
    
    def crossover(self, parent1, parent2):
        """Crossover de um ponto"""
        point = random.randint(1, len(parent1['chromosome']) - 1)
        child1_chromosome = parent1['chromosome'][:point] + parent2['chromosome'][point:]
        child2_chromosome = parent2['chromosome'][:point] + parent1['chromosome'][point:]
        
        return [
            {'chromosome': child1_chromosome, 'fitness': 0},
            {'chromosome': child2_chromosome, 'fitness': 0}
        ]
    
    def mutation(self, chromosome, rate=0.1):
        """Mutação dos genes"""
        for i in range(len(chromosome)):
            if random.random() < rate:
                if self.problem_type == "binary":
                    chromosome[i] = 1 - chromosome[i]
                elif self.problem_type == "numeric":
                    chromosome[i] += random.uniform(-1, 1)
                else:  # optimization
                    chromosome[i] = random.random()
        return chromosome
    
    def evolve_step(self):
        """Um passo da evolução do algoritmo genético"""
        # Avalia fitness
        for individual in self.population:
            individual['fitness'] = self.fitness_function(individual['chromosome'])
        
        # Seleção
        selected = self.selection()
        
        # Nova geração
        new_population = []
        
        # Elitismo: mantém melhor indivíduo
        best = max(self.population, key=lambda x: x['fitness'])
        new_population.append(best)
        
        # Crossover e mutação
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(selected, 2)
            children = self.crossover(parent1, parent2)
            
            for child in children:
                child['chromosome'] = self.mutation(child['chromosome'])
                if len(new_population) < self.population_size:
                    new_population.append(child)
        
        self.population = new_population
        self.generation += 1
    
    def get_teaching_data(self):
        """Retorna dados para ensino"""
        if not self.population:
            return {}
        
        fitnesses = [ind['fitness'] for ind in self.population]
        best_individual = max(self.population, key=lambda x: x['fitness'])
        
        return {
            'generation': self.generation,
            'population_size': len(self.population),
            'best_fitness': max(fitnesses),
            'avg_fitness': sum(fitnesses) / len(fitnesses),
            'worst_fitness': min(fitnesses),
            'best_chromosome': best_individual['chromosome'],
            'diversity': self.calculate_diversity(),
            'convergence': self.check_convergence()
        }
    
    def calculate_diversity(self):
        """Calcula diversidade da população"""
        if len(self.population) < 2:
            return 0
        
        total_distance = 0
        comparisons = 0
        
        for i in range(len(self.population)):
            for j in range(i+1, len(self.population)):
                distance = sum(abs(a - b) for a, b in 
                             zip(self.population[i]['chromosome'], 
                                 self.population[j]['chromosome']))
                total_distance += distance
                comparisons += 1
        
        return total_distance / comparisons if comparisons > 0 else 0
    
    def check_convergence(self):
        """Verifica se algoritmo convergiu"""
        fitnesses = [ind['fitness'] for ind in self.population]
        variance = sum((f - sum(fitnesses)/len(fitnesses))**2 for f in fitnesses) / len(fitnesses)
        return variance < 0.01

def initialize_educational_modules():
    """Inicializa todos os módulos educacionais"""
    
    # Simulador de evolução
    evolution = EvolutionEducator()
    for _ in range(20):
        evolution.population.append(evolution.create_organism())
    
    # Simulador de ecologia
    ecology = EcologySimulator()
    ecology.add_species('plant', 30)
    ecology.add_species('herbivore', 15)
    ecology.add_species('predator', 5)
    
    # Professor de algoritmos genéticos
    genetic_teacher = GeneticAlgorithmTeacher()
    genetic_teacher.population = [
        {'chromosome': genetic_teacher.create_chromosome(), 'fitness': 0}
        for _ in range(genetic_teacher.population_size)
    ]
    
    return {
        'evolution': evolution,
        'ecology': ecology,
        'genetic_algorithm': genetic_teacher
    }

if __name__ == "__main__":
    # Teste dos módulos educacionais
    modules = initialize_educational_modules()
    
    print("🎓 AEON Educational Modules Initialized!")
    print("📚 Evolution Educator: Ready")
    print("🌿 Ecology Simulator: Ready") 
    print("🧬 Genetic Algorithm Teacher: Ready")
    
    # Demonstração rápida
    for i in range(5):
        print(f"\n--- Step {i+1} ---")
        
        # Evolução
        modules['evolution'].evolve_generation()
        evolution_data = modules['evolution'].lesson_data
        print(f"Evolution Gen {evolution_data.get('generation', 0)}: Avg Fitness = {evolution_data.get('avg_fitness', 0):.3f}")
        
        # Ecologia
        modules['ecology'].simulate_step()
        ecology_stats = modules['ecology'].get_ecosystem_stats()
        print(f"Ecology Time {ecology_stats['time']}: Plants={ecology_stats['plant_count']}, Herbivores={ecology_stats['herbivore_count']}, Predators={ecology_stats['predator_count']}")
        
        # Algoritmo Genético
        modules['genetic_algorithm'].evolve_step()
        ga_data = modules['genetic_algorithm'].get_teaching_data()
        print(f"GA Gen {ga_data.get('generation', 0)}: Best Fitness = {ga_data.get('best_fitness', 0):.3f}")
