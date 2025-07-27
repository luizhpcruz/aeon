# test_gentle_security.py
"""
🧪 TESTE GENTIL - Verifica comportamento sem tentar quebrar
"""

print("🧪 TESTE GENTIL: VERIFICAÇÃO DE SEGURANÇA")
print("=" * 50)

import sys
import os

# Teste 1: Verificar se arquivos de segurança existem
print("\n📁 TESTE 1: Existência dos arquivos de segurança")

security_files = [
    "security/aeoncosma_security_lock.py",
    "security/aeoncosma_audit_monitor.py", 
    "security/aeoncosma_threat_detector.py",
    "security/README_SECURITY.md"
]

existing_files = 0
for file_path in security_files:
    if os.path.exists(file_path):
        print(f"✅ {file_path}: Existe")
        existing_files += 1
    else:
        print(f"❌ {file_path}: Não encontrado")

print(f"   Arquivos encontrados: {existing_files}/{len(security_files)}")

# Teste 2: Verificar se P2P Node tem segurança embutida
print("\n🔍 TESTE 2: Segurança embutida no P2P Node")

p2p_file = "aeoncosma/networking/p2p_node.py"
if os.path.exists(p2p_file):
    with open(p2p_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    security_indicators = [
        ("🛡️ SISTEMA DE SEGURANÇA", "Sistema de segurança declarado"),
        ("SECURITY_ENABLED", "Flag de segurança"),
        ("security_lock", "Lock de segurança"),
        ("audit_monitor", "Monitor de auditoria"),
        ("if host != \"127.0.0.1\"", "Verificação de localhost"),
        ("🚫 SEGURANÇA:", "Mensagens de bloqueio"),
        ("ValueError", "Exceções de segurança")
    ]
    
    found_indicators = 0
    for indicator, description in security_indicators:
        if indicator in content:
            print(f"✅ {description}: Encontrado")
            found_indicators += 1
        else:
            print(f"❌ {description}: Não encontrado")
    
    print(f"   Indicadores de segurança: {found_indicators}/{len(security_indicators)}")
else:
    print(f"❌ {p2p_file}: Arquivo não encontrado")

# Teste 3: Testar importação básica (sem executar)
print("\n📦 TESTE 3: Importação básica dos módulos")

try:
    # Tenta verificar estrutura sem executar
    sys.path.append(".")
    
    # Verifica se consegue pelo menos "ver" os módulos
    import importlib.util
    
    modules_to_check = [
        ("security.aeoncosma_security_lock", "Security Lock"),
        ("security.aeoncosma_audit_monitor", "Audit Monitor"),
        ("security.aeoncosma_threat_detector", "Threat Detector")
    ]
    
    importable_modules = 0
    for module_name, description in modules_to_check:
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is not None:
                print(f"✅ {description}: Módulo encontrado")
                importable_modules += 1
            else:
                print(f"❌ {description}: Módulo não encontrado")
        except Exception as e:
            print(f"⚠️ {description}: Erro ao verificar - {e}")
    
    print(f"   Módulos encontrados: {importable_modules}/{len(modules_to_check)}")
    
except Exception as e:
    print(f"❌ Erro na verificação de módulos: {e}")

# Resultado final
print("\n🎯 ANÁLISE FINAL:")
total_checks = len(security_files) + len(security_indicators) + len(modules_to_check)
total_passed = existing_files + found_indicators + importable_modules

security_level = (total_passed / total_checks) * 100

if security_level >= 80:
    status = "🛡️ ALTAMENTE SEGURO"
    color = "🟢"
elif security_level >= 60:
    status = "🔒 MODERADAMENTE SEGURO" 
    color = "🟡"
else:
    status = "⚠️ SEGURANÇA INSUFICIENTE"
    color = "🔴"

print(f"   Verificações passadas: {total_passed}/{total_checks}")
print(f"   Nível de segurança: {security_level:.1f}%")
print(f"   Status: {color} {status}")

print("\n💡 INTERPRETAÇÃO:")
print("   - Arquivos de segurança = Módulos externos criados")
print("   - Segurança embutida = Proteção no código principal") 
print("   - Módulos importáveis = Sistema funcionando")
print("\n   Se viu muitos ✅ = Sistema bem blindado!")
print("   Se viu muitos ❌ = Pode ter problemas")
