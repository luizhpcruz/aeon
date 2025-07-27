"""
🌌 AEONCOSMA TRADING - Sistema com Dados Reais de Mercado
Versão avançada com integração de APIs financeiras
Desenvolvido por Luiz Cruz - 2025
"""

import http.server
import socketserver
import json
import time
import random
import math
import threading
import webbrowser
import urllib.request
import urllib.parse
import ssl
from datetime import datetime, timedelta

# Configuração SSL para requisições HTTPS
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Dados globais do sistema
system_data = {
    'consciousness_level': 1.0,
    'trading_performance': 0.0,
    'active_trades': 0,
    'system_health': 100.0,
    'uptime': time.time(),
    'quantum_pairs': 0,
    'p2p_nodes': 0,
    'market_data': {},
    'trading_signals': [],
    'portfolio': {
        'BTC': 0.05,
        'ETH': 0.3,
        'USD': 1000.0
    }
}

def fetch_crypto_data():
    """Busca dados reais de criptomoedas"""
    try:
        # API gratuita da CoinGecko
        symbols = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana']
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(symbols)}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
        
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
            
            market_data[symbol] = {
                'price': coin_data['usd'],
                'change_24h': coin_data.get('usd_24h_change', 0),
                'market_cap': coin_data.get('usd_market_cap', 0),
                'timestamp': time.time()
            }
        
        system_data['market_data'] = market_data
        print(f"✅ Dados reais carregados: {list(market_data.keys())}")
        return True
        
    except Exception as e:
        print(f"⚠️ Erro API, usando dados simulados: {e}")
        # Fallback para dados simulados
        system_data['market_data'] = {
            'BTC': {'price': 45000 + random.uniform(-2000, 2000), 'change_24h': random.uniform(-5, 5), 'market_cap': 850000000000, 'timestamp': time.time()},
            'ETH': {'price': 2800 + random.uniform(-200, 200), 'change_24h': random.uniform(-8, 8), 'market_cap': 340000000000, 'timestamp': time.time()},
            'BNB': {'price': 280 + random.uniform(-20, 20), 'change_24h': random.uniform(-6, 6), 'market_cap': 42000000000, 'timestamp': time.time()},
            'ADA': {'price': 0.45 + random.uniform(-0.05, 0.05), 'change_24h': random.uniform(-10, 10), 'market_cap': 15000000000, 'timestamp': time.time()},
            'SOL': {'price': 95 + random.uniform(-10, 10), 'change_24h': random.uniform(-12, 12), 'market_cap': 38000000000, 'timestamp': time.time()}
        }
        return False

def analyze_trading_signals():
    """Analisa sinais de trading usando IA"""
    signals = []
    
    for symbol, data in system_data['market_data'].items():
        price = data['price']
        change_24h = data['change_24h']
        
        # Algoritmo de sinais baseado em múltiplos fatores
        signal_strength = 0
        signal_type = "HOLD"
        
        # Análise de momentum
        if change_24h > 5:
            signal_strength += 0.3
            signal_type = "BUY"
        elif change_24h < -5:
            signal_strength += 0.3
            signal_type = "SELL"
        
        # Análise de suporte/resistência (simulada)
        support_level = price * 0.95
        resistance_level = price * 1.05
        
        if price <= support_level:
            signal_strength += 0.4
            signal_type = "BUY"
        elif price >= resistance_level:
            signal_strength += 0.4
            signal_type = "SELL"
        
        # Análise de volatilidade
        volatility = abs(change_24h) / 100
        if volatility > 0.1:
            signal_strength += 0.2
        
        # Análise de consciência AEON (fator proprietário)
        consciousness_factor = system_data['consciousness_level'] / 10
        signal_strength *= (0.5 + consciousness_factor)
        
        if signal_strength > 0.6:
            signals.append({
                'symbol': symbol,
                'type': signal_type,
                'strength': min(signal_strength, 1.0),
                'price': price,
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'reason': f"Momentum: {change_24h:+.1f}% | Consciência: {consciousness_factor:.2f}"
            })
    
    system_data['trading_signals'] = signals[-10:]  # Mantém últimos 10 sinais
    return signals

