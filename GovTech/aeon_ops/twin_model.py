import pandas as pd
import numpy as np

class HydropowerTwin:
    def __init__(self, df):
        self.df = df.copy()

    def simulate(self, inflow_series, efficiency=0.9):
        # inflow_series: DataFrame com col 'date', 'inflow_m3_s'
        records = []
        for _, row in inflow_series.iterrows():
            plant = self.df.iloc[0]  # exemplo com primeira linha
            # estimativa de volume em km3
            inflow_vol = row['inflow_m3_s'] * 3600 * 24 / 1e9
            # cálculo simplificado: energia = inflow_vol * head * g * efficiency
            energy_gwh = inflow_vol * plant['dam_height_m'] * 9.81 * efficiency / 3.6e12
            records.append({
                'date': row['date'],
                'plant': plant['name'],
                'energy_gwh': energy_gwh,
                'inflow_km3': inflow_vol
            })
        return pd.DataFrame(records)

def ingest_csv(path):
    return pd.read_csv(path)
