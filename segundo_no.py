#!/usr/bin/env python3
"""
🔗 SEGUNDO NÓ AEONCOSMA - Teste de Conectividade P2P
Inicia segundo nó na porta 9001 para testar descoberta automática
"""

import sys
import os
import asyncio

# Adiciona path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'aeoncosma'))

async def main():
    """Executa segundo nó"""
    print("🔗 INICIANDO SEGUNDO NÓ AEONCOSMA")
    print("=" * 50)
    
    try:
        from main import AeonCosmaOrchestrator
        
        # Cria orquestrador do segundo nó
        orchestrator = AeonCosmaOrchestrator(
            node_id="aeon_beta",
            host="127.0.0.1", 
            port=9001  # Porta diferente
        )
        
        # Inicializa e inicia
        if await orchestrator.initialize():
            if await orchestrator.start():
                print("\n🎯 SEGUNDO NÓ EXECUTANDO - Pressione Ctrl+C para parar")
                
                # Mantém sistema rodando
                while orchestrator.running:
                    await asyncio.sleep(1)
            else:
                print("❌ Falha ao iniciar segundo nó")
                return 1
        else:
            print("❌ Falha ao inicializar segundo nó")
            return 1
            
    except KeyboardInterrupt:
        print("\n🛑 Segundo nó interrompido")
    except Exception as e:
        print(f"❌ Erro no segundo nó: {e}")
    finally:
        await orchestrator.stop()
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
