#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Dependências - Physics-Informed Neural Networks (AEON)

Este script verifica se todas as dependências necessárias para os módulos
PINN e Bayesiano estão instaladas corretamente.
"""

import sys
from importlib import import_module

def test_dependencies():
    """Testa se todas as dependências estão instaladas."""
    
    dependencies = {
        # Core scientific computing
        'numpy': 'Computação científica básica',
        'pandas': 'Manipulação de dados',
        'scipy': 'Funções científicas avançadas',
        
        # Deep Learning
        'torch': 'PyTorch para PINNs',
        
        # Bayesian Analysis  
        'pymc': 'Análise Bayesiana MCMC',
        'arviz': 'Análise estatística Bayesiana',
        
        # Visualization (optional)
        'matplotlib': 'Visualizações (opcional)',
        
        # Standard library
        'json': 'Serialização JSON',
        'logging': 'Sistema de logs',
        'pathlib': 'Manipulação de caminhos'
    }
    
    print("🧪 TESTE DE DEPENDÊNCIAS - AEON PINN")
    print("=" * 50)
    
    results = {}
    
    for module_name, description in dependencies.items():
        try:
            import_module(module_name)
            status = "✅ OK"
            results[module_name] = True
        except ImportError as e:
            status = f"❌ ERRO: {str(e)}"
            results[module_name] = False
        
        print(f"{module_name:12} - {status:20} | {description}")
    
    # Resumo
    total = len(dependencies)
    passed = sum(results.values())
    failed = total - passed
    
    print("\n" + "=" * 50)
    print(f"📊 RESUMO:")
    print(f"   Total: {total}")
    print(f"   ✅ Instaladas: {passed}")
    print(f"   ❌ Faltando: {failed}")
    
    if failed == 0:
        print(f"🎊 PERFEITO! Todas as dependências estão instaladas.")
        print(f"🚀 Você pode executar os módulos PINN e Bayesiano!")
    else:
        print(f"⚠️  ATENÇÃO: {failed} dependências faltando.")
        print(f"💻 Execute: pip install -r requirements_pinn.txt")
    
    # Teste específico do PyTorch
    if results.get('torch', False):
        try:
            import torch
            print(f"\n🔥 PyTorch Info:")
            print(f"   Versão: {torch.__version__}")
            print(f"   CUDA disponível: {torch.cuda.is_available()}")
            if torch.cuda.is_available():
                print(f"   Dispositivos CUDA: {torch.cuda.device_count()}")
        except Exception as e:
            print(f"   ⚠️  Erro ao verificar PyTorch: {e}")
    
    # Teste específico do PyMC
    if results.get('pymc', False):
        try:
            import pymc as pm
            print(f"\n🧠 PyMC Info:")
            print(f"   Versão: {pm.__version__}")
            print(f"   Backend disponível: OK")
        except Exception as e:
            print(f"   ⚠️  Erro ao verificar PyMC: {e}")
    
    print("=" * 50)
    
    return results

def run_simple_tests():
    """Executa testes básicos das funcionalidades."""
    
    print("\n🧪 TESTES FUNCIONAIS BÁSICOS")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Teste 1: Criar tensor PyTorch
    total_tests += 1
    try:
        import torch
        x = torch.randn(10, 1)
        y = torch.sin(x)
        print("✅ Teste 1: Criação de tensores PyTorch")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Teste 1: {e}")
    
    # Teste 2: Operações NumPy
    total_tests += 1
    try:
        import numpy as np
        data = np.random.normal(0, 1, 100)
        mean = np.mean(data)
        std = np.std(data)
        print("✅ Teste 2: Operações NumPy básicas")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Teste 2: {e}")
    
    # Teste 3: Pandas DataFrame
    total_tests += 1
    try:
        import pandas as pd
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        print("✅ Teste 3: Criação DataFrame Pandas")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Teste 3: {e}")
    
    # Teste 4: JSON serialization
    total_tests += 1
    try:
        import json
        data = {'test': 'value', 'number': 42}
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        print("✅ Teste 4: Serialização JSON")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Teste 4: {e}")
    
    print(f"\n📊 Testes funcionais: {tests_passed}/{total_tests} passaram")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    print("🚀 AEON - Verificação de Ambiente")
    print("Este script verifica se o ambiente está pronto para PINNs")
    print()
    
    # Teste de dependências
    deps_ok = test_dependencies()
    
    # Testes funcionais
    if all(deps_ok.values()):
        functional_ok = run_simple_tests()
        
        if functional_ok:
            print("\n🎯 CONCLUSÃO: Ambiente totalmente funcional!")
            print("   Você pode executar:")
            print("   • python pinn_demo.py")
            print("   • python integrated_digital_twin.py") 
            print("   • python src/bayesian/mcmc_real.py")
        else:
            print("\n⚠️  CONCLUSÃO: Dependências OK, mas há problemas funcionais")
    else:
        print("\n❌ CONCLUSÃO: Instale as dependências faltando primeiro")
        print("   pip install torch numpy pandas scipy pymc arviz")
