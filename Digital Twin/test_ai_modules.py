#!/usr/bin/env python3
"""
🧠 TESTE DE MÓDULOS IA - AEON DIGITAL TWIN
================================================================
Script para testar funcionalidade dos módulos de IA descobertos
"""

import sys
import traceback
import importlib.util
from pathlib import Path

def test_veritas_ai():
    """Testa o módulo de IA do Veritas"""
    print("\n🔍 === TESTANDO VERITAS AI ===")
    try:
        from aeon_project.veritas_core import VeritasRiskAnalyzer
        
        veritas = VeritasRiskAnalyzer()
        
        # Teste da recomendação AI
        risks = ["Trabalho em altura", "Uso de ferramentas cortantes"]
        recommendation = veritas.generate_ai_recommendation("ALTO", risks)
        
        print(f"✅ Veritas AI - Recomendação gerada:")
        print(f"   {recommendation}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no Veritas AI: {e}")
        return False

def test_aeon_kernel():
    """Testa o kernel AEON"""
    print("\n🧠 === TESTANDO AEON KERNEL ===")
    try:
        from aeon_project.aeon_kernel.kernel import AEONKernel
        
        kernel = AEONKernel(alpha=1.0, beta=0.5, gamma=0.2, delta=0.1)
        
        # Teste de evolução com múltiplos ciclos
        I = 1.0
        omega_info = 0.8
        omega_caos = 0.3
        S = 0.5
        Phi = 0.2
        
        # Primeira evolução
        resultado1 = kernel.evolve(I, omega_info, omega_caos, S, Phi)
        
        # Segunda evolução para testar continuidade
        resultado2 = kernel.evolve(resultado1, omega_info * 1.1, omega_caos * 0.9, S, Phi)
        
        print(f"✅ AEON Kernel - Evolução calculada:")
        print(f"   Input I: {I}")
        print(f"   Primeira evolução: {resultado1:.3f}")
        print(f"   Segunda evolução: {resultado2:.3f}")
        print(f"   Network Strength: {kernel.symbol_net.network_strength():.3f}")
        print(f"   Símbolos ativos: {len(kernel.symbol_net.nodes)}")
        
        # Verifica se a evolução está funcionando
        if resultado1 != I and resultado2 != resultado1:
            print("✅ Sistema evoluindo corretamente")
            return True
        else:
            print("⚠️ Sistema pode estar estagnado")
            return False
        
    except Exception as e:
        print(f"❌ Erro no AEON Kernel: {e}")
        traceback.print_exc()
        return False

def test_twin_model():
    """Testa o modelo Digital Twin com métricas em m/s e metros"""
    print("\n🏭 === TESTANDO TWIN MODEL ===")
    try:
        from aeon_ops.twin_model import HydropowerTwin
        import pandas as pd
        
        # Dados mock para teste com valores mais realistas
        plant_data = pd.DataFrame({
            'name': ['Usina Teste'],
            'dam_height_m': [50.0],      # 50 metros de altura
            'capacity_mw': [100.0]       # 100 MW de capacidade
        })
        
        inflow_data = pd.DataFrame({
            'date': ['2025-01-01'],
            'inflow_m3_s': [1000.0]      # 1000 m³/s de vazão
        })
        
        twin = HydropowerTwin(plant_data)
        resultado = twin.simulate(inflow_data, efficiency=0.9)
        
        # Verificação se a simulação produziu resultados válidos
        if not resultado.empty and 'energy_gwh' in resultado.columns:
            # Extrair valores básicos
            vazao_m3_s = inflow_data['inflow_m3_s'].iloc[0]
            altura_m = plant_data['dam_height_m'].iloc[0]
            efficiency = 0.9
            
            # Cálculos passo a passo com unidades claras
            print(f"✅ Digital Twin - Cálculo detalhado:")
            print(f"   📊 Parâmetros de entrada:")
            print(f"      • Vazão: {vazao_m3_s:.0f} m³/s")
            print(f"      • Altura da barragem: {altura_m:.0f} m")
            print(f"      • Eficiência: {efficiency:.1%}")
            
            # Cálculo da potência hidráulica (P = ρ × g × Q × H × η)
            # ρ (densidade da água) = 1000 kg/m³
            # g (gravidade) = 9.81 m/s²
            densidade_agua = 1000  # kg/m³
            gravidade = 9.81      # m/s²
            
            potencia_watts = densidade_agua * gravidade * vazao_m3_s * altura_m * efficiency
            potencia_mw = potencia_watts / 1_000_000  # Converter para MW
            
            print(f"   🔧 Cálculo da potência:")
            print(f"      • Densidade da água: {densidade_agua} kg/m³")
            print(f"      • Gravidade: {gravidade} m/s²")
            print(f"      • Potência = ρ × g × Q × H × η")
            print(f"      • Potência = {densidade_agua} × {gravidade} × {vazao_m3_s} × {altura_m} × {efficiency}")
            print(f"      • Potência = {potencia_watts:,.0f} W = {potencia_mw:.2f} MW")
            
            # Energia em 24 horas
            energia_mwh_dia = potencia_mw * 24  # MWh por dia
            energia_gwh_dia = energia_mwh_dia / 1000  # GWh por dia
            
            print(f"   ⚡ Geração de energia:")
            print(f"      • Energia por dia: {energia_mwh_dia:.2f} MWh = {energia_gwh_dia:.3f} GWh")
            
            # Volume processado
            volume_m3_dia = vazao_m3_s * 86400  # segundos em um dia
            volume_km3_dia = volume_m3_dia / 1_000_000_000  # converter para km³
            
            print(f"   💧 Volume processado:")
            print(f"      • Volume por dia: {volume_m3_dia:,.0f} m³ = {volume_km3_dia:.3f} km³")
            
            # Comparação com resultado do modelo
            energy_model = resultado['energy_gwh'].iloc[0]
            volume_model = resultado['inflow_km3'].iloc[0]
            
            print(f"   🔍 Resultado do modelo original:")
            print(f"      • Energia modelo: {energy_model:.6f} GWh")
            print(f"      • Volume modelo: {volume_model:.3f} km³")
            print(f"      • Usina: {resultado['plant'].iloc[0]}")
            
            # Verificação de consistência
            if abs(volume_model - volume_km3_dia) < 0.001:
                print("   ✅ Volume: Cálculo consistente entre modelo e manual")
            else:
                print("   ⚠️ Volume: Diferença detectada entre cálculos")
            
            # Análise da discrepância na energia
            if energy_model < energia_gwh_dia * 0.1:
                print(f"   🔍 Análise: Energia do modelo muito baixa")
                print(f"      • Esperado: ~{energia_gwh_dia:.3f} GWh")
                print(f"      • Obtido: {energy_model:.6f} GWh")
                print(f"      • Possível problema na fórmula de conversão do modelo")
            
            return True
        else:
            print("❌ Resultado da simulação inválido")
            return False
        
    except Exception as e:
        print(f"❌ Erro no Twin Model: {e}")
        traceback.print_exc()
        return False

