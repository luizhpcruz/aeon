#!/usr/bin/env python3
"""
Standalone V.E.R.N.A. node runner for P2P testing
"""
import asyncio
import json
import random
from pathlib import Path

async def run_verna_node():
    """Simula um nó V.E.R.N.A. standalone que grava resultados locais"""
    print("🧠 V.E.R.N.A. Node - Starting...")
    
    try:
        # Simulação de emergência simbólica
        geracoes = 60
        cl = min(1.0, max(0.0, random.gauss(0.72, 0.08)))  # Cohesion Level
        k = min(1.0, max(0.0, random.gauss(0.35, 0.1)))    # Complexity
        emergence_factor = cl * k
        
        # Métricas sintéticas V.E.R.N.A.
        symbols_evolved = random.randint(15, 25)
        semantic_coherence = min(1.0, max(0.0, random.gauss(0.68, 0.12)))
        adaptation_rate = min(1.0, max(0.0, random.gauss(0.42, 0.08)))
        
        payload = {
            "ok": True,
            "node": "verna",
            "timestamp": "2025-08-11T19:30:00",
            "geracoes": geracoes,
            "cl": cl,
            "k": k,
            "emergence_factor": emergence_factor,
            "symbols_evolved": symbols_evolved,
            "semantic_coherence": semantic_coherence,
            "adaptation_rate": adaptation_rate,
            "status": "emergent_stable"
        }
        
        # Salva resultado local
        logs_dir = Path("logs")
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = logs_dir / "node_verna_result.json"
        output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        
        print(f"✅ V.E.R.N.A.: gen={payload['geracoes']} CL={payload['cl']:.3f} "
              f"K={payload['k']:.3f} símb={payload['symbols_evolved']} "
              f"coer={payload['semantic_coherence']:.3f}")
        print(f"📁 Resultado salvo em: {output_file}")
        
    except Exception as e:
        payload = {
            "ok": False,
            "node": "verna",
            "error": str(e),
            "timestamp": "2025-08-11T19:30:00"
        }
        print(f"❌ V.E.R.N.A. erro: {e}")
    
    return payload

if __name__ == "__main__":
    asyncio.run(run_verna_node())
