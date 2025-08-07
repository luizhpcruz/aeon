#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO AVANÇADO - DIGITAL TWIN
=====================================
Análise detalhada do cálculo de energia no Digital Twin
"""

def diagnose_twin_calculation():
    """Diagnostica o cálculo de energia do Digital Twin com métricas em m/s e metros"""
    print("🔍 === DIAGNÓSTICO DIGITAL TWIN - MÉTRICAS DETALHADAS ===")
    
    try:
        from aeon_ops.twin_model import HydropowerTwin
        import pandas as pd
        
        # Dados com valores realistas para teste
        plant_data = pd.DataFrame({
            'name': ['Usina Diagnóstico'],
            'dam_height_m': [100.0],  # 100 metros de altura
            'capacity_mw': [500.0]    # 500 MW de capacidade
        })
        
        inflow_data = pd.DataFrame({
            'date': ['2025-01-01'],
            'inflow_m3_s': [2000.0]  # 2000 m³/s (vazão alta)
        })
        
        twin = HydropowerTwin(plant_data)
        
        # Parâmetros do cálculo
        vazao_m3_s = inflow_data['inflow_m3_s'].iloc[0]
        altura_m = plant_data['dam_height_m'].iloc[0] 
        capacidade_mw = plant_data['capacity_mw'].iloc[0]
        efficiency = 0.9
        
        print(f"📊 === PARÂMETROS DE ENTRADA ===")
        print(f"   🏭 Usina: {plant_data['name'].iloc[0]}")
        print(f"   📏 Altura da barragem: {altura_m:.0f} metros")
        print(f"   💧 Vazão de entrada: {vazao_m3_s:.0f} m³/s")
        print(f"   ⚡ Capacidade instalada: {capacidade_mw:.0f} MW")
        print(f"   🎯 Eficiência: {efficiency:.1%}")
        
        # Cálculo manual detalhado da potência hidráulica
        print(f"\n🔧 === CÁLCULO MANUAL DA POTÊNCIA ===")
        
        # Constantes físicas
        densidade_agua = 1000  # kg/m³
        gravidade = 9.81      # m/s²
        
        print(f"   🌊 Densidade da água (ρ): {densidade_agua} kg/m³")
        print(f"   🌍 Aceleração da gravidade (g): {gravidade} m/s²")
        
        # Fórmula: P = ρ × g × Q × H × η
        potencia_teorica_watts = densidade_agua * gravidade * vazao_m3_s * altura_m * efficiency
        potencia_teorica_mw = potencia_teorica_watts / 1_000_000
        
        print(f"   📐 Fórmula: P = ρ × g × Q × H × η")
        print(f"   📐 P = {densidade_agua} × {gravidade} × {vazao_m3_s} × {altura_m} × {efficiency}")
        print(f"   📐 P = {potencia_teorica_watts:,.0f} W")
        print(f"   📐 P = {potencia_teorica_mw:.2f} MW")
        
        # Verificação contra capacidade instalada
        if potencia_teorica_mw > capacidade_mw:
            print(f"   ⚠️ Potência teórica ({potencia_teorica_mw:.2f} MW) > Capacidade ({capacidade_mw} MW)")
            print(f"   🔧 Limitando à capacidade instalada")
            potencia_real_mw = capacidade_mw
        else:
            potencia_real_mw = potencia_teorica_mw
            print(f"   ✅ Potência dentro da capacidade instalada")
        
        print(f"   🎯 Potência real de saída: {potencia_real_mw:.2f} MW")
        
        # Cálculos de energia e volume por diferentes períodos
        print(f"\n⚡ === GERAÇÃO DE ENERGIA ===")
        
        # Por hora
        energia_mwh_hora = potencia_real_mw * 1  # 1 hora
        energia_kwh_hora = energia_mwh_hora * 1000
        
        # Por dia  
        energia_mwh_dia = potencia_real_mw * 24
        energia_gwh_dia = energia_mwh_dia / 1000
        
        # Por mês (30 dias)
        energia_gwh_mes = energia_gwh_dia * 30
        
        print(f"   ⏰ Por hora: {energia_mwh_hora:.2f} MWh = {energia_kwh_hora:,.0f} kWh")
        print(f"   📅 Por dia: {energia_mwh_dia:.1f} MWh = {energia_gwh_dia:.3f} GWh")
        print(f"   📆 Por mês: {energia_gwh_mes:.2f} GWh")
        
        print(f"\n💧 === VOLUME DE ÁGUA PROCESSADO ===")
        
        # Volume por diferentes períodos
        volume_m3_hora = vazao_m3_s * 3600
        volume_m3_dia = vazao_m3_s * 86400
        volume_km3_dia = volume_m3_dia / 1_000_000_000
        
        print(f"   ⏰ Por hora: {volume_m3_hora:,.0f} m³")
        print(f"   📅 Por dia: {volume_m3_dia:,.0f} m³ = {volume_km3_dia:.3f} km³")
        
        # Executa simulação do modelo original
        print(f"\n🔍 === RESULTADO DO MODELO ORIGINAL ===")
        resultado = twin.simulate(inflow_data, efficiency=efficiency)
        
        energy_modelo = resultado['energy_gwh'].iloc[0]
        volume_modelo = resultado['inflow_km3'].iloc[0]
        
        print(f"   ⚡ Energia modelo: {energy_modelo:.6f} GWh")
        print(f"   💧 Volume modelo: {volume_modelo:.3f} km³")
        
        # Comparação e análise
        print(f"\n📊 === COMPARAÇÃO E ANÁLISE ===")
        
        print(f"   📈 Energia esperada vs obtida:")
        print(f"      • Manual: {energia_gwh_dia:.3f} GWh/dia")
        print(f"      • Modelo: {energy_modelo:.6f} GWh/dia")
        print(f"      • Diferença: {abs(energia_gwh_dia - energy_modelo):.6f} GWh")
        
        if abs(volume_modelo - volume_km3_dia) < 0.001:
            print(f"   ✅ Volume: Consistente entre cálculos")
        else:
            print(f"   ⚠️ Volume: Diferença de {abs(volume_modelo - volume_km3_dia):.3f} km³")
        
        # Diagnóstico do problema de energia
        ratio = energy_modelo / energia_gwh_dia if energia_gwh_dia > 0 else 0
        print(f"   📊 Razão modelo/manual: {ratio:.6f}")
        
        if ratio < 0.01:
            print(f"   � DIAGNÓSTICO: Problema na fórmula de conversão do modelo")
            print(f"      • O modelo está usando conversões inadequadas")
            print(f"      • Fator de erro: ~{1/ratio:.0f}x menor que esperado")
            print(f"      • Possível problema: conversão GWh inadequada")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no diagnóstico: {e}")
        return False

if __name__ == "__main__":
    diagnose_twin_calculation()
