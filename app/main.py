"""
Fractal Trading Dashboard
========================

Interface gráfica interativa para análise fractal de trading.
Integra visualizações em tempo real com análise técnica avançada.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import json
import asyncio
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional

# Configurar matplotlib para não exigir display
import matplotlib
matplotlib.use('Agg')  # Backend sem GUI para fallback

# Importar módulos locais
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from fractal import FractalAnalyzer
    from trading_ai import TradingAI
    from integrated_fractal_sim import IntegratedFractalTrader
    modules_available = True
except ImportError as e:
    print(f"Aviso: Módulos não disponíveis - {e}")
    # Fallback para modo demo
    FractalAnalyzer = None
    TradingAI = None
    IntegratedFractalTrader = None
    modules_available = False

logger = logging.getLogger(__name__)

class FractalDashboard:
    """
    Dashboard principal para análise fractal de trading.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔮 Fractal P2P Trading Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Estilo moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_styles()
        
        # Componentes principais
        if modules_available:
            self.fractal_analyzer = FractalAnalyzer()
            self.trading_ai = TradingAI()
            self.integrated_trader = IntegratedFractalTrader()
        else:
            self.fractal_analyzer = None
            self.trading_ai = None
            self.integrated_trader = None
        
        # Variáveis de estado
        self.current_symbol = tk.StringVar(value="AAPL")
        self.analysis_results = {}
        self.is_analyzing = False
        
        # Interface
        self.setup_ui()
        
        # Dados demo para fallback
        self.demo_mode = not modules_available
        if self.demo_mode:
            self._setup_demo_data()
            
        # Inicializar rede P2P em background
        if modules_available:
            threading.Thread(target=self._init_p2p_network, daemon=True).start()
    
    def _configure_styles(self):
        """Configurar estilos visuais modernos."""
        self.style.configure('Modern.TFrame', background='#2b2b2b')
        self.style.configure('Modern.TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        self.style.configure('Modern.TButton', background='#404040', foreground='white')
        self.style.configure('Title.TLabel', background='#2b2b2b', foreground='#00ff88', font=('Arial', 14, 'bold'))
        self.style.configure('Metric.TLabel', background='#2b2b2b', foreground='#88ff00', font=('Arial', 12, 'bold'))
    
    def setup_ui(self):
        """Configurar interface do usuário."""
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(main_frame, text="🔮 Fractal P2P Trading Dashboard", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Frame superior - controles
        control_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self._setup_controls(control_frame)
        
        # Frame do meio - métricas
        metrics_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        metrics_frame.pack(fill=tk.X, pady=(0, 10))
        
        self._setup_metrics(metrics_frame)
        
        # Frame inferior - gráficos
        charts_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        charts_frame.pack(fill=tk.BOTH, expand=True)
        
        self._setup_charts(charts_frame)
    
    def _setup_controls(self, parent):
        """Configurar controles superiores."""
        # Símbolo
        ttk.Label(parent, text="Símbolo:", style='Modern.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        
        symbol_entry = ttk.Entry(parent, textvariable=self.current_symbol, width=10)
        symbol_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Período
        ttk.Label(parent, text="Período:", style='Modern.TLabel').pack(side=tk.LEFT, padx=(10, 5))
        
        self.period_var = tk.StringVar(value="1y")
        period_combo = ttk.Combobox(parent, textvariable=self.period_var, 
                                   values=["1mo", "3mo", "6mo", "1y", "2y", "5y"], 
                                   width=8, state="readonly")
        period_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botões
        analyze_btn = ttk.Button(parent, text="📊 Analisar", command=self.analyze_symbol)
        analyze_btn.pack(side=tk.LEFT, padx=(10, 5))
        
        save_btn = ttk.Button(parent, text="💾 Salvar", command=self.save_analysis)
        save_btn.pack(side=tk.LEFT, padx=(5, 5))
        
        load_btn = ttk.Button(parent, text="📂 Carregar", command=self.load_analysis)
        load_btn.pack(side=tk.LEFT, padx=(5, 5))
        
        # Status
        self.status_label = ttk.Label(parent, text="Pronto", style='Modern.TLabel')
        self.status_label.pack(side=tk.RIGHT, padx=(10, 0))
    
    def _setup_metrics(self, parent):
        """Configurar painel de métricas."""
        # Frame para métricas
        left_metrics = ttk.Frame(parent, style='Modern.TFrame')
        left_metrics.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_metrics = ttk.Frame(parent, style='Modern.TFrame')
        right_metrics.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Métricas fractais
        ttk.Label(left_metrics, text="Métricas Fractais", style='Title.TLabel').pack(anchor=tk.W)
        
        self.hurst_label = ttk.Label(left_metrics, text="Expoente de Hurst: --", style='Metric.TLabel')
        self.hurst_label.pack(anchor=tk.W, pady=2)
        
        self.dimension_label = ttk.Label(left_metrics, text="Dimensão Fractal: --", style='Metric.TLabel')
        self.dimension_label.pack(anchor=tk.W, pady=2)
        
        self.trend_label = ttk.Label(left_metrics, text="Tipo de Tendência: --", style='Modern.TLabel')
        self.trend_label.pack(anchor=tk.W, pady=2)
        
        self.complexity_label = ttk.Label(left_metrics, text="Complexidade: --", style='Modern.TLabel')
        self.complexity_label.pack(anchor=tk.W, pady=2)
        
        # Sinais de trading
        ttk.Label(right_metrics, text="Sinais de Trading", style='Title.TLabel').pack(anchor=tk.W)
        
        self.signals_text = tk.Text(right_metrics, height=6, width=50, bg='#1e1e1e', fg='white', 
                                   font=('Consolas', 9))
        self.signals_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Scrollbar para sinais
        signals_scroll = ttk.Scrollbar(right_metrics, command=self.signals_text.yview)
        self.signals_text.config(yscrollcommand=signals_scroll.set)
    
    def _setup_charts(self, parent):
        """Configurar área de gráficos."""
        # Notebook para múltiplas abas
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba 1: Preços e Fractais
        self.price_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.price_frame, text="📈 Preços & Fractais")
        
        # Aba 2: Análise Fractal
        self.fractal_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.fractal_frame, text="🔍 Análise Fractal")
        
        # Aba 3: Sinais AI
        self.ai_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.ai_frame, text="🤖 Sinais AI")
        
        # Configurar matplotlib
        plt.style.use('dark_background')
        
        # Gráfico de preços
        self.price_fig = Figure(figsize=(12, 6), facecolor='#2b2b2b')
        self.price_canvas = FigureCanvasTkAgg(self.price_fig, self.price_frame)
        self.price_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Gráfico fractal
        self.fractal_fig = Figure(figsize=(12, 6), facecolor='#2b2b2b')
        self.fractal_canvas = FigureCanvasTkAgg(self.fractal_fig, self.fractal_frame)
        self.fractal_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Gráfico AI
        self.ai_fig = Figure(figsize=(12, 6), facecolor='#2b2b2b')
        self.ai_canvas = FigureCanvasTkAgg(self.ai_fig, self.ai_frame)
        self.ai_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _setup_demo_data(self):
        """Configurar dados demo quando módulos não estão disponíveis."""
        import random
        try:
            import numpy as np
        except ImportError:
            # Fallback sem numpy
            dates = [datetime.now() - timedelta(days=i) for i in range(252, 0, -1)]
            prices = [100 + random.gauss(0, 2) + 0.1 * i for i in range(252)]
        else:
            # Simular dados de preços
            dates = [datetime.now() - timedelta(days=i) for i in range(252, 0, -1)]
            prices = [100 + random.gauss(0, 2) + 0.1 * i for i in range(252)]
        
        self.demo_data = {
            'dates': dates,
            'prices': prices,
            'hurst': 0.65,
            'dimension': 1.45,
            'trend': 'persistent',
            'complexity': 'medium'
        }
    
    def _init_p2p_network(self):
        """Inicializar rede P2P em background."""
        try:
            if self.integrated_trader:
                # Inicializar rede P2P
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(
                    self.integrated_trader.p2p_network.start_network(port=8080)
                )
        except Exception as e:
            print(f"Erro ao inicializar rede P2P: {e}")
    
    def analyze_symbol(self):
        """Analisar símbolo selecionado."""
        if self.is_analyzing:
            return
        
        symbol = self.current_symbol.get().upper()
        period = self.period_var.get()
        
        if not symbol:
            messagebox.showerror("Erro", "Digite um símbolo válido")
            return
        
        # Executar análise em thread separada
        self.is_analyzing = True
        self.status_label.config(text="Analisando...")
        
        thread = threading.Thread(target=self._run_analysis, args=(symbol, period))
        thread.daemon = True
        thread.start()
    
    def _run_analysis(self, symbol: str, period: str):
        """Executar análise em background."""
        try:
            if self.demo_mode:
                self._run_demo_analysis(symbol)
            else:
                self._run_real_analysis(symbol, period)
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Erro na análise: {e}"))
        finally:
            self.is_analyzing = False
            self.root.after(0, lambda: self.status_label.config(text="Pronto"))
    
    def _run_demo_analysis(self, symbol: str):
        """Executar análise demo."""
        # Simular delay
        import time
        time.sleep(2)
        
        # Atualizar UI no thread principal
        self.root.after(0, lambda: self._update_demo_display(symbol))
    
    def _run_real_analysis(self, symbol: str, period: str):
        """Executar análise real usando sistema integrado."""
        if self.integrated_trader:
            # Usar análise integrada
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(
                self.integrated_trader.analyze_and_trade(symbol, period)
            )
            
            # Extrair dados para display
            data = None
            signals = []
            
            if 'fractal_analysis' in results:
                # Simular dados de mercado para display
                dates = [datetime.now() - timedelta(days=i) for i in range(252, 0, -1)]
                prices = [100 + i * 0.1 for i in range(252)]  # Dados simulados
                
                data = {
                    'dates': dates,
                    'prices': prices
                }
                
                # Extrair sinais
                if 'trading_recommendation' in results:
                    rec = results['trading_recommendation']
                    signals = [{
                        'type': rec['signal'],
                        'confidence': rec['confidence'],
                        'reason': rec['reason']
                    }]
        else:
            # Fallback para análise simples
            results = {
                'symbol': symbol,
                'fractals': {
                    'hurst_exponent': 0.65,
                    'box_dimension': 1.45,
                    'trend_type': 'persistent',
                    'complexity': 'medium'
                }
            }
            data = None
            signals = []
        
        # Atualizar UI no thread principal
        self.root.after(0, lambda: self._update_display(results, signals, data))
    
    def _update_demo_display(self, symbol: str):
        """Atualizar display com dados demo."""
        # Atualizar métricas
        self.hurst_label.config(text=f"Expoente de Hurst: {self.demo_data['hurst']:.3f}")
        self.dimension_label.config(text=f"Dimensão Fractal: {self.demo_data['dimension']:.3f}")
        self.trend_label.config(text=f"Tipo de Tendência: {self.demo_data['trend']}")
        self.complexity_label.config(text=f"Complexidade: {self.demo_data['complexity']}")
        
        # Atualizar sinais
        demo_signals = [
            "🟢 BUY - Fractal de baixa detectado (Confiança: 85%)",
            "📊 INFO - Tendência persistente identificada",
            "⚠️ WATCH - Volatilidade aumentando"
        ]
        
        self.signals_text.delete(1.0, tk.END)
        self.signals_text.insert(tk.END, "\n".join(demo_signals))
        
        # Atualizar gráficos
        self._plot_demo_charts(symbol)
    
    def _update_display(self, results: Dict, signals: List, data):
        """Atualizar display com resultados reais."""
        self.analysis_results = results
        
        # Atualizar métricas
        hurst = results['fractals']['hurst_exponent']
        dimension = results['fractals']['box_dimension']
        trend = results['fractals']['trend_type']
        complexity = results['fractals']['complexity']
        
        self.hurst_label.config(text=f"Expoente de Hurst: {hurst:.3f}")
        self.dimension_label.config(text=f"Dimensão Fractal: {dimension:.3f}")
        self.trend_label.config(text=f"Tipo de Tendência: {trend}")
        self.complexity_label.config(text=f"Complexidade: {complexity}")
        
        # Atualizar sinais
        self.signals_text.delete(1.0, tk.END)
        for signal in signals[-10:]:  # Últimos 10 sinais
            icon = "🟢" if signal['type'] == 'buy' else "🔴"
            confidence_pct = signal['confidence'] * 100
            text = f"{icon} {signal['type'].upper()} - {signal['reason']} (Confiança: {confidence_pct:.0f}%)\n"
            self.signals_text.insert(tk.END, text)
        
        # Atualizar gráficos
        self._plot_real_charts(data, results)
    
    def _plot_demo_charts(self, symbol: str):
        """Plotar gráficos demo."""
        import numpy as np
        
        # Gráfico de preços
        self.price_fig.clear()
        ax1 = self.price_fig.add_subplot(111)
        
        dates = self.demo_data['dates']
        prices = self.demo_data['prices']
        
        ax1.plot(dates, prices, color='#00ff88', linewidth=1.5, label=f'{symbol} Preço')
        ax1.set_title(f'{symbol} - Análise de Preços (DEMO)', color='white', fontsize=14)
        ax1.set_ylabel('Preço ($)', color='white')
        ax1.tick_params(colors='white')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Adicionar fractais simulados
        fractal_indices = np.random.choice(len(prices), 20, replace=False)
        for i in fractal_indices:
            if i % 2 == 0:  # Fractal de alta
                ax1.scatter(dates[i], prices[i], color='red', marker='v', s=50, zorder=5)
            else:  # Fractal de baixa
                ax1.scatter(dates[i], prices[i], color='lime', marker='^', s=50, zorder=5)
        
        self.price_canvas.draw()
        
        # Gráfico fractal
        self._plot_demo_fractal_analysis()
    
    def _plot_demo_fractal_analysis(self):
        """Plotar análise fractal demo."""
        import numpy as np
        
        self.fractal_fig.clear()
        
        # Subplot 1: Box Counting
        ax1 = self.fractal_fig.add_subplot(221)
        box_sizes = np.logspace(0.5, 2, 20)
        box_counts = box_sizes ** (-1.45)  # Simular dimensão fractal
        
        ax1.loglog(box_sizes, box_counts, 'o-', color='#00ff88', markersize=4)
        ax1.set_xlabel('Tamanho da Caixa', color='white')
        ax1.set_ylabel('Número de Caixas', color='white')
        ax1.set_title('Box Counting (Demo)', color='white')
        ax1.tick_params(colors='white')
        ax1.grid(True, alpha=0.3)
        
        # Subplot 2: R/S Analysis
        ax2 = self.fractal_fig.add_subplot(222)
        lags = np.logspace(0.5, 2, 20)
        rs_values = lags ** 0.65  # Simular Hurst
        
        ax2.loglog(lags, rs_values, 's-', color='#ff8800', markersize=4)
        ax2.set_xlabel('Lag', color='white')
        ax2.set_ylabel('R/S', color='white')
        ax2.set_title('Análise R/S (Demo)', color='white')
        ax2.tick_params(colors='white')
        ax2.grid(True, alpha=0.3)
        
        # Subplot 3: Distribuição de Returns
        ax3 = self.fractal_fig.add_subplot(223)
        returns = np.random.normal(0, 0.02, 252)
        
        ax3.hist(returns, bins=30, alpha=0.7, color='#8800ff', edgecolor='white')
        ax3.set_xlabel('Returns', color='white')
        ax3.set_ylabel('Frequência', color='white')
        ax3.set_title('Distribuição de Returns (Demo)', color='white')
        ax3.tick_params(colors='white')
        ax3.grid(True, alpha=0.3)
        
        # Subplot 4: Correlação de Longo Prazo
        ax4 = self.fractal_fig.add_subplot(224)
        lags = range(1, 51)
        correlations = [0.65 ** lag for lag in lags]  # Decay baseado em Hurst
        
        ax4.plot(lags, correlations, color='#ff0088', linewidth=2)
        ax4.set_xlabel('Lag', color='white')
        ax4.set_ylabel('Correlação', color='white')
        ax4.set_title('Correlação de Longo Prazo (Demo)', color='white')
        ax4.tick_params(colors='white')
        ax4.grid(True, alpha=0.3)
        
        self.fractal_fig.tight_layout()
        self.fractal_canvas.draw()
    
    def _plot_real_charts(self, data, results: Dict):
        """Plotar gráficos com dados reais."""
        # Implementar quando dados reais estiverem disponíveis
        self._plot_demo_charts(self.current_symbol.get())
    
    def _show_error(self, message: str):
        """Mostrar erro na UI."""
        messagebox.showerror("Erro", message)
        self.status_label.config(text="Erro")
    
    def save_analysis(self):
        """Salvar análise atual."""
        if not self.analysis_results and not self.demo_mode:
            messagebox.showwarning("Aviso", "Nenhuma análise para salvar")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if self.demo_mode:
                    # Salvar dados demo
                    demo_analysis = {
                        'symbol': self.current_symbol.get(),
                        'timestamp': datetime.now().isoformat(),
                        'fractals': {
                            'hurst_exponent': self.demo_data['hurst'],
                            'box_dimension': self.demo_data['dimension'],
                            'trend_type': self.demo_data['trend'],
                            'complexity': self.demo_data['complexity']
                        },
                        'demo_mode': True
                    }
                    
                    with open(filename, 'w') as f:
                        json.dump(demo_analysis, f, indent=2)
                else:
                    # Salvar análise real
                    self.fractal_analyzer.save_analysis(filename)
                
                messagebox.showinfo("Sucesso", f"Análise salva em {filename}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    
    def load_analysis(self):
        """Carregar análise de arquivo."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    analysis = json.load(f)
                
                # Atualizar display com dados carregados
                if analysis.get('demo_mode', False):
                    self.current_symbol.set(analysis.get('symbol', 'DEMO'))
                    self._update_demo_display(analysis.get('symbol', 'DEMO'))
                else:
                    if self.fractal_analyzer:
                        self.fractal_analyzer.load_analysis(filename)
                        self.analysis_results = analysis
                        self._update_display(analysis, [], None)
                
                messagebox.showinfo("Sucesso", f"Análise carregada de {filename}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar: {e}")
    
    def run(self):
        """Iniciar dashboard."""
        # Carregar análise demo inicial
        if self.demo_mode:
            self.root.after(1000, lambda: self._update_demo_display("DEMO"))
        
        self.root.mainloop()


def main():
    """Função principal."""
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        dashboard = FractalDashboard()
        dashboard.run()
    except Exception as e:
        print(f"Erro ao iniciar dashboard: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
