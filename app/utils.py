"""
Fractal Trading Utilities
=========================

Funções utilitárias para geração, normalização e visualização
de séries temporais fractais para análise de trading.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Tuple, Optional, Union
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def generate_fractal_series(length: int = 3000, hurst: float = 0.7, seed: Optional[int] = None) -> np.ndarray:
    """
    Gera uma série temporal fractal com Hurst exponent (persistência)
    usando o método de caminhadas aleatórias fracionárias.
    
    Args:
        length: Comprimento da série temporal
        hurst: Expoente de Hurst (0.5 = random walk, >0.5 = persistente, <0.5 = anti-persistente)
        seed: Seed para reprodutibilidade
        
    Returns:
        Array numpy com série temporal fractal
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Gerar ruído gaussiano
    g = np.random.normal(0, 1, length)
    f = np.zeros(length)
    
    # Processo fracionário
    for i in range(1, length):
        if i == 1:
            f[i] = f[i - 1] + g[i]
        else:
            # Incorporar memória fractal baseada no expoente de Hurst
            memory_term = hurst * (f[i - 1] - f[i - 2])
            f[i] = f[i - 1] + g[i] + memory_term
    
    return f

def generate_realistic_price_series(
    length: int = 1000, 
    initial_price: float = 100.0,
    volatility: float = 0.02,
    trend: float = 0.0001,
    hurst: float = 0.6,
    seasonal_component: bool = True
) -> np.ndarray:
    """
    Gera série de preços realista combinando tendência, volatilidade e características fractais.
    
    Args:
        length: Número de pontos
        initial_price: Preço inicial
        volatility: Volatilidade diária
        trend: Tendência de crescimento por período
        hurst: Expoente de Hurst para persistência
        seasonal_component: Se incluir componente sazonal
        
    Returns:
        Array com série de preços
    """
    # Componente fractal
    fractal_component = generate_fractal_series(length, hurst) * volatility
    
    # Tendência
    trend_component = np.linspace(0, trend * length, length)
    
    # Componente sazonal (opcional)
    seasonal_component_array = np.zeros(length)
    if seasonal_component:
        # Ciclo de aproximadamente 250 dias (ano de trading)
        for i in range(length):
            seasonal_component_array[i] = 0.01 * np.sin(2 * np.pi * i / 250)
    
    # Combinar componentes
    log_returns = fractal_component + trend_component + seasonal_component_array
    
    # Converter para preços usando log-returns
    prices = np.zeros(length)
    prices[0] = initial_price
    
    for i in range(1, length):
        prices[i] = prices[i-1] * np.exp(log_returns[i])
    
    return prices

def normalize(series: Union[List, np.ndarray], method: str = "minmax") -> np.ndarray:
    """
    Normaliza uma série temporal.
    
    Args:
        series: Série temporal para normalizar
        method: Método de normalização ("minmax", "zscore", "robust")
        
    Returns:
        Série normalizada
    """
    series = np.array(series)
    
    if method == "minmax":
        min_val = np.min(series)
        max_val = np.max(series)
        if max_val == min_val:
            return np.zeros_like(series)
        return (series - min_val) / (max_val - min_val)
    
    elif method == "zscore":
        mean_val = np.mean(series)
        std_val = np.std(series)
        if std_val == 0:
            return np.zeros_like(series)
        return (series - mean_val) / std_val
    
    elif method == "robust":
        median_val = np.median(series)
        mad = np.median(np.abs(series - median_val))  # Median Absolute Deviation
        if mad == 0:
            return np.zeros_like(series)
        return (series - median_val) / mad
    
    else:
        raise ValueError(f"Método de normalização desconhecido: {method}")

def plot_series(
    original: np.ndarray, 
    predicted: Optional[np.ndarray] = None,
    title: str = "Fractal Series",
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6),
    style: str = 'dark_background'
) -> None:
    """
    Plota série temporal original e predições.
    
    Args:
        original: Série original
        predicted: Série predita (opcional)
        title: Título do gráfico
        save_path: Caminho para salvar figura (opcional)
        figsize: Tamanho da figura
        style: Estilo do matplotlib
    """
    try:
        plt.style.use(style)
        fig, ax = plt.subplots(figsize=figsize, facecolor='#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        # Plot série original
        ax.plot(original, label="Original", color='#00ff88', linewidth=1.5, alpha=0.8)
        
        # Plot predições se fornecidas
        if predicted is not None:
            offset = len(original)
            x_pred = range(offset, offset + len(predicted))
            ax.plot(x_pred, predicted, label="Predicted", color='#ff8800', 
                   linestyle='--', linewidth=2, alpha=0.9)
            
            # Conectar última observação com primeira predição
            ax.plot([offset-1, offset], [original[-1], predicted[0]], 
                   color='#ff8800', linestyle='--', linewidth=2, alpha=0.9)
        
        ax.set_title(title, color='white', fontsize=14, fontweight='bold')
        ax.set_xlabel('Tempo', color='white')
        ax.set_ylabel('Valor', color='white')
        ax.legend(facecolor='#404040', edgecolor='white')
        ax.grid(True, alpha=0.3)
        ax.tick_params(colors='white')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, facecolor='#2b2b2b', edgecolor='none', dpi=300)
            logger.info(f"Gráfico salvo em: {save_path}")
        
        plt.show()
        
    except Exception as e:
        logger.error(f"Erro ao plotar série: {e}")

