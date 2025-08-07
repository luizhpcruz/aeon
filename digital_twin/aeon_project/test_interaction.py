#!/usr/bin/env python3
"""
Exemplo de interação programática com AEON Digital Twin
"""

import requests
import json

# Configuração da API
BASE_URL = "http://localhost:8000"

def test_kernel_evolution():
    """Testa evolução do kernel simbólico"""
    response = requests.post(f"{BASE_URL}/kernel/evolve", json={
        "I": 1.0,
        "omega_info": 0.5,
        "omega_caos": 0.2,
        "S": 0.1,
        "Phi": 0.05
    })
    return response.json()

def test_uhe_simulation():
    """Testa simulação de UHEs"""
    inflow_data = [
        {"date": "2025-08-01", "inflow_m3_s": 150},
        {"date": "2025-08-02", "inflow_m3_s": 200},
        {"date": "2025-08-03", "inflow_m3_s": 180}
    ]
    response = requests.post(f"{BASE_URL}/ops/simulate", json=inflow_data)
    return response.json()

def test_document_generation():
    """Testa geração de documentos SSMA"""
    response = requests.post(f"{BASE_URL}/ops/generate_and_sign", json={
        "task_id": "OS-45",
        "location": "UHE Paraibuna - Subestação"
    })
    return response.json()

if __name__ == "__main__":
    print("🧠 Testando Kernel Simbólico...")
    kernel_result = test_kernel_evolution()
    print(f"Resultado: {kernel_result}")
    
    print("\n⚡ Testando Simulação UHE...")
    uhe_result = test_uhe_simulation()
    print(f"Simulações geradas: {len(uhe_result)} registros")
    
    print("\n📄 Testando Geração de Documentos...")
    doc_result = test_document_generation()
    print(f"Documento ID: {doc_result.get('document_id', 'N/A')}")
    print(f"Hash: {doc_result.get('hash', 'N/A')[:16]}...")
