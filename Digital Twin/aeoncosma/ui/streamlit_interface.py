"""
🌟 AEONCOSMA Streamlit Interface
Interface web interativa para plataforma AEONCOSMA
Copyright 2025 - Luiz H. P. Cruz
"""

import streamlit as st
import asyncio
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="AEONCOSMA Engine",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .module-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin-bottom: 1rem;
    }
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    .status-online { background-color: #28a745; }
    .status-offline { background-color: #dc3545; }
    .status-warning { background-color: #ffc107; }
</style>
""", unsafe_allow_html=True)

# URL da API
API_BASE_URL = "http://localhost:8000"

def check_api_status():
    """Verificar se a API está online"""
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_system_status():
    """Obter status do sistema"""
    try:
        response = requests.get(f"{API_BASE_URL}/status")
        return response.json() if response.status_code == 200 else None
    except:
        return None

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🌟 AEONCOSMA Engine</h1>
    <p>Plataforma Modular Integrando IA, Blockchain, P2P, Quantum e Cosmologia</p>
    <p><strong>Criado por: Luiz H. P. Cruz</strong></p>
</div>
""", unsafe_allow_html=True)

# Sidebar para navegação
st.sidebar.title("🚀 Navegação")

# Verificar status da API
api_online = check_api_status()
status_color = "status-online" if api_online else "status-offline"
status_text = "Online" if api_online else "Offline"

st.sidebar.markdown(f"""
<div style="margin-bottom: 20px;">
    <h4>Status da API:</h4>
    <span class="status-indicator {status_color}"></span> {status_text}
</div>
""", unsafe_allow_html=True)

# Menu de módulos
modules = [
    "🏠 Dashboard",
    "🧠 Inteligência Artificial", 
    "🔐 Criptografia",
    "🌐 Rede P2P",
    "📡 Comunicação Quântica",
    "🌌 Análise Cosmológica"
]

selected_module = st.sidebar.selectbox("Selecione o Módulo:", modules)

# ============================================================================
# 🏠 DASHBOARD
# ============================================================================

if selected_module == "🏠 Dashboard":
    st.header("📊 Dashboard do Sistema")
    
    if api_online:
        system_status = get_system_status()
        
        if system_status:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🚀 Sistema", "AEONCOSMA", "Operacional")
            
            with col2:
                st.metric("📅 Data", datetime.now().strftime("%d/%m/%Y"))
            
            with col3:
                st.metric("⏰ Hora", datetime.now().strftime("%H:%M:%S"))
            
            st.subheader("🔧 Status dos Módulos")
            
            modules_data = system_status.get("modules", {})
            
            # Cards dos módulos
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="module-card">
                    <h4>🧠 Inteligência Artificial</h4>
                    <p>Sistema de aprendizado neural e simbólico</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="module-card">
                    <h4>🔐 Criptografia</h4>
                    <p>Segurança avançada com AES-256 e RSA-4096</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="module-card">
                    <h4>📡 Comunicação Quântica</h4>
                    <p>Protocolo BB84 para distribuição de chaves</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="module-card">
                    <h4>🌐 Rede P2P</h4>
                    <p>Comunicação descentralizada peer-to-peer</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="module-card">
                    <h4>🌌 Análise Cosmológica</h4>
                    <p>Dados do Pantheon+, Planck e BAO</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Erro ao obter status do sistema")
    else:
        st.error("❌ API não está disponível. Verifique se o servidor está rodando.")
        st.info("💡 Execute: `python aeoncosma_api.py` para iniciar a API")

# ============================================================================
# 🧠 INTELIGÊNCIA ARTIFICIAL
# ============================================================================

elif selected_module == "🧠 Inteligência Artificial":
    st.header("🧠 Módulo de Inteligência Artificial")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Treinamento", "🔮 Predição", "📈 Modelos"])
    
    with tab1:
        st.subheader("🎯 Treinamento de Modelo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            model_type = st.selectbox("Tipo de Modelo:", ["neural", "symbolic", "hybrid"])
            epochs = st.slider("Épocas de Treinamento:", 10, 1000, 100)
        
        with col2:
            data_format = st.selectbox("Formato dos Dados:", ["JSON", "CSV", "Array"])
        
        data_input = st.text_area("Dados de Treinamento (JSON):", 
                                  value='[{"x": [1, 2, 3], "y": 1}, {"x": [2, 3, 4], "y": 0}]',
                                  height=150)
        
        if st.button("🚀 Iniciar Treinamento"):
            if api_online:
                try:
                    data = json.loads(data_input)
                    payload = {
                        "data": data,
                        "model_type": model_type,
                        "epochs": epochs
                    }
                    
                    with st.spinner("Treinando modelo..."):
                        response = requests.post(f"{API_BASE_URL}/ia/learn", json=payload)
                        
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Treinamento concluído!")
                        st.json(result)
                    else:
                        st.error("❌ Erro no treinamento")
                        
                except json.JSONDecodeError:
                    st.error("❌ Formato JSON inválido")
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
            else:
                st.error("❌ API não disponível")
    
    with tab2:
        st.subheader("🔮 Predição")
        
        prediction_input = st.text_area("Dados para Predição:", 
                                       value='{"features": [1, 2, 3, 4]}')
        
        if st.button("🎯 Fazer Predição"):
            if api_online:
                try:
                    data = json.loads(prediction_input)
                    response = requests.post(f"{API_BASE_URL}/ia/predict", json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Predição realizada!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Predição", result.get("prediction", "N/A"))
                        with col2:
                            confidence = result.get("confidence", 0)
                            st.metric("Confiança", f"{confidence:.2%}")
                            
                    else:
                        st.error("❌ Erro na predição")
                        
                except json.JSONDecodeError:
                    st.error("❌ Formato JSON inválido")
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
            else:
                st.error("❌ API não disponível")
    
    with tab3:
        st.subheader("📈 Modelos Disponíveis")
        
        if api_online:
            try:
                response = requests.get(f"{API_BASE_URL}/ia/models")
                if response.status_code == 200:
                    models = response.json()
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("🧠 **Modelos Neurais:**")
                        for model in models.get("neural_architectures", []):
                            st.write(f"• {model}")
                    
                    with col2:
                        st.write("🔧 **Modelos Simbólicos:**")
                        for model in models.get("symbolic_methods", []):
                            st.write(f"• {model}")
                    
                    with col3:
                        st.write("🔀 **Modelos Híbridos:**")
                        for model in models.get("hybrid_approaches", []):
                            st.write(f"• {model}")
                            
            except Exception as e:
                st.error(f"❌ Erro ao carregar modelos: {str(e)}")
        else:
            st.error("❌ API não disponível")

# ============================================================================
# 🔐 CRIPTOGRAFIA
# ============================================================================

elif selected_module == "🔐 Criptografia":
    st.header("🔐 Módulo de Criptografia")
    
    tab1, tab2, tab3 = st.tabs(["🔒 Criptografia", "🔓 Descriptografia", "✍️ Assinatura"])
    
    with tab1:
        st.subheader("🔒 Criptografar Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            algorithm = st.selectbox("Algoritmo:", ["AES-GCM", "AES-CBC", "ChaCha20-Poly1305"])
        
        data_to_encrypt = st.text_area("Dados para Criptografar:", 
                                     value="Mensagem secreta do AEONCOSMA")
        
        if st.button("🔒 Criptografar"):
            if api_online and data_to_encrypt:
                try:
                    payload = {
                        "data": data_to_encrypt,
                        "algorithm": algorithm
                    }
                    
                    with st.spinner("Criptografando..."):
                        response = requests.post(f"{API_BASE_URL}/crypto/encrypt", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Dados criptografados!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.text_area("Dados Criptografados:", 
                                       value=result.get("encrypted_data", ""), 
                                       height=100)
                        with col2:
                            st.text_area("Chave:", 
                                       value=result.get("key", ""), 
                                       height=100)
                        
                        st.json(result)
                    else:
                        st.error("❌ Erro na criptografia")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
            else:
                st.error("❌ API não disponível ou dados vazios")
    
    with tab2:
        st.subheader("🔓 Descriptografar Dados")
        
        encrypted_data = st.text_area("Dados Criptografados:")
        key = st.text_area("Chave:")
        algorithm_decrypt = st.selectbox("Algoritmo:", ["AES-GCM", "AES-CBC", "ChaCha20-Poly1305"], key="decrypt_algo")
        
        if st.button("🔓 Descriptografar"):
            if api_online and encrypted_data and key:
                try:
                    payload = {
                        "encrypted_data": encrypted_data,
                        "key": key,
                        "algorithm": algorithm_decrypt
                    }
                    
                    with st.spinner("Descriptografando..."):
                        response = requests.post(f"{API_BASE_URL}/crypto/decrypt", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Dados descriptografados!")
                        st.text_area("Mensagem Original:", 
                                   value=result.get("decrypted_data", ""))
                        st.json(result)
                    else:
                        st.error("❌ Erro na descriptografia")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
            else:
                st.error("❌ Campos obrigatórios não preenchidos")
    
    with tab3:
        st.subheader("✍️ Assinatura Digital")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📝 Assinar Mensagem**")
            message_to_sign = st.text_area("Mensagem:", value="Documento AEONCOSMA")
            
            if st.button("✍️ Assinar"):
                if api_online and message_to_sign:
                    try:
                        payload = {"message": message_to_sign}
                        response = requests.post(f"{API_BASE_URL}/crypto/sign", json=payload)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✅ Mensagem assinada!")
                            st.text_area("Assinatura:", value=result.get("signature", ""))
                            st.session_state.signature = result.get("signature", "")
                            st.session_state.public_key = result.get("public_key", "")
                        else:
                            st.error("❌ Erro na assinatura")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
        
        with col2:
            st.write("**✅ Verificar Assinatura**")
            message_to_verify = st.text_area("Mensagem:", key="verify_msg")
            signature_to_verify = st.text_area("Assinatura:", 
                                             value=st.session_state.get("signature", ""))
            public_key = st.text_area("Chave Pública:", 
                                    value=st.session_state.get("public_key", ""))
            
            if st.button("✅ Verificar"):
                if api_online and all([message_to_verify, signature_to_verify, public_key]):
                    try:
                        payload = {
                            "message": message_to_verify,
                            "signature": signature_to_verify,
                            "public_key": public_key
                        }
                        response = requests.post(f"{API_BASE_URL}/crypto/verify", json=payload)
                        
                        if response.status_code == 200:
                            result = response.json()
                            if result.get("valid", False):
                                st.success("✅ Assinatura válida!")
                            else:
                                st.error("❌ Assinatura inválida!")
                            st.json(result)
                        else:
                            st.error("❌ Erro na verificação")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")

# ============================================================================
# 🌐 REDE P2P
# ============================================================================

elif selected_module == "🌐 Rede P2P":
    st.header("🌐 Módulo de Rede P2P")
    
    tab1, tab2, tab3 = st.tabs(["📡 Broadcast", "👥 Peers", "💬 Mensagens"])
    
    with tab1:
        st.subheader("📡 Transmitir Mensagem")
        
        col1, col2 = st.columns(2)
        
        with col1:
            message_type = st.selectbox("Tipo:", ["general", "urgent", "system", "data"])
            priority = st.slider("Prioridade:", 1, 10, 5)
        
        message = st.text_area("Mensagem:", value="Olá da rede AEONCOSMA P2P!")
        
        if st.button("📡 Transmitir"):
            if api_online and message:
                try:
                    payload = {
                        "message": message,
                        "message_type": message_type,
                        "priority": priority
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/p2p/broadcast", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Mensagem transmitida!")
                        st.json(result)
                    else:
                        st.error("❌ Erro na transmissão")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
            else:
                st.error("❌ Mensagem vazia ou API indisponível")
    
    with tab2:
        st.subheader("👥 Peers Conectados")
        
        if st.button("🔄 Atualizar Peers"):
            if api_online:
                try:
                    response = requests.get(f"{API_BASE_URL}/p2p/peers")
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Status atualizado!")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Peers Online", result.get("connected_peers", 0))
                        
                        with col2:
                            st.metric("Mensagens Enviadas", result.get("messages_sent", 0))
                        
                        with col3:
                            st.metric("Mensagens Recebidas", result.get("messages_received", 0))
                        
                        st.json(result)
                    else:
                        st.error("❌ Erro ao obter peers")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
        
        st.subheader("➕ Conectar Novo Peer")
        col1, col2 = st.columns(2)
        
        with col1:
            peer_id = st.text_input("ID do Peer:")
        
        with col2:
            peer_address = st.text_input("Endereço:")
        
        if st.button("🔗 Conectar"):
            if api_online and peer_id and peer_address:
                try:
                    payload = {
                        "peer_id": peer_id,
                        "address": peer_address
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/p2p/connect", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Peer conectado!")
                        st.json(result)
                    else:
                        st.error("❌ Erro na conexão")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
    
    with tab3:
        st.subheader("💬 Mensagens Recebidas")
        
        if st.button("📬 Atualizar Mensagens"):
            if api_online:
                try:
                    response = requests.get(f"{API_BASE_URL}/p2p/messages")
                    
                    if response.status_code == 200:
                        result = response.json()
                        messages = result.get("received_messages", [])
                        
                        if messages:
                            st.success(f"✅ {len(messages)} mensagens encontradas")
                            
                            for i, msg in enumerate(messages):
                                with st.expander(f"Mensagem {i+1} - {msg.get('sender', 'Unknown')}"):
                                    st.write(f"**Conteúdo:** {msg.get('content', '')}")
                                    st.write(f"**Tipo:** {msg.get('message_type', '')}")
                                    st.write(f"**Timestamp:** {msg.get('timestamp', '')}")
                        else:
                            st.info("📭 Nenhuma mensagem recebida")
                    else:
                        st.error("❌ Erro ao obter mensagens")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")

# ============================================================================
# 📡 COMUNICAÇÃO QUÂNTICA
# ============================================================================

elif selected_module == "📡 Comunicação Quântica":
    st.header("📡 Módulo de Comunicação Quântica")
    
    tab1, tab2, tab3 = st.tabs(["📤 Enviar", "📥 Receber", "🔑 Chaves Quânticas"])
    
    with tab1:
        st.subheader("📤 Enviar Mensagem Quântica")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sender = st.text_input("Remetente:", value="Alice")
            receiver = st.text_input("Destinatário:", value="Bob")
        
        with col2:
            protocol = st.selectbox("Protocolo:", ["BB84", "SARG04", "B92"])
        
        quantum_message = st.text_area("Mensagem:", value="Mensagem secreta via quantum!")
        
        if st.button("📤 Enviar Quantum"):
            if api_online and quantum_message:
                try:
                    payload = {
                        "message": quantum_message,
                        "sender": sender,
                        "receiver": receiver,
                        "protocol": protocol
                    }
                    
                    with st.spinner("Transmitindo via canal quântico..."):
                        response = requests.post(f"{API_BASE_URL}/quantum/send", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Mensagem quântica enviada!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("ID da Mensagem", result.get("message_id", ""))
                        with col2:
                            st.metric("Qubits Enviados", result.get("qubits_sent", 0))
                        
                        st.session_state.quantum_message_id = result.get("message_id", "")
                        st.json(result)
                    else:
                        st.error("❌ Erro no envio quântico")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
    
    with tab2:
        st.subheader("📥 Receber Mensagem Quântica")
        
        message_id = st.text_input("ID da Mensagem:", 
                                 value=st.session_state.get("quantum_message_id", ""))
        
        if st.button("📥 Receber Quantum"):
            if api_online and message_id:
                try:
                    with st.spinner("Decodificando mensagem quântica..."):
                        response = requests.get(f"{API_BASE_URL}/quantum/receive/{message_id}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result.get("status") == "quantum_message_received":
                            st.success("✅ Mensagem quântica recebida!")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Remetente", result.get("sender", ""))
                            with col2:
                                st.metric("Qubits Medidos", result.get("qubits_measured", 0))
                            
                            st.text_area("Mensagem Decodificada:", 
                                       value=result.get("decoded_message", ""))
                            
                            st.json(result)
                        else:
                            st.error("❌ Mensagem não encontrada")
                    else:
                        st.error("❌ Erro na recepção")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
    
    with tab3:
        st.subheader("🔑 Distribuição de Chaves Quânticas")
        
        key_length = st.slider("Comprimento da Chave (bits):", 128, 512, 256)
        
        if st.button("🔑 Gerar Chave Quântica"):
            if api_online:
                try:
                    payload = {"length": key_length}
                    
                    with st.spinner("Gerando chave quântica..."):
                        response = requests.post(f"{API_BASE_URL}/quantum/key", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Chave quântica gerada!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Comprimento", f"{result.get('key_length', 0)} bits")
                        with col2:
                            st.metric("Fidelidade", f"{result.get('entanglement_fidelity', 0):.2%}")
                        
                        st.text_area("Chave Quântica:", 
                                   value=result.get("key", ""),
                                   height=100)
                        
                        st.json(result)
                    else:
                        st.error("❌ Erro na geração de chave")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
        
        if st.button("📊 Status do Canal"):
            if api_online:
                try:
                    response = requests.get(f"{API_BASE_URL}/quantum/status")
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Canal", "Aberto" if result.get("is_open") else "Fechado")
                        
                        with col2:
                            st.metric("Ruído", f"{result.get('noise_level', 0):.1%}")
                        
                        with col3:
                            st.metric("Fidelidade", f"{result.get('entanglement_fidelity', 0):.1%}")
                        
                        st.json(result)
                    else:
                        st.error("❌ Erro ao obter status")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")

# ============================================================================
# 🌌 ANÁLISE COSMOLÓGICA
# ============================================================================

elif selected_module == "🌌 Análise Cosmológica":
    st.header("🌌 Módulo de Análise Cosmológica")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 Ajuste de Modelo", "📊 MCMC", "📈 Dados", "⚠️ Tensão H0"])
    
    with tab1:
        st.subheader("🔧 Ajuste do Modelo ΛCDM")
        
        col1, col2 = st.columns(2)
        
        with col1:
            model = st.selectbox("Modelo Cosmológico:", ["ΛCDM"])
            data_type = st.selectbox("Tipo de Dados:", ["supernovas", "bao", "cmb"])
        
        if st.button("🚀 Executar Ajuste"):
            if api_online:
                try:
                    payload = {
                        "model": model,
                        "data_type": data_type
                    }
                    
                    with st.spinner("Ajustando modelo cosmológico..."):
                        response = requests.post(f"{API_BASE_URL}/cosmos/fit", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Ajuste concluído!")
                        
                        # Mostrar parâmetros ajustados
                        params = result.get("best_fit_parameters", {})
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            h0 = params.get("H0", {})
                            st.metric("H₀", f"{h0.get('value', 0):.1f} ± {h0.get('error', 0):.1f}", 
                                    "km/s/Mpc")
                        
                        with col2:
                            om = params.get("Omega_m", {})
                            st.metric("Ωₘ", f"{om.get('value', 0):.3f} ± {om.get('error', 0):.3f}")
                        
                        with col3:
                            ol = params.get("Omega_L", {})
                            st.metric("ΩΛ", f"{ol.get('value', 0):.3f} ± {ol.get('error', 0):.3f}")
                        
                        # Qualidade do ajuste
                        goodness = result.get("goodness_of_fit", {})
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("χ²", f"{goodness.get('chi2', 0):.1f}")
                        with col2:
                            st.metric("χ² reduzido", f"{goodness.get('reduced_chi2', 0):.2f}")
                        
                        st.json(result)
                    else:
                        st.error("❌ Erro no ajuste")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
    
    with tab2:
        st.subheader("📊 Análise MCMC")
        
        steps = st.slider("Número de Passos:", 500, 5000, 1000)
        
        if st.button("🔗 Executar MCMC"):
            if api_online:
                try:
                    payload = {
                        "steps": steps,
                        "model": "ΛCDM"
                    }
                    
                    with st.spinner("Executando cadeia MCMC..."):
                        response = requests.post(f"{API_BASE_URL}/cosmos/mcmc", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ MCMC concluído!")
                        
                        # Taxa de aceitação
                        acceptance = result.get("acceptance_rate", 0)
                        st.metric("Taxa de Aceitação", f"{acceptance:.2%}")
                        
                        # Estatísticas posteriores
                        posterior = result.get("posterior_statistics", {})
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("H₀ (km/s/Mpc)")
                            h0_stats = posterior.get("H0", {})
                            st.write(f"**Média:** {h0_stats.get('mean', 0):.1f}")
                            st.write(f"**Desvio:** {h0_stats.get('std', 0):.1f}")
                            st.write(f"**Mediana:** {h0_stats.get('median', 0):.1f}")
                        
                        with col2:
                            st.subheader("Ωₘ")
                            om_stats = posterior.get("Omega_m", {})
                            st.write(f"**Média:** {om_stats.get('mean', 0):.3f}")
                            st.write(f"**Desvio:** {om_stats.get('std', 0):.3f}")
                            st.write(f"**Mediana:** {om_stats.get('median', 0):.3f}")
                        
                        # Plotar cadeia (se houver dados)
                        chain_data = result.get("chain_samples", {})
                        if chain_data:
                            h0_chain = chain_data.get("H0", [])
                            om_chain = chain_data.get("Omega_m", [])
                            
                            if h0_chain and om_chain:
                                fig = go.Figure()
                                
                                # Scatter plot dos parâmetros
                                fig.add_trace(go.Scatter(
                                    x=om_chain,
                                    y=h0_chain,
                                    mode='markers',
                                    name='MCMC Samples',
                                    marker=dict(size=3, alpha=0.6)
                                ))
                                
                                fig.update_layout(
                                    title="Distribuição Posterior (Últimas 100 amostras)",
                                    xaxis_title="Ωₘ",
                                    yaxis_title="H₀ (km/s/Mpc)"
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                        
                        st.json(result)
                    else:
                        st.error("❌ Erro no MCMC")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
    
    with tab3:
        st.subheader("📈 Dados Cosmológicos")
        
        if st.button("📊 Carregar Dados"):
            if api_online:
                try:
                    response = requests.get(f"{API_BASE_URL}/cosmos/data")
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Supernovas Pantheon+", result.get("pantheon_supernovas", 0))
                        
                        with col2:
                            st.metric("Medições BAO", result.get("bao_measurements", 0))
                        
                        with col3:
                            st.metric("Parâmetros Planck", result.get("planck_parameters", 0))
                        
                        # Amostra de supernova
                        sample_sn = result.get("sample_supernova")
                        if sample_sn:
                            st.subheader("📍 Amostra de Supernova")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Nome:** {sample_sn.get('name')}")
                                st.write(f"**Redshift:** {sample_sn.get('redshift'):.4f}")
                            
                            with col2:
                                st.write(f"**Módulo de Distância:** {sample_sn.get('distance_modulus'):.2f}")
                                st.write(f"**Erro:** {sample_sn.get('error'):.2f}")
                        
                        # Amostra BAO
                        sample_bao = result.get("sample_bao")
                        if sample_bao:
                            st.subheader("🌊 Amostra BAO")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Survey:** {sample_bao.get('survey')}")
                                st.write(f"**Redshift:** {sample_bao.get('redshift')}")
                            
                            with col2:
                                st.write(f"**DM/rs:** {sample_bao.get('DM_rs'):.2f}")
                                st.write(f"**Erro:** {sample_bao.get('error'):.2f}")
                        
                    else:
                        st.error("❌ Erro ao carregar dados")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
        
        if st.button("🌟 Parâmetros do Planck"):
            if api_online:
                try:
                    response = requests.get(f"{API_BASE_URL}/cosmos/planck")
                    
                    if response.status_code == 200:
                        result = response.json()
                        planck_params = result.get("planck_parameters", {})
                        
                        st.subheader("🛰️ Parâmetros Cosmológicos - Planck 2020")
                        
                        for param_name, param_data in planck_params.items():
                            col1, col2, col3 = st.columns([2, 1, 3])
                            
                            with col1:
                                st.write(f"**{param_data.get('name')}**")
                            
                            with col2:
                                value = param_data.get('value', 0)
                                error = param_data.get('error', 0)
                                unit = param_data.get('unit', '')
                                st.write(f"{value:.3f} ± {error:.3f} {unit}")
                            
                            with col3:
                                st.write(param_data.get('description', ''))
                        
                    else:
                        st.error("❌ Erro ao carregar parâmetros do Planck")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
    
    with tab4:
        st.subheader("⚠️ Tensão da Constante de Hubble")
        
        if st.button("🔍 Analisar Tensão H₀"):
            if api_online:
                try:
                    response = requests.get(f"{API_BASE_URL}/cosmos/tension")
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.write("### 📊 Medições Locais vs. Universo Primordial")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🌟 Medições Locais")
                            local = result.get("local_measurements", {})
                            
                            for survey, data in local.items():
                                st.write(f"**{survey.replace('_', ' ')}:**")
                                st.write(f"H₀ = {data.get('value', 0):.1f} ± {data.get('error', 0):.1f} km/s/Mpc")
                                st.write(f"Método: {data.get('method', '')}")
                                st.write("---")
                        
                        with col2:
                            st.subheader("🌌 Universo Primordial")
                            early = result.get("early_universe", {})
                            
                            for survey, data in early.items():
                                st.write(f"**{survey.replace('_', ' ')}:**")
                                st.write(f"H₀ = {data.get('value', 0):.1f} ± {data.get('error', 0):.1f} km/s/Mpc")
                                st.write(f"Método: {data.get('method', '')}")
                                st.write("---")
                        
                        # Gráfico da tensão
                        local_values = [data.get('value', 0) for data in local.values()]
                        early_values = [data.get('value', 0) for data in early.values()]
                        
                        fig = go.Figure()
                        
                        fig.add_trace(go.Bar(
                            name='Medições Locais',
                            x=list(local.keys()),
                            y=local_values,
                            marker_color='lightcoral'
                        ))
                        
                        fig.add_trace(go.Bar(
                            name='Universo Primordial',
                            x=list(early.keys()),
                            y=early_values,
                            marker_color='lightblue'
                        ))
                        
                        fig.update_layout(
                            title="Tensão H₀: Local vs. Primordial",
                            yaxis_title="H₀ (km/s/Mpc)",
                            barmode='group'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Explicações possíveis
                        st.subheader("🤔 Possíveis Explicações")
                        explanations = result.get("possible_explanations", [])
                        
                        for i, explanation in enumerate(explanations, 1):
                            st.write(f"{i}. {explanation}")
                        
                        st.warning(f"⚠️ **Significância da Tensão:** {result.get('tension_significance', 'N/A')}")
                        
                    else:
                        st.error("❌ Erro ao analisar tensão")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")

# ============================================================================
# 🔄 AUTO-REFRESH
# ============================================================================

# Adicionar auto-refresh para o dashboard
if selected_module == "🏠 Dashboard":
    if st.sidebar.checkbox("🔄 Auto-refresh (5s)"):
        time.sleep(5)
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>AEONCOSMA Engine v1.0.0</strong> - Plataforma Modular Avançada</p>
    <p>Desenvolvido por <strong>Luiz H. P. Cruz</strong> | Copyright 2025</p>
    <p>🧠 IA • 🔐 Crypto • 🌐 P2P • 📡 Quantum • 🌌 Cosmos</p>
</div>
""", unsafe_allow_html=True)
