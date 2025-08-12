#!/usr/bin/env python3
"""
Test node - simple version without imports
"""
import json
import random
from pathlib import Path

def test_node():
    print("🧪 Test Node - Starting...")
    
    # Simple synthetic data without external imports
    payload = {
        "ok": True,
        "node": "test",
        "timestamp": "2025-08-11T19:45:00",
        "random_value": random.random(),
        "test_metric": random.randint(10, 100)
    }
    
    # Save result
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = logs_dir / "test_node_result.json"
    output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"✅ Test: valor={payload['random_value']:.3f} métrica={payload['test_metric']}")
    print(f"📁 Resultado salvo em: {output_file}")
    
    return payload

if __name__ == "__main__":
    test_node()
