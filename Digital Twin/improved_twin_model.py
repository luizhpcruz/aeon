#!/usr/bin/env python3
"""
🔧 MODELO DIGITAL TWIN CORRIGIDO
===============================
Versão melhorada com cálculos corretos em m/s e metros
"""

import pandas as pd
import numpy as np

class HydropowerTwinImproved:
    """
    Versão melhorada do Digital Twin com cálculos corretos
    Utiliza unidades em metros e m³/s para melhor clareza
    """
    
    def __init__(self, plant_data):
        self.plant_data = plant_data.copy()
        
        # Constantes físicas
        self.densidade_agua = 1000  # kg/m³
        self.gravidade = 9.81      # m/s²
    
    def simulate(self, inflow_data, efficiency=0.9):
        """
        Simula geração de energia hidrelétrica
        
        Args:
            inflow_data: DataFrame com colunas ['date', 'inflow_m3_s']
            efficiency: Eficiência da turbina (0.0 a 1.0)
        
        Returns:
            DataFrame com resultados detalhados
        """
        results = []
        
        for _, inflow_row in inflow_data.iterrows():
            plant = self.plant_data.iloc[0]
            
            # Parâmetros de entrada
            vazao_m3_s = inflow_row['inflow_m3_s']
            altura_m = plant['dam_height_m']
            capacidade_mw = plant['capacity_mw']
            
            # Cálculo da potência hidráulica teórica
            # P = ρ × g × Q × H × η
            potencia_teorica_w = (self.densidade_agua * 
                                self.gravidade * 
                                vazao_m3_s * 
                                altura_m * 
                                efficiency)
            
            potencia_teorica_mw = potencia_teorica_w / 1_000_000
            
            # Limitação pela capacidade instalada
            potencia_real_mw = min(potencia_teorica_mw, capacidade_mw)
            
            # Cálculos de energia
            energia_mwh_hora = potencia_real_mw * 1  # MWh por hora
            energia_mwh_dia = potencia_real_mw * 24  # MWh por dia
            energia_gwh_dia = energia_mwh_dia / 1000  # GWh por dia
            
            # Cálculos de volume
            volume_m3_dia = vazao_m3_s * 86400  # m³ por dia
            volume_km3_dia = volume_m3_dia / 1_000_000_000  # km³ por dia
            
            # Fatores de capacidade
            fator_capacidade = potencia_real_mw / capacidade_mw if capacidade_mw > 0 else 0
            
            results.append({
                'date': inflow_row['date'],
                'plant': plant['name'],
                
                # Parâmetros de entrada
                'vazao_m3_s': vazao_m3_s,
                'altura_m': altura_m,
                'capacidade_mw': capacidade_mw,
                'efficiency': efficiency,
                
                # Resultados de potência
                'potencia_teorica_mw': potencia_teorica_mw,
                'potencia_real_mw': potencia_real_mw,
                'fator_capacidade': fator_capacidade,
                
                # Resultados de energia
                'energia_mwh_hora': energia_mwh_hora,
                'energia_mwh_dia': energia_mwh_dia,
                'energia_gwh_dia': energia_gwh_dia,
                
                # Resultados de volume
                'volume_m3_dia': volume_m3_dia,
                'volume_km3_dia': volume_km3_dia,
                
                # Para compatibilidade com modelo antigo
                'energy_gwh': energia_gwh_dia,
                'inflow_km3': volume_km3_dia
            })
        
        return pd.DataFrame(results)
    
    def get_summary_metrics(self, results_df):
        """
        Gera métricas resumidas dos resultados
        """
        if results_df.empty:
            return {}
        
        return {
            'potencia_media_mw': results_df['potencia_real_mw'].mean(),
            'energia_total_gwh_mes': results_df['energia_gwh_dia'].sum() * 30,
            'volume_total_km3_mes': results_df['volume_km3_dia'].sum() * 30,
            'fator_capacidade_medio': results_df['fator_capacidade'].mean(),
            'eficiencia_operacional': results_df['efficiency'].mean()
        }

def test_improved_twin():
    """Testa o modelo Digital Twin melhorado"""
    print("🔧 === TESTE DO MODELO DIGITAL TWIN MELHORADO ===")
    
    # Dados de teste
    plant_data = pd.DataFrame({
        'name': ['Usina Melhorada'],
        'dam_height_m': [80.0],
        'capacity_mw': [300.0]
    })
    
    inflow_data = pd.DataFrame({
        'date': ['2025-01-01', '2025-01-02'],
        'inflow_m3_s': [1500.0, 1200.0]
    })
    
    # Criar e executar simulação
    twin = HydropowerTwinImproved(plant_data)
    results = twin.simulate(inflow_data, efficiency=0.92)
    
    print(f"\n📊 === RESULTADOS DETALHADOS ===")
    for idx, row in results.iterrows():
        print(f"\n📅 Data: {row['date']}")
        print(f"   💧 Vazão: {row['vazao_m3_s']:.0f} m³/s")
        print(f"   📏 Altura: {row['altura_m']:.0f} m")
        print(f"   ⚡ Potência teórica: {row['potencia_teorica_mw']:.2f} MW")
        print(f"   🎯 Potência real: {row['potencia_real_mw']:.2f} MW")
        print(f"   📈 Fator de capacidade: {row['fator_capacidade']:.1%}")
        print(f"   ⚡ Energia/dia: {row['energia_gwh_dia']:.3f} GWh")
        print(f"   💧 Volume/dia: {row['volume_km3_dia']:.3f} km³")
    
    # Métricas resumidas
    summary = twin.get_summary_metrics(results)
    print(f"\n📈 === MÉTRICAS RESUMIDAS ===")
    print(f"   ⚡ Potência média: {summary['potencia_media_mw']:.2f} MW")
    print(f"   📊 Energia mensal: {summary['energia_total_gwh_mes']:.2f} GWh")
    print(f"   💧 Volume mensal: {summary['volume_total_km3_mes']:.2f} km³")
    print(f"   📈 Fator capacidade: {summary['fator_capacidade_medio']:.1%}")
    
    return True

if __name__ == "__main__":
    test_improved_twin()