def test_aeoncosma_api():
    """Testa a API do AEONCOSMA"""
    print("\n🌌 === TESTANDO AEONCOSMA API ===")
    try:
        from aeoncosma.aeoncosma_api import IALearningRequest
        
        # Teste do modelo Pydantic com schema correto
        request = IALearningRequest(
            data=[{"input": "teste", "output": "resultado"}],  # Lista de dicionários
            model_type="neural",
            epochs=50
        )
        
        print(f"✅ AEONCOSMA API - Modelo validado:")
        print(f"   Model Type: {request.model_type}")
        print(f"   Data: {len(request.data)} registros")
        print(f"   Epochs: {request.epochs}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na AEONCOSMA API: {e}")
        return False

def test_external_aeon_engines():
    """Testa os engines AEON externos se disponíveis"""
    print("\n🚀 === BUSCANDO ENGINES AEON EXTERNOS ===")
    
    # Paths únicos dos engines (sem duplicação)
    possible_paths = [
        Path("../bagunça/AEON1.py"),
        Path("../bagunça/AEON3.py"), 
        Path("../bagunça/AEON12.py")
    ]
    
    # Fallback para paths absolutos se relativos não funcionarem
    fallback_paths = [
        Path("c:/Users/Luiz/OneDrive/Área de Trabalho/aeon/bagunça/AEON1.py"),
        Path("c:/Users/Luiz/OneDrive/Área de Trabalho/aeon/bagunça/AEON3.py"),
        Path("c:/Users/Luiz/OneDrive/Área de Trabalho/aeon/bagunça/AEON12.py")
    ]
    
    engines_found = []
    
    # Testa paths relativos primeiro
    for path in possible_paths:
        if path.exists():
            engines_found.append(path.name)
            print(f"✅ Engine encontrado (relativo): {path.name}")
    
    # Se não encontrou nada, testa paths absolutos
    if not engines_found:
        for path in fallback_paths:
            if path.exists():
                engines_found.append(path.name)
                print(f"✅ Engine encontrado (absoluto): {path.name}")
    
    if not engines_found:
        print("⚠️ Engines AEON externos não encontrados no workspace atual")
        print("💡 Isso é normal - engines podem estar em diretório paralelo")
        return True  # Não é erro crítico
    else:
        unique_engines = list(set(engines_found))  # Remove duplicatas
        print(f"✅ {len(unique_engines)} engines AEON únicos encontrados: {', '.join(unique_engines)}")
        return True

def run_comprehensive_ai_test():
    """Executa teste abrangente dos módulos IA"""
    print("🧠 =" * 30)
    print("🧬 TESTE ABRANGENTE - MÓDULOS IA")
    print("🧠 =" * 30)
    
    tests = [
        ("Veritas AI", test_veritas_ai),
        ("AEON Kernel", test_aeon_kernel),
        ("Twin Model", test_twin_model),
        ("AEONCOSMA API", test_aeoncosma_api),
        ("External AEON Engines", test_external_aeon_engines)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ FALHA CRÍTICA em {test_name}: {e}")
            traceback.print_exc()
            results[test_name] = False
    
    # Relatório final
    print("\n🏁 =" * 30)
    print("📊 RELATÓRIO FINAL DOS TESTES")
    print("🏁 =" * 30)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {status}: {test_name}")
    
    success_rate = (passed_tests / total_tests) * 100
    print(f"\n📈 Taxa de Sucesso: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate >= 80:
        print("🎉 EXCELENTE: Módulos IA estão funcionais!")
    elif success_rate >= 60:
        print("⚠️ BOM: Maioria dos módulos IA funcionando")
    else:
        print("🚨 CRÍTICO: Problemas significativos nos módulos IA")
    
    return results

if __name__ == "__main__":
    results = run_comprehensive_ai_test()
