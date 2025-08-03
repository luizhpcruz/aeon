from fastapi import APIRouter
from aeon_ops.twin_model import ingest_csv, HydropowerTwin
import pandas as pd
import numpy as np

router = APIRouter()

@router.post("/simulate")
def simulate_hydropower():
    # Carregar dados de exemplo
    df = ingest_csv('aeon_ops/data/uhe_data.csv')
    twin = HydropowerTwin(df)

    # Simulação fictícia de inflow nos próximos 7 dias
    dates = pd.date_range('2025-08-01', periods=7)
    flow = np.random.uniform(100, 300, size=7)
    inflow_series = pd.DataFrame({'date': dates, 'inflow_m3_s': flow})

    result = twin.simulate(inflow_series)
    return result.to_dict(orient='records')
