# launch_aeoncosma.py
"""
🚀 LANÇAMENTO AEONCOSMA
Script simplificado para iniciar o sistema
"""

import sys
import os
import asyncio

# Adiciona path
sys.path.append('aeoncosma')

async def main():
    """Lança AEONCOSMA"""
    print("🚀 LANÇANDO AEONCOSMA - SISTEMA P2P COM IA AUTÔNOMA")
    print("=" * 60)
    
    try:
        # Importa e executa
        from aeoncosma.main import main as aeoncosma_main
        return await aeoncosma_main()
    except Exception as e:
        print(f"❌ Erro ao lançar: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