def plot_comparative_analysis(
    data_dict: dict,
    title: str = "Análise Comparativa de Séries",
    save_path: Optional[str] = None
) -> None:
    """
    Plota múltiplas séries para comparação.
    
    Args:
        data_dict: Dicionário com {nome: série}
        title: Título do gráfico
        save_path: Caminho para salvar
    """
    try:
        plt.style.use('dark_background')
        fig, axes = plt.subplots(len(data_dict), 1, figsize=(12, 3*len(data_dict)), 
                                facecolor='#2b2b2b')
        if len(data_dict) == 1:
            axes = [axes]
        
        colors = ['#00ff88', '#ff8800', '#8800ff', '#ff0088', '#00ffff']
        
        for i, (name, series) in enumerate(data_dict.items()):
            ax = axes[i]
            ax.set_facecolor('#2b2b2b')
            
            color = colors[i % len(colors)]
            ax.plot(series, label=name, color=color, linewidth=1.5)
            ax.set_title(name, color='white', fontweight='bold')
            ax.set_ylabel('Valor', color='white')
            ax.grid(True, alpha=0.3)
            ax.tick_params(colors='white')
        
        axes[-1].set_xlabel('Tempo', color='white')
        fig.suptitle(title, color='white', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, facecolor='#2b2b2b', edgecolor='none', dpi=300)
        
        plt.show()
        
    except Exception as e:
        logger.error(f"Erro na análise comparativa: {e}")

def calculate_fractal_metrics(series: np.ndarray) -> dict:
    """
    Calcula métricas fractais para uma série temporal.
    
    Args:
        series: Série temporal
        
    Returns:
        Dicionário com métricas fractais
    """
    try:
        # Volatilidade
        returns = np.diff(series) / series[:-1]
        volatility = np.std(returns)
        
        # Tendência (slope da regressão linear)
        x = np.arange(len(series))
        trend = np.polyfit(x, series, 1)[0]
        
        # Auto-correlação
        autocorr = np.corrcoef(series[:-1], series[1:])[0, 1] if len(series) > 1 else 0
        
        # Range/Média (medida de dispersão)
        range_mean_ratio = (np.max(series) - np.min(series)) / np.mean(series) if np.mean(series) != 0 else 0
        
        # Distribuição de retornos
        if len(returns) > 0:
            skewness = np.mean(((returns - np.mean(returns)) / np.std(returns)) ** 3) if np.std(returns) > 0 else 0
            kurtosis = np.mean(((returns - np.mean(returns)) / np.std(returns)) ** 4) if np.std(returns) > 0 else 0
        else:
            skewness = 0
            kurtosis = 0
        
        return {
            "volatility": volatility,
            "trend": trend,
            "autocorrelation": autocorr,
            "range_mean_ratio": range_mean_ratio,
            "skewness": skewness,
            "kurtosis": kurtosis,
            "mean": np.mean(series),
            "std": np.std(series),
            "min": np.min(series),
            "max": np.max(series)
        }
        
    except Exception as e:
        logger.error(f"Erro no cálculo de métricas fractais: {e}")
        return {}

