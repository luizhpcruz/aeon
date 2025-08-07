import pandas as pd
import numpy as np

def ingest_csv(path):
    df = pd.read_csv(path)
    return df

class HydropowerTwin:
    def __init__(self, df):
        self.df = df.copy()

    def simulate(self, inflow_series, efficiency=0.9):
        records = []
        for _, row in inflow_series.iterrows():
            plant = self.df.iloc[0]  # usa a primeira usina
            inflow_vol = row['inflow_m3_s'] * 3600 * 24 / 1e9
            energy_gwh = inflow_vol * plant['dam_height_m'] * 9.81 * efficiency / 3.6e12
            records.append({
                'date': row['date'],
                'plant': plant['name'],
                'energy_gwh': energy_gwh,
                'inflow_km3': inflow_vol
            })
        return pd.DataFrame(records)
