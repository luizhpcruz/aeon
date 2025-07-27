"""
🌌 AEONCOSMA DIRECT START - Solução para Problemas de Execução
"""
import subprocess
import sys
import os

def start_aeoncosma():
    print("🚀 Iniciando AEONCOSMA Trading...")
    try:
        # Executa o arquivo principal
        result = subprocess.run([sys.executable, "aeoncosma_simple.py"], 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    start_aeoncosma()
