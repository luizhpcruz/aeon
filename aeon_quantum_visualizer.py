#!/usr/bin/env python3
"""
🎨 AEON Quantum Visualization Dashboard
Sistema avançado de visualização para análise de entropia quântica
Geração de gráficos dinâmicos e interfaces interativas
"""

import json
import math
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import webbrowser
import threading

# Tentar importar bibliotecas de visualização
try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.patches import Circle, Rectangle
    from matplotlib.collections import LineCollection
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
    print("✅ Matplotlib disponível")
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️ Matplotlib não disponível. Usando visualização ASCII.")

try:
    from quantum_entropy_analyzer import QuantumEntropyAnalyzer, EntropySnapshot
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False
    print("⚠️ Analisador quântico não disponível")

class AeonQuantumVisualizer:
    """Visualizador avançado para dados de entropia quântica AEON"""
    
    def __init__(self, data_source: Optional['QuantumEntropyAnalyzer'] = None):
        self.data_source = data_source
        self.html_output_dir = Path("aeon_visualizations")
        self.html_output_dir.mkdir(exist_ok=True)
        
        # Configurações de estilo
        self.colors = {
            'quantum': '#00ffff',      # Cyan
            'classical': '#ff6b35',    # Orange
            'entanglement': '#7209b7', # Purple
            'total': '#ffffff',        # White
            'coherence': '#4cc9f0',    # Light blue
            'temperature': '#f72585',  # Pink
            'complexity': '#4361ee'    # Blue
        }
        
        self.style_config = {
            'background': '#0a0a0a',   # Dark background
            'grid': '#333333',         # Dark grid
            'text': '#ffffff',         # White text
            'accent': '#00ff41'        # Matrix green
        }
        
    def generate_ascii_visualization(self, data: List[EntropySnapshot]) -> str:
        """Gera visualização ASCII dos dados de entropia"""
        if not data:
            return "📊 Nenhum dado disponível para visualização"
        
        output = []
        output.append("🌌 AEON Quantum Entropy Evolution")
        output.append("=" * 60)
        
        # Extrai valores para plotting ASCII
        entropies = [s.total_entropy for s in data[-20:]]  # Últimos 20 pontos
        max_entropy = max(entropies) if entropies else 1
        min_entropy = min(entropies) if entropies else 0
        
        # Normaliza para 0-40 (largura do gráfico ASCII)
        height = 15
        width = min(len(entropies), 50)
        
        if max_entropy > min_entropy:
            normalized = [(e - min_entropy) / (max_entropy - min_entropy) * height for e in entropies[-width:]]
        else:
            normalized = [height // 2] * len(entropies[-width:])
        
        # Desenha gráfico ASCII
        for row in range(height, -1, -1):
            line = ""
            for col in range(width):
                if col < len(normalized):
                    if abs(normalized[col] - row) < 0.5:
                        line += "█"
                    elif row == 0:
                        line += "▁"
                    else:
                        line += " "
                else:
                    line += " "
            
            # Escala Y
            y_value = min_entropy + (max_entropy - min_entropy) * row / height
            output.append(f"{y_value:6.2f} │{line}")
        
        # Eixo X
        output.append("       " + "└" + "─" * width)
        output.append("        " + "".join([str(i % 10) for i in range(width)]))
        
        # Estatísticas
        latest = data[-1]
        output.append("")
        output.append("📈 Estatísticas Atuais:")
        output.append(f"   🔬 Entropia Total: {latest.total_entropy:.3f}")
        output.append(f"   ⚛️ Entropia Quântica: {latest.quantum_entropy:.3f}")
        output.append(f"   🌡️ Temperatura: {latest.system_temperature:.3f}")
        output.append(f"   ✨ Coerência: {latest.coherence_level:.3f}")
        output.append(f"   🧩 Complexidade: {latest.complexity_index:.3f}")
        
        # Análise dimensional
        if latest.dimensional_analysis:
            output.append("")
            output.append("🔍 Análise Dimensional:")
            for dim_name, value in latest.dimensional_analysis.items():
                output.append(f"   📐 {dim_name}: {value:.3f}")
        
        return "\n".join(output)
    
    def generate_html_dashboard(self, data: List[EntropySnapshot]) -> str:
        """Gera dashboard HTML interativo com dados de entropia"""
        if not data:
            return self._generate_empty_dashboard()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"aeon_quantum_dashboard_{timestamp}.html"
        filepath = self.html_output_dir / filename
        
        # Prepara dados para JavaScript
        js_data = self._prepare_data_for_js(data)
        
        # Template HTML
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌌 AEON Quantum Entropy Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    <style>
        body {{
            font-family: 'Consolas', 'Monaco', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin: 0;
            background: linear-gradient(45deg, #00ffff, #ff6b35);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .chart-container {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .chart-title {{
            font-size: 1.2em;
            margin-bottom: 15px;
            text-align: center;
            color: #00ff41;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .dimensional-analysis {{
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
        }}
        
        .dimensional-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        
        .dim-item {{
            text-align: center;
            padding: 10px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 8px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            font-size: 0.9em;
            opacity: 0.7;
        }}
        
        @keyframes glow {{
            0% {{ box-shadow: 0 0 5px rgba(0, 255, 65, 0.3); }}
            50% {{ box-shadow: 0 0 20px rgba(0, 255, 65, 0.6); }}
            100% {{ box-shadow: 0 0 5px rgba(0, 255, 65, 0.3); }}
        }}
        
        .chart-container:hover {{
            animation: glow 2s infinite;
            transition: all 0.3s ease;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌌 AEON Quantum Entropy Dashboard</h1>
        <p>Sistema de Análise Avançada de Entropia Quântica</p>
        <p>📅 Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value" id="totalEntropy">{data[-1].total_entropy:.3f}</div>
            <div class="stat-label">🔬 Entropia Total</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="temperature">{data[-1].system_temperature:.3f}</div>
            <div class="stat-label">🌡️ Temperatura</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="coherence">{data[-1].coherence_level:.3f}</div>
            <div class="stat-label">✨ Coerência</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="complexity">{data[-1].complexity_index:.3f}</div>
            <div class="stat-label">🧩 Complexidade</div>
        </div>
    </div>
    
    <div class="dashboard-grid">
        <div class="chart-container">
            <div class="chart-title">📈 Evolução da Entropia Total</div>
            <canvas id="entropyChart"></canvas>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">🔬 Componentes de Entropia</div>
            <canvas id="componentsChart"></canvas>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">🌡️ Temperatura vs Coerência</div>
            <canvas id="tempCoherenceChart"></canvas>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">🧩 Índice de Complexidade</div>
            <canvas id="complexityChart"></canvas>
        </div>
    </div>
    
    <div class="dimensional-analysis">
        <div class="chart-title">📐 Análise Dimensional</div>
        <div class="dimensional-grid" id="dimensionalGrid">
            <!-- Preenchido via JavaScript -->
        </div>
    </div>
    
    <div class="footer">
        <p>🧬 Projeto AEON - Sistema de Análise Quântica</p>
        <p>💻 Dashboard gerado automaticamente pelo Quantum Visualizer</p>
    </div>
    
    <script>
        // Dados de entropia
        const entropyData = {js_data};
        
        // Configuração global dos gráficos
        Chart.defaults.color = '#ffffff';
        Chart.defaults.backgroundColor = 'rgba(255, 255, 255, 0.1)';
        Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.2)';
        Chart.defaults.font.family = 'Consolas, Monaco, monospace';
        
        // Gráfico de evolução da entropia total
        const entropyCtx = document.getElementById('entropyChart').getContext('2d');
        new Chart(entropyCtx, {{
            type: 'line',
            data: {{
                labels: entropyData.timestamps,
                datasets: [{{
                    label: 'Entropia Total',
                    data: entropyData.total_entropy,
                    borderColor: '#00ffff',
                    backgroundColor: 'rgba(0, 255, 255, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: false,
                        grid: {{ color: 'rgba(255, 255, 255, 0.1)' }}
                    }},
                    x: {{
                        grid: {{ color: 'rgba(255, 255, 255, 0.1)' }}
                    }}
                }},
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});
        
        // Gráfico de componentes de entropia
        const componentsCtx = document.getElementById('componentsChart').getContext('2d');
        new Chart(componentsCtx, {{
            type: 'line',
            data: {{
                labels: entropyData.timestamps,
                datasets: [
                    {{
                        label: 'Quântica',
                        data: entropyData.quantum_entropy,
                        borderColor: '#00ffff',
                        backgroundColor: 'rgba(0, 255, 255, 0.1)',
                        fill: false
                    }},
                    {{
                        label: 'Clássica',
                        data: entropyData.classical_entropy,
                        borderColor: '#ff6b35',
                        backgroundColor: 'rgba(255, 107, 53, 0.1)',
                        fill: false
                    }},
                    {{
                        label: 'Emaranhamento',
                        data: entropyData.entanglement_entropy,
                        borderColor: '#7209b7',
                        backgroundColor: 'rgba(114, 9, 183, 0.1)',
                        fill: false
                    }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: false,
                        grid: {{ color: 'rgba(255, 255, 255, 0.1)' }}
                    }},
                    x: {{
                        grid: {{ color: 'rgba(255, 255, 255, 0.1)' }}
                    }}
                }}
            }}
        }});
        
        // Gráfico temperatura vs coerência
        const tempCtx = document.getElementById('tempCoherenceChart').getContext('2d');
        new Chart(tempCtx, {{
            type: 'line',
            data: {{
                labels: entropyData.timestamps,
                datasets: [
                    {{
                        label: 'Temperatura',
                        data: entropyData.temperature,
                        borderColor: '#f72585',
                        backgroundColor: 'rgba(247, 37, 133, 0.1)',
                        yAxisID: 'y'
                    }},
                    {{
                        label: 'Coerência',
                        data: entropyData.coherence,
                        borderColor: '#4cc9f0',
                        backgroundColor: 'rgba(76, 201, 240, 0.1)',
                        yAxisID: 'y1'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        type: 'linear',
                        display: true,
                        position: 'left',
                        grid: {{ color: 'rgba(255, 255, 255, 0.1)' }},
                        title: {{ display: true, text: 'Temperatura' }}
                    }},
                    y1: {{
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: {{ drawOnChartArea: false }},
                        title: {{ display: true, text: 'Coerência' }}
                    }},
                    x: {{
                        grid: {{ color: 'rgba(255, 255, 255, 0.1)' }}
                    }}
                }}
            }}
        }});
        
        // Gráfico de complexidade
        const complexityCtx = document.getElementById('complexityChart').getContext('2d');
        new Chart(complexityCtx, {{
            type: 'bar',
            data: {{
                labels: entropyData.timestamps.slice(-10), // Últimos 10 pontos
                datasets: [{{
                    label: 'Complexidade',
                    data: entropyData.complexity.slice(-10),
                    backgroundColor: 'rgba(67, 97, 238, 0.6)',
                    borderColor: '#4361ee',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{ color: 'rgba(255, 255, 255, 0.1)' }}
                    }},
                    x: {{
                        grid: {{ color: 'rgba(255, 255, 255, 0.1)' }}
                    }}
                }},
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});
        
        // Preenche análise dimensional
        const dimensionalGrid = document.getElementById('dimensionalGrid');
        const latestDimensional = entropyData.dimensional_analysis[entropyData.dimensional_analysis.length - 1];
        
        for (const [key, value] of Object.entries(latestDimensional)) {{
            const dimItem = document.createElement('div');
            dimItem.className = 'dim-item';
            dimItem.innerHTML = `
                <div style="font-size: 1.5em; color: #00ff41;">${{value.toFixed(3)}}</div>
                <div style="font-size: 0.8em; opacity: 0.8;">${{key.replace('_', ' ').toUpperCase()}}</div>
            `;
            dimensionalGrid.appendChild(dimItem);
        }}
        
        // Atualização automática das estatísticas
        function updateStats() {{
            const latest = entropyData.total_entropy[entropyData.total_entropy.length - 1];
            const temp = entropyData.temperature[entropyData.temperature.length - 1];
            const coh = entropyData.coherence[entropyData.coherence.length - 1];
            const comp = entropyData.complexity[entropyData.complexity.length - 1];
            
            document.getElementById('totalEntropy').textContent = latest.toFixed(3);
            document.getElementById('temperature').textContent = temp.toFixed(3);
            document.getElementById('coherence').textContent = coh.toFixed(3);
            document.getElementById('complexity').textContent = comp.toFixed(3);
        }}
        
        // Efeitos visuais
        function addGlowEffect() {{
            const cards = document.querySelectorAll('.stat-card');
            cards.forEach(card => {{
                card.addEventListener('mouseenter', () => {{
                    card.style.transform = 'scale(1.05)';
                    card.style.boxShadow = '0 0 20px rgba(0, 255, 65, 0.5)';
                    card.style.transition = 'all 0.3s ease';
                }});
                
                card.addEventListener('mouseleave', () => {{
                    card.style.transform = 'scale(1)';
                    card.style.boxShadow = 'none';
                }});
            }});
        }}
        
        // Inicialização
        document.addEventListener('DOMContentLoaded', () => {{
            updateStats();
            addGlowEffect();
            console.log('🌌 AEON Quantum Dashboard carregado com sucesso!');
        }});
    </script>
</body>
</html>"""
        
        # Salva arquivo HTML
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🎨 Dashboard HTML gerado: {filepath}")
        return str(filepath)
    
    def _prepare_data_for_js(self, data: List[EntropySnapshot]) -> str:
        """Prepara dados para uso em JavaScript"""
        timestamps = [s.timestamp for s in data]
        
        js_data = {
            'timestamps': timestamps,
            'total_entropy': [s.total_entropy for s in data],
            'quantum_entropy': [s.quantum_entropy for s in data],
            'classical_entropy': [s.classical_entropy for s in data],
            'entanglement_entropy': [s.entanglement_entropy for s in data],
            'temperature': [s.system_temperature for s in data],
            'coherence': [s.coherence_level for s in data],
            'complexity': [s.complexity_index for s in data],
            'dimensional_analysis': [s.dimensional_analysis for s in data]
        }
        
        return json.dumps(js_data, default=str)
    
    def _generate_empty_dashboard(self) -> str:
        """Gera dashboard vazio quando não há dados"""
        filepath = self.html_output_dir / "aeon_quantum_empty.html"
        
        html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌌 AEON Dashboard - Aguardando Dados</title>
    <style>
        body {
            font-family: 'Consolas', 'Monaco', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        .waiting-container {
            background: rgba(255, 255, 255, 0.05);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(0, 255, 65, 0.3);
            border-top: 3px solid #00ff41;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="waiting-container">
        <div class="spinner"></div>
        <h1>🌌 AEON Quantum Dashboard</h1>
        <p>⏳ Aguardando dados de entropia quântica...</p>
        <p>Execute o analisador para gerar visualizações</p>
    </div>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def create_matplotlib_plots(self, data: List[EntropySnapshot]) -> List[str]:
        """Cria gráficos usando matplotlib (se disponível)"""
        if not MATPLOTLIB_AVAILABLE or not data:
            return []
        
        plt.style.use('dark_background')
        
        # Configura fontes e cores
        plt.rcParams['font.family'] = 'monospace'
        plt.rcParams['figure.facecolor'] = '#0a0a0a'
        plt.rcParams['axes.facecolor'] = '#1a1a1a'
        plt.rcParams['axes.edgecolor'] = '#333333'
        plt.rcParams['grid.color'] = '#333333'
        plt.rcParams['text.color'] = '#ffffff'
        plt.rcParams['axes.labelcolor'] = '#ffffff'
        plt.rcParams['xtick.color'] = '#ffffff'
        plt.rcParams['ytick.color'] = '#ffffff'
        
        plot_files = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Evolução da entropia total
        plt.figure(figsize=(12, 6))
        times = list(range(len(data)))
        entropies = [s.total_entropy for s in data]
        
        plt.plot(times, entropies, color=self.colors['total'], linewidth=2, label='Entropia Total')
        plt.fill_between(times, entropies, alpha=0.3, color=self.colors['total'])
        plt.title('🌌 Evolução da Entropia Total - AEON', fontsize=16, color=self.colors['accent'])
        plt.xlabel('Tempo (passos)')
        plt.ylabel('Entropia')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        file1 = self.html_output_dir / f'entropy_evolution_{timestamp}.png'
        plt.savefig(file1, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
        plot_files.append(str(file1))
        plt.close()
        
        # 2. Componentes de entropia
        plt.figure(figsize=(12, 8))
        quantum = [s.quantum_entropy for s in data]
        classical = [s.classical_entropy for s in data]
        entanglement = [s.entanglement_entropy for s in data]
        
        plt.plot(times, quantum, color=self.colors['quantum'], linewidth=2, label='Quântica')
        plt.plot(times, classical, color=self.colors['classical'], linewidth=2, label='Clássica')
        plt.plot(times, entanglement, color=self.colors['entanglement'], linewidth=2, label='Emaranhamento')
        
        plt.title('🔬 Componentes de Entropia - AEON', fontsize=16, color=self.colors['accent'])
        plt.xlabel('Tempo (passos)')
        plt.ylabel('Entropia')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        file2 = self.html_output_dir / f'entropy_components_{timestamp}.png'
        plt.savefig(file2, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
        plot_files.append(str(file2))
        plt.close()
        
        # 3. Análise de coerência e temperatura
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        temperatures = [s.system_temperature for s in data]
        coherences = [s.coherence_level for s in data]
        
        ax1.plot(times, temperatures, color=self.colors['temperature'], linewidth=2)
        ax1.set_ylabel('Temperatura', color=self.colors['temperature'])
        ax1.tick_params(axis='y', labelcolor=self.colors['temperature'])
        ax1.grid(True, alpha=0.3)
        ax1.set_title('🌡️ Evolução da Temperatura', color=self.colors['accent'])
        
        ax2.plot(times, coherences, color=self.colors['coherence'], linewidth=2)
        ax2.set_ylabel('Coerência', color=self.colors['coherence'])
        ax2.tick_params(axis='y', labelcolor=self.colors['coherence'])
        ax2.set_xlabel('Tempo (passos)')
        ax2.grid(True, alpha=0.3)
        ax2.set_title('✨ Evolução da Coerência', color=self.colors['accent'])
        
        plt.tight_layout()
        file3 = self.html_output_dir / f'temp_coherence_{timestamp}.png'
        plt.savefig(file3, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
        plot_files.append(str(file3))
        plt.close()
        
        # 4. Análise dimensional (se disponível)
        if data[-1].dimensional_analysis:
            dims = data[-1].dimensional_analysis
            labels = list(dims.keys())
            values = list(dims.values())
            
            plt.figure(figsize=(10, 8))
            colors_gradient = plt.cm.plasma(np.linspace(0, 1, len(labels)))
            
            bars = plt.bar(labels, values, color=colors_gradient)
            plt.title('📐 Análise Dimensional - Estado Atual', fontsize=16, color=self.colors['accent'])
            plt.ylabel('Valor Dimensional')
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3, axis='y')
            
            # Adiciona valores nas barras
            for bar, value in zip(bars, values):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{value:.3f}', ha='center', va='bottom', color='white')
            
            plt.tight_layout()
            file4 = self.html_output_dir / f'dimensional_analysis_{timestamp}.png'
            plt.savefig(file4, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
            plot_files.append(str(file4))
            plt.close()
        
        print(f"📊 {len(plot_files)} gráficos matplotlib gerados")
        return plot_files
    
    def create_live_dashboard(self, update_interval: int = 5) -> str:
        """Cria dashboard em tempo real que se atualiza automaticamente"""
        if not self.data_source:
            print("⚠️ Fonte de dados não disponível para dashboard ao vivo")
            return ""
        
        filepath = self.html_output_dir / "aeon_live_dashboard.html"
        
        # HTML com WebSocket ou polling para atualização em tempo real
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌌 AEON Live Quantum Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Consolas', 'Monaco', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .live-indicator {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #00ff41;
            color: #000;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
        }}
        
        .charts-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }}
        
        .chart-box {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .status-bar {{
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
    </style>
</head>
<body>
    <div class="live-indicator">🔴 LIVE</div>
    
    <div class="header">
        <h1>🌌 AEON Live Quantum Dashboard</h1>
        <p>Monitoramento em tempo real da entropia quântica</p>
    </div>
    
    <div class="status-bar">
        <div>📊 Última atualização: <span id="lastUpdate">--</span></div>
        <div>⚡ Status: <span id="status">Inicializando...</span></div>
        <div>🔄 Próxima atualização em: <span id="countdown">{update_interval}</span>s</div>
    </div>
    
    <div class="charts-container">
        <div class="chart-box">
            <h3>📈 Entropia em Tempo Real</h3>
            <canvas id="liveEntropyChart"></canvas>
        </div>
        
        <div class="chart-box">
            <h3>🌡️ Parâmetros do Sistema</h3>
            <canvas id="systemParamsChart"></canvas>
        </div>
    </div>
    
    <script>
        let entropyChart, paramsChart;
        let dataBuffer = [];
        const maxDataPoints = 50;
        
        // Inicializa gráficos
        function initCharts() {{
            const entropyCtx = document.getElementById('liveEntropyChart').getContext('2d');
            entropyChart = new Chart(entropyCtx, {{
                type: 'line',
                data: {{
                    labels: [],
                    datasets: [{{
                        label: 'Entropia Total',
                        data: [],
                        borderColor: '#00ffff',
                        backgroundColor: 'rgba(0, 255, 255, 0.1)',
                        fill: true,
                        tension: 0.4
                    }}]
                }},
                options: {{
                    responsive: true,
                    animation: {{ duration: 0 }},
                    scales: {{
                        y: {{ beginAtZero: false }},
                        x: {{ display: false }}
                    }}
                }}
            }});
            
            const paramsCtx = document.getElementById('systemParamsChart').getContext('2d');
            paramsChart = new Chart(paramsCtx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Quântica', 'Clássica', 'Emaranhamento'],
                    datasets: [{{
                        data: [1, 1, 1],
                        backgroundColor: ['#00ffff', '#ff6b35', '#7209b7']
                    }}]
                }},
                options: {{
                    responsive: true,
                    animation: {{ duration: 500 }}
                }}
            }});
        }}
        
        // Atualiza dados (simulação - em implementação real, viria do servidor)
        function updateData() {{
            const now = new Date();
            const timeStr = now.toLocaleTimeString();
            
            // Simula novos dados
            const newData = {{
                timestamp: timeStr,
                total_entropy: Math.random() * 10 + 5,
                quantum_entropy: Math.random() * 3 + 1,
                classical_entropy: Math.random() * 3 + 1,
                entanglement_entropy: Math.random() * 2 + 0.5,
                temperature: Math.random() * 2 + 1,
                coherence: Math.random() * 0.5 + 0.5
            }};
            
            // Adiciona ao buffer
            dataBuffer.push(newData);
            if (dataBuffer.length > maxDataPoints) {{
                dataBuffer.shift();
            }}
            
            // Atualiza gráfico de entropia
            entropyChart.data.labels = dataBuffer.map(d => d.timestamp);
            entropyChart.data.datasets[0].data = dataBuffer.map(d => d.total_entropy);
            entropyChart.update();
            
            // Atualiza gráfico de parâmetros
            const latest = dataBuffer[dataBuffer.length - 1];
            paramsChart.data.datasets[0].data = [
                latest.quantum_entropy,
                latest.classical_entropy,
                latest.entanglement_entropy
            ];
            paramsChart.update();
            
            // Atualiza status
            document.getElementById('lastUpdate').textContent = timeStr;
            document.getElementById('status').textContent = 'Ativo';
        }}
        
        // Countdown para próxima atualização
        let countdown = {update_interval};
        function updateCountdown() {{
            document.getElementById('countdown').textContent = countdown;
            countdown--;
            if (countdown < 0) {{
                countdown = {update_interval};
                updateData();
            }}
        }}
        
        // Inicialização
        document.addEventListener('DOMContentLoaded', () => {{
            initCharts();
            updateData(); // Primeira atualização
            setInterval(updateCountdown, 1000); // Atualiza countdown a cada segundo
        }});
    </script>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🔴 Dashboard ao vivo criado: {filepath}")
        return str(filepath)
    
    def export_visualization_report(self, data: List[EntropySnapshot]) -> str:
        """Exporta relatório completo de visualização"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.html_output_dir / f"aeon_visualization_report_{timestamp}.json"
        
        # ASCII visualization
        ascii_viz = self.generate_ascii_visualization(data)
        
        # Matplotlib plots (se disponível)
        plot_files = self.create_matplotlib_plots(data) if MATPLOTLIB_AVAILABLE else []
        
        # HTML dashboard
        html_file = self.generate_html_dashboard(data)
        
        # Live dashboard
        live_file = self.create_live_dashboard()
        
        # Compila relatório
        report = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'data_points': len(data),
                'visualization_tools': {
                    'matplotlib_available': MATPLOTLIB_AVAILABLE,
                    'ascii_visualization': True,
                    'html_dashboard': True,
                    'live_dashboard': True
                }
            },
            'generated_files': {
                'html_dashboard': html_file,
                'live_dashboard': live_file,
                'matplotlib_plots': plot_files,
                'output_directory': str(self.html_output_dir)
            },
            'ascii_visualization': ascii_viz,
            'summary': {
                'total_files_generated': 2 + len(plot_files),
                'visualization_types': ['HTML Dashboard', 'Live Dashboard', 'ASCII Plot'] + (['Matplotlib Plots'] if plot_files else [])
            }
        }
        
        # Salva relatório
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📋 Relatório de visualização exportado: {report_file}")
        return str(report_file)

def main():
    """Demonstração do sistema de visualização"""
    print("🎨 AEON Quantum Visualization Dashboard")
    print("=" * 50)
    
    # Inicializa visualizador
    visualizer = AeonQuantumVisualizer()
    
    # Tenta carregar dados do analisador
    if ANALYZER_AVAILABLE:
        print("🔬 Criando dados de teste com analisador quântico...")
        analyzer = QuantumEntropyAnalyzer(dimensions=4, system_size=100)
        
        # Gera algumas snapshots de teste
        snapshots = []
        for i in range(20):
            analyzer.evolve_system(0.1)
            snapshot = analyzer.calculate_system_entropy()
            snapshots.append(snapshot)
            
            if i % 5 == 0:
                print(f"  📊 Snapshot {i+1}: S={snapshot.total_entropy:.3f}")
        
        visualizer.data_source = analyzer
        
    else:
        print("⚠️ Analisador não disponível. Criando dados sintéticos...")
        # Cria dados sintéticos para demonstração
        snapshots = []
        for i in range(20):
            snapshot = type('MockSnapshot', (), {
                'timestamp': (datetime.now() - timedelta(seconds=20-i)).isoformat(),
                'total_entropy': 5 + 2 * math.sin(i * 0.3) + 0.5 * (i / 10),
                'quantum_entropy': 2 + math.sin(i * 0.2),
                'classical_entropy': 1.5 + 0.5 * math.cos(i * 0.4),
                'entanglement_entropy': 0.8 + 0.3 * math.sin(i * 0.5),
                'system_temperature': 1.2 + 0.4 * math.sin(i * 0.25),
                'coherence_level': 0.7 + 0.2 * math.cos(i * 0.15),
                'complexity_index': 2 + 0.8 * math.sin(i * 0.35),
                'evolution_rate': 0.1 * math.sin(i * 0.1),
                'dimensional_analysis': {
                    'fractal_dimension': 1.8 + 0.2 * math.sin(i * 0.2),
                    'entanglement_dimension': 0.6 + 0.1 * math.cos(i * 0.3),
                    'spectral_dimension': 2.1 + 0.15 * math.sin(i * 0.25),
                    'information_dimension': 1.5 + 0.3 * math.cos(i * 0.4)
                }
            })()
            snapshots.append(snapshot)
    
    # Gera visualizações
    print("\n🎨 Gerando visualizações...")
    
    # ASCII
    print("\n📟 Visualização ASCII:")
    ascii_output = visualizer.generate_ascii_visualization(snapshots)
    print(ascii_output)
    
    # HTML Dashboard
    html_file = visualizer.generate_html_dashboard(snapshots)
    print(f"\n🌐 Dashboard HTML: {html_file}")
    
    # Matplotlib plots (se disponível)
    if MATPLOTLIB_AVAILABLE:
        plot_files = visualizer.create_matplotlib_plots(snapshots)
        print(f"\n📊 Gráficos Matplotlib: {len(plot_files)} arquivos")
    
    # Live dashboard
    live_file = visualizer.create_live_dashboard()
    print(f"\n🔴 Dashboard ao vivo: {live_file}")
    
    # Relatório completo
    report_file = visualizer.export_visualization_report(snapshots)
    print(f"\n📋 Relatório completo: {report_file}")
    
    # Tenta abrir dashboard no navegador
    try:
        print(f"\n🌐 Abrindo dashboard no navegador...")
        webbrowser.open(f"file://{Path(html_file).resolve()}")
    except Exception as e:
        print(f"⚠️ Não foi possível abrir navegador: {e}")
        print(f"💡 Abra manualmente: {html_file}")
    
    print("\n✅ Sistema de visualização concluído!")
    print("🎯 Dashboards gerados com sucesso!")

if __name__ == "__main__":
    main()
