#!/usr/bin/env python3
"""
🚀 ATIVADOR DE NÓS AEONCOSMA
Script para ativar múltiplos nós P2P simultaneamente
Desenvolvido por Luiz Cruz - 2025
"""

import subprocess
import time
import threading
import os
import sys

def run_node(command, node_name):
    """Executa um nó em processo separado"""
    try:
        print(f"🚀 Iniciando {node_name}...")
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Monitora saída em tempo real
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[{node_name}] {line.strip()}")
        
        process.wait()
        print(f"✅ {node_name} finalizado")
        
    except Exception as e:
        print(f"❌ Erro ao executar {node_name}: {e}")

def main():
    """Função principal - ativa múltiplos nós"""
    print("🌐 AEONCOSMA - ATIVADOR DE NÓS P2P")
    print("=" * 50)
    
    # Configuração dos nós
    nodes = [
        {
            "command": "python aeoncosma\\main.py",
            "name": "NÓ_PRINCIPAL",
            "delay": 0
        },
        {
            "command": "python aeoncosma\\networking\\p2p_node.py --port 9001 --node-id segundo_no",
            "name": "SEGUNDO_NÓ",
            "delay": 3
        },
        {
            "command": "python aeoncosma\\networking\\p2p_node.py --port 9002 --node-id terceiro_no",
            "name": "TERCEIRO_NÓ", 
            "delay": 6
        }
    ]
    
    threads = []
    
    for node in nodes:
        # Delay escalonado para inicialização
        if node["delay"] > 0:
            print(f"⏰ Aguardando {node['delay']}s para {node['name']}...")
            time.sleep(node["delay"])
        
        # Cria thread para o nó
        thread = threading.Thread(
            target=run_node,
            args=(node["command"], node["name"]),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        
        print(f"✅ {node['name']} iniciado em thread separada")
    
    print("\n🌐 TODOS OS NÓS FORAM INICIADOS!")
    print("💡 Pressione Ctrl+C para parar todos os nós")
    
    try:
        # Aguarda todos os threads
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\n🛑 Parando todos os nós...")
        print("✅ Sistema finalizado pelo usuário")

if __name__ == "__main__":
    main()
