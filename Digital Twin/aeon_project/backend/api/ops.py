from fastapi import APIRouter
from aeon_ops.twin_model import HydropowerTwin
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from aeon_ops.modules.apr_it_pt import generate_document
import pandas as pd

router = APIRouter()

@router.post("/simulate")
async def simulate_hydropower(inflow_data: list):
    # Mock UHE data
    uhe_data = pd.DataFrame({
        'name': ['Paraibuna', 'São Simão'],
        'dam_height_m': [104, 127],
        'capacity_mw': [85, 1710]
    })
    
    twin = HydropowerTwin(uhe_data)
    inflow_df = pd.DataFrame(inflow_data)
    result = twin.simulate_all(inflow_df)
    return result.to_dict(orient="records")

@router.post("/generate_and_sign")
async def generate_document_apr(task_data: dict):
    doc = generate_document(
        task_data.get("task_id", "OS-45"),
        task_data.get("location", "UHE Default"),
        {"name": "João Silva", "govbr_id": "98765432100"},
        {"name": "Supervisor", "govbr_id": "30988877766"}
    )
    return doc
