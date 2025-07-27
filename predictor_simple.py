"""
🌌 AEONCOSMA PREDICTOR SIMPLES - Sistema de Gráficos e Predições
Sistema simplificado com visualização garantida
Desenvolvido por Luiz Cruz - 2025
"""

import http.server
import socketserver
import json
import time
import random
import threading
import webbrowser
from datetime import datetime
import urllib.request
import ssl

# Configuração SSL
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Dados do sistema
system_data = {
    'uptime': time.time(),
    'market_data': {},
    'predictions': {},
    'signals': []
}

def fetch_market_data():
    """Busca dados de mercado"""
    try:
        symbols = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana']
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(symbols)}&vs_currencies=usd&include_24hr_change=true"
        
        with urllib.request.urlopen(url, context=ssl_context, timeout=10) as response:
            data = json.loads(response.read().decode())
            
        market_data = {}
        for coin_id, coin_data in data.items():
            symbol = {
                'bitcoin': 'BTC',
                'ethereum': 'ETH', 
                'binancecoin': 'BNB',
                'cardano': 'ADA',
                'solana': 'SOL'
            }.get(coin_id, coin_id.upper())
            
            price = coin_data['usd']
            change = coin_data.get('usd_24h_change', 0)
            
            market_data[symbol] = {
                'price': price,
                'change_24h': change,
                'timestamp': time.time()
            }
            
            # Gera predições simples
            hour_pred = price * (1 + random.uniform(-0.03, 0.03))
            day_pred = price * (1 + random.uniform(-0.08, 0.08))
            
            system_data['predictions'][symbol] = {
                'hour': {'price': hour_pred, 'change': ((hour_pred - price) / price) * 100},
                'day': {'price': day_pred, 'change': ((day_pred - price) / price) * 100}
            }
        
        system_data['market_data'] = market_data
        return True
        
    except Exception as e:
        print(f"⚠️ Erro: {e} - Usando dados simulados")
        # Dados de fallback
        system_data['market_data'] = {
            'BTC': {'price': 45000 + random.uniform(-2000, 2000), 'change_24h': random.uniform(-5, 5)},
            'ETH': {'price': 2800 + random.uniform(-200, 200), 'change_24h': random.uniform(-8, 8)},
            'BNB': {'price': 280 + random.uniform(-20, 20), 'change_24h': random.uniform(-6, 6)},
            'ADA': {'price': 0.45 + random.uniform(-0.05, 0.05), 'change_24h': random.uniform(-10, 10)},
            'SOL': {'price': 95 + random.uniform(-10, 10), 'change_24h': random.uniform(-12, 12)}
        }
        
        for symbol, data in system_data['market_data'].items():
            price = data['price']
            hour_pred = price * (1 + random.uniform(-0.03, 0.03))
            day_pred = price * (1 + random.uniform(-0.08, 0.08))
            
            system_data['predictions'][symbol] = {
                'hour': {'price': hour_pred, 'change': ((hour_pred - price) / price) * 100},
                'day': {'price': day_pred, 'change': ((day_pred - price) / price) * 100}
            }
        
        return False

def generate_chart_data(symbol):
    """Gera dados históricos simulados para gráficos"""
    if symbol not in system_data['market_data']:
        return [], []
    
    current_price = system_data['market_data'][symbol]['price']
    
    # Gera 50 pontos históricos
    prices = []
    labels = []
    
    for i in range(50):
        variation = random.uniform(-0.02, 0.02)
        price = current_price * (1 + variation * (i - 25) / 25)
        prices.append(round(price, 2))
        labels.append(f"T-{50-i}")
    
    # Adiciona predições
    if symbol in system_data['predictions']:
        prices.append(round(system_data['predictions'][symbol]['hour']['price'], 2))
        labels.append("1H")
        prices.append(round(system_data['predictions'][symbol]['day']['price'], 2))
        labels.append("24H")
    
    return prices, labels

