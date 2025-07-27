#!/usr/bin/env python3
"""
🌐 ATIVADOR FINAL DE NÓS AEONCOSMA
Sistema para ativar rede P2P distribuída
Desenvolvido por Luiz Cruz - 2025
"""

import subprocess
import time
import sys
import os
from datetime import datetime

def start_node_process(port, node_id, delay=0):
    """Inicia um nó em processo separado"""
    try:
        if delay > 0:
            print(f"⏰ Aguardando {delay}s para {node_id}...")
            time.sleep(delay)
        
        # Comando para iniciar o nó
        cmd = f'python aeoncosma/networking/p2p_node.py --port {port} --node-id {node_id}'
        
        print(f"🚀 Iniciando {node_id} na porta {port}...")
        
        # Inicia processo
        process = subprocess.Popen(
            cmd,
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        print(f"✅ {node_id} iniciado (PID: {process.pid})")
        return process
        
    except Exception as e:
        print(f"❌ Erro ao iniciar {node_id}: {e}")
        return None

def check_node_status(port):
    """Verifica se um nó está ativo"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    """Ativa múltiplos nós AEONCOSMA"""
    print("🌐 ATIVADOR FINAL - REDE AEONCOSMA P2P")
    print("=" * 50)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuração dos nós
    nodes = [
        {"port": 9000, "node_id": "aeon_principal", "delay": 0},
        {"port": 9001, "node_id": "segundo_no", "delay": 2},
        {"port": 9002, "node_id": "terceiro_no", "delay": 4}
    ]
    
    processes = []
    
    # Verifica quais nós já estão ativos
    print("\n🔍 Verificando nós existentes...")
    active_nodes = []
    
    for node in nodes:
        if check_node_status(node["port"]):
            print(f"🟢 {node['node_id']} (porta {node['port']}): JÁ ATIVO")
            active_nodes.append(node)
        else:
            print(f"🔴 {node['node_id']} (porta {node['port']}): INATIVO")
    
    # Inicia nós inativos
    nodes_to_start = [n for n in nodes if n not in active_nodes]
    
    if not nodes_to_start:
        print("\n✅ TODOS OS NÓS JÁ ESTÃO ATIVOS!")
    else:
        print(f"\n🚀 Iniciando {len(nodes_to_start)} nós...")
        
        for node in nodes_to_start:
            process = start_node_process(
                node["port"], 
                node["node_id"], 
                node["delay"]
            )
            if process:
                processes.append((process, node))
    
    # Aguarda inicialização e verifica status
    if nodes_to_start:
        print("\n⏰ Aguardando inicialização completa...")
        time.sleep(10)
    
    # Verifica status final
    print("\n📊 VERIFICAÇÃO FINAL DA REDE:")
    active_count = 0
    
    for node in nodes:
        if check_node_status(node["port"]):
            print(f"✅ {node['node_id']} (porta {node['port']}): ATIVO")
            active_count += 1
        else:
            print(f"❌ {node['node_id']} (porta {node['port']}): FALHOU")
    
    # Resultado final
    print("\n" + "=" * 50)
    print(f"📈 RESULTADO: {active_count}/{len(nodes)} nós ativos")
    
    if active_count == len(nodes):
        print("🎯 REDE P2P COMPLETAMENTE DISTRIBUÍDA!")
        print("🌐 Sistema AEONCOSMA 100% operacional")
    elif active_count >= 2:
        print("🟡 Rede parcialmente distribuída")
        print("⚠️ Alguns nós falharam na inicialização")
    elif active_count == 1:
        print("🟠 Apenas 1 nó ativo - Rede centralizada")
    else:
        print("🔴 NENHUM NÓ ATIVO - Sistema falhou")
    
    print(f"\n💡 Para conectar manualmente:")
    print(f"   Nó Principal: localhost:9000")
    print(f"   Segundo Nó: localhost:9001")
    print(f"   Terceiro Nó: localhost:9002")
    
    print(f"\n🔧 Para monitorar: python monitor_nos.py")
    print(f"🧪 Para testar: python teste_rapido.py")

if __name__ == "__main__":
    main()
