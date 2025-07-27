# test_embedded_security.py
"""
🧪 TESTE DA SEGURANÇA EMBUTIDA NO P2P NODE
Testa a lógica de segurança que está dentro do próprio código
"""

import sys
import os

print("🧪 TESTE: SEGURANÇA EMBUTIDA NO P2P NODE")
print("=" * 50)

# Teste 1: Tentativa de host externo (DEVE FALHAR)
print("\n🚨 TESTE 1: Tentativa de host externo")
try:
    sys.path.append("aeoncosma")
    from aeoncosma.networking.p2p_node import P2PNode
    
    # Tenta criar nó com IP externo - DEVE SER BLOQUEADO
    node = P2PNode(host="192.168.1.100", port=9000, node_id="test_malicious")
    print("❌ FALHA: Host externo foi aceito! SISTEMA VULNERÁVEL!")
    
except ValueError as e:
    print(f"✅ SUCESSO: Host externo bloqueado - {e}")
except ImportError as e:
    print(f"⚠️ AVISO: Não foi possível importar P2PNode - {e}")
except Exception as e:
    print(f"🔒 BLOQUEADO: {e}")

# Teste 2: Tentativa de AEON address externo (DEVE FALHAR)
print("\n🚨 TESTE 2: Tentativa de AEON address externo")
try:
    node = P2PNode(
        host="127.0.0.1", 
        port=9000, 
        node_id="test_malicious", 
        aeon_address="http://malicious-server.com:8000/validate"
    )
    print("❌ FALHA: AEON externo foi aceito! SISTEMA VULNERÁVEL!")
    
except ValueError as e:
    print(f"✅ SUCESSO: AEON externo bloqueado - {e}")
except Exception as e:
    print(f"🔒 BLOQUEADO: {e}")

# Teste 3: Configuração normal (DEVE FUNCIONAR)
print("\n✅ TESTE 3: Configuração segura normal")
try:
    node = P2PNode(
        host="127.0.0.1", 
        port=9001, 
        node_id="test_secure", 
        aeon_address="http://127.0.0.1:8000/validate"
    )
    print("✅ SUCESSO: Configuração segura aceita")
    
    # Testa informações do nó
    info = node.get_network_info()
    print(f"   Node ID: {info['node_id']}")
    print(f"   Address: {info['address']}")
    print(f"   Security Mode: {info.get('validation_mode', 'unknown')}")
    
except Exception as e:
    print(f"❌ ERRO INESPERADO: {e}")

print("\n🎯 RESULTADO DO TESTE EMBEBIDO:")
print("Se viu '✅ SUCESSO: ... bloqueado' = SISTEMA SEGURO")
print("Se viu '❌ FALHA: ... aceito' = SISTEMA VULNERÁVEL")