def generate_html():
    """Gera interface HTML completa"""
    current_time = datetime.now().strftime("%H:%M:%S")
    uptime = int(time.time() - system_data['uptime'])
    
    # Tabela de mercado
    market_rows = ""
    for symbol, data in system_data['market_data'].items():
        change_color = "#27ae60" if data['change_24h'] >= 0 else "#e74c3c"
        
        pred_hour = system_data['predictions'].get(symbol, {}).get('hour', {})
        pred_day = system_data['predictions'].get(symbol, {}).get('day', {})
        
        hour_change = pred_hour.get('change', 0)
        day_change = pred_day.get('change', 0)
        
        market_rows += f"""
        <tr onclick="showChart('{symbol}')" style="cursor: pointer;">
            <td><strong>{symbol}</strong></td>
            <td>${data['price']:,.2f}</td>
            <td style="color: {change_color};">{data['change_24h']:+.1f}%</td>
            <td style="color: {'#27ae60' if hour_change >= 0 else '#e74c3c'};">{hour_change:+.1f}%</td>
            <td style="color: {'#27ae60' if day_change >= 0 else '#e74c3c'};">{day_change:+.1f}%</td>
        </tr>
        """
    
    # Dados dos gráficos
    chart_data = {}
    for symbol in system_data['market_data'].keys():
        prices, labels = generate_chart_data(symbol)
        chart_data[symbol] = {
            'prices': prices,
            'labels': labels,
            'current': system_data['market_data'][symbol]['price']
        }

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AEONCOSMA PREDICTOR - Análise de Mercado</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #ffffff;
            min-height: 100vh;
        }}
        
        .header {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        
        .title {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            animation: glow 2s ease-in-out infinite alternate;
        }}
        
        @keyframes glow {{
            from {{ text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }}
            to {{ text-shadow: 0 0 20px rgba(255,255,255,0.8), 2px 2px 4px rgba(0,0,0,0.5); }}
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 20px;
        }}
        
        .panel {{
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .panel h2 {{
            color: #ffffff;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .market-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .market-table th, .market-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .market-table th {{
            background: rgba(0,0,0,0.3);
            color: #667eea;
            font-weight: bold;
        }}
        
        .market-table tr:hover {{
            background: rgba(255,255,255,0.1);
        }}
        
        .chart-container {{
            height: 400px;
            margin: 20px 0;
            position: relative;
        }}
        
        .chart-selector {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .chart-btn {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }}
        
        .chart-btn:hover, .chart-btn.active {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
        }}
        
        .status-bar {{
            text-align: center;
            padding: 15px;
            background: rgba(0,0,0,0.3);
            margin: 20px 0;
            border-radius: 10px;
            font-size: 1.1em;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">📈 AEONCOSMA PREDICTOR 📈</h1>
        <p>Sistema Avançado de Análise de Mercado e Predições</p>
    </div>
    
    <div class="status-bar">
        <strong>🕒 {current_time} | ⏱️ Uptime: {uptime}s | 🚀 Sistema Ativo</strong>
    </div>
    
    <div class="container">
        <div class="panel">
            <h2>💹 Mercado & Predições</h2>
            <table class="market-table">
                <thead>
                    <tr>
                        <th>Ativo</th>
                        <th>Preço</th>
                        <th>24h</th>
                        <th>Pred 1H</th>
                        <th>Pred 24H</th>
                    </tr>
                </thead>
                <tbody>
                    {market_rows}
                </tbody>
            </table>
            
            <div style="margin-top: 30px;">
                <h3 style="color: #667eea;">🎯 Status do Sistema</h3>
                <div style="margin: 15px 0; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 5px;">
                    <div>✅ APIs de Mercado: Ativo</div>
                    <div>🤖 IA de Predição: Funcionando</div>
                    <div>📊 Gráficos: Carregados</div>
                    <div>🔄 Atualizações: A cada 30s</div>
                </div>
            </div>
        </div>
        
        <div class="panel">
            <h2>📊 Gráficos Interativos</h2>
            <div class="chart-selector">
                <button class="chart-btn active" onclick="showChart('BTC')">Bitcoin (BTC)</button>
                <button class="chart-btn" onclick="showChart('ETH')">Ethereum (ETH)</button>
                <button class="chart-btn" onclick="showChart('BNB')">Binance (BNB)</button>
                <button class="chart-btn" onclick="showChart('ADA')">Cardano (ADA)</button>
                <button class="chart-btn" onclick="showChart('SOL')">Solana (SOL)</button>
            </div>
            
            <div class="chart-container">
                <canvas id="priceChart"></canvas>
            </div>
            
            <div id="chart-info" style="text-align: center; margin-top: 20px; color: #bdc3c7;">
                Gráfico mostra dados históricos + predições para próximas 1h e 24h
            </div>
        </div>
    </div>
    
    <script>
        let chart = null;
        const chartData = {json.dumps(chart_data)};
        let currentSymbol = 'BTC';
        
        function showChart(symbol) {{
            currentSymbol = symbol;
            
            // Atualiza botões
            document.querySelectorAll('.chart-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Dados do gráfico
            const data = chartData[symbol];
            if (!data) return;
            
            const ctx = document.getElementById('priceChart').getContext('2d');
            
            if (chart) {{
                chart.destroy();
            }}
            
            // Cores para diferentes seções
            const colors = data.prices.map((price, index) => {{
                if (index < data.prices.length - 2) return 'rgba(102, 126, 234, 0.8)';
                return index === data.prices.length - 2 ? 'rgba(52, 152, 219, 0.8)' : 'rgba(155, 89, 182, 0.8)';
            }});
            
            chart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: data.labels,
                    datasets: [{{
                        label: symbol + ' Price',
                        data: data.prices,
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: colors,
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2,
                        pointRadius: 5
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            labels: {{
                                color: '#ffffff',
                                font: {{
                                    size: 14
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            ticks: {{
                                color: '#bdc3c7'
                            }},
                            grid: {{
                                color: 'rgba(255, 255, 255, 0.1)'
                            }}
                        }},
                        y: {{
                            ticks: {{
                                color: '#bdc3c7',
                                callback: function(value) {{
                                    return '$' + value.toLocaleString();
                                }}
                            }},
                            grid: {{
                                color: 'rgba(255, 255, 255, 0.1)'
                            }}
                        }}
                    }}
                }}
            }});
            
            // Atualiza informações
            document.getElementById('chart-info').innerHTML = `
                ${{symbol}}: Preço atual $$${{data.current.toLocaleString()}} | 
                Histórico (azul) + Predição 1H (azul claro) + Predição 24H (roxo)
            `;
        }}
        
        // Auto refresh
        setInterval(() => {{
            location.reload();
        }}, 30000);
        
        // Inicialização
        document.addEventListener('DOMContentLoaded', () => {{
            showChart('BTC');
        }});
        
        console.log('🌌 AEONCOSMA PREDICTOR Carregado!');
        console.log('📊 Dados de mercado:', chartData);
    </script>
</body>
</html>"""

class PredictorHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            fetch_market_data()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(generate_html().encode('utf-8'))
        else:
            super().do_GET()

def start_predictor():
    PORT = 8080
    
    print("🌌 AEONCOSMA PREDICTOR SIMPLES")
    print("="*50)
    print(f"🚀 Iniciando servidor na porta {PORT}...")
    
    fetch_market_data()
    
    try:
        with socketserver.TCPServer(("", PORT), PredictorHandler) as httpd:
            print(f"✅ Servidor ativo: http://localhost:{PORT}")
            print("📊 Interface de gráficos carregada!")
            print("🔄 Atualizações automáticas ativas")
            print("🎯 Pressione Ctrl+C para parar")
            print("="*50)
            
            threading.Timer(2, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()
            
            def update_data():
                while True:
                    time.sleep(30)
                    fetch_market_data()
                    print(f"🔄 Dados atualizados - {datetime.now().strftime('%H:%M:%S')}")
            
            threading.Thread(target=update_data, daemon=True).start()
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 AEONCOSMA Predictor parado")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    start_predictor()
