import streamlit as st
import requests
import json
import websocket
import threading
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="AEON Chat - Comunicação Corporativa",
    page_icon="💬",
    layout="wide"
)

# CSS para estilizar o chat
st.markdown("""
<style>
.chat-message {
    padding: 0.5rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    border-left: 4px solid #4CAF50;
    background-color: #f0f2f6;
}
.emergency-alert {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #ff4b4b;
    color: white;
    border-left: 4px solid #d32f2f;
    margin: 0.5rem 0;
}
.ssma-alert {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #ff9800;
    color: white;
    border-left: 4px solid #f57c00;
    margin: 0.5rem 0;
}
.user-online {
    color: #4CAF50;
    font-weight: bold;
}
.user-offline {
    color: #757575;
}
</style>
""", unsafe_allow_html=True)

# Título e cabeçalho
st.title("💬 AEON Chat - Comunicação Corporativa")
st.subheader("Sistema integrado de comunicação para funcionários")

# Sidebar para login e configurações
with st.sidebar:
    st.header("👤 Login")
    
    # Simulação de login gov.br
    govbr_id = st.text_input("ID gov.br (CPF)", value="12345678900")
    user_name = st.text_input("Nome", value="João Silva")
    department = st.selectbox("Departamento", 
                             ["Operação", "Manutenção", "SSMA", "Administração", "Engenharia"])
    role = st.selectbox("Função", 
                       ["Operador", "Técnico", "Supervisor", "Gerente", "Especialista SSMA"])
    
    if st.button("🔐 Conectar"):
        st.session_state.user_logged_in = True
        st.session_state.user_data = {
            "govbr_id": govbr_id,
            "name": user_name,
            "department": department,
            "role": role
        }
        st.success(f"Conectado como {user_name}")
    
    st.divider()
    
    # Lista de usuários online
    st.header("👥 Usuários Online")
    try:
        response = requests.get("http://localhost:8000/chat/online_users")
        if response.status_code == 200:
            online_users = response.json().get("online_users", [])
            for user in online_users:
                st.markdown(f'<span class="user-online">🟢 {user}</span>', 
                           unsafe_allow_html=True)
        else:
            st.write("Nenhum usuário online")
    except:
        st.write("Servidor offline")

