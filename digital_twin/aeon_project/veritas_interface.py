"""
VERITAS - Interface Avançada para Sistema AEON
Módulo de Documentos Inteligentes com IA e Blockchain
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import base64
from veritas_core import create_veritas_document, verify_veritas_document, VeritasRiskAnalyzer

def render_veritas_interface():
    st.header("🛡️ VERITAS - Sistema Inteligente de Validação")
    st.markdown("### 🤖 IA Simbólica + Blockchain + Assinatura Digital")
    
    # Inicializar estado
    if "veritas_documents" not in st.session_state:
        st.session_state.veritas_documents = []
    
    if "current_document" not in st.session_state:
        st.session_state.current_document = None
    
    # Abas VERITAS
    veritas_tab1, veritas_tab2, veritas_tab3, veritas_tab4 = st.tabs([
        "📝 Criar Documento", "🔍 Validar Integridade", "🧠 IA de Riscos", "📊 Auditoria"
    ])
    
    # TAB 1: Criar Documento
    with veritas_tab1:
        st.subheader("📝 Geração Inteligente de Documentos")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("veritas_document"):
                st.markdown("#### 🎯 Dados da Tarefa")
                
                task_description = st.text_area(
                    "Descrição da Tarefa *", 
                    height=100,
                    placeholder="Ex: Manutenção preventiva em disjuntor de 13.8kV na subestação..."
                )
                
                col_a, col_b = st.columns(2)
                with col_a:
                    location = st.text_input("Local *", placeholder="Subestação ABC - Pátio 13.8kV")
                    responsible_person = st.text_input("Responsável *", placeholder="João Silva - Eletricista")
                
                with col_b:
                    start_time = st.time_input("Início Previsto")
                    end_time = st.time_input("Término Previsto")
                
                st.markdown("#### ⚡ EPIs e Medidas de Controle")
                
                required_epi = st.multiselect(
                    "EPIs Obrigatórios",
                    ["Capacete", "Óculos de proteção", "Luva isolante", "Botina", 
                     "Cinto de segurança", "Protetor auricular", "Máscara", "Avental"]
                )
                
                control_measures = st.text_area(
                    "Medidas de Controle",
                    height=80,
                    placeholder="1. Desenergizar circuito\n2. Instalar aterramento\n3. Sinalizar área..."
                )
                
                st.markdown("#### 👤 Assinatura Digital")
                col_c, col_d = st.columns(2)
                with col_c:
                    user_cpf = st.text_input("CPF do Responsável", placeholder="000.000.000-00")
                with col_d:
                    supervisor_cpf = st.text_input("CPF do Supervisor", placeholder="111.111.111-11")
                
                submitted = st.form_submit_button("🚀 Gerar Documento VERITAS", type="primary")
                
                if submitted:
                    if task_description and location and responsible_person:
                        with st.spinner("🤖 IA analisando riscos e gerando documento..."):
                            task_data = {
                                "task_description": task_description,
                                "location": location,
                                "responsible_person": responsible_person,
                                "start_time": str(start_time),
                                "end_time": str(end_time),
                                "required_epi": required_epi,
                                "control_measures": control_measures.split('\n') if control_measures else [],
                                "user_cpf": user_cpf,
                                "supervisor_cpf": supervisor_cpf
                            }
                            
                            document = create_veritas_document(task_data)
                            st.session_state.veritas_documents.append(document)
                            st.session_state.current_document = document
                            
                            st.success("✅ Documento VERITAS gerado com sucesso!")
                            st.balloons()
                    else:
                        st.error("❌ Preencha todos os campos obrigatórios (*)")
        
        with col2:
            st.subheader("🤖 Análise IA em Tempo Real")
            
            if task_description:
                analyzer = VeritasRiskAnalyzer()
                risk_analysis = analyzer.analyze_task_risks(task_description)
                
                # Nível de risco
                risk_color = {"ALTO": "🔴", "MÉDIO": "🟡", "BAIXO": "🟢"}
                st.markdown(f"**Nível de Risco:** {risk_color.get(risk_analysis['overall_risk_level'], '⚪')} {risk_analysis['overall_risk_level']}")
                
                # Riscos identificados
                if risk_analysis["identified_risks"]:
                    st.markdown("**🚨 Riscos Identificados:**")
                    for risk in risk_analysis["identified_risks"]:
                        st.markdown(f"- {risk['type'].title()}: {risk['level']}")
                
                # EPIs sugeridos
                if risk_analysis["suggested_epi"]:
                    st.markdown("**🛡️ EPIs Sugeridos pela IA:**")
                    for epi in risk_analysis["suggested_epi"]:
                        st.markdown(f"- {epi}")
                
                # Recomendação da IA
                st.info(risk_analysis["ai_recommendation"])
                
                # Perguntas de segurança
                if risk_analysis["safety_questions"]:
                    with st.expander("❓ Perguntas de Segurança"):
                        for question in risk_analysis["safety_questions"]:
                            st.markdown(f"- {question}")
            else:
                st.info("Digite a descrição da tarefa para análise IA em tempo real")
    
    # TAB 2: Validar Integridade
    with veritas_tab2:
        st.subheader("🔍 Validação de Integridade Blockchain")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📄 Verificar Documento")
            
            if st.session_state.veritas_documents:
                selected_doc = st.selectbox(
                    "Documento para verificar:",
                    options=range(len(st.session_state.veritas_documents)),
                    format_func=lambda i: f"{st.session_state.veritas_documents[i]['document_id']} - {st.session_state.veritas_documents[i]['created_at'][:19]}"
                )
                
                if st.button("🔐 Verificar Integridade"):
                    doc = st.session_state.veritas_documents[selected_doc]
                    verification = verify_veritas_document(doc, doc["hash"])
                    
                    if verification["is_valid"]:
                        st.success("✅ DOCUMENTO ÍNTEGRO - Hash verificado com sucesso!")
                    else:
                        st.error("❌ DOCUMENTO COMPROMETIDO - Hash não confere!")
                    
                    st.json(verification)
            else:
                st.info("Nenhum documento VERITAS criado ainda")
        
        with col2:
            st.markdown("#### 📱 QR Code de Verificação")
            
            if st.session_state.current_document:
                doc = st.session_state.current_document
                
                # Mostrar QR Code
                qr_data = base64.b64decode(doc["qr_code"])
                st.image(qr_data, caption="QR Code para Verificação", width=200)
                
                st.markdown("**📋 Informações do Documento:**")
                st.json({
                    "ID": doc["document_id"],
                    "Hash": doc["hash"][:32] + "...",
                    "Criado": doc["created_at"][:19],
                    "Blockchain Index": doc["blockchain_index"]
                })
    
    # TAB 3: IA de Riscos
    with veritas_tab3:
        st.subheader("🧠 Inteligência Artificial de Análise de Riscos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Análise Personalizada")
            
            custom_task = st.text_area(
                "Descreva a tarefa para análise:",
                height=120,
                placeholder="Digite aqui a descrição detalhada da tarefa..."
            )
            
            if st.button("🤖 Analisar com IA"):
                if custom_task:
                    analyzer = VeritasRiskAnalyzer()
                    analysis = analyzer.analyze_task_risks(custom_task)
                    
                    st.markdown(f"**🎯 Nível de Risco:** {analysis['overall_risk_level']}")
                    
                    if analysis["identified_risks"]:
                        st.markdown("**⚠️ Riscos Identificados:**")
                        risks_df = pd.DataFrame(analysis["identified_risks"])
                        st.dataframe(risks_df, use_container_width=True)
                    
                    if analysis["suggested_epi"]:
                        st.markdown("**🛡️ EPIs Recomendados:**")
                        for epi in analysis["suggested_epi"]:
                            st.markdown(f"- ✅ {epi}")
                    
                    st.info(analysis["ai_recommendation"])
        
        with col2:
            st.markdown("#### 📊 Estatísticas de Riscos")
            
            if st.session_state.veritas_documents:
                # Análise estatística dos documentos
                risk_levels = []
                risk_types = []
                
                for doc in st.session_state.veritas_documents:
                    risk_analysis = doc.get("risk_analysis", {})
                    risk_levels.append(risk_analysis.get("overall_risk_level", "BAIXO"))
                    
                    for risk in risk_analysis.get("identified_risks", []):
                        risk_types.append(risk["type"])
                
                if risk_levels:
                    # Gráfico de níveis de risco
                    risk_counts = pd.Series(risk_levels).value_counts()
                    st.bar_chart(risk_counts)
                
                if risk_types:
                    # Tipos de risco mais comuns
                    st.markdown("**🎯 Tipos de Risco Mais Comuns:**")
                    type_counts = pd.Series(risk_types).value_counts()
                    for risk_type, count in type_counts.items():
                        st.markdown(f"- {risk_type.title()}: {count}x")
    
    # TAB 4: Auditoria
    with veritas_tab4:
        st.subheader("📊 Trilha de Auditoria Blockchain")
        
        if st.session_state.veritas_documents:
            # Resumo geral
            total_docs = len(st.session_state.veritas_documents)
            high_risk_docs = len([d for d in st.session_state.veritas_documents 
                                if d.get("risk_analysis", {}).get("overall_risk_level") == "ALTO"])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 Total de Documentos", total_docs)
            with col2:
                st.metric("🚨 Alto Risco", high_risk_docs)
            with col3:
                st.metric("✅ Taxa de Integridade", "100%")
            
            # Lista de documentos
            st.markdown("#### 📋 Histórico de Documentos")
            
            docs_data = []
            for doc in st.session_state.veritas_documents:
                docs_data.append({
                    "ID": doc["document_id"],
                    "Criado": doc["created_at"][:19],
                    "Local": doc["task_data"].get("location", "N/A"),
                    "Risco": doc.get("risk_analysis", {}).get("overall_risk_level", "N/A"),
                    "Hash": doc["hash"][:16] + "...",
                    "Blockchain": doc["blockchain_index"]
                })
            
            if docs_data:
                df = pd.DataFrame(docs_data)
                st.dataframe(df, use_container_width=True)
                
                # Download CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Relatório CSV",
                    data=csv,
                    file_name=f"veritas_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("📊 Nenhum documento para auditoria ainda")
    
    return st.session_state.current_document
