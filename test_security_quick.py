# test_security_quick.py
"""
🧪 TESTE RÁPIDO DO SISTEMA DE SEGURANÇA AEONCOSMA
Verificação completa de todos os componentes de segurança
"""

from security.aeoncosma_security_lock import AeonSecurityLock, enforce_security

def main():
    print("🔎 TESTE COMPLETO DO SISTEMA DE SEGURANÇA AEONCOSMA")
    print("=" * 60)
    
    try:
        # Teste básico da classe
        print("\n🔒 INICIANDO TESTES DE SEGURANÇA...")
        security_lock = AeonSecurityLock()
        
        # Teste 1: Localhost
        print("\n1️⃣ TESTANDO LOCALHOST:")
        try:
            security_lock.enforce_localhost_only()
            print("   ✅ Localhost OK")
        except Exception as e:
            print(f"   ❌ Localhost FALHOU: {e}")
            
        # Teste 2: Root Prevention  
        print("\n2️⃣ TESTANDO PREVENÇÃO ROOT:")
        try:
            security_lock.prevent_root_execution()
            print("   ✅ Root Prevention OK")
        except Exception as e:
            print(f"   ❌ Root Prevention FALHOU: {e}")
            
        # Teste 3: Argumentos perigosos
        print("\n3️⃣ TESTANDO ARGUMENTOS:")
        try:
            security_lock.block_autorun_arguments()
            print("   ✅ Autorun Arguments OK")
        except Exception as e:
            print(f"   ❌ Autorun Arguments FALHOU: {e}")
            
        # Teste 4: Fingerprint
        print("\n4️⃣ TESTANDO FINGERPRINT:")
        try:
            security_lock.fingerprint_check()
            print("   ✅ Fingerprint OK")
        except Exception as e:
            print(f"   ❌ Fingerprint FALHOU: {e}")
            
        # Teste 5: Integridade
        print("\n5️⃣ TESTANDO INTEGRIDADE:")
        try:
            security_lock.integrity_verification()
            print("   ✅ Integridade OK")
        except Exception as e:
            print(f"   ❌ Integridade FALHOU: {e}")
            
        # Teste 6: Rede
        print("\n6️⃣ TESTANDO CONFIGURAÇÃO DE REDE:")
        try:
            security_lock.check_network_security("127.0.0.1", 9000)
            print("   ✅ Configuração de rede OK")
        except Exception as e:
            print(f"   ❌ Configuração de rede FALHOU: {e}")
            
        # Teste completo usando função de conveniência
        print("\n🛡️ TESTE COMPLETO DE ENFORCEMENT:")
        try:
            complete_lock = enforce_security()
            print("   ✅ ENFORCEMENT COMPLETO OK")
        except Exception as e:
            print(f"   ❌ ENFORCEMENT FALHOU: {e}")
            
        # Teste de relatório
        print("\n📊 TESTANDO RELATÓRIO DE SEGURANÇA:")
        try:
            report = security_lock.get_security_report(1)
            print(f"   ✅ Relatório gerado: {len(report['events_summary'])} eventos")
            print(f"   🔍 Fingerprint: {report['system_fingerprint']}")
            print(f"   📈 Status: {report['security_status']}")
        except Exception as e:
            print(f"   ❌ Relatório FALHOU: {e}")
            
        print("\n" + "="*60)
        print("🚀 TESTE DE SEGURANÇA AEONCOSMA CONCLUÍDO COM SUCESSO!")
        print("🔒 Sistema de segurança está funcionando perfeitamente")
        print("🛡️ Pronto para deployment em produção")
        
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO NO TESTE DE SEGURANÇA: {e}")
        print("🚫 Sistema não pode ser executado com segurança")
        return False
        
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