# Área principal do chat
if st.session_state.get("user_logged_in", False):
    
    # Tabs para diferentes tipos de comunicação
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat Geral", "🚨 Alertas SSMA", "📄 Documentos", "⚡ Emergência"])
    
    with tab1:
        st.header("Chat Geral")
        
        # Área de mensagens
        chat_container = st.container()
        
        # Input para nova mensagem
        col1, col2 = st.columns([4, 1])
        with col1:
            new_message = st.text_input("Digite sua mensagem...", key="chat_input")
        with col2:
            if st.button("📤 Enviar"):
                if new_message:
                    # Aqui seria enviado via WebSocket
                    st.success("Mensagem enviada!")
        
        # Mensagens do chat (simuladas)
        with chat_container:
            st.markdown("""
            <div class="chat-message">
                <strong>Maria Souza (SSMA)</strong> - 14:30<br>
                Lembrete: Reunião de segurança às 15h na sala de treinamento
            </div>
            <div class="chat-message">
                <strong>Carlos Lima (Operação)</strong> - 14:25<br>
                Manobra programada na SE-A concluída com sucesso
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.header("🚨 Alertas SSMA")
        
        # Formulário para criar alerta
        with st.expander("Criar Novo Alerta SSMA"):
            alert_type = st.selectbox("Tipo de Alerta", 
                                    ["Risco Identificado", "Incidente", "Quase-acidente", "Condição Insegura"])
            alert_location = st.text_input("Local")
            alert_description = st.text_area("Descrição do Alerta")
            alert_priority = st.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Crítica"])
            
            if st.button("🚨 Enviar Alerta SSMA"):
                alert_data = {
                    "type": "ssma_alert",
                    "alert_type": alert_type,
                    "location": alert_location,
                    "description": alert_description,
                    "priority": alert_priority,
                    "sender": st.session_state.user_data["name"]
                }
                try:
                    response = requests.post("http://localhost:8000/chat/send_notification", 
                                           json=alert_data)
                    if response.status_code == 200:
                        st.success("Alerta SSMA enviado!")
                    else:
                        st.error("Erro ao enviar alerta")
                except:
                    st.error("Servidor não disponível")
        
        # Alertas recentes
        st.subheader("Alertas Recentes")
        st.markdown("""
        <div class="ssma-alert">
            <strong>🚨 ALERTA SSMA - ALTA PRIORIDADE</strong><br>
            <strong>Local:</strong> UHE Paraibuna - Subestação A<br>
            <strong>Descrição:</strong> Vazamento de óleo detectado no transformador T1<br>
            <strong>Reportado por:</strong> Pedro Santos (Manutenção) - 13:45
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.header("📄 Compartilhamento de Documentos")
        
        # Gerar novo documento APR/IT/PT
        with st.expander("Gerar Documento SSMA"):
            doc_type = st.selectbox("Tipo de Documento", ["APR", "IT", "PT", "APR+IT+PT"])
            task_id = st.text_input("ID da Tarefa", value="OS-47")
            location = st.text_input("Local da Atividade", value="UHE Paraibuna")
            
            if st.button("📄 Gerar e Compartilhar"):
                try:
                    response = requests.post("http://localhost:8000/ops/generate_and_sign", 
                                           json={"task_id": task_id, "location": location})
                    if response.status_code == 200:
                        doc = response.json()
                        st.success(f"Documento gerado: {doc['document_id']}")
                        
                        # Compartilhar no chat
                        share_data = {
                            "type": "document_share",
                            "document_id": doc['document_id'],
                            "document_type": doc_type,
                            "title": f"{doc_type} - {task_id}",
                            "sender": st.session_state.user_data["name"]
                        }
                        st.json(doc)
                except:
                    st.error("Erro ao gerar documento")
        
        # Documentos compartilhados recentemente
        st.subheader("Documentos Compartilhados")
        st.info("📄 APR-OS-45.pdf - Compartilhado por Maria SSMA - 12:30")
        st.info("📄 IT-OS-46.pdf - Compartilhado por Carlos Operação - 11:15")
    
    with tab4:
        st.header("⚡ Canal de Emergência")
        
        # Botão de emergência
        st.error("🚨 USAR APENAS EM SITUAÇÕES DE EMERGÊNCIA REAL")
        
        emergency_type = st.selectbox("Tipo de Emergência", 
                                    ["Acidente de Trabalho", "Incêndio", "Vazamento", "Falha de Equipamento Crítico", "Emergência Médica"])
        emergency_location = st.text_input("Local da Emergência")
        emergency_description = st.text_area("Descrição da Emergência")
        
        if st.button("🚨 ATIVAR EMERGÊNCIA", type="primary"):
            emergency_data = {
                "title": f"EMERGÊNCIA: {emergency_type}",
                "description": emergency_description,
                "location": emergency_location,
                "severity": "critical",
                "sender": st.session_state.user_data["name"],
                "requires_ack": True
            }
            
            try:
                response = requests.post("http://localhost:8000/chat/send_notification", 
                                       json=emergency_data)
                if response.status_code == 200:
                    st.error("🚨 ALERTA DE EMERGÊNCIA ATIVADO!")
                    st.balloons()  # Efeito visual para chamar atenção
            except:
                st.error("Erro ao ativar emergência - Use meios alternativos!")

else:
    st.warning("👤 Por favor, faça login na barra lateral para acessar o chat")
    st.info("""
    ### 🌟 Funcionalidades do AEON Chat:
    
    **💬 Chat em Tempo Real:**
    - Comunicação instantânea entre funcionários
    - Grupos por departamento e função
    - Histórico de mensagens
    
    **🚨 Alertas SSMA:**
    - Notificações de segurança prioritárias
    - Relatório de incidentes em tempo real
    - Integração com documentos APR/IT/PT
    
    **📄 Compartilhamento de Documentos:**
    - Geração automática de APR, IT, PT
    - Assinatura digital integrada
    - Notificações de novos documentos
    
    **⚡ Canal de Emergência:**
    - Alerta imediato para toda a equipe
    - Geolocalização automática
    - Protocolo de resposta a emergências
    """)

# Rodapé
st.markdown("---")
st.caption("🔒 AEON Digital Twin - Sistema Corporativo Seguro | Integração gov.br")
