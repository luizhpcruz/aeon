#!/usr/bin/env python3
"""
🔌 TESTE RÁPIDO DE CONECTIVIDADE
Verifica nós ativos e testa conexão
"""

import socket
import json
import time
from datetime import datetime

def quick_port_scan():
    """Verifica rapidamente quais portas estão em uso"""
    print("🔍 VERIFICAÇÃO RÁPIDA DE PORTAS")
    print("=" * 30)
    
    ports = [9000, 9001, 9002, 8000, 8001]
    active_ports = []
    
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(('127.0.0.1', port))
            
            if result == 0:
                print(f"🟢 Porta {port}: ATIVA")
                active_ports.append(port)
            else:
                print(f"🔴 Porta {port}: Disponível")
                
            sock.close()
            
        except Exception as e:
            print(f"⚠️ Porta {port}: Erro - {e}")
    
    return active_ports

def test_node_connection(port):
    """Testa conexão com um nó específico"""
    try:
        print(f"\n🔗 Testando conexão com localhost:{port}")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect(('127.0.0.1', port))
        
        # Envia dados de teste
        test_data = {
            "node_id": f"test_client_{int(time.time())}",
            "host": "127.0.0.1",
            "port": 9999,
            "timestamp": datetime.now().isoformat(),
            "context": {"type": "connectivity_test"}
        }
        
        sock.send(json.dumps(test_data).encode('utf-8'))
        
        # Recebe resposta
        response = sock.recv(4096).decode('utf-8')
        if response:
            response_data = json.loads(response)
            print(f"📥 Resposta: {response_data}")
            
            if response_data.get("status") == "accepted":
                print(f"✅ Nó {port}: ACEITO")
                return True
            else:
                print(f"⚠️ Nó {port}: REJEITADO")
                return False
        
        sock.close()
        
    except Exception as e:
        print(f"❌ Erro ao conectar com porta {port}: {e}")
        return False

def main():
    """Executa teste rápido"""
    print("⚡ TESTE RÁPIDO DE CONECTIVIDADE AEONCOSMA")
    print("=" * 50)
    
    # Verifica portas ativas
    active_ports = quick_port_scan()
    
    if not active_ports:
        print("\n❌ NENHUM NÓ ATIVO DETECTADO")
        print("💡 Para ativar o sistema principal:")
        print("   python aeoncosma/main.py")
        return
    
    print(f"\n🎯 NETOS ATIVOS DETECTADOS: {len(active_ports)}")
    
    # Testa conectividade com nós ativos
    successful_connections = 0
    
    for port in active_ports:
        if test_node_connection(port):
            successful_connections += 1
    
    print(f"\n📊 RESULTADO:")
    print(f"🌐 Portas ativas: {len(active_ports)}")
    print(f"✅ Conexões bem-sucedidas: {successful_connections}")
    print(f"❌ Conexões falharam: {len(active_ports) - successful_connections}")
    
    if successful_connections > 0:
        print("\n🎯 REDE P2P OPERACIONAL!")
    else:
        print("\n⚠️ Nós detectados mas sem comunicação P2P")

if __name__ == "__main__":
    main()
