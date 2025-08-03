from fastapi import FastAPI
import json
import uuid
from datetime import datetime

app = FastAPI(
    title="AEON‑AI Platform",
    description="Sistema Digital Twin + IA Simbólica + Chat Corporativo",
    version="2.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "AEON Digital Twin Platform",
        "version": "2.0.0",
        "status": "online",
        "features": [
            "IA Simbólica Evolutiva",
            "Digital Twin de UHEs", 
            "Chat Corporativo",
            "Documentação SSMA"
        ]
    }

@app.post("/kernel/evolve")
async def evolve_kernel(data: dict):
    # Simulação do kernel simbólico
    I = data.get("I", 1.0)
    omega_info = data.get("omega_info", 0.5)
    omega_caos = data.get("omega_caos", 0.2)
    S = data.get("S", 0.1)
    Phi = data.get("Phi", 0.05)
    
    alpha, beta, gamma, delta = 1.0, 0.5, 0.2, 0.1
    dI = alpha * omega_info + beta * omega_caos - gamma * S + delta * Phi
    evolved_value = I + dI
    symbol_strength = abs(dI) * 1.5  # Simulação da força simbólica
    
    return {
        "evolved_value": evolved_value,
        "symbol_strength": symbol_strength,
        "parameters": {
            "alpha": alpha, "beta": beta, "gamma": gamma, "delta": delta
        }
    }

@app.post("/ops/simulate")
async def simulate_hydropower(data: dict):
    # Simulação das UHEs
    inflow_data = data.get("inflow_data", data)
    if isinstance(inflow_data, dict):
        inflow_data = [inflow_data]
    
    results = []
    uhe_data = [
        {"name": "Paraibuna", "dam_height_m": 104, "capacity_mw": 85},
        {"name": "São Simão", "dam_height_m": 127, "capacity_mw": 1710},
        {"name": "Itaipu", "dam_height_m": 196, "capacity_mw": 14000}
    ]
    
    for inflow in inflow_data:
        for plant in uhe_data:
            vol = inflow["inflow_m3_s"] * 86400 / 1e9  # m³/s para km³/dia
            energy_gwh = vol * plant["dam_height_m"] * 9.81 * 0.9 / 3.6e12
            
            results.append({
                "date": inflow["date"],
                "plant": plant["name"],
                "inflow_m3_s": inflow["inflow_m3_s"],
                "energy_gwh": round(energy_gwh, 3),
                "threshold_alert": energy_gwh < plant["capacity_mw"] * 0.7 / 1000
            })
    
    return results

@app.post("/ops/generate_and_sign")
async def generate_document(task_data: dict):
    # Geração de documento SSMA
    doc = {
        "document_id": f"aeonops-{uuid.uuid4().hex[:16]}",
        "task_id": task_data.get("task_id", "OS-45"),
        "location": task_data.get("location", "UHE Paraibuna"),
        "created_at": datetime.now().isoformat() + "Z",
        "apr": {
            "prepared_by": task_data.get("operator", {"name": "João Silva", "cpf": "12345678900"}),
            "risk_category": "Alta (Fiação e ambiente com tensão)",
            "identified_hazards": [
                "Contato acidental com circuito energizado",
                "Ferramenta solta causando arco elétrico"
            ],
            "control_measures": [
                "Uso obrigatório de luva isolante + gorro resistente a arco",
                "Bloqueio prévio: desligamento e abertura de dispositivos"
            ]
        },
        "it": {
            "steps": [
                "1. Informar à operação que vai iniciar sequência de seccionamento",
                "2. Pirômetro: resistência de contato abaixo de 300mΩ",
                "3. Verificação de tensão = 0V antes de iniciar o trabalho",
                "4. Instalação de sinalizador próximo",
                "5. Realização de teste funcional p/ marcha de carga"
            ]
        },
        "pt": {
            "permit_approval": {
                "supervisor": "Maria Souza",
                "approved_at": datetime.now().isoformat() + "Z"
            },
            "validity": {
                "start": datetime.now().isoformat() + "Z",
                "end": datetime.now().replace(hour=17, minute=30).isoformat() + "Z"
            }
        }
    }
    
    # Simular hash
    import hashlib
    doc_str = json.dumps(doc, sort_keys=True)
    doc["hash"] = hashlib.sha256(doc_str.encode()).hexdigest()
    
    return doc

@app.get("/chat/online_users")
async def get_online_users():
    return {
        "online_users": ["joao.silva", "maria.souza", "carlos.lima"],
        "count": 3
    }

@app.post("/chat/send_notification")
async def send_notification(notification_data: dict):
    return {
        "status": "notification_sent",
        "message_id": str(uuid.uuid4()),
        "sent_at": datetime.now().isoformat() + "Z"
    }
