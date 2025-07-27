"""
AEON Evolution - Main Entry Point
=================================

Ponto de entrada principal para o simulador AEON evolutivo.
Implementa a equação F(t) = A * sin(Bt + φ) + C * e^(-λt) + D * log(t + 1)
com cadeia dinâmica entre espécies.

Desenvolvido por Luiz Cruz - 2025
"""

import os
import sys
import logging
from pathlib import Path

# Adicionar o diretório aeon ao path
sys.path.append(str(Path(__file__).parent))

from aeon.simulator import AeonSimulator
from aeon.dynamics import ChainDynamics, create_predator_prey_system, create_competitive_system

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_output_directory():
    """Cria diretório de output se não existir."""
    output_dir = Path("aeon/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    return str(output_dir)

def run_basic_simulation():
    """Executa simulação básica com 3 espécies."""
    logger.info("🚀 Iniciando Simulação AEON Básica")
    
    # Parâmetros para 3 espécies
    params = [
        [1.0, 2.0, 0.1, 0.5, 0.01, 1.0],  # espécie 1
        [0.8, 1.5, 0.2, 0.4, 0.02, 1.2],  # espécie 2  
        [1.2, 2.5, 0.3, 0.6, 0.01, 0.9],  # espécie 3
    ]
    
    # Criar simulador
    output_dir = create_output_directory()
    simulator = AeonSimulator(output_dir)
    
    # Executar simulação
    t, results = simulator.simulate_chain(
        n_species=3,
        t_range=50,
        params_list=params,
        n_points=1000
    )
    
    # Salvar resultados
    simulator.save_results("basic_results.txt")
    simulator.save_logs("basic_logs.txt")
    
    # Análise
    analysis = simulator.analyze_results()
    logger.info(f"✅ Simulação concluída - {analysis['evolution_summary']['total_generations']} gerações")
    
    return simulator, analysis

def run_ecosystem_simulation():
    """Executa simulação de ecossistema com interações."""
    logger.info("🌱 Iniciando Simulação de Ecossistema")
    
    # Criar sistema de dinâmica
    dynamics = ChainDynamics()
    dynamics.create_default_ecosystem(n_species=4)
    
    # Executar simulação evolutiva
    evolution_results = dynamics.run_evolutionary_simulation(
        generations=10,
        t_range=30,
        mutation_rate=0.02
    )
    
    # Salvar resultados do ecossistema
    output_dir = create_output_directory()
    
    with open(f"{output_dir}/ecosystem_results.txt", "w", encoding='utf-8') as f:
        f.write("# SIMULAÇÃO DE ECOSSISTEMA AEON\n")
        f.write("# Desenvolvido por Luiz Cruz - 2025\n\n")
        
        # Salvar propriedades da rede
        network_props = evolution_results['network_properties']
        f.write("# PROPRIEDADES DA REDE\n")
        f.write(f"Espécies: {network_props['n_species']}\n")
        f.write(f"Interações: {network_props['n_interactions']}\n") 
        f.write(f"Densidade: {network_props['density']:.4f}\n")
        f.write(f"Mais conectada: {network_props['most_connected']}\n\n")
        
        # Salvar evolução do fitness
        f.write("# EVOLUÇÃO DO FITNESS\n")
        for gen, fitness_data in enumerate(evolution_results['fitness_history']):
            f.write(f"Geração {gen+1}:\n")
            for species, fitness in fitness_data.items():
                f.write(f"  {species}: {fitness:.6f}\n")
            f.write("\n")
    
    logger.info("✅ Simulação de ecossistema concluída")
    return evolution_results

def run_predator_prey_simulation():
    """Executa simulação predador-presa."""
    logger.info("🦅 Iniciando Simulação Predador-Presa")
    
    # Parâmetros predador (mais agressivo)
    predator_params = [1.5, 3.0, 0.0, 0.8, 0.05, 0.5]
    
    # Parâmetros presa (mais defensivo)
    prey_params = [0.8, 1.2, 0.5, 1.2, 0.02, 1.5]
    
    # Criar sistema
    dynamics = create_predator_prey_system(predator_params, prey_params)
    
    # Simular
    results = dynamics.simulate_ecosystem(t_range=40)
    
    # Salvar resultados
    output_dir = create_output_directory()
    
    with open(f"{output_dir}/predator_prey_results.txt", "w", encoding='utf-8') as f:
        f.write("# SIMULAÇÃO PREDADOR-PRESA AEON\n")
        f.write("# Desenvolvido por Luiz Cruz - 2025\n\n")
        
        # Salvar dados temporais
        f.write("# TEMPO\n")
        for t_val in results['time']:
            f.write(f"{t_val:.6f}\n")
        f.write("\n")
        
        # Salvar populações
        for species_id, values in results['species_results'].items():
            f.write(f"# {species_id.upper()}\n")
            for val in values:
                f.write(f"{val:.6f}\n")
            f.write("\n")
        
        # Salvar fitness
        f.write("# FITNESS\n")
        for species_id, fitness in results['fitness_values'].items():
            f.write(f"{species_id}: {fitness:.6f}\n")
    
    logger.info("✅ Simulação predador-presa concluída")
    return results

def run_mutation_experiment():
    """Executa experimento de mutação adaptativa."""
    logger.info("🧬 Iniciando Experimento de Mutação")
    
    # Parâmetros base
    base_params = [1.0, 1.0, 0.0, 1.0, 0.1, 1.0]
    
    # Criar simulador
    output_dir = create_output_directory()
    simulator = AeonSimulator(output_dir)
    
    # Simular evolução com mutações
    mutation_results = simulator.simulate_with_mutations(
        base_params=base_params,
        n_generations=20,
        mutation_rate=0.05,
        t_range=30
    )
    
    # Salvar resultados
    with open(f"{output_dir}/mutation_results.txt", "w", encoding='utf-8') as f:
        f.write("# EXPERIMENTO DE MUTAÇÃO AEON\n")
        f.write("# Desenvolvido por Luiz Cruz - 2025\n\n")
        
        f.write(f"Gerações: {len(mutation_results['generations'])}\n")
        f.write(f"Fitness final: {mutation_results['final_fitness']:.6f}\n\n")
        
        # Evolução dos parâmetros
        f.write("# EVOLUÇÃO DOS PARÂMETROS\n")
        for gen, params in enumerate(mutation_results['parameters_evolution']):
            f.write(f"Geração {gen+1}: {params}\n")
    
    logger.info("✅ Experimento de mutação concluído")
    return mutation_results

def run_comprehensive_analysis():
    """Executa análise abrangente de todos os sistemas."""
    logger.info("📊 Iniciando Análise Abrangente")
    
    results = {}
    
    # Executar todas as simulações
    logger.info("Executando simulação básica...")
    simulator, basic_analysis = run_basic_simulation()
    results['basic'] = basic_analysis
    
    logger.info("Executando simulação de ecossistema...")
    ecosystem_results = run_ecosystem_simulation()
    results['ecosystem'] = ecosystem_results
    
    logger.info("Executando simulação predador-presa...")
    predprey_results = run_predator_prey_simulation()
    results['predator_prey'] = predprey_results
    
    logger.info("Executando experimento de mutação...")
    mutation_results = run_mutation_experiment()
    results['mutation'] = mutation_results
    
    # Criar relatório final
    output_dir = create_output_directory()
    
    with open(f"{output_dir}/comprehensive_report.txt", "w", encoding='utf-8') as f:
        f.write("# RELATÓRIO ABRANGENTE - SIMULAÇÃO AEON\n")
        f.write("# Desenvolvido por Luiz Cruz - 2025\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("## RESUMO EXECUTIVO\n")
        f.write(f"- Simulação Básica: {results['basic']['evolution_summary']['total_generations']} gerações\n")
        f.write(f"- Ecossistema: {results['ecosystem']['network_properties']['n_species']} espécies\n")
        f.write(f"- Predador-Presa: 2 espécies em interação\n")
        f.write(f"- Mutação: {len(results['mutation']['generations'])} gerações evolutivas\n\n")
        
        f.write("## CONCLUSÕES\n")
        f.write("1. Sistema AEON demonstra comportamento evolutivo estável\n")
        f.write("2. Interações entre espécies geram dinâmicas complexas\n")
        f.write("3. Mutação adaptativa permite evolução controlada\n")
        f.write("4. Equação base F(t) = A*sin(Bt+φ) + C*e^(-λt) + D*log(t+1) é robusta\n\n")
        
        f.write("## PRÓXIMOS PASSOS\n")
        f.write("- Implementar redes neurais para parâmetros adaptativos\n")
        f.write("- Adicionar interface gráfica para visualização\n")
        f.write("- Integrar com sistema de trading P2P\n")
        f.write("- Desenvolver métricas de performance mais sofisticadas\n")
    
    logger.info("✅ Análise abrangente concluída")
    return results

def main():
    """Função principal."""
    print("🌟 AEON EVOLUTION SIMULATOR")
    print("Desenvolvido por Luiz Cruz - 2025")
    print("=" * 40)
    
    try:
        # Criar diretórios necessários
        create_output_directory()
        
        # Menu de opções
        print("\nOpções disponíveis:")
        print("1. Simulação Básica (3 espécies)")
        print("2. Simulação de Ecossistema")
        print("3. Simulação Predador-Presa")
        print("4. Experimento de Mutação")
        print("5. Análise Abrangente (todas)")
        print("0. Executar padrão (básica)")
        
        choice = input("\nEscolha uma opção (0-5): ").strip()
        
        if choice == "1":
            run_basic_simulation()
        elif choice == "2":
            run_ecosystem_simulation()
        elif choice == "3":
            run_predator_prey_simulation()
        elif choice == "4":
            run_mutation_experiment()
        elif choice == "5":
            run_comprehensive_analysis()
        else:
            # Padrão: executar simulação básica
            logger.info("Executando simulação padrão...")
            run_basic_simulation()
        
        print("\n✅ Simulação concluída com sucesso!")
        print("📁 Verifique os resultados em 'aeon/output/'")
        
    except KeyboardInterrupt:
        logger.info("Simulação interrompida pelo usuário")
    except Exception as e:
        logger.error(f"Erro durante execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
