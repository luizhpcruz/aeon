#!/usr/bin/env python3
"""
🧪 TESTE INDIVIDUAL DE NÓ P2P
Testa criação e funcionalidade de um único nó
"""

import sys
import os
import time
from datetime import datetime

# Adiciona path para importações
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'aeoncosma'))

def test_single_node():
    """Testa um único nó P2P"""
    print("🧪 TESTE DE NÓ P2P INDIVIDUAL")
    print("=" * 40)
    
    try:
        # Importa classe do nó
        from aeoncosma.networking.p2p_node import P2PNode
        
        # Cria nó de teste
        print("🚀 Criando nó de teste...")
        node = P2PNode(
            host="127.0.0.1",
            port=9003,  # Porta diferente para teste
            node_id="teste_individual"
        )
        
        print(f"✅ Nó criado: {node.node_id}")
        print(f"📍 Endereço: {node.host}:{node.port}")
        
        # Verifica se sistema modular está ativo
        if hasattr(node, 'aeon_core') and node.aeon_core:
            print("🧠 Sistema AEON Core: ATIVO")
            
            # Testa decisão
            test_context = {
                "node_id": "peer_teste",
                "host": "127.0.0.1",
                "port": 9004,
                "timestamp": datetime.now().isoformat(),
                "reputation_score": 0.8,
                "context": {"type": "test_connection"}
            }
            
            decision = node.aeon_core.make_decision(test_context)
            print(f"🎯 Decisão AEON: {decision.get('approved')} (Score: {decision.get('final_score', 0):.3f})")
            
        else:
            print("⚠️ Sistema AEON Core: INATIVO (modo básico)")
        
        # Verifica informações da rede
        network_info = node.get_network_info()
        print(f"📊 Status da rede: {network_info.get('status')}")
        print(f"🔧 Modo de validação: {network_info.get('validation_mode')}")
        
        # Inicia o nó brevemente
        print("\n🚀 Iniciando nó para teste...")
        node.start()
        
        # Aguarda um pouco
        time.sleep(3)
        
        # Verifica se está rodando
        if node.running:
            print("✅ Nó está rodando corretamente")
            
            # Testa informações atualizadas
            updated_info = node.get_network_info()
            print(f"⏰ Uptime: {updated_info.get('uptime')}s")
            print(f"👥 Peers conectados: {updated_info.get('peers_count')}")
            
        else:
            print("❌ Nó não está rodando")
        
        # Para o nó
        print("\n🛑 Parando nó de teste...")
        node.stop()
        
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        return True
        
    except Exception as e:
        print(f"❌ ERRO NO TESTE: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 TESTE INDIVIDUAL AEONCOSMA")
    print("=" * 50)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = test_single_node()
    
    print("\n" + "=" * 50)
    if success:
        print("🎯 TESTE INDIVIDUAL: SUCESSO!")
        print("💡 Sistema está funcional e pronto para rede distribuída")
    else:
        print("❌ TESTE INDIVIDUAL: FALHOU!")
        print("⚠️ Verifique os erros acima")

if __name__ == "__main__":
    main()