def create_market_data_frame(
    prices: np.ndarray,
    start_date: Optional[datetime] = None,
    freq: str = "D"
) -> pd.DataFrame:
    """
    Criar DataFrame de dados de mercado a partir de série de preços.
    
    Args:
        prices: Array de preços
        start_date: Data inicial (padrão: hoje)
        freq: Frequência ("D" = diário, "H" = horário)
        
    Returns:
        DataFrame com dados OHLCV simulados
    """
    if start_date is None:
        start_date = datetime.now() - timedelta(days=len(prices))
    
    # Criar índice temporal
    if freq == "D":
        dates = pd.date_range(start=start_date, periods=len(prices), freq="D")
    elif freq == "H":
        dates = pd.date_range(start=start_date, periods=len(prices), freq="H")
    else:
        dates = pd.date_range(start=start_date, periods=len(prices), freq=freq)
    
    # Simular dados OHLCV baseados nos preços de fechamento
    data = []
    for i, close_price in enumerate(prices):
        # Simular variação intraday
        daily_volatility = 0.02  # 2% de volatilidade intraday
        high = close_price * (1 + np.random.uniform(0, daily_volatility))
        low = close_price * (1 - np.random.uniform(0, daily_volatility))
        
        if i == 0:
            open_price = close_price
        else:
            # Open próximo ao close anterior com gap pequeno
            gap = np.random.normal(0, 0.005)  # 0.5% gap médio
            open_price = prices[i-1] * (1 + gap)
        
        # Volume simulado (correlacionado com volatilidade)
        base_volume = 1000000
        volume_multiplier = 1 + abs(np.random.normal(0, 0.5))
        volume = int(base_volume * volume_multiplier)
        
        data.append({
            "Open": open_price,
            "High": max(open_price, high, close_price),
            "Low": min(open_price, low, close_price),
            "Close": close_price,
            "Volume": volume
        })
    
    df = pd.DataFrame(data, index=dates)
    
    # Adicionar colunas calculadas
    df['Returns'] = df['Close'].pct_change()
    df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Volatility'] = df['Returns'].rolling(window=20).std()
    
    return df

def generate_test_scenarios() -> dict:
    """
    Gerar cenários de teste para análise fractal.
    
    Returns:
        Dicionário com diferentes cenários de séries temporais
    """
    scenarios = {}
    
    # Cenário 1: Série persistente (trending)
    scenarios["Persistente (H=0.8)"] = generate_fractal_series(
        length=500, hurst=0.8, seed=42
    )
    
    # Cenário 2: Série anti-persistente (mean-reverting)
    scenarios["Anti-persistente (H=0.3)"] = generate_fractal_series(
        length=500, hurst=0.3, seed=43
    )
    
    # Cenário 3: Random walk
    scenarios["Random Walk (H=0.5)"] = generate_fractal_series(
        length=500, hurst=0.5, seed=44
    )
    
    # Cenário 4: Preços realistas de ação em alta
    scenarios["Ação em Alta"] = generate_realistic_price_series(
        length=500, initial_price=100, volatility=0.025, trend=0.0008
    )
    
    # Cenário 5: Preços realistas de ação em baixa
    scenarios["Ação em Baixa"] = generate_realistic_price_series(
        length=500, initial_price=100, volatility=0.03, trend=-0.0005
    )
    
    # Cenário 6: Mercado lateral com volatilidade
    scenarios["Mercado Lateral"] = generate_realistic_price_series(
        length=500, initial_price=100, volatility=0.02, trend=0.0001
    )
    
    return scenarios

# Funções de análise estatística

def hurst_exponent_rs(series: np.ndarray) -> float:
    """
    Calcular expoente de Hurst usando método R/S.
    
    Args:
        series: Série temporal
        
    Returns:
        Expoente de Hurst estimado
    """
    try:
        n = len(series)
        if n < 10:
            return 0.5
        
        # Calcular log returns
        log_returns = np.diff(np.log(series))
        
        # Diferentes tamanhos de janela
        window_sizes = np.unique(np.logspace(1, np.log10(n//4), 15).astype(int))
        rs_values = []
        
        for window_size in window_sizes:
            if window_size >= n:
                continue
            
            # Dividir em janelas
            n_windows = n // window_size
            rs_window = []
            
            for i in range(n_windows):
                start = i * window_size
                end = start + window_size
                window = log_returns[start:end]
                
                if len(window) < 2:
                    continue
                
                # Calcular R/S para esta janela
                mean_return = np.mean(window)
                cumulative_devs = np.cumsum(window - mean_return)
                
                R = np.max(cumulative_devs) - np.min(cumulative_devs)
                S = np.std(window)
                
                if S > 0:
                    rs_window.append(R / S)
            
            if rs_window:
                rs_values.append(np.mean(rs_window))
        
        if len(rs_values) < 2:
            return 0.5
        
        # Regressão linear em escala log-log
        log_window_sizes = np.log(window_sizes[:len(rs_values)])
        log_rs_values = np.log(rs_values)
        
        hurst = np.polyfit(log_window_sizes, log_rs_values, 1)[0]
        
        return max(0.0, min(1.0, hurst))
        
    except Exception as e:
        logger.error(f"Erro no cálculo do expoente de Hurst: {e}")
        return 0.5

# Instâncias utilitárias globais

def get_demo_data(scenario: str = "Ação em Alta") -> pd.DataFrame:
    """Obter dados de demonstração formatados."""
    scenarios = generate_test_scenarios()
    
    if scenario not in scenarios:
        scenario = "Ação em Alta"
    
    prices = scenarios[scenario]
    return create_market_data_frame(prices)

# Configuração de logging para utils
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
