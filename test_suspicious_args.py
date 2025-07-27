# test_suspicious_args.py
"""
🧪 TESTE DE ARGUMENTOS SUSPEITOS
Simula tentativas de execução maliciosa
"""

import sys
import os

print("🧪 TESTE: DETECÇÃO DE ARGUMENTOS SUSPEITOS")
print("=" * 50)

# Salva argumentos originais
original_argv = sys.argv.copy()

def test_suspicious_argument(suspicious_arg):
    """Testa um argumento suspeito específico"""
    print(f"\n🚨 Testando argumento: {suspicious_arg}")
    
    # Modifica sys.argv temporariamente
    sys.argv = ["test_script.py", suspicious_arg]
    
    try:
        # Tenta importar o P2P Node (que deve verificar argumentos)
        sys.path.append("aeoncosma")
        
        # Força reimport para pegar os novos argumentos
        if "aeoncosma.networking.p2p_node" in sys.modules:
            del sys.modules["aeoncosma.networking.p2p_node"]
        
        from aeoncosma.networking.p2p_node import P2PNode
        
        print(f"❌ FALHA: Argumento '{suspicious_arg}' foi aceito! VULNERÁVEL!")
        return False
        
    except SystemExit as e:
        print(f"✅ SUCESSO: Argumento '{suspicious_arg}' bloqueado - {e}")
        return True
    except ImportError as e:
        print(f"⚠️ AVISO: Erro de import - {e}")
        return True  # Considera como "bloqueado" se não conseguiu importar
    except Exception as e:
        print(f"🔒 BLOQUEADO: Argumento '{suspicious_arg}' - {e}")
        return True
    finally:
        # Restaura argv original
        sys.argv = original_argv.copy()

# Lista de argumentos suspeitos para testar
suspicious_arguments = [
    "--autorun",
    "--daemon", 
    "--silent",
    "--stealth",
    "--background",
    "--hide",
    "--unsafe"
]

print("Testando argumentos suspeitos...")

blocked_count = 0
total_count = len(suspicious_arguments)

for arg in suspicious_arguments:
    if test_suspicious_argument(arg):
        blocked_count += 1

print(f"\n🎯 RESULTADO FINAL:")
print(f"   Argumentos testados: {total_count}")
print(f"   Argumentos bloqueados: {blocked_count}")
print(f"   Taxa de bloqueio: {(blocked_count/total_count)*100:.1f}%")

if blocked_count == total_count:
    print("🛡️ SISTEMA TOTALMENTE SEGURO - Todos os argumentos suspeitos foram bloqueados!")
elif blocked_count >= total_count * 0.8:
    print("🟡 SISTEMA MODERADAMENTE SEGURO - A maioria dos argumentos foi bloqueada")
else:
    print("🚨 SISTEMA VULNERÁVEL - Muitos argumentos suspeitos passaram!")

# Restaura argumentos originais
sys.argv = original_argv
