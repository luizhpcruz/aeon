"""
AEONCOSMA Advanced Visualization Suite
=====================================
Sistema híbrido de visualização usando múltiplas bibliotecas e ferramentas.

Integra:
- Matplotlib: Gráficos científicos estáticos
- Seaborn: Análise estatística
- Plotly: Interatividade 3D/web
- Bokeh: Streaming em tempo real
- NetworkX + Gephi export: Análise de redes
- D3.js integration: Visualizações customizadas
- OpenAI Integration: Análise inteligente de dados
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import bokeh.plotting as bk
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import curdoc
import networkx as nx
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import psutil
import random
import math

# Importar módulo de IA
try:
    from aeoncosma.ui.ai_analytics_integration import AEONCOSMAAIAnalytics
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

class AdvancedVisualizationSuite:
    """Suite completa de visualizações avançadas para AEONCOSMA"""
    
    def __init__(self):
        self.data_sources = {}
        self.network_graph = nx.Graph()
        self.time_series_data = []
        self.setup_styling()
        
        # Configurar IA Analytics se disponível
        if AI_AVAILABLE:
            try:
                self.ai_analytics = AEONCOSMAAIAnalytics()
                self.ai_enabled = True
            except Exception as e:
                st.warning(f"Módulo de IA não configurado: {e}")
                self.ai_enabled = False
        else:
            self.ai_enabled = False
        
    def setup_styling(self):
        """Configura estilos padrão para todas as visualizações"""
        # Matplotlib/Seaborn styling
        plt.style.use('dark_background')
        sns.set_theme(style="darkgrid", palette="husl")
        
        # Cores AEONCOSMA
        self.color_palette = {
            'primary': '#00ff88',
            'secondary': '#ff6b35', 
            'accent': '#4a90e2',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'dark': '#2c3e50',
            'light': '#ecf0f1'
        }
        
    def create_matplotlib_scientific_plots(self, data: Dict) -> List[plt.Figure]:
        """Cria gráficos científicos estáticos com Matplotlib"""
        figures = []
        
        # 1. Performance científica do sistema
        fig1, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig1.suptitle('AEONCOSMA - Análise Científica de Performance', 
                     fontsize=16, color=self.color_palette['primary'])
        
        # CPU Usage over time
        times = data.get('timestamps', list(range(100)))
        cpu_data = data.get('cpu_usage', [random.uniform(20, 80) for _ in times])
        
        axes[0, 0].plot(times, cpu_data, color=self.color_palette['accent'], linewidth=2)
        axes[0, 0].set_title('CPU Usage Evolution', color='white')
        axes[0, 0].set_ylabel('CPU %', color='white')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Memory distribution
        memory_types = ['Used', 'Available', 'Cached', 'Buffers']
        memory_values = [45, 30, 15, 10]
        colors = [self.color_palette['primary'], self.color_palette['secondary'], 
                 self.color_palette['accent'], self.color_palette['warning']]
        
        axes[0, 1].pie(memory_values, labels=memory_types, colors=colors, autopct='%1.1f%%')
        axes[0, 1].set_title('Memory Distribution', color='white')
        
        # Network topology metrics
        node_degrees = data.get('node_degrees', [random.randint(1, 20) for _ in range(50)])
        axes[1, 0].hist(node_degrees, bins=20, color=self.color_palette['primary'], alpha=0.7)
        axes[1, 0].set_title('Node Degree Distribution', color='white')
        axes[1, 0].set_xlabel('Degree', color='white')
        axes[1, 0].set_ylabel('Frequency', color='white')
        
        # Energy consumption heatmap
        energy_matrix = np.random.rand(10, 10) * 100
        im = axes[1, 1].imshow(energy_matrix, cmap='YlOrRd', aspect='auto')
        axes[1, 1].set_title('Energy Consumption Heatmap', color='white')
        fig1.colorbar(im, ax=axes[1, 1])
        
        figures.append(fig1)
        
        # 2. Quantum analysis plot
        fig2, ax = plt.subplots(figsize=(12, 8))
        
        # Simular dados quânticos
        theta = np.linspace(0, 4*np.pi, 1000)
        quantum_state_real = np.cos(theta) * np.exp(-theta/10)
        quantum_state_imag = np.sin(theta) * np.exp(-theta/10)
        
        ax.plot(theta, quantum_state_real, label='Real Part', 
               color=self.color_palette['primary'], linewidth=2)
        ax.plot(theta, quantum_state_imag, label='Imaginary Part', 
               color=self.color_palette['secondary'], linewidth=2)
        
        ax.set_title('Quantum State Evolution - AEONCOSMA Core', 
                    fontsize=14, color=self.color_palette['primary'])
        ax.set_xlabel('Time (θ)', color='white')
        ax.set_ylabel('Amplitude', color='white')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        figures.append(fig2)
        
        return figures
    
    def create_seaborn_statistical_analysis(self, data: Dict) -> List[plt.Figure]:
        """Cria análises estatísticas com Seaborn"""
        figures = []
        
        # Gerar dados de exemplo para análise
        np.random.seed(42)
        n_nodes = 200
        
        # Dataset simulado de performance de nós
        node_data = pd.DataFrame({
            'node_type': np.random.choice(['master', 'validator', 'ai', 'crypto', 'energy'], n_nodes),
            'cpu_usage': np.random.normal(50, 15, n_nodes),
            'memory_usage': np.random.normal(60, 20, n_nodes),
            'network_latency': np.random.exponential(10, n_nodes),
            'uptime_hours': np.random.normal(720, 100, n_nodes),
            'consensus_score': np.random.beta(2, 5, n_nodes) * 100
        })
        
        # 1. Matriz de correlação
        fig1, ax = plt.subplots(figsize=(10, 8))
        correlation_matrix = node_data.select_dtypes(include=[np.number]).corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='RdYlBu_r', center=0,
                   square=True, linewidths=0.5, ax=ax)
        ax.set_title('Node Performance Correlation Matrix', 
                    fontsize=14, color=self.color_palette['primary'])
        figures.append(fig1)
        
        # 2. Distribuições por tipo de nó
        fig2, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig2.suptitle('Performance Distribution by Node Type', 
                     fontsize=16, color=self.color_palette['primary'])
        
        # CPU usage by node type
        sns.boxplot(data=node_data, x='node_type', y='cpu_usage', ax=axes[0, 0])
        axes[0, 0].set_title('CPU Usage Distribution')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Memory vs CPU scatter
        sns.scatterplot(data=node_data, x='cpu_usage', y='memory_usage', 
                       hue='node_type', size='consensus_score', ax=axes[0, 1])
        axes[0, 1].set_title('Memory vs CPU Usage')
        
        # Network latency distribution
        sns.histplot(data=node_data, x='network_latency', hue='node_type', 
                    multiple="stack", ax=axes[1, 0])
        axes[1, 0].set_title('Network Latency Distribution')
        
        # Uptime vs Consensus Score
        sns.regplot(data=node_data, x='uptime_hours', y='consensus_score', ax=axes[1, 1])
        axes[1, 1].set_title('Uptime vs Consensus Score')
        
        figures.append(fig2)
        
        return figures
    
    def create_plotly_interactive_3d(self, network_data: Dict) -> List[go.Figure]:
        """Cria visualizações 3D interativas com Plotly"""
        figures = []
        
        # 1. Rede 3D interativa melhorada
        fig1 = go.Figure()
        
        # Gerar dados de rede 3D
        n_nodes = 100
        node_positions = {
            'x': [random.uniform(-20, 20) for _ in range(n_nodes)],
            'y': [random.uniform(-20, 20) for _ in range(n_nodes)],
            'z': [random.uniform(-20, 20) for _ in range(n_nodes)]
        }
        
        node_types = ['master', 'validator', 'ai', 'crypto', 'energy', 'quantum', 'cosmos']
        node_colors = {
            'master': '#ff0000',
            'validator': '#00ff00', 
            'ai': '#0000ff',
            'crypto': '#ff00ff',
            'energy': '#ffff00',
            'quantum': '#00ffff',
            'cosmos': '#ff8800'
        }
        
        # Adicionar nós
        for i in range(n_nodes):
            node_type = random.choice(node_types)
            fig1.add_trace(go.Scatter3d(
                x=[node_positions['x'][i]],
                y=[node_positions['y'][i]], 
                z=[node_positions['z'][i]],
                mode='markers',
                marker=dict(
                    size=random.uniform(5, 15),
                    color=node_colors[node_type],
                    opacity=0.8
                ),
                name=f'{node_type}_{i}',
                hovertemplate=f'<b>{node_type} Node {i}</b><br>' +
                             f'Position: ({node_positions["x"][i]:.1f}, ' +
                             f'{node_positions["y"][i]:.1f}, {node_positions["z"][i]:.1f})<br>' +
                             f'Type: {node_type}<extra></extra>'
            ))
        
        # Adicionar conexões (edges)
        edge_x, edge_y, edge_z = [], [], []
        for i in range(0, n_nodes, 5):  # Conectar alguns nós
            for j in range(i+1, min(i+3, n_nodes)):
                edge_x.extend([node_positions['x'][i], node_positions['x'][j], None])
                edge_y.extend([node_positions['y'][i], node_positions['y'][j], None])
                edge_z.extend([node_positions['z'][i], node_positions['z'][j], None])
        
        fig1.add_trace(go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color='rgba(125,125,125,0.5)', width=2),
            name='Connections',
            showlegend=False
        ))
        
        fig1.update_layout(
            title='AEONCOSMA 3D Network - Interactive View',
            scene=dict(
                xaxis_title='X Coordinate',
                yaxis_title='Y Coordinate', 
                zaxis_title='Z Coordinate',
                bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='rgba(255,255,255,0.2)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.2)'),
                zaxis=dict(gridcolor='rgba(255,255,255,0.2)')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        figures.append(fig1)
        
        # 2. Dashboard multi-dimensional
        fig2 = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Real-time Metrics', 'Node Distribution', 
                          'Energy Consumption', 'Network Topology'),
            specs=[[{"secondary_y": True}, {"type": "pie"}],
                   [{"type": "surface"}, {"type": "scatter3d"}]]
        )
        
        # Real-time metrics
        times = list(range(100))
        cpu_data = [random.uniform(20, 80) for _ in times]
        memory_data = [random.uniform(30, 90) for _ in times]
        
        fig2.add_trace(go.Scatter(x=times, y=cpu_data, name='CPU %', 
                                 line=dict(color=self.color_palette['primary'])), 
                      row=1, col=1)
        fig2.add_trace(go.Scatter(x=times, y=memory_data, name='Memory %',
                                 line=dict(color=self.color_palette['secondary'])), 
                      row=1, col=1, secondary_y=True)
        
        # Node type distribution
        node_counts = [20, 15, 12, 8, 5, 3, 2]
        fig2.add_trace(go.Pie(labels=node_types, values=node_counts,
                             marker_colors=list(node_colors.values())), 
                      row=1, col=2)
        
        # Energy consumption surface
        x_energy = np.linspace(-5, 5, 20)
        y_energy = np.linspace(-5, 5, 20)
        X, Y = np.meshgrid(x_energy, y_energy)
        Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1*np.sqrt(X**2 + Y**2))
        
        fig2.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Viridis'), 
                      row=2, col=1)
        
        fig2.update_layout(
            title_text="AEONCOSMA Advanced Dashboard",
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        figures.append(fig2)
        
        return figures
    
    def create_bokeh_realtime_dashboard(self) -> bk.Document:
        """Cria dashboard em tempo real com Bokeh"""
        
        # Fonte de dados para streaming
        source = ColumnDataSource(data=dict(
            time=[],
            cpu=[],
            memory=[],
            network=[]
        ))
        
        # Gráfico de CPU
        cpu_plot = bk.figure(
            title="Real-time CPU Usage",
            x_axis_label='Time',
            y_axis_label='CPU %',
            width=400,
            height=300,
            background_fill_color='#2F2F2F'
        )
        cpu_plot.line('time', 'cpu', source=source, 
                     line_color=self.color_palette['primary'], line_width=2)
        
        # Gráfico de Memory
        memory_plot = bk.figure(
            title="Real-time Memory Usage", 
            x_axis_label='Time',
            y_axis_label='Memory %',
            width=400,
            height=300,
            background_fill_color='#2F2F2F'
        )
        memory_plot.line('time', 'memory', source=source,
                        line_color=self.color_palette['secondary'], line_width=2)
        
        # Callback para atualização em tempo real
        def update_data():
            new_data = dict(
                time=[len(source.data['time'])],
                cpu=[random.uniform(20, 80)],
                memory=[random.uniform(30, 90)],
                network=[random.uniform(0, 100)]
            )
            source.stream(new_data, rollover=100)
        
        # Layout
        layout = column(
            row(cpu_plot, memory_plot),
            sizing_mode="stretch_width"
        )
        
        # Configurar documento
        doc = curdoc()
        doc.add_root(layout)
        doc.add_periodic_callback(update_data, 1000)  # Atualizar a cada segundo
        
        return doc
    
    def export_gephi_network(self, filename: str = "aeoncosma_network.gexf"):
        """Exporta rede para análise no Gephi"""
        
        # Criar rede para análise
        G = nx.Graph()
        
        # Adicionar nós com atributos
        node_types = ['master', 'validator', 'ai', 'crypto', 'energy', 'quantum', 'cosmos']
        for i in range(100):
            node_type = random.choice(node_types)
            G.add_node(i, 
                      type=node_type,
                      cpu_usage=random.uniform(20, 80),
                      memory_usage=random.uniform(30, 90),
                      centrality=random.uniform(0, 1))
        
        # Adicionar arestas com pesos
        for i in range(100):
            for j in range(i+1, min(i+5, 100)):
                if random.random() > 0.7:  # 30% chance de conexão
                    weight = random.uniform(0.1, 1.0)
                    G.add_edge(i, j, weight=weight)
        
        # Calcular métricas de rede
        centrality = nx.betweenness_centrality(G)
        clustering = nx.clustering(G)
        
        # Adicionar métricas como atributos dos nós
        for node in G.nodes():
            G.nodes[node]['betweenness'] = centrality[node]
            G.nodes[node]['clustering'] = clustering[node]
        
        # Exportar para Gephi
        filepath = f"c:\\Users\\Luiz\\OneDrive\\Área de Trabalho\\aeon\\Digital Twin\\aeoncosma\\ui\\{filename}"
        nx.write_gexf(G, filepath)
        
        return filepath
    
    def generate_d3js_integration_code(self) -> str:
        """Gera código D3.js para visualizações customizadas"""
        
        d3_code = """
        // AEONCOSMA D3.js Custom Visualization
        
        const width = 800;
        const height = 600;
        
        const svg = d3.select("#aeoncosma-viz")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .style("background", "#1a1a1a");
        
        // Dados de exemplo
        const nodes = [
            {id: "master", group: 1, value: 30},
            {id: "ai", group: 2, value: 20},
            {id: "crypto", group: 3, value: 15},
            {id: "energy", group: 4, value: 25},
            {id: "quantum", group: 5, value: 10}
        ];
        
        const links = [
            {source: "master", target: "ai", value: 1},
            {source: "master", target: "crypto", value: 1},
            {source: "ai", target: "energy", value: 1},
            {source: "crypto", target: "quantum", value: 1}
        ];
        
        // Simulação de força
        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2));
        
        // Desenhar links
        const link = svg.append("g")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("stroke", "#00ff88")
            .attr("stroke-opacity", 0.6)
            .attr("stroke-width", d => Math.sqrt(d.value) * 2);
        
        // Desenhar nós
        const node = svg.append("g")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", d => d.value)
            .attr("fill", d => d3.schemeCategory10[d.group])
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
        
        // Adicionar labels
        const text = svg.append("g")
            .selectAll("text")
            .data(nodes)
            .enter().append("text")
            .text(d => d.id)
            .attr("font-size", 12)
            .attr("fill", "white")
            .attr("text-anchor", "middle");
        
        // Atualizar posições
        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
        
            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
                
            text
                .attr("x", d => d.x)
                .attr("y", d => d.y + 5);
        });
        
        // Funções de drag
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
        """
        
        return d3_code

def main():
    """Interface principal do Streamlit"""
    st.set_page_config(
        page_title="AEONCOSMA Advanced Visualization Suite",
        page_icon="🌌",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🌌 AEONCOSMA Advanced Visualization Suite")
    st.markdown("### Sistema Híbrido de Visualização de Dados")
    
    # Criar instância da suite
    viz_suite = AdvancedVisualizationSuite()
    
    # Sidebar para seleção de visualizações
    st.sidebar.title("Visualizations")
    viz_type = st.sidebar.selectbox(
        "Choose Visualization Type:",
        ["Matplotlib Scientific", "Seaborn Statistical", "Plotly Interactive 3D", 
         "Network Analysis", "Export Options", "D3.js Integration", "🤖 AI Analytics"]
    )
    
    # Gerar dados de exemplo
    sample_data = {
        'timestamps': list(range(100)),
        'cpu_usage': [random.uniform(20, 80) for _ in range(100)],
        'node_degrees': [random.randint(1, 20) for _ in range(50)],
        'network_data': {}
    }
    
    if viz_type == "Matplotlib Scientific":
        st.header("📊 Scientific Analysis with Matplotlib")
        
        with st.spinner("Generating scientific plots..."):
            figures = viz_suite.create_matplotlib_scientific_plots(sample_data)
            
            for i, fig in enumerate(figures):
                st.pyplot(fig)
                st.markdown("---")
    
    elif viz_type == "Seaborn Statistical":
        st.header("📈 Statistical Analysis with Seaborn")
        
        with st.spinner("Generating statistical analysis..."):
            figures = viz_suite.create_seaborn_statistical_analysis(sample_data)
            
            for i, fig in enumerate(figures):
                st.pyplot(fig)
                st.markdown("---")
    
    elif viz_type == "Plotly Interactive 3D":
        st.header("🌐 Interactive 3D Visualizations")
        
        with st.spinner("Creating interactive plots..."):
            figures = viz_suite.create_plotly_interactive_3d(sample_data)
            
            for fig in figures:
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("---")
    
    elif viz_type == "Network Analysis":
        st.header("🕸️ Network Analysis & Gephi Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export Network for Gephi"):
                with st.spinner("Exporting network..."):
                    filepath = viz_suite.export_gephi_network()
                    st.success(f"Network exported to: {filepath}")
                    st.info("💡 Open this file in Gephi for advanced network analysis!")
        
        with col2:
            st.markdown("""
            **Gephi Analysis Features:**
            - Node centrality analysis
            - Community detection
            - Network clustering
            - Force-directed layouts
            - Statistical analysis
            """)
    
    elif viz_type == "Export Options":
        st.header("💾 Export & Integration Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Available Export Formats:**
            - 📊 Matplotlib: PNG, PDF, SVG
            - 📈 Seaborn: High-res scientific plots
            - 🌐 Plotly: HTML, PDF, PNG
            - 🕸️ NetworkX: GEXF for Gephi
            - 🗃️ Data: CSV, JSON, Parquet
            """)
        
        with col2:
            st.markdown("""
            **Integration APIs:**
            - Apache Superset dashboard
            - Metabase integration
            - Grafana monitoring
            - Custom REST endpoints
            - Real-time data streaming
            """)
    
    elif viz_type == "D3.js Integration":
        st.header("⚡ D3.js Custom Visualizations")
        
        st.markdown("### Generated D3.js Code:")
        d3_code = viz_suite.generate_d3js_integration_code()
        st.code(d3_code, language='javascript')
        
        st.markdown("""
        **To use this code:**
        1. Include D3.js library in your HTML
        2. Create a div with id="aeoncosma-viz"
        3. Copy and run this JavaScript code
        4. Customize as needed for your specific data
        """)
        
    elif viz_type == "🤖 AI Analytics":
        st.header("🤖 AEONCOSMA AI-Powered Analytics")
        
        if viz_suite.ai_enabled:
            # Interface de consulta natural
            st.subheader("💬 Natural Language Query Interface")
            user_query = st.text_area(
                "Ask anything about your AEONCOSMA data:",
                placeholder="Example: What are the performance metrics for the last 24 hours?",
                height=100
            )
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("🧠 Generate AI Insights", type="primary"):
                    if user_query:
                        with st.spinner("🤖 AI analyzing your query..."):
                            try:
                                if viz_suite.ai_analytics.api_key:
                                    # Usar análise com IA
                                    insights = viz_suite.ai_analytics.query_database_with_ai(user_query, viz_suite.ai_analytics.api_key)
                                    
                                    st.subheader("📊 AI-Generated Insights")
                                    st.json(insights)
                                else:
                                    st.warning("� OpenAI API key não configurada. Configure para ativar análises avançadas.")
                                    
                                    # Mostrar dados básicos do banco
                                    st.subheader("📊 Database Overview")
                                    schema = viz_suite.ai_analytics.get_database_schema()
                                    st.text(schema)
                                
                            except Exception as e:
                                st.error(f"AI Analysis error: {str(e)}")
                    else:
                        st.warning("Please enter a query first.")
            
            with col2:
                if st.button("🔍 Smart Query Generation"):
                    if user_query:
                        with st.spinner("🤖 Converting to SQL..."):
                            try:
                                if viz_suite.ai_analytics.api_key:
                                    # Gerar query SQL inteligente
                                    results = viz_suite.ai_analytics.query_database_with_ai(user_query, viz_suite.ai_analytics.api_key)
                                    
                                    st.subheader("🔧 AI Query Results")
                                    if 'sql_query' in results:
                                        st.code(results['sql_query'], language='sql')
                                    
                                    if 'resultado' in results:
                                        st.subheader("📋 Query Results")
                                        if results['resultado']:
                                            df = pd.DataFrame(results['resultado'])
                                            st.dataframe(df)
                                        else:
                                            st.info("No results found.")
                                else:
                                    st.warning("🔑 OpenAI API key needed for intelligent query generation.")
                                        
                            except Exception as e:
                                st.error(f"Query generation error: {str(e)}")
            
            # Análises pré-definidas
            st.subheader("⚡ Quick AI Analyses")
            
            analysis_col1, analysis_col2, analysis_col3 = st.columns(3)
            
            with analysis_col1:
                if st.button("🚀 Database Overview"):
                    with st.spinner("Analyzing database..."):
                        try:
                            schema = viz_suite.ai_analytics.get_database_schema()
                            st.text_area("Database Schema", schema, height=200)
                        except Exception as e:
                            st.error(f"Analysis error: {str(e)}")
            
            with analysis_col2:
                if st.button("� Sample Questions"):
                    with st.spinner("Loading sample questions..."):
                        try:
                            questions = viz_suite.ai_analytics.get_sample_questions()
                            for i, q in enumerate(questions, 1):
                                st.write(f"{i}. {q}")
                        except Exception as e:
                            st.error(f"Questions error: {str(e)}")
            
            with analysis_col3:
                if st.button("� Node Count"):
                    with st.spinner("Counting nodes..."):
                        try:
                            import sqlite3
                            conn = sqlite3.connect(viz_suite.ai_analytics.database_path)
                            cursor = conn.cursor()
                            cursor.execute("SELECT COUNT(*) FROM network_nodes")
                            count = cursor.fetchone()[0]
                            conn.close()
                            st.metric("Total Nodes", count)
                        except Exception as e:
                            st.error(f"Count error: {str(e)}")
            
            # Status da IA
            st.subheader("🤖 AI Module Status")
            status_col1, status_col2 = st.columns(2)
            
            with status_col1:
                st.metric("AI Module", "✅ Enabled" if viz_suite.ai_enabled else "❌ Disabled")
                st.metric("OpenAI API", "✅ Connected" if viz_suite.ai_analytics.api_key else "❌ Not configured")
            
            with status_col2:
                st.metric("Database", "✅ Connected" if viz_suite.ai_analytics.database_path else "❌ Not configured")
                st.metric("Query Engine", "✅ Ready")
        
        else:
            st.warning("🤖 AI Analytics module not available.")
            st.info("""
            To enable AI Analytics:
            1. Install OpenAI package: `pip install openai`
            2. Configure your OpenAI API key
            3. Restart the application
            """)
    
    # Footer info
    st.sidebar.markdown("---")
    st.sidebar.info("""
    🌟 **AEONCOSMA Visualization Suite**
    
    Integrating the best visualization tools:
    - Matplotlib (Scientific)
    - Seaborn (Statistical) 
    - Plotly (Interactive)
    - Bokeh (Real-time)
    - NetworkX + Gephi (Networks)
    - D3.js (Custom Web)
    """)

if __name__ == "__main__":
    main()
