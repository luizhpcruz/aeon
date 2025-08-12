#!/usr/bin/env python3
"""
Standalone coordinator node that aggregates results from other nodes
"""
import asyncio
import json
import time
from pathlib import Path
from typing import Dict, Any

async def run_coordinator_node():
    """Coordenador que monitora e agrega resultados dos outros nós"""
    print("🎯 Coordinator Node - Starting...")
    
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Arquivos de resultado esperados dos nós
    node_files = [
        ("entropy", "node_entropy_result.json"),
        ("cosmologia", "node_cosmologia_result.json"), 
        ("verna", "node_verna_result.json"),
        ("cosma", "node_cosma_result.json")
    ]
    
    aggregated_results = {}
    timeout_seconds = 30
    start_time = time.time()
    
    print("🔍 Aguardando resultados dos nós...")
    
    while time.time() - start_time < timeout_seconds:
        found_count = 0
        
        for node_name, filename in node_files:
            file_path = logs_dir / filename
            
            if file_path.exists() and node_name not in aggregated_results:
                try:
                    data = json.loads(file_path.read_text(encoding="utf-8"))
                    aggregated_results[node_name] = data
                    
                    if data.get("ok"):
                        print(f"✅ {node_name.upper()} recebido")
                    else:
                        print(f"❌ {node_name.upper()} com erro: {data.get('error', 'unknown')}")
                        
                except Exception as e:
                    print(f"⚠️  Erro ao ler {filename}: {e}")
            
            if node_name in aggregated_results:
                found_count += 1
        
        # Se temos todos os resultados, sair do loop
        if found_count == len(node_files):
            break
            
        await asyncio.sleep(0.5)
    
    # Criar resumo consolidado
    summary = {
        "coordinator_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "nodes_found": len(aggregated_results),
        "nodes_expected": len(node_files),
        "success_rate": len(aggregated_results) / len(node_files),
        "results": aggregated_results
    }
    
    # Salvar resumo consolidado
    summary_file = logs_dir / "coordinator_summary.json"
    summary_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Relatório final
    print(f"\n📊 RELATÓRIO FINAL:")
    print(f"Nós encontrados: {summary['nodes_found']}/{summary['nodes_expected']}")
    print(f"Taxa de sucesso: {summary['success_rate']:.1%}")
    
    successful_nodes = [name for name, data in aggregated_results.items() if data.get("ok")]
    failed_nodes = [name for name, data in aggregated_results.items() if not data.get("ok")]
    
    if successful_nodes:
        print(f"✅ Sucessos: {', '.join(successful_nodes)}")
    if failed_nodes:
        print(f"❌ Falhas: {', '.join(failed_nodes)}")
    
    missing_nodes = [name for name, _ in node_files if name not in aggregated_results]
    if missing_nodes:
        print(f"⏰ Timeout: {', '.join(missing_nodes)}")
    
    print(f"📁 Resumo salvo em: {summary_file}")
    
    return summary

if __name__ == "__main__":
    asyncio.run(run_coordinator_node())
