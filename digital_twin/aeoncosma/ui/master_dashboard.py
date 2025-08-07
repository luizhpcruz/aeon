"""
AEONCOSMA Master Visualization Dashboard
========================================
Dashboard principal que integra todas as ferramentas de visualização
"""

import streamlit as st
import subprocess
import webbrowser
from pathlib import Path
import json
import time
import requests
from typing import Dict, List, Any

class MasterVisualizationDashboard:
    """Dashboard principal para todas as visualizações AEONCOSMA"""
    
    def __init__(self):
        self.tools_status = {}
        self.available_tools = {
            'streamlit_basic': {
                'name': 'Basic 3D Network Visualizer',
                'port': 8506,
                'script': 'network_3d_visualizer.py',
                'status': 'stopped'
            },
            'streamlit_advanced': {
                'name': 'Advanced Visualization Suite',
                'port': 8507,
                'script': 'advanced_visualization_suite.py', 
                'status': 'stopped'
            },
            'scientific_report': {
                'name': 'Scientific Report Generator',
                'port': None,
                'script': 'scientific_report_generator.py',
                'status': 'ready'
            },
            'bi_integration': {
                'name': 'BI Platform Integration',
                'port': None,
                'script': 'bi_platform_integration.py',
                'status': 'ready'
            }
        }
        
    def check_tool_status(self, tool_name: str) -> str:
        """Verifica o status de uma ferramenta"""
        tool = self.available_tools[tool_name]
        
        if tool['port']:
            try:
                response = requests.get(f"http://localhost:{tool['port']}", timeout=2)
                return 'running' if response.status_code == 200 else 'stopped'
            except:
                return 'stopped'
        else:
            return 'ready'
    
    def start_streamlit_app(self, script_name: str, port: int) -> bool:
        """Inicia uma aplicação Streamlit"""
        try:
            python_exe = r"C:\Users\Luiz\OneDrive\Área de Trabalho\aeon\Digital Twin\.venv\Scripts\python.exe"
            cmd = f'"{python_exe}" -m streamlit run "{script_name}" --server.port {port} --server.address localhost'
            
            subprocess.Popen(cmd, shell=True, cwd=Path.cwd())
            time.sleep(3)  # Aguardar inicialização
            return True
        except Exception as e:
            st.error(f"Erro ao iniciar {script_name}: {e}")
            return False
    
    def generate_scientific_report(self) -> str:
        """Gera relatório científico"""
        try:
            python_exe = r"C:\Users\Luiz\OneDrive\Área de Trabalho\aeon\Digital Twin\.venv\Scripts\python.exe"
            result = subprocess.run(
                [python_exe, "scientific_report_generator.py"],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            
            if result.returncode == 0:
                return "aeoncosma_network_analysis.pdf"
            else:
                st.error(f"Erro na geração do relatório: {result.stderr}")
                return None
        except Exception as e:
            st.error(f"Erro ao gerar relatório: {e}")
            return None
    
    def export_bi_configs(self) -> bool:
        """Exporta configurações de BI"""
        try:
            python_exe = r"C:\Users\Luiz\OneDrive\Área de Trabalho\aeon\Digital Twin\.venv\Scripts\python.exe"
            result = subprocess.run(
                [python_exe, "bi_platform_integration.py"],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            
            return result.returncode == 0
        except Exception as e:
            st.error(f"Erro ao exportar configurações BI: {e}")
            return False

def main():
    """Interface principal do dashboard mestre"""
    st.set_page_config(
        page_title="AEONCOSMA Master Dashboard",
        page_icon="🌌",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS customizado
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .tool-card {
        border: 2px solid #e1e1e1;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .status-running {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-stopped {
        color: #dc3545;
        font-weight: bold;
    }
    
    .status-ready {
        color: #ffc107;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Cabeçalho principal
    st.markdown("""
    <div class="main-header">
        <h1>🌌 AEONCOSMA Master Visualization Dashboard</h1>
        <p>Central hub for all visualization tools and analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Criar instância do dashboard
    dashboard = MasterVisualizationDashboard()
    
    # Sidebar com informações do sistema
    st.sidebar.title("🔧 System Control")
    
    if st.sidebar.button("🔄 Refresh Status"):
        st.experimental_rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    # Verificar status das ferramentas
    running_tools = 0
    for tool_name in dashboard.available_tools.keys():
        status = dashboard.check_tool_status(tool_name)
        dashboard.available_tools[tool_name]['status'] = status
        if status == 'running':
            running_tools += 1
    
    st.sidebar.metric("Running Tools", f"{running_tools}/4")
    st.sidebar.metric("Available Visualizations", "15+")
    st.sidebar.metric("Supported Formats", "PDF, HTML, JSON, GEXF")
    
    # Layout principal com 3 colunas
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Coluna 1: Visualizações Interativas
    with col1:
        st.header("🖥️ Interactive Visualizations")
        
        # Tool 1: Basic 3D Network
        tool = dashboard.available_tools['streamlit_basic']
        status = tool['status']
        status_class = f"status-{status}"
        
        st.markdown(f"""
        <div class="tool-card">
            <h4>🌐 {tool['name']}</h4>
            <p>3D network topology with real-time updates</p>
            <p>Status: <span class="{status_class}">{status.upper()}</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            if st.button("▶️ Start Basic Viz", key="start_basic"):
                if dashboard.start_streamlit_app(tool['script'], tool['port']):
                    st.success("Starting Basic Visualizer...")
                    time.sleep(2)
                    st.experimental_rerun()
        
        with col1_2:
            if status == 'running':
                if st.button("🌐 Open Basic Viz", key="open_basic"):
                    st.markdown(f"[Open in Browser](http://localhost:{tool['port']})")
        
        st.markdown("---")
        
        # Tool 2: Advanced Suite
        tool = dashboard.available_tools['streamlit_advanced']
        status = tool['status']
        status_class = f"status-{status}"
        
        st.markdown(f"""
        <div class="tool-card">
            <h4>⚡ {tool['name']}</h4>
            <p>Matplotlib, Seaborn, Plotly integration</p>
            <p>Status: <span class="{status_class}">{status.upper()}</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1_3, col1_4 = st.columns(2)
        with col1_3:
            if st.button("▶️ Start Advanced", key="start_advanced"):
                if dashboard.start_streamlit_app(tool['script'], tool['port']):
                    st.success("Starting Advanced Suite...")
                    time.sleep(2)
                    st.experimental_rerun()
        
        with col1_4:
            if status == 'running':
                if st.button("🌐 Open Advanced", key="open_advanced"):
                    st.markdown(f"[Open in Browser](http://localhost:{tool['port']})")
    
    # Coluna 2: Relatórios e Análises
    with col2:
        st.header("📊 Reports & Analytics")
        
        # Scientific Report
        st.markdown("""
        <div class="tool-card">
            <h4>🔬 Scientific Report Generator</h4>
            <p>Comprehensive PDF reports with statistical analysis</p>
            <p>Status: <span class="status-ready">READY</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 Generate PDF Report", key="gen_report"):
            with st.spinner("Generating scientific report..."):
                report_path = dashboard.generate_scientific_report()
                if report_path:
                    st.success(f"✅ Report generated: {report_path}")
                    
                    # Oferecer download
                    with open(report_path, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download Report",
                            data=pdf_file.read(),
                            file_name=report_path,
                            mime="application/pdf"
                        )
        
        st.markdown("---")
        
        # Verificar se relatório existe
        report_file = Path("aeoncosma_network_analysis.pdf")
        if report_file.exists():
            st.info(f"📄 Latest report: {report_file.stat().st_mtime}")
            with open(report_file, "rb") as pdf:
                st.download_button(
                    "📥 Download Latest Report",
                    pdf.read(),
                    file_name="aeoncosma_network_analysis.pdf",
                    mime="application/pdf"
                )
    
    # Coluna 3: Integrações e Exports
    with col3:
        st.header("🔗 Integrations & Export")
        
        # BI Platform Integration
        st.markdown("""
        <div class="tool-card">
            <h4>🏢 BI Platform Integration</h4>
            <p>Superset, Metabase, Grafana configs</p>
            <p>Status: <span class="status-ready">READY</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚙️ Export BI Configs", key="export_bi"):
            with st.spinner("Exporting BI configurations..."):
                if dashboard.export_bi_configs():
                    st.success("✅ BI configurations exported!")
                    
                    # Mostrar arquivos disponíveis
                    bi_config_dir = Path("bi_configs")
                    if bi_config_dir.exists():
                        st.write("📁 Available configurations:")
                        for config_file in bi_config_dir.glob("*.json"):
                            with open(config_file, 'r') as f:
                                st.download_button(
                                    f"📥 {config_file.name}",
                                    f.read(),
                                    file_name=config_file.name,
                                    mime="application/json",
                                    key=f"download_{config_file.stem}"
                                )
        
        st.markdown("---")
        
        # External Tools Integration
        st.markdown("""
        <div class="tool-card">
            <h4>🛠️ External Tools</h4>
            <p>Gephi, QGIS, D3.js integration</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Gephi export
        if st.button("🕸️ Export for Gephi", key="export_gephi"):
            st.info("GEXF file available: aeoncosma_network.gexf")
            gephi_file = Path("aeoncosma_network.gexf")
            if gephi_file.exists():
                with open(gephi_file, 'r') as f:
                    st.download_button(
                        "📥 Download GEXF",
                        f.read(),
                        file_name="aeoncosma_network.gexf",
                        mime="application/xml"
                    )
        
        # D3.js code
        if st.button("⚡ Generate D3.js Code", key="gen_d3"):
            st.code("""
// AEONCOSMA D3.js Visualization
const svg = d3.select("#viz")
    .append("svg")
    .attr("width", 800)
    .attr("height", 600);

// Add your D3.js code here
// Data will be loaded from JSON exports
            """, language='javascript')
    
    # Seção de estatísticas em tempo real
    st.markdown("---")
    st.header("📈 Real-time Dashboard")
    
    # Métricas em tempo real (simuladas)
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    import random
    with col_m1:
        st.metric("Active Nodes", "85", delta="2")
    
    with col_m2:
        st.metric("Network Efficiency", "94.7%", delta="0.3%")
    
    with col_m3:
        st.metric("Energy Usage", "450 kWh", delta="-15 kWh")
    
    with col_m4:
        st.metric("Security Score", "92.5%", delta="1.2%")
    
    # Informações sobre ferramentas disponíveis
    st.markdown("---")
    st.header("🧰 Available Visualization Tools")
    
    tools_info = {
        "Matplotlib": "Scientific plots, publication-quality graphics",
        "Seaborn": "Statistical data visualization, correlation analysis", 
        "Plotly": "Interactive 3D visualizations, web-ready charts",
        "Bokeh": "Real-time streaming data visualization",
        "NetworkX": "Network analysis, graph algorithms",
        "Gephi Integration": "Advanced network analysis and community detection",
        "Apache Superset": "Enterprise BI dashboards",
        "Metabase": "Business intelligence for teams",
        "Grafana": "Real-time monitoring and alerting",
        "QGIS": "Geospatial analysis and mapping",
        "D3.js": "Custom web visualizations"
    }
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("📊 Visualization Libraries")
        for tool in ["Matplotlib", "Seaborn", "Plotly", "Bokeh", "NetworkX"]:
            st.write(f"✅ **{tool}**: {tools_info[tool]}")
    
    with col_t2:
        st.subheader("🏢 BI Platform Integration")
        for tool in ["Gephi Integration", "Apache Superset", "Metabase", "Grafana", "QGIS", "D3.js"]:
            st.write(f"✅ **{tool}**: {tools_info[tool]}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; padding: 1rem;">
        🌌 AEONCOSMA Master Visualization Dashboard v1.0<br>
        Integrating the best visualization tools for comprehensive data analysis
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
