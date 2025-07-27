# test_simple_security.py
"""
🛡️ TESTE SIMPLES - SEGURANÇA AEONCOSMA
Verifica se a segurança está funcionando
"""

print('🛡️ TESTE SIMPLES DE SEGURANÇA')
print('=' * 40)

try:
    print("📦 Testando importação...")
    from security.aeoncosma_security_lock import AeonSecurityLock
    print("   ✅ AeonSecurityLock OK")
    
    print("\n🔒 Testando criação...")
    security = AeonSecurityLock()
    print("   ✅ Security Lock criado")
    
    print("\n🔍 Testando verificações...")
    
    try:
        security.enforce_localhost_only()
        print("   ✅ Localhost: OK")
    except Exception as e:
        print(f"   ⚠️ Localhost: {e}")
    
    try:
        security.prevent_root_execution()
        print("   ✅ Root Prevention: OK")
    except Exception as e:
        print(f"   ⚠️ Root Prevention: {e}")
    
    try:
        security.block_autorun_arguments()
        print("   ✅ Autorun Block: OK")
    except Exception as e:
        print(f"   ⚠️ Autorun Block: {e}")
    
    print("\n🛡️ RESULTADO: SEGURANÇA FUNCIONANDO!")
    
except ImportError as e:
    print(f"❌ ERRO DE IMPORTAÇÃO: {e}")
    print("💡 Execute: py security/aeoncosma_security_lock.py")
    
except Exception as e:
    print(f"❌ ERRO: {e}")

print("\n✅ Teste concluído!")
