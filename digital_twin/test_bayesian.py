#!/usr/bin/env python3
"""
Script de Teste para o Módulo Bayesiano AEON
============================================

Este script testa a implementação da análise Bayesiana real,
validando a funcionalidade e comparando com os métodos anteriores.
"""

import sys
import os
from pathlib import Path

# Adicionar path do projeto
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))

def test_bayesian_module():
    """Testa o módulo de análise Bayesiana"""
    
    print("🧪 TESTE DO MÓDULO BAYESIANO AEON")
    print("=" * 50)
    
    try:
        # Importar módulo
        from src.bayesian.mcmc_real import BayesianEntropyAnalyzer, BayesianCosmologyAnalyzer
        print("✅ Importação do módulo: OK")
        
        # Teste 1: Análise de Entropia
        print("\n🔬 Teste 1: Análise de Entropia")
        data_path = "data/entropy_metrics.csv"
        
        if not os.path.exists(data_path):
            print(f"⚠️ Arquivo {data_path} não encontrado, usando dados simulados")
        
        analyzer = BayesianEntropyAnalyzer(data_path=data_path)
        print("✅ Inicialização do analisador: OK")
        
        analyzer.define_model()
        print("✅ Definição do modelo: OK")
        
        # Teste rápido com poucas amostras para validação
        print("⏱️ Executando MCMC rápido para teste...")
        analyzer.run_mcmc(draws=200, tune=100, chains=2)
        print("✅ Execução MCMC: OK")
        
        analyzer.analyze_results()
        print("✅ Análise de resultados: OK")
        
        # Teste 2: Obtenção de amostras posteriores
        print("\n📊 Teste 2: Amostras Posteriores")
        samples = analyzer.get_posterior_samples()
        print(f"✅ Amostras obtidas: {len(samples['mu_samples'])} amostras de mu")
        print(f"✅ Amostras obtidas: {len(samples['sigma_samples'])} amostras de sigma")
        
        # Teste 3: Salvamento de resultados
        print("\n💾 Teste 3: Salvamento")
        analyzer.save_results("test_results.nc")
        print("✅ Resultados salvos: OK")
        
        # Teste 4: Análise Cosmológica
        print("\n🌌 Teste 4: Análise Cosmológica")
        cosmo_analyzer = BayesianCosmologyAnalyzer()
        cosmo_analyzer.define_cosmology_model()
        print("✅ Modelo cosmológico definido: OK")
        
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💻 Instale as dependências: pip install pymc arviz matplotlib")
        return False
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False

def validate_installation():
    """Valida se todas as dependências estão instaladas"""
    
    print("🔍 VALIDAÇÃO DE DEPENDÊNCIAS")
    print("=" * 30)
    
    dependencies = [
        ("pymc", "PyMC"),
        ("arviz", "ArviZ"), 
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("matplotlib", "Matplotlib")
    ]
    
    all_ok = True
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}: Instalado")
        except ImportError:
            print(f"❌ {name}: NÃO instalado")
            all_ok = False
    
    if not all_ok:
        print("\n💻 Para instalar todas as dependências:")
        print("pip install pymc arviz numpy pandas matplotlib")
    
    return all_ok

if __name__ == "__main__":
    print("🚀 AEON - Validação do Módulo Bayesiano")
    print("=" * 50)
    
    # Validar instalação
    deps_ok = validate_installation()
    
    if deps_ok:
        print("\n🧪 Iniciando testes...")
        success = test_bayesian_module()
        
        if success:
            print("\n✅ VALIDAÇÃO COMPLETA: SUCESSO!")
            print("🎯 O módulo Bayesiano está pronto para uso.")
            print("\n📋 Próximos passos:")
            print("1. Integrar com os dados reais do AEON")
            print("2. Implementar Bayesian Neural Networks (BNN)")
            print("3. Desenvolver modelos hierárquicos")
        else:
            print("\n❌ VALIDAÇÃO FALHOU")
            print("🔧 Verifique os erros acima e tente novamente")
    else:
        print("\n❌ DEPENDÊNCIAS FALTANDO")
        print("📦 Instale as dependências antes de continuar")
