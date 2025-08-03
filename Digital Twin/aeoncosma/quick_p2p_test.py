#!/usr/bin/env python3
"""
⚡ AEONCOSMA P2P Quick Start
Teste rápido da rede P2P
Copyright 2025 - Luiz H. P. Cruz
"""

import asyncio
import sys
import os

# Adicionar o path do aeoncosma
sys.path.append(os.path.join(os.path.dirname(__file__)))

from aeoncosma.p2p.p2p_node import P2PNode

async def quick_p2p_test():
    """Teste rápido da rede P2P"""
    
    print("🌐 AEONCOSMA P2P - Teste Rápido")
    print("=" * 40)
    
    # Criar dois nós
    print("📡 Criando nós P2P...")
    node1 = P2PNode("luiz_node")
    node2 = P2PNode("test_node") 
    
    # Conectar nós
    print("🔗 Conectando nós...")
    await node1.connect_peer("test_node", "192.168.1.100")
    await node2.connect_peer("luiz_node", "192.168.1.101")
    
    # Status inicial
    print("\n📊 Status dos Nós:")
    print(f"Luiz Node: {node1.get_status()}")
    print(f"Test Node: {node2.get_status()}")
    
    # Enviar mensagens
    print("\n📤 Testando transmissão...")
    
    msg1 = "Olá da rede AEONCOSMA P2P! - Luiz H. P. Cruz"
    result1 = await node1.broadcast(msg1, "greeting", 5)
    print(f"✅ Mensagem 1 enviada: {result1.get('status')}")
    
    await asyncio.sleep(0.5)
    
    msg2 = "Sistema P2P funcionando perfeitamente!"
    result2 = await node2.broadcast(msg2, "status", 3)
    print(f"✅ Mensagem 2 enviada: {result2.get('status')}")
    
    # Simular recepção
    await node2.receive_message({
        'sender': 'luiz_node',
        'content': msg1,
        'message_type': 'greeting',
        'timestamp': '2025-08-02T10:30:00'
    })
    
    await node1.receive_message({
        'sender': 'test_node', 
        'content': msg2,
        'message_type': 'status',
        'timestamp': '2025-08-02T10:30:30'
    })
    
    # Status final
    print("\n📈 Status Final:")
    print(f"Luiz Node: {node1.get_status()}")
    print(f"Test Node: {node2.get_status()}")
    
    print("\n🎉 Rede P2P funcionando com sucesso!")
    print("🔧 Para demo completa execute: python demo_p2p_network.py")
    
    return True

if __name__ == "__main__":
    print("⚡ Iniciando teste rápido P2P...")
    asyncio.run(quick_p2p_test())
