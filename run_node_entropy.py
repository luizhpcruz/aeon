#!/usr/bin/env python3
"""
Standalone entropy node runner for P2P testing
"""
import asyncio
import json
import random
import math
from pathlib import Path

def simulate_entropy_simple(n_ciclos=40, n_fitas=5, n_celulas=32):
    """Simplified entropy simulation without external deps"""
    ciclos = list(range(n_ciclos))
    entropia_values = []
    complexidade_values = []
    
    for i in ciclos:
        base_entropy = 3.5 + 0.5 * math.sin(i * 0.3) + random.gauss(0, 0.1)
        base_complex = 0.6 + 0.2 * math.cos(i * 0.2) + random.gauss(0, 0.05)
        entropia_values.append(max(0.0, base_entropy))
        complexidade_values.append(max(0.0, min(1.0, base_complex)))
    
    return {
        "config": {"n_ciclos": n_ciclos, "n_fitas": n_fitas, "n_celulas": n_celulas},
        "resultados": {
            "entropia_global_media": sum(entropia_values) / len(entropia_values),
            "complexidade_global_media": sum(complexidade_values) / len(complexidade_values),
            "entropia_maxima": max(entropia_values),
        }
    }

async def run_entropy_node():
    """Simula um nó de entropia standalone que grava resultados locais"""
    print("🔬 Entropy Node - Starting...")
    
    try:
        # Executa simulação simplificada
        result = simulate_entropy_simple(n_ciclos=40, n_fitas=5, n_celulas=32)
        
        # Prepara payload para coordenador
        payload = {
            "ok": True,
            "node": "entropy",
            "timestamp": "2025-08-11T19:30:00",
            "n_ciclos": result["config"]["n_ciclos"],
            "n_fitas": result["config"]["n_fitas"],
            "entropia_media": result["resultados"]["entropia_global_media"],
            "complexidade_media": result["resultados"]["complexidade_global_media"],
            "entropia_max": result["resultados"]["entropia_maxima"],
        }
        
        # Salva resultado local
        logs_dir = Path("logs")
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = logs_dir / "node_entropy_result.json"
        output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        
        print(f"✅ Entropy: fitas={payload['n_fitas']} ciclos={payload['n_ciclos']} "
              f"H̄={payload['entropia_media']:.4f} C̄={payload['complexidade_media']:.4f} "
              f"Hmax={payload['entropia_max']:.4f}")
        print(f"📁 Resultado salvo em: {output_file}")
        
    except Exception as e:
        payload = {
            "ok": False,
            "node": "entropy", 
            "error": str(e),
            "timestamp": "2025-08-11T19:30:00"
        }
        print(f"❌ Entropy erro: {e}")
    
    return payload

if __name__ == "__main__":
    asyncio.run(run_entropy_node())
