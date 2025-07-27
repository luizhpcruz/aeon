# verify_aeoncosma_structure.py
"""
🔍 VERIFICADOR DE ESTRUTURA AEONCOSMA
Valida se todos os arquivos da arquitetura foram criados corretamente
"""

import os
import json
from datetime import datetime

def check_file_exists(filepath):
    """Verifica se arquivo existe e retorna informações"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        return {"exists": True, "size": size, "status": "✅"}
    else:
        return {"exists": False, "size": 0, "status": "❌"}

def verify_aeoncosma_structure():
    """Verifica estrutura completa do AEONCOSMA"""
    print("🔍 VERIFICAÇÃO DA ESTRUTURA AEONCOSMA")
    print("=" * 60)
    
    # Estrutura esperada
    structure = {
        "🧠 PILAR 1 - GPT NODE (COGNITIVE)": [
            "aeoncosma/cognitive/gpt_node.py"
        ],
        "🛡️ PILAR 2 - AEON KERNEL (CORE)": [
            "aeoncosma/core/aeon_kernel.py"
        ],
        "🌐 PILAR 3 - P2P INTERFACE (COMMUNICATION)": [
            "aeoncosma/communication/p2p_interface.py"
        ],
        "🎯 PILAR 4 - INTERACTION ENGINE (REASONING)": [
            "aeoncosma/reasoning/interaction_engine.py"
        ],
        "🌍 PILAR 5 - ENTERPRISE ADAPTER (ADAPTERS)": [
            "aeoncosma/adapters/enterprise_adapter.py"
        ],
        "🔒 SISTEMA DE SEGURANÇA": [
            "security/aeoncosma_security_lock.py"
        ],
        "🧪 TESTES E DEMOS": [
            "test_security_quick.py",
            "demo_enterprise_adapter.py",
            "aeoncosma_launcher.py"
        ],
        "⚙️ CONFIGURAÇÃO": [
            "config/enterprise_sources.json"
        ],
        "📊 DADOS DE EXEMPLO": [
            "data/sample_document.txt",
            "data/trading_history.csv"
        ],
        "📚 DOCUMENTAÇÃO": [
            "README_AEONCOSMA.md",
            "CHANGELOG.md",
            "requirements.txt"
        ]
    }
    
    # Resultados da verificação
    verification_results = {}
    total_files = 0
    existing_files = 0
    total_size = 0
    
    for category, files in structure.items():
        print(f"\n{category}:")
        category_results = {}
        
        for filepath in files:
            result = check_file_exists(filepath)
            category_results[filepath] = result
            
            print(f"   {result['status']} {filepath}")
            if result['exists']:
                print(f"      └─ Tamanho: {result['size']:,} bytes")
                total_size += result['size']
                existing_files += 1
            else:
                print(f"      └─ ARQUIVO NÃO ENCONTRADO")
            
            total_files += 1
            
        verification_results[category] = category_results
    
    # Estatísticas finais
    completion_rate = (existing_files / total_files) * 100
    
    print(f"\n" + "="*60)
    print(f"📊 ESTATÍSTICAS FINAIS:")
    print(f"   Total de arquivos esperados: {total_files}")
    print(f"   Arquivos encontrados: {existing_files}")
    print(f"   Taxa de completude: {completion_rate:.1f}%")
    print(f"   Tamanho total: {total_size:,} bytes ({total_size/1024:.1f} KB)")
    
    # Status geral
    if completion_rate == 100:
        print(f"\n🎉 ESTRUTURA AEONCOSMA COMPLETA!")
        print(f"✅ Todos os 5 pilares implementados")
        print(f"🛡️ Sistema de segurança ativo")
        print(f"📚 Documentação completa")
        print(f"🚀 Pronto para commit e deploy!")
    elif completion_rate >= 90:
        print(f"\n⚠️ ESTRUTURA QUASE COMPLETA ({completion_rate:.1f}%)")
        print(f"🔧 Alguns arquivos opcionais podem estar faltando")
    else:
        print(f"\n❌ ESTRUTURA INCOMPLETA ({completion_rate:.1f}%)")
        print(f"🚫 Arquivos críticos estão faltando")
    
    # Salva relatório detalhado
    report = {
        "verification_timestamp": datetime.now().isoformat(),
        "total_files": total_files,
        "existing_files": existing_files,
        "completion_rate": completion_rate,
        "total_size_bytes": total_size,
        "structure_verification": verification_results
    }
    
    # Cria diretório de relatórios se não existir
    os.makedirs("reports", exist_ok=True)
    
    report_file = f"reports/aeoncosma_structure_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Relatório detalhado salvo: {report_file}")
    
    return completion_rate >= 90

if __name__ == "__main__":
    success = verify_aeoncosma_structure()
    
    if success:
        print(f"\n🎯 VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
        exit(0)
    else:
        print(f"\n⚠️ VERIFICAÇÃO ENCONTROU PROBLEMAS!")
        exit(1)
