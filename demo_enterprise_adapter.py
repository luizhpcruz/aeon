# demo_enterprise_adapter.py
"""
🌍 DEMONSTRAÇÃO AEONCOSMA ENTERPRISE ADAPTER
Exemplo completo de uso dos tentáculos empresariais
"""

import asyncio
from aeoncosma.adapters.enterprise_adapter import EnterpriseAdapter

async def demo_enterprise_adapter():
    """Demonstração completa do Enterprise Adapter"""
    print("🌍 DEMO: AEONCOSMA ENTERPRISE ADAPTER")
    print("=" * 60)
    
    # Cria adaptador
    adapter = EnterpriseAdapter("demo_enterprise_node")
    
    print(f"\n📊 STATUS INICIAL:")
    status = adapter.get_adapter_status()
    print(f"   Fontes configuradas: {len(status['configured_sources'])}")
    print(f"   Fontes ativas: {len(status['active_sources'])}")
    print(f"   NLP disponível: {status['nlp_available']}")
    print(f"   Segurança ativa: {status['security_enabled']}")
    
    # Testa conexões
    print(f"\n🔗 TESTANDO CONEXÕES:")
    connections = await adapter.test_all_connections()
    
    for source_id, result in connections.items():
        status_icon = "✅" if result["connected"] else "❌"
        print(f"   {status_icon} {source_id}: {'CONECTADO' if result['connected'] else 'FALHOU'}")
        if not result["connected"] and result.get("last_error"):
            print(f"      └─ Erro: {result['last_error'][:80]}...")
    
    # Demonstra busca de dados
    print(f"\n📊 EXTRAINDO INSIGHTS DE FONTES:")
    
    # Fonte 1: API de exemplo
    print(f"\n🔍 Fonte: sample_api")
    insight1 = await adapter.fetch_data("sample_api", "technology posts")
    if insight1:
        print(f"   ✅ Insight extraído (ID: {insight1.insight_id[:8]}...)")
        print(f"   📈 Confiança: {insight1.confidence:.2f}")
        print(f"   💭 Sentimento: {insight1.sentiment}")
        print(f"   🔑 Keywords: {', '.join(insight1.keywords[:3])}")
        print(f"   🏷️ Entidades: {len(insight1.entities)}")
    else:
        print(f"   ❌ Falha na extração")
    
    # Fonte 2: Documento local
    print(f"\n🔍 Fonte: local_documents")
    insight2 = await adapter.fetch_data("local_documents", "financial analysis")
    if insight2:
        print(f"   ✅ Insight extraído (ID: {insight2.insight_id[:8]}...)")
        print(f"   📈 Confiança: {insight2.confidence:.2f}")
        print(f"   💭 Sentimento: {insight2.sentiment}")
        print(f"   🔑 Keywords: {', '.join(insight2.keywords[:3])}")
        print(f"   🏷️ Entidades: {len(insight2.entities)}")
        
        # Mostra algumas entidades extraídas
        if insight2.entities:
            print(f"   📋 Entidades encontradas:")
            for entity in insight2.entities[:3]:
                print(f"      • {entity['type']}: {entity['value']}")
    else:
        print(f"   ❌ Falha na extração")
    
    # Insights recentes
    print(f"\n💡 INSIGHTS RECENTES:")
    recent_insights = adapter.get_recent_insights(limit=5)
    
    for i, insight in enumerate(recent_insights, 1):
        print(f"   {i}. {insight['insight_id'][:8]}... ({insight['source_id']})")
        print(f"      └─ {insight['sentiment']} | Confiança: {insight['confidence']:.2f}")
    
    # Status final
    print(f"\n📊 ESTATÍSTICAS FINAIS:")
    final_status = adapter.get_adapter_status()
    stats = final_status['stats']
    print(f"   Conexões bem-sucedidas: {stats['successful_connections']}")
    print(f"   Conexões falharam: {stats['failed_connections']}")
    print(f"   Buscas de dados: {stats['data_fetches']}")
    print(f"   Insights extraídos: {stats['insights_extracted']}")
    print(f"   Cache hits/misses: {stats['cache_hits']}/{stats['cache_misses']}")
    
    # Exporta ledger de insights
    print(f"\n📤 EXPORTANDO LEDGER DE INSIGHTS:")
    ledger = adapter.export_insights_ledger(limit=10)
    
    # Salva ledger
    import os
    os.makedirs("exports", exist_ok=True)
    ledger_file = f"exports/insights_ledger_demo.json"
    
    with open(ledger_file, 'w', encoding='utf-8') as f:
        f.write(ledger)
    
    print(f"   ✅ Ledger exportado: {ledger_file}")
    print(f"   📊 Total de insights no ledger: {len(recent_insights)}")
    
    print(f"\n🎯 DEMO CONCLUÍDA COM SUCESSO!")
    print(f"🌍 Enterprise Adapter pronto para integração empresarial")

if __name__ == "__main__":
    asyncio.run(demo_enterprise_adapter())