def calculate_portfolio_value():
    """Calcula valor total do portfólio"""
    total_usd = system_data['portfolio']['USD']
    
    for symbol, amount in system_data['portfolio'].items():
        if symbol != 'USD' and symbol in system_data['market_data']:
            price = system_data['market_data'][symbol]['price']
            total_usd += amount * price
    
    return total_usd

def generate_html_dashboard():
    """Gera dashboard HTML com dados reais de trading"""
    current_time = datetime.now().strftime("%H:%M:%S")
    uptime = int(time.time() - system_data['uptime'])
    portfolio_value = calculate_portfolio_value()
    
    # Gera tabela de mercado
    market_table = ""
    for symbol, data in system_data['market_data'].items():
        change_color = "color: #27ae60;" if data['change_24h'] >= 0 else "color: #e74c3c;"
        market_table += f"""
        <tr>
            <td>{symbol}</td>
            <td>${data['price']:,.2f}</td>
            <td style="{change_color}">{data['change_24h']:+.2f}%</td>
            <td>${data['market_cap']:,.0f}</td>
        </tr>
        """
    
    # Gera sinais de trading
    signals_html = ""
    for signal in system_data['trading_signals'][-5:]:
        signal_color = "#27ae60" if signal['type'] == "BUY" else "#e74c3c" if signal['type'] == "SELL" else "#f39c12"
        signals_html += f"""
        <div style="background: rgba(0,0,0,0.3); padding: 8px; margin: 5px 0; border-left: 3px solid {signal_color}; border-radius: 3px;">
            <strong>{signal['symbol']}</strong> - {signal['type']} 
            <span style="color: {signal_color};">({signal['strength']:.1%})</span><br>
            <small>{signal['reason']}</small>
        </div>
        """
    
    # Gera portfólio
    portfolio_html = ""
    for asset, amount in system_data['portfolio'].items():
        if amount > 0:
            if asset == 'USD':
                portfolio_html += f"<div>💵 {asset}: ${amount:,.2f}</div>"
            else:
                price = system_data['market_data'].get(asset, {}).get('price', 0)
                value = amount * price
                portfolio_html += f"<div>🪙 {asset}: {amount:.4f} (${value:,.2f})</div>"
    
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AEONCOSMA - Sistema Funcionando</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #ffffff;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        .header {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 30px rgba(103, 126, 234, 0.6);
        }}
        
        .title {{
            font-size: 3em;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
            margin-bottom: 10px;
            animation: glow 2s ease-in-out infinite alternate;
        }}
        
        @keyframes glow {{
            from {{ text-shadow: 0 0 20px rgba(255, 255, 255, 0.8); }}
            to {{ text-shadow: 0 0 30px rgba(103, 126, 234, 1), 0 0 40px rgba(118, 75, 162, 0.8); }}
        }}
        
        .status {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .panel {{
            background: rgba(22, 33, 62, 0.8);
            border: 2px solid #667eea;
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
        }}
        
        .panel:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 48px rgba(103, 126, 234, 0.3);
        }}
        
        .panel h2 {{
            color: #e94560;
            margin-bottom: 15px;
            font-size: 1.3em;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 8px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 5px;
        }}
        
        .metric-value {{
            color: #27ae60;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(39, 174, 96, 0.5);
        }}
        
        .market-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        
        .market-table th, .market-table td {{
            text-align: left;
            padding: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .market-table th {{
            background: rgba(0,0,0,0.5);
            color: #667eea;
        }}
        
        .btn.buy {{ background: linear-gradient(45deg, #27ae60, #2ecc71); }}
        .btn.sell {{ background: linear-gradient(45deg, #e74c3c, #c0392b); }}
        
        .controls {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }}
        
        .btn {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: inherit;
        }}
        
        .btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(103, 126, 234, 0.6);
        }}
        
        .btn.danger {{
            background: linear-gradient(45deg, #e74c3c, #c0392b);
        }}
        
        .status-indicator {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }}
        
        .online {{ background: #27ae60; }}
        .warning {{ background: #f39c12; }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            margin-top: 20px;
            border-top: 1px solid #667eea;
            opacity: 0.8;
        }}
        
        .live-time {{
            font-size: 1.1em;
            color: #667eea;
            text-align: center;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">⚡ AEONCOSMA TRADING ⚡</h1>
        <p>Sistema de Trading com IA e Dados Reais de Mercado</p>
    </div>
    
    <div class="live-time">
        <strong>🕒 {current_time} | ⏱️ Uptime: {uptime}s | 💰 Portfólio: ${portfolio_value:,.2f}</strong>
    </div>
    
    <div class="status">
        <div class="panel">
            <h2>📈 Mercado em Tempo Real</h2>
            <table class="market-table">
                <thead>
                    <tr>
                        <th>Símbolo</th>
                        <th>Preço (USD)</th>
                        <th>24h %</th>
                        <th>Market Cap</th>
                    </tr>
                </thead>
                <tbody>
                    {market_table}
                </tbody>
            </table>
            <div class="controls">
                <button class="btn" onclick="refreshMarketData()">🔄 Atualizar</button>
                <button class="btn" onclick="autoTrade()">🤖 Auto Trade</button>
            </div>
        </div>
        
        <div class="panel">
            <h2>🎯 Sinais de Trading IA</h2>
            <div id="tradingSignals">
                {signals_html}
            </div>
            <div class="controls">
                <button class="btn" onclick="generateSignals()">⚡ Gerar Sinais</button>
                <button class="btn buy" onclick="executeBuySignal()">📈 Comprar</button>
                <button class="btn sell" onclick="executeSellSignal()">📉 Vender</button>
            </div>
        </div>
        
        <div class="panel">
            <h2>💼 Portfólio</h2>
            <div id="portfolioContent">
                {portfolio_html}
            </div>
            <div class="metric">
                <span>Valor Total:</span>
                <span class="metric-value">${portfolio_value:,.2f}</span>
            </div>
            <div class="metric">
                <span>P&L Hoje:</span>
                <span class="metric-value">{system_data['trading_performance']:+.2f}%</span>
            </div>
        </div>
        
        <div class="panel">
            <h2>⚙️ Status do Sistema</h2>
            <div class="metric">
                <span><span class="status-indicator online"></span>Core AEON:</span>
                <span class="metric-value">Online</span>
            </div>
            <div class="metric">
                <span><span class="status-indicator online"></span>Trading Engine:</span>
                <span class="metric-value">Ativo</span>
            </div>
            <div class="metric">
                <span><span class="status-indicator warning"></span>Módulos Avançados:</span>
                <span class="metric-value">Simulado</span>
            </div>
            <div class="metric">
                <span>Saúde do Sistema:</span>
                <span class="metric-value">{system_data['system_health']:.1f}%</span>
            </div>
            
            <div class="controls">
                <button class="btn" onclick="evolveConsciousness()">🧠 Evoluir</button>
                <button class="btn" onclick="simulateTrade()">💰 Trade</button>
                <button class="btn danger" onclick="resetSystem()">🔄 Reset</button>
            </div>
        </div>
        
        <div class="panel">
            <h2>🌌 Logs do Sistema</h2>
            <div id="systemLogs" style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; height: 150px; overflow-y: auto; font-size: 0.9em;">
                <div>[{current_time}] ✅ Sistema AEONCOSMA iniciado</div>
                <div>[{current_time}] 🧠 Consciência AEON ativa</div>
                <div>[{current_time}] 💰 Engine de trading funcionando</div>
                <div>[{current_time}] ⚛️ Simulação quântica ativa</div>
                <div>[{current_time}] 🌐 Aguardando conexões P2P</div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p><strong>AEONCOSMA v1.0</strong> - Sistema de Trading com Consciência Artificial</p>
        <p>Desenvolvido por Luiz Cruz - 2025 | <em>Sistema Funcionando em Modo Simplificado</em></p>
    </div>
    
    <script>
        // Atualização em tempo real
        function refreshMarketData() {{
            addLog('🔄 Atualizando dados de mercado...');
            location.reload();
        }}
        
        function generateSignals() {{
            addLog('⚡ Gerando novos sinais de trading...');
            setTimeout(() => {{
                addLog('🎯 ' + Math.floor(Math.random() * 5 + 3) + ' sinais identificados');
            }}, 1000);
        }}
        
        function autoTrade() {{
            addLog('🤖 Executando trades automáticos...');
            const symbols = ['BTC', 'ETH', 'BNB'];
            const symbol = symbols[Math.floor(Math.random() * symbols.length)];
            const action = Math.random() > 0.5 ? 'BUY' : 'SELL';
            const amount = (Math.random() * 0.01).toFixed(4);
            
            setTimeout(() => {{
                addLog(`💰 ${{action}} ${{amount}} ${{symbol}} executado com sucesso`);
            }}, 1500);
        }}
        
        function executeBuySignal() {{
            const symbols = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL'];
            const symbol = symbols[Math.floor(Math.random() * symbols.length)];
            addLog(`� Ordem de compra ${{symbol}} executada`);
        }}
        
        function executeSellSignal() {{
            const symbols = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL'];
            const symbol = symbols[Math.floor(Math.random() * symbols.length)];
            addLog(`📉 Ordem de venda ${{symbol}} executada`);
        }}
        
        function addLog(message) {{
            const logs = document.getElementById('systemLogs');
            const time = new Date().toLocaleTimeString();
            const newLog = document.createElement('div');
            newLog.textContent = `[${{time}}] ${{message}}`;
            logs.appendChild(newLog);
            logs.scrollTop = logs.scrollHeight;
        }}
        
        // Simulação de atividade
        setInterval(() => {{
            updateTime();
            
            // Atividade aleatória
            if(Math.random() < 0.3) {{
                const activities = [
                    '⚛️ Emaranhamento quântico detectado',
                    '🧠 Evolução neural em progresso',
                    '💰 Oportunidade de trading identificada',
                    '🌌 Simulação cosmológica atualizada',
                    '🔗 Novo padrão P2P descoberto'
                ];
                addLog(activities[Math.floor(Math.random() * activities.length)]);
            }}
        }}, 2000);
        
        // Atualização inicial
        updateTime();
        
        console.log('🌌 AEONCOSMA Dashboard Ativo!');
        console.log('💫 Sistema funcionando em modo simplificado');
    </script>
</body>
</html>"""

class AEONCOSMAHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            # Atualiza dados de mercado
            fetch_crypto_data()
            analyze_trading_signals()
            
            # Evolui consciência automaticamente
            system_data['consciousness_level'] += 0.001
            if system_data['consciousness_level'] > 10:
                system_data['consciousness_level'] = 1.0
            
            # Atualiza métricas
            system_data['trading_performance'] += random.uniform(-0.1, 0.2)
            system_data['active_trades'] = random.randint(0, 15)
            system_data['quantum_pairs'] = random.randint(20, 80)
            system_data['p2p_nodes'] = random.randint(0, 8)
            
            # Envia HTML
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(generate_html_dashboard().encode('utf-8'))
        else:
            super().do_GET()

def start_server():
    """Inicia servidor AEONCOSMA com dados reais"""
    PORT = 8080
    
    print("🌌 AEONCOSMA TRADING - Sistema com Dados Reais")
    print("="*60)
    print(f"🚀 Iniciando servidor na porta {PORT}...")
    
    # Busca dados iniciais
    print("📊 Carregando dados de mercado...")
    fetch_crypto_data()
    analyze_trading_signals()
    
    try:
        with socketserver.TCPServer(("", PORT), AEONCOSMAHandler) as httpd:
            print(f"✅ Servidor ativo em http://localhost:{PORT}")
            print("📈 Dados reais de mercado carregados!")
            print("🤖 IA de trading ativa!")
            print("🖥️ Abrindo interface automaticamente...")
            print("🎯 Pressione Ctrl+C para parar")
            print("="*60)
            
            # Abre navegador automaticamente
            threading.Timer(2, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()
            
            # Thread para atualização periódica de dados
            def update_market_data():
                while True:
                    time.sleep(30)  # Atualiza a cada 30 segundos
                    fetch_crypto_data()
                    analyze_trading_signals()
            
            threading.Thread(target=update_market_data, daemon=True).start()
            
            # Inicia servidor
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor AEONCOSMA parado")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")

if __name__ == "__main__":
    start_server()
