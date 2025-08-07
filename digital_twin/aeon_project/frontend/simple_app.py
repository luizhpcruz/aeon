import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    layout="wide", 
    page_title="AEON‑AI Platform", 
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1f77b4, #ff7f0e);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #1f77b4;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
.error-box {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Cabeçalho principal
st.markdown("""
<div class="main-header">
    <h1>🚀 AEON‑AI Digital Twin Platform</h1>
    <p>Sistema Integrado: IA Simbólica + UHE Simulation + SSMA + Chat Corporativo</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎛️ AEON‑AI Ops")
st.sidebar.markdown("---")

# Status do servidor
try:
    response = requests.get("http://localhost:8000/", timeout=2)
    if response.status_code == 200:
        st.sidebar.success("🟢 Backend Online")
        server_info = response.json()
        st.sidebar.json({"version": server_info.get("version", "N/A")})
    else:
        st.sidebar.error("🔴 Backend com problemas")
except:
    st.sidebar.error("🔴 Backend Offline")
    st.sidebar.warning("Inicie o servidor: `uvicorn backend.main:app --reload`")

st.sidebar.markdown("---")

# Menu de navegação
choice = st.sidebar.selectbox("📋 Seções", [
    "🏠 Dashboard", 
    "🧠 Kernel IA", 
    "💧 UHE Twin", 
    "📄 Documentos SSMA",
    "💬 Chat Test",
    "🔧 Sistema"
])

# === DASHBOARD ===
if choice == "🏠 Dashboard":
    st.title("📊 Dashboard Principal")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🧠 Kernel Status", "Online", "▲ 1.2%")
    with col2:
        st.metric("💧 UHEs Monitoradas", "6", "▲ 2")
    with col3:
        st.metric("📄 Docs Gerados", "23", "▲ 5")
    with col4:
        st.metric("👥 Usuários Online", "12", "▲ 3")
    
    st.markdown("---")
    
    # Gráfico de exemplo
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Evolução do Kernel IA")
        # Dados simulados
        df_kernel = pd.DataFrame({
            'Tempo': pd.date_range('2025-08-01', periods=10, freq='H'),
            'Valor': [1.0, 1.2, 1.5, 1.3, 1.8, 2.1, 1.9, 2.3, 2.0, 2.5]
        })
        st.line_chart(df_kernel.set_index('Tempo'))
    
    with col2:
        st.subheader("⚡ Geração UHE (GWh)")
        # Dados simulados
        df_uhe = pd.DataFrame({
            'UHE': ['Paraibuna', 'São Simão', 'Itaipu', 'Sobradinho'],
            'Geração': [85, 1710, 14000, 1050]
        })
        st.bar_chart(df_uhe.set_index('UHE'))

# === KERNEL IA ===
elif choice == "🧠 Kernel IA":
    st.title("🧠 Simulação do Kernel Simbólico")
    st.write("Evolução da IA baseada em símbolos com parâmetros ajustáveis.")
    
    with st.expander("ℹ️ Como usar", expanded=True):
        st.info("""
        **Parâmetros:**
        - **I**: Valor inicial (base: 1.0)
        - **Omega Info**: Fluxo de informação (0.0-1.0)
        - **Omega Caos**: Fator caótico (0.0-1.0)
        - **S**: Entropia do sistema (0.0-1.0)
        - **Phi**: Fator de coerência (0.0-1.0)
        """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎛️ Parâmetros")
        I = st.number_input("I (Valor Inicial)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        omega_info = st.slider("Omega Info", 0.0, 1.0, 0.5, 0.1)
        omega_caos = st.slider("Omega Caos", 0.0, 1.0, 0.2, 0.1)
        S = st.slider("S (Entropia)", 0.0, 1.0, 0.1, 0.1)
        Phi = st.slider("Phi (Coerência)", 0.0, 1.0, 0.05, 0.01)
        
        if st.button("🚀 Executar Evolução", type="primary"):
            try:
                payload = {
                    "I": I,
                    "omega_info": omega_info,
                    "omega_caos": omega_caos,
                    "S": S,
                    "Phi": Phi
                }
                response = requests.post("http://localhost:8000/kernel/evolve", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.kernel_result = result
                    st.success("✅ Evolução executada com sucesso!")
                else:
                    st.error(f"❌ Erro: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")
    
    with col2:
        st.subheader("📊 Resultado")
        if 'kernel_result' in st.session_state:
            result = st.session_state.kernel_result
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 Valor Evoluído: {result['evolved_value']:.3f}</h3>
                <p>🔗 Força da Rede: {result['symbol_strength']:.3f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulação de múltiplas evoluções
            if st.button("📈 Simular Sequência"):
                values = [I]
                for i in range(10):
                    new_val = values[-1] + (omega_info * 0.1 + omega_caos * 0.05)
                    values.append(new_val)
                
                df_evolution = pd.DataFrame({
                    'Iteração': range(11),
                    'Valor': values
                })
                st.line_chart(df_evolution.set_index('Iteração'))
        else:
            st.info("🎮 Execute uma evolução para ver os resultados")

# === UHE TWIN ===
elif choice == "💧 UHE Twin":
    st.title("💧 Digital Twin - Usinas Hidrelétricas")
    st.write("Simulação de geração energética baseada em dados reais das UHEs brasileiras.")
    
    # Upload ou seleção de dados
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ Configuração")
        
        # Período de simulação
        start_date = st.date_input("📅 Data Inicial", datetime.now().date())
        days = st.number_input("📊 Dias para simular", min_value=1, max_value=30, value=7)
        
        # Geração de dados de vazão
        st.subheader("🌊 Dados de Vazão")
        vazao_min = st.number_input("Vazão Mínima (m³/s)", min_value=10, max_value=500, value=100)
        vazao_max = st.number_input("Vazão Máxima (m³/s)", min_value=100, max_value=1000, value=300)
        
        # Gerar dados automaticamente
        dates = pd.date_range(start_date, periods=days)
        import random
        vazoes = [random.randint(vazao_min, vazao_max) for _ in range(days)]
        
        st.subheader("📋 Preview dos Dados")
        preview_df = pd.DataFrame({
            'Data': dates,
            'Vazão (m³/s)': vazoes
        })
        st.dataframe(preview_df, use_container_width=True)
        
        if st.button("⚡ Simular Geração", type="primary"):
            try:
                inflow_data = [
                    {"date": str(date), "inflow_m3_s": vazao} 
                    for date, vazao in zip(dates, vazoes)
                ]
                
                response = requests.post("http://localhost:8000/ops/simulate", json=inflow_data)
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.uhe_result = result
                    st.success(f"✅ Simulação concluída! {len(result)} registros gerados.")
                else:
                    st.error(f"❌ Erro na simulação: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")
    
    with col2:
        st.subheader("📊 Resultados da Simulação")
        
        if 'uhe_result' in st.session_state:
            result_df = pd.DataFrame(st.session_state.uhe_result)
            
            # Estatísticas
            col2a, col2b, col2c = st.columns(3)
            with col2a:
                st.metric("🏭 Usinas", result_df['plant'].nunique())
            with col2b:
                st.metric("⚡ Geração Total", f"{result_df['energy_gwh'].sum():.2f} GWh")
            with col2c:
                alertas = result_df['threshold_alert'].sum()
                st.metric("🚨 Alertas", alertas, delta=f"{'⚠️' if alertas > 0 else '✅'}")
            
            # Gráficos
            st.subheader("📈 Geração por Usina")
            chart_df = result_df.groupby('plant')['energy_gwh'].sum().reset_index()
            st.bar_chart(chart_df.set_index('plant'))
            
            # Tabela detalhada
            st.subheader("📋 Dados Detalhados")
            st.dataframe(result_df, use_container_width=True)
            
            # Alertas
            if alertas > 0:
                st.warning(f"⚠️ {alertas} alertas de baixa geração detectados!")
                alertas_df = result_df[result_df['threshold_alert'] == True]
                st.dataframe(alertas_df[['plant', 'energy_gwh', 'date']], use_container_width=True)
                
        else:
            st.info("🎮 Execute uma simulação para ver os resultados")

# === DOCUMENTOS SSMA ===
elif choice == "📄 Documentos SSMA":
    st.title("📄 Geração de Documentos SSMA")
    st.write("Sistema integrado para APR, IT e PT com assinatura digital gov.br.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📝 Novo Documento")
        
        task_id = st.text_input("🆔 ID da Tarefa", value="OS-47", help="Identificador único da ordem de serviço")
        location = st.text_input("📍 Local", value="UHE Paraibuna - Subestação A", help="Local onde a atividade será executada")
        
        doc_type = st.selectbox("📋 Tipo de Documento", 
                               ["APR", "IT", "PT", "APR+IT+PT"], 
                               index=3)
        
        # Informações do solicitante
        st.subheader("👤 Solicitante")
        operator_name = st.text_input("Nome", value="João Silva")
        operator_cpf = st.text_input("CPF", value="12345678900")
        operator_role = st.selectbox("Função", ["Operador", "Técnico", "Especialista"])
        
        if st.button("📄 Gerar Documento", type="primary"):
            try:
                payload = {
                    "task_id": task_id,
                    "location": location,
                    "operator": {
                        "name": operator_name,
                        "cpf": operator_cpf,
                        "role": operator_role
                    }
                }
                
                response = requests.post("http://localhost:8000/ops/generate_and_sign", json=payload)
                if response.status_code == 200:
                    document = response.json()
                    st.session_state.generated_doc = document
                    st.success("✅ Documento gerado com sucesso!")
                else:
                    st.error(f"❌ Erro na geração: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")
    
    with col2:
        st.subheader("📋 Documento Gerado")
        
        if 'generated_doc' in st.session_state:
            doc = st.session_state.generated_doc
            
            # Informações do documento
            st.markdown(f"""
            <div class="success-box">
                <h4>📄 {doc.get('document_id', 'N/A')}</h4>
                <p><strong>🆔 ID:</strong> {doc.get('task_id', 'N/A')}</p>
                <p><strong>📍 Local:</strong> {doc.get('location', 'N/A')}</p>
                <p><strong>🕒 Criado:</strong> {doc.get('created_at', 'N/A')}</p>
                <p><strong>🔐 Hash:</strong> {doc.get('hash', 'N/A')[:16]}...</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Seções do documento
            tabs = st.tabs(["🚨 APR", "📋 IT", "✅ PT", "🔍 JSON Completo"])
            
            with tabs[0]:
                if 'apr' in doc:
                    apr = doc['apr']
                    st.write("**👤 Preparado por:**", apr.get('prepared_by', {}).get('name', 'N/A'))
                    st.write("**⚠️ Categoria de Risco:**", apr.get('risk_category', 'N/A'))
                    
                    st.write("**🚨 Riscos Identificados:**")
                    for risk in apr.get('identified_hazards', []):
                        st.write(f"• {risk}")
                    
                    st.write("**🛡️ Medidas de Controle:**")
                    for measure in apr.get('control_measures', []):
                        st.write(f"• {measure}")
            
            with tabs[1]:
                if 'it' in doc:
                    it = doc['it']
                    st.write("**📋 Passos da Instrução de Trabalho:**")
                    for i, step in enumerate(it.get('steps', []), 1):
                        st.write(f"{i}. {step}")
            
            with tabs[2]:
                if 'pt' in doc:
                    pt = doc['pt']
                    st.write("**✅ Permissão de Trabalho Aprovada**")
                    approval = pt.get('permit_approval', {})
                    validity = pt.get('validity', {})
                    st.write(f"**📅 Válido de:** {validity.get('start', 'N/A')} até {validity.get('end', 'N/A')}")
            
            with tabs[3]:
                st.json(doc)
                
            # Ações do documento
            st.subheader("🔧 Ações")
            col2a, col2b, col2c = st.columns(3)
            with col2a:
                if st.button("📧 Compartilhar"):
                    st.info("📧 Documento compartilhado via chat!")
            with col2b:
                if st.button("🖨️ Imprimir PDF"):
                    st.info("🖨️ Gerando PDF...")
            with col2c:
                if st.button("🔍 Validar Hash"):
                    st.success("✅ Hash válido!")
        else:
            st.info("📝 Gere um documento para visualizar")

# === CHAT TEST ===
elif choice == "💬 Chat Test":
    st.title("💬 Teste do Sistema de Chat")
    st.write("Interface para testar a comunicação corporativa.")
    
    # Status da conexão
    try:
        response = requests.get("http://localhost:8000/chat/online_users")
        if response.status_code == 200:
            st.success("🟢 Sistema de Chat Online")
            users = response.json().get("online_users", [])
            st.write(f"👥 Usuários conectados: {len(users)}")
        else:
            st.error("🔴 Chat com problemas")
    except:
        st.error("🔴 Sistema de Chat Offline")
    
    # Teste de notificação
    st.subheader("📢 Enviar Notificação de Teste")
    
    col1, col2 = st.columns(2)
    with col1:
        notif_title = st.text_input("Título", value="Teste AEON")
        notif_content = st.text_area("Conteúdo", value="Mensagem de teste do sistema")
        notif_priority = st.selectbox("Prioridade", ["normal", "high", "emergency"])
    
    with col2:
        if st.button("📤 Enviar Notificação"):
            try:
                payload = {
                    "title": notif_title,
                    "content": notif_content,
                    "priority": notif_priority
                }
                response = requests.post("http://localhost:8000/chat/send_notification", json=payload)
                if response.status_code == 200:
                    st.success("✅ Notificação enviada!")
                else:
                    st.error(f"❌ Erro: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")

# === SISTEMA ===
elif choice == "🔧 Sistema":
    st.title("🔧 Informações do Sistema")
    
    # Status geral
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Status dos Serviços")
        
        # Backend
        try:
            response = requests.get("http://localhost:8000/")
            if response.status_code == 200:
                st.success("🟢 Backend FastAPI: Online")
                info = response.json()
                st.json(info)
            else:
                st.error("🔴 Backend: Com problemas")
        except:
            st.error("🔴 Backend: Offline")
        
        # Chat
        try:
            response = requests.get("http://localhost:8000/chat/online_users")
            if response.status_code == 200:
                st.success("🟢 Sistema Chat: Online")
            else:
                st.error("🔴 Sistema Chat: Com problemas")
        except:
            st.error("🔴 Sistema Chat: Offline")
    
    with col2:
        st.subheader("🚀 Comandos Rápidos")
        
        st.code("""
# Iniciar Backend
uvicorn backend.main:app --reload

# Iniciar Chat App
streamlit run frontend/chat_app.py

# Testar APIs
curl http://localhost:8000/
        """)
        
        st.subheader("📁 Estrutura do Projeto")
        st.text("""
aeon_project/
├── backend/           # APIs FastAPI
├── frontend/          # Interfaces Streamlit
├── aeon_kernel/       # IA Simbólica
├── aeon_ops/          # Operações SSMA
├── aeon_chat/         # Sistema Chat
└── tests/             # Testes
        """)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    🚀 <strong>AEON Digital Twin Platform v2.0</strong> | 
    🔒 Integração gov.br | 
    ⚡ Powered by FastAPI + Streamlit
</div>
""", unsafe_allow_html=True)
