#!/usr/bin/env python3
"""
🚀 SEGUNDO NÓ AEONCOSMA P2P
Ativa um segundo nó independente na rede
"""

import sys
import os

# Adiciona path para importações
sys.path.append(os.path.dirname(__file__))

from aeoncosma.networking.p2p_node import P2PNode
import time

def main():
    """Ativa segundo nó na rede P2P"""
    print("🚀 INICIANDO SEGUNDO NÓ AEONCOSMA")
    print("=" * 40)
    
    # Configuração do segundo nó
    segundo_no = P2PNode(
        host="127.0.0.1",
        port=9001,
        node_id="segundo_no"
    )
    
    try:
        # Inicia o nó
        segundo_no.start()
        
        # Aguarda um pouco e tenta conectar ao nó principal
        time.sleep(2)
        print(f"\n🔗 Tentando conectar ao nó principal...")
        
        response = segundo_no.connect_to_peer("127.0.0.1", 9000, "segundo_no")
        if response:
            print(f"✅ Conectado ao nó principal: {response}")
        else:
            print(f"⚠️ Não conseguiu conectar ao nó principal")
        
        print(f"\n🌐 Segundo nó ativo. Pressione Ctrl+C para parar.")
        
        # Mantém o nó rodando
        while segundo_no.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Parando segundo nó...")
    finally:
        segundo_no.stop()
        print(f"✅ Segundo nó finalizado")

if __name__ == "__main__":
    main()
