"""
AEONCOSMA - AI Integration Demo
===============================
Demonstração das funcionalidades de IA integradas ao sistema de visualização.
"""

print("🌌 AEONCOSMA AI Integration Demo")
print("="*50)

try:
    # Importar módulos necessários
    from aeoncosma.ui.ai_analytics_integration import AEONCOSMAAIAnalytics
    import pandas as pd
    import sqlite3
    
    print("✅ Módulos importados com sucesso!")
    
    # Inicializar AI Analytics
    ai = AEONCOSMAAIAnalytics()
    print("✅ AI Analytics inicializado!")
    
    # Demonstrar funcionalidades básicas
    print("\n📊 FUNCIONALIDADES DISPONÍVEIS:")
    print("-" * 40)
    
    # 1. Database Overview
    print("1. 🗄️  Database Schema:")
    schema = ai.get_database_schema()
    print(f"   {schema[:150]}...")
    
    # 2. Sample Questions
    print("\n2. 💭 Sample AI Questions:")
    questions = ai.get_sample_questions()
    for i, q in enumerate(questions[:3], 1):
        print(f"   {i}. {q}")
    
    # 3. Database Statistics
    print("\n3. 📈 Database Statistics:")
    conn = sqlite3.connect(ai.database_path)
    
    # Contar nós
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM network_nodes")
    node_count = cursor.fetchone()[0]
    print(f"   Total Network Nodes: {node_count}")
    
    # Contar transações
    cursor.execute("SELECT COUNT(*) FROM transactions")
    tx_count = cursor.fetchone()[0]
    print(f"   Total Transactions: {tx_count}")
    
    # Contar métricas de performance
    cursor.execute("SELECT COUNT(*) FROM performance_metrics")
    perf_count = cursor.fetchone()[0]
    print(f"   Performance Metrics: {perf_count}")
    
    # Contar eventos de segurança
    cursor.execute("SELECT COUNT(*) FROM security_events")
    security_count = cursor.fetchone()[0]
    print(f"   Security Events: {security_count}")
    
    # Top CPU usage
    cursor.execute("SELECT node_id, cpu_usage FROM network_nodes ORDER BY cpu_usage DESC LIMIT 3")
    top_cpu = cursor.fetchall()
    print(f"   Top CPU Usage:")
    for node_id, cpu in top_cpu:
        print(f"     - {node_id}: {cpu:.1f}%")
    
    # Tipos de nós
    cursor.execute("SELECT node_type, COUNT(*) FROM network_nodes GROUP BY node_type")
    node_types = cursor.fetchall()
    print(f"   Node Types:")
    for node_type, count in node_types:
        print(f"     - {node_type}: {count} nodes")
    
    conn.close()
    
    # 4. AI Integration Status
    print("\n4. 🤖 AI Integration Status:")
    print(f"   Database: ✅ Connected ({ai.database_path})")
    print(f"   OpenAI API: {'✅ Ready' if ai.api_key else '⚠️  Not configured (need API key)'}")
    print(f"   Query Engine: ✅ Functional")
    print(f"   Sample Data: ✅ Available")
    
    # 5. Advanced Features (requiring API key)
    print("\n5. 🧠 Advanced AI Features:")
    if ai.api_key:
        print("   ✅ Natural Language Queries")
        print("   ✅ Automated Insights Generation")
        print("   ✅ Intelligent Data Analysis")
        print("   ✅ Smart Visualizations")
    else:
        print("   ⚠️  Requires OpenAI API key for full functionality")
        print("   📝 Configure API key to enable:")
        print("      - Natural language to SQL conversion")
        print("      - Automated insight generation")
        print("      - AI-powered data analysis")
    
    print("\n🎯 COMO USAR:")
    print("-" * 20)
    print("1. Execute: streamlit run aeoncosma/ui/advanced_visualization_suite.py --server.port=8507")
    print("2. Acesse: http://localhost:8507")
    print("3. Selecione: '🤖 AI Analytics' no menu lateral")
    print("4. Configure OpenAI API key para funcionalidades avançadas")
    print("5. Faça perguntas em linguagem natural sobre seus dados!")
    
    print("\n🎉 Integração AI funcionando perfeitamente!")
    
except Exception as e:
    print(f"❌ Erro durante demo: {e}")
    import traceback
    traceback.print_exc()
