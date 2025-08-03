"""
AEONCOSMA AI Analytics Integration
=================================
Integração OpenAI para análise inteligente de dados e geração automática de insights
"""

import sqlite3
import openai
import streamlit as st
import pandas as pd
import numpy as np
import json
import random
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns

class AEONCOSMAAIAnalytics:
    """Sistema de análise inteligente com OpenAI para AEONCOSMA"""
    
    def __init__(self, api_key: str = None):
        """
        Inicializa o sistema de IA
        
        Args:
            api_key: Chave da API OpenAI (será solicitada via interface se não fornecida)
        """
        self.api_key = api_key
        self.database_path = "aeoncosma_data.db"
        self.setup_database()
        
        if api_key:
            openai.api_key = api_key
    
    def setup_database(self):
        """Cria e popula banco de dados de exemplo do AEONCOSMA"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Tabela de nós da rede
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS network_nodes (
            id INTEGER PRIMARY KEY,
            node_id TEXT UNIQUE,
            node_type TEXT,
            cpu_usage REAL,
            memory_usage REAL,
            network_latency REAL,
            energy_consumption REAL,
            uptime_hours REAL,
            consensus_score REAL,
            security_level INTEGER,
            location_x REAL,
            location_y REAL,
            location_z REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabela de métricas de performance
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY,
            metric_name TEXT,
            metric_value REAL,
            node_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(node_id) REFERENCES network_nodes(node_id)
        )
        """)
        
        # Tabela de transações
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            transaction_id TEXT UNIQUE,
            from_node TEXT,
            to_node TEXT,
            amount REAL,
            transaction_type TEXT,
            processing_time REAL,
            gas_fee REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(from_node) REFERENCES network_nodes(node_id),
            FOREIGN KEY(to_node) REFERENCES network_nodes(node_id)
        )
        """)
        
        # Tabela de eventos de segurança
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY,
            event_type TEXT,
            severity_level INTEGER,
            node_id TEXT,
            description TEXT,
            resolved BOOLEAN DEFAULT FALSE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(node_id) REFERENCES network_nodes(node_id)
        )
        """)
        
        # Inserir dados de exemplo se não existirem
        cursor.execute("SELECT COUNT(*) FROM network_nodes")
        if cursor.fetchone()[0] == 0:
            self.populate_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def populate_sample_data(self, cursor):
        """Popula o banco com dados de exemplo"""
        import random
        from datetime import datetime, timedelta
        
        # Tipos de nós AEONCOSMA
        node_types = ['master', 'validator', 'ai', 'crypto', 'energy', 'quantum', 'cosmos', 
                     'storage', 'compute', 'gateway', 'oracle', 'relay', 'monitor']
        
        # Inserir nós da rede
        for i in range(100):
            node_type = random.choice(node_types)
            cursor.execute("""
            INSERT INTO network_nodes 
            (node_id, node_type, cpu_usage, memory_usage, network_latency, 
             energy_consumption, uptime_hours, consensus_score, security_level,
             location_x, location_y, location_z)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"{node_type}_{i:03d}",
                node_type,
                random.uniform(20, 90),
                random.uniform(30, 85),
                np.random.exponential(10),
                random.uniform(50, 500),
                random.uniform(100, 8760),
                random.uniform(70, 100),
                random.randint(1, 10),
                random.uniform(-20, 20),
                random.uniform(-20, 20),
                random.uniform(-20, 20)
            ))
        
        # Inserir métricas de performance
        metrics = ['throughput', 'latency', 'error_rate', 'bandwidth_usage', 'connection_count']
        for i in range(500):
            cursor.execute("""
            INSERT INTO performance_metrics (metric_name, metric_value, node_id)
            VALUES (?, ?, ?)
            """, (
                random.choice(metrics),
                random.uniform(0, 100),
                f"{random.choice(node_types)}_{random.randint(0, 99):03d}"
            ))
        
        # Inserir transações
        transaction_types = ['transfer', 'smart_contract', 'consensus', 'validation', 'mining']
        for i in range(200):
            from_node = f"{random.choice(node_types)}_{random.randint(0, 99):03d}"
            to_node = f"{random.choice(node_types)}_{random.randint(0, 99):03d}"
            cursor.execute("""
            INSERT INTO transactions 
            (transaction_id, from_node, to_node, amount, transaction_type, processing_time, gas_fee)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"tx_{i:06d}",
                from_node,
                to_node,
                random.uniform(0.1, 1000),
                random.choice(transaction_types),
                random.uniform(0.1, 5.0),
                random.uniform(0.001, 0.1)
            ))
        
        # Inserir eventos de segurança
        event_types = ['intrusion_attempt', 'ddos_attack', 'malware_detected', 'unauthorized_access', 'anomaly_detected']
        for i in range(50):
            cursor.execute("""
            INSERT INTO security_events (event_type, severity_level, node_id, description, resolved)
            VALUES (?, ?, ?, ?, ?)
            """, (
                random.choice(event_types),
                random.randint(1, 5),
                f"{random.choice(node_types)}_{random.randint(0, 99):03d}",
                f"Security event {i} detected on network",
                random.choice([True, False])
            ))
    
    def query_database_with_ai(self, pergunta: str, api_key: str = None) -> Dict[str, Any]:
        """
        Usa OpenAI para gerar SQL e executar consultas no banco AEONCOSMA
        
        Args:
            pergunta: Pergunta em linguagem natural
            api_key: Chave da API OpenAI
            
        Returns:
            Dict com SQL gerado, resultado e visualização
        """
        if api_key:
            openai.api_key = api_key
        
        # Conecta ao banco
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Obter schema do banco para ajudar o GPT
        schema_info = self.get_database_schema()
        
        # Prompt melhorado para o GPT
        prompt = f"""
        Você é um especialista em SQL para o sistema AEONCOSMA (rede blockchain distribuída).
        
        SCHEMA DO BANCO:
        {schema_info}
        
        PERGUNTA DO USUÁRIO: "{pergunta}"
        
        Gere APENAS a query SQL correta para SQLite. Não inclua explicações, apenas o SQL puro.
        
        REGRAS:
        - Use apenas as tabelas e colunas que existem no schema
        - Para consultas de performance, use a tabela performance_metrics
        - Para análise de nós, use network_nodes
        - Para transações, use transactions
        - Para segurança, use security_events
        - Limite resultados a 100 registros com LIMIT quando apropriado
        - Use agregações (COUNT, AVG, SUM) quando fizer sentido
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.1
            )
            
            sql_query = response["choices"][0]["message"]["content"].strip()
            
            # Limpar o SQL (remover markdown se houver)
            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
            print(f"\n🔍 SQL Gerado:\n{sql_query}\n")
            
            # Executar query
            cursor.execute(sql_query)
            resultado = cursor.fetchall()
            
            # Obter nomes das colunas
            column_names = [description[0] for description in cursor.description]
            
            conn.close()
            
            return {
                'success': True,
                'sql_query': sql_query,
                'resultado': resultado,
                'columns': column_names,
                'count': len(resultado)
            }
            
        except Exception as e:
            conn.close()
            return {
                'success': False,
                'error': str(e),
                'sql_query': sql_query if 'sql_query' in locals() else 'N/A'
            }
    
    def get_database_schema(self) -> str:
        """Retorna informações sobre o schema do banco"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        schema_info = ""
        
        # Obter informações das tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            schema_info += f"\nTabela: {table_name}\n"
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for col in columns:
                schema_info += f"  - {col[1]} ({col[2]})\n"
        
        conn.close()
        return schema_info
    
    def generate_ai_insights(self, data_summary: str, api_key: str = None) -> str:
        """
        Gera insights usando IA baseado nos dados
        
        Args:
            data_summary: Resumo dos dados para análise
            api_key: Chave da API OpenAI
            
        Returns:
            Insights gerados pela IA
        """
        if api_key:
            openai.api_key = api_key
        
        prompt = f"""
        Você é um especialista em análise de dados para sistemas blockchain distribuídos (AEONCOSMA).
        
        DADOS PARA ANÁLISE:
        {data_summary}
        
        Gere insights técnicos e estratégicos baseados nos dados. Inclua:
        1. Principais tendências identificadas
        2. Possíveis problemas ou anomalias
        3. Recomendações de otimização
        4. Métricas-chave para monitorar
        5. Riscos potenciais
        
        Seja específico e técnico, focando em blockchain, performance de rede e segurança.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3
            )
            
            return response["choices"][0]["message"]["content"]
            
        except Exception as e:
            return f"Erro ao gerar insights: {str(e)}"
    
    def create_visualization_from_data(self, resultado: List, columns: List[str], viz_type: str = "auto"):
        """
        Cria visualização apropriada baseada nos dados retornados
        
        Args:
            resultado: Dados da consulta
            columns: Nomes das colunas
            viz_type: Tipo de visualização ('auto', 'bar', 'line', 'pie', 'scatter')
            
        Returns:
            Figura matplotlib ou plotly
        """
        if not resultado:
            return None
        
        # Converter para DataFrame
        df = pd.DataFrame(resultado, columns=columns)
        
        # Determinar tipo de visualização automaticamente
        if viz_type == "auto":
            if len(columns) == 2:
                if df.dtypes[1] in ['int64', 'float64']:
                    viz_type = "bar"
                else:
                    viz_type = "pie"
            elif len(columns) > 2:
                viz_type = "scatter"
            else:
                viz_type = "bar"
        
        # Criar visualização
        fig = plt.figure(figsize=(10, 6))
        
        if viz_type == "bar":
            if len(columns) >= 2:
                plt.bar(df.iloc[:, 0].astype(str), df.iloc[:, 1])
                plt.title(f'{columns[1]} por {columns[0]}')
                plt.xlabel(columns[0])
                plt.ylabel(columns[1])
                plt.xticks(rotation=45)
        
        elif viz_type == "pie":
            if len(columns) >= 2:
                plt.pie(df.iloc[:, 1], labels=df.iloc[:, 0], autopct='%1.1f%%')
                plt.title(f'Distribuição: {columns[1]} por {columns[0]}')
        
        elif viz_type == "line":
            if len(columns) >= 2:
                plt.plot(df.iloc[:, 0], df.iloc[:, 1], marker='o')
                plt.title(f'{columns[1]} ao longo de {columns[0]}')
                plt.xlabel(columns[0])
                plt.ylabel(columns[1])
        
        elif viz_type == "scatter":
            if len(columns) >= 2:
                plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
                plt.title(f'{columns[1]} vs {columns[0]}')
                plt.xlabel(columns[0])
                plt.ylabel(columns[1])
        
        plt.tight_layout()
        return fig
    
    def get_sample_questions(self) -> List[str]:
        """Retorna perguntas de exemplo para demonstração"""
        return [
            "Quais são os 10 nós com maior uso de CPU?",
            "Qual é a média de latência por tipo de nó?",
            "Quantas transações foram processadas por tipo?",
            "Quais nós têm o maior score de consenso?",
            "Quantos eventos de segurança não foram resolvidos?",
            "Qual é o consumo médio de energia por tipo de nó?",
            "Quais são as 5 transações mais caras em gas fee?",
            "Quantos nós de cada tipo existem na rede?",
            "Qual é o tempo médio de processamento por tipo de transação?",
            "Quais nós têm uptime acima de 1000 horas?"
        ]

def create_streamlit_interface():
    """Interface Streamlit para o sistema de IA"""
    st.set_page_config(
        page_title="AEONCOSMA AI Analytics",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AEONCOSMA AI Analytics")
    st.markdown("### Análise Inteligente de Dados com OpenAI")
    
    # Sidebar para configuração
    st.sidebar.title("⚙️ Configuração")
    
    # Campo para API key
    api_key = st.sidebar.text_input("OpenAI API Key", type="password", 
                                   help="Insira sua chave da API OpenAI")
    
    if not api_key:
        st.warning("⚠️ Por favor, insira sua chave da API OpenAI na barra lateral para continuar.")
        st.info("""
        **Como obter uma chave da API OpenAI:**
        1. Visite https://platform.openai.com/api-keys
        2. Faça login em sua conta OpenAI
        3. Clique em "Create new secret key"
        4. Copie a chave e cole no campo ao lado
        """)
        return
    
    # Inicializar sistema de IA
    ai_system = AEONCOSMAAIAnalytics(api_key)
    
    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Consulta IA", "📊 Visualizações", "💡 Insights", "📋 Dados"])
    
    with tab1:
        st.header("Consulta Inteligente ao Banco de Dados")
        
        # Perguntas de exemplo
        st.subheader("📝 Perguntas de Exemplo")
        sample_questions = ai_system.get_sample_questions()
        
        col1, col2 = st.columns(2)
        with col1:
            for i, question in enumerate(sample_questions[:5]):
                if st.button(f"📌 {question}", key=f"q1_{i}"):
                    st.session_state.selected_question = question
        
        with col2:
            for i, question in enumerate(sample_questions[5:]):
                if st.button(f"📌 {question}", key=f"q2_{i}"):
                    st.session_state.selected_question = question
        
        # Campo de input
        pergunta = st.text_input(
            "🤔 Faça sua pergunta:",
            value=st.session_state.get('selected_question', ''),
            placeholder="Ex: Quais são os nós com maior consumo de energia?"
        )
        
        if st.button("🔍 Analisar", type="primary"):
            if pergunta:
                with st.spinner("🤖 IA analisando sua pergunta..."):
                    resultado = ai_system.query_database_with_ai(pergunta, api_key)
                
                if resultado['success']:
                    st.success(f"✅ Consulta executada com sucesso! {resultado['count']} resultados encontrados.")
                    
                    # Mostrar SQL gerado
                    st.subheader("🔍 SQL Gerado pela IA")
                    st.code(resultado['sql_query'], language='sql')
                    
                    # Mostrar resultado
                    st.subheader("📊 Resultados")
                    if resultado['resultado']:
                        df = pd.DataFrame(resultado['resultado'], columns=resultado['columns'])
                        st.dataframe(df, use_container_width=True)
                        
                        # Criar visualização
                        fig = ai_system.create_visualization_from_data(
                            resultado['resultado'], 
                            resultado['columns']
                        )
                        if fig:
                            st.pyplot(fig)
                    else:
                        st.info("Nenhum resultado encontrado.")
                
                else:
                    st.error(f"❌ Erro na consulta: {resultado['error']}")
                    if 'sql_query' in resultado:
                        st.code(resultado['sql_query'], language='sql')
    
    with tab2:
        st.header("📊 Visualizações Automáticas")
        
        # Métricas gerais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Total de nós
            total_nodes = ai_system.query_database_with_ai("Quantos nós existem na rede?", api_key)
            if total_nodes['success'] and total_nodes['resultado']:
                st.metric("Total de Nós", total_nodes['resultado'][0][0])
        
        with col2:
            # Transações hoje
            total_tx = ai_system.query_database_with_ai("Quantas transações foram processadas?", api_key)
            if total_tx['success'] and total_tx['resultado']:
                st.metric("Total Transações", total_tx['resultado'][0][0])
        
        with col3:
            # Eventos de segurança
            security_events = ai_system.query_database_with_ai("Quantos eventos de segurança não resolvidos existem?", api_key)
            if security_events['success'] and security_events['resultado']:
                st.metric("Eventos Segurança", security_events['resultado'][0][0], delta=-2)
        
        with col4:
            # CPU médio
            avg_cpu = ai_system.query_database_with_ai("Qual é a média de uso de CPU de todos os nós?", api_key)
            if avg_cpu['success'] and avg_cpu['resultado']:
                st.metric("CPU Médio", f"{avg_cpu['resultado'][0][0]:.1f}%")
        
        # Dashboard de visualizações
        st.subheader("📈 Dashboard Automático")
        
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            # Distribuição por tipo de nó
            node_dist = ai_system.query_database_with_ai("Conte quantos nós existem por tipo", api_key)
            if node_dist['success'] and node_dist['resultado']:
                fig_pie = ai_system.create_visualization_from_data(
                    node_dist['resultado'], 
                    node_dist['columns'], 
                    'pie'
                )
                if fig_pie:
                    st.pyplot(fig_pie)
        
        with col_viz2:
            # Top 10 nós por CPU
            top_cpu = ai_system.query_database_with_ai("Quais são os 10 nós com maior uso de CPU?", api_key)
            if top_cpu['success'] and top_cpu['resultado']:
                fig_bar = ai_system.create_visualization_from_data(
                    top_cpu['resultado'], 
                    top_cpu['columns'], 
                    'bar'
                )
                if fig_bar:
                    st.pyplot(fig_bar)
    
    with tab3:
        st.header("💡 Insights Gerados pela IA")
        
        if st.button("🧠 Gerar Insights Automáticos", type="primary"):
            with st.spinner("🤖 IA analisando dados da rede..."):
                # Coletar dados de resumo
                summary_queries = [
                    "SELECT AVG(cpu_usage), AVG(memory_usage), AVG(network_latency) FROM network_nodes",
                    "SELECT node_type, COUNT(*), AVG(consensus_score) FROM network_nodes GROUP BY node_type",
                    "SELECT COUNT(*) as total_events, AVG(severity_level) FROM security_events WHERE resolved = 0"
                ]
                
                data_summary = "RESUMO DOS DADOS AEONCOSMA:\n\n"
                
                for query in summary_queries:
                    try:
                        conn = sqlite3.connect(ai_system.database_path)
                        cursor = conn.cursor()
                        cursor.execute(query)
                        result = cursor.fetchall()
                        data_summary += f"Query: {query}\nResultado: {result}\n\n"
                        conn.close()
                    except:
                        pass
                
                # Gerar insights
                insights = ai_system.generate_ai_insights(data_summary, api_key)
                
                st.markdown("### 🎯 Análise Inteligente da Rede AEONCOSMA")
                st.markdown(insights)
    
    with tab4:
        st.header("📋 Estrutura do Banco de Dados")
        
        schema_info = ai_system.get_database_schema()
        st.text(schema_info)
        
        st.subheader("🔍 Explorar Tabelas")
        
        # Seletor de tabela
        tables = ['network_nodes', 'performance_metrics', 'transactions', 'security_events']
        selected_table = st.selectbox("Selecione uma tabela:", tables)
        
        if st.button(f"📊 Mostrar dados de {selected_table}"):
            result = ai_system.query_database_with_ai(f"SELECT * FROM {selected_table} LIMIT 20", api_key)
            if result['success']:
                df = pd.DataFrame(result['resultado'], columns=result['columns'])
                st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    create_streamlit_interface()
