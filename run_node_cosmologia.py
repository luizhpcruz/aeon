#!/usr/bin/env python3
"""
Standalone cosmologia node runner for P2P testing  
"""
import asyncio
import json
import random
from pathlib import Path

async def run_cosmologia_node():
    """Simula um nó de cosmologia standalone que grava resultados locais"""
    print("🌌 Cosmologia Node - Starting...")
    
    try:
        # Parâmetros simulados
        n_obs = 200
        z_vals = [abs(random.gauss(1.0, 0.4)) for _ in range(n_obs)]
        z_vals.sort()
        z_median = z_vals[len(z_vals)//2] if z_vals else 0.0
        deflexao_media = max(0.0, random.gauss(0.02, 0.01))
        h0 = random.gauss(70.0, 5.0)  # Hubble constant
        
        payload = {
            "ok": True,
            "node": "cosmologia",
            "timestamp": "2025-08-11T19:30:00", 
            "n_obs": n_obs,
            "z_median": z_median,
            "deflexao_media": deflexao_media,
            "h0_estimate": h0,
            "modelo": "ΛCDM_synthetic"
        }
        
        # Salva resultado local
        logs_dir = Path("logs")
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = logs_dir / "node_cosmologia_result.json"
        output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        
        print(f"✅ Cosmologia: obs={payload['n_obs']} z~{payload['z_median']:.2f} "
              f"defl̄={payload['deflexao_media']:.4f} H₀={payload['h0_estimate']:.1f}")
        print(f"📁 Resultado salvo em: {output_file}")
        
    except Exception as e:
        payload = {
            "ok": False,
            "node": "cosmologia",
            "error": str(e),
            "timestamp": "2025-08-11T19:30:00"
        }
        print(f"❌ Cosmologia erro: {e}")
    
    return payload

if __name__ == "__main__":
    asyncio.run(run_cosmologia_node())
