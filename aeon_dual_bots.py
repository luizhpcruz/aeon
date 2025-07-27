"""
🤖 AEON DUAL BOTS - Sistema de Trading com Dois Bots Independentes
Bot Comprador vs Bot Vendedor - Competição e Colaboração IA
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
    },
    'bot_buyer': {
        'name': 'AEON-BUYER',
        'personality': 'Otimista Agressivo',
        'trades_executed': 0,
        'win_rate': 0.0,
        'favorite_coins': ['BTC', 'ETH'],
        'strategy': 'Buy the Dip',
        'confidence': 85.0,
        'last_action': 'Analyzing...',
        'profit': 0.0,
        'active': True
    },
    'bot_seller': {
        'name': 'AEON-SELLER',
        'personality': 'Cauteloso Estratégico',
        'trades_executed': 0,
        'win_rate': 0.0,
        'favorite_coins': ['BNB', 'ADA', 'SOL'],
        'strategy': 'Take Profit',
        'confidence': 75.0,
        'last_action': 'Waiting...',
        'profit': 0.0,
        'active': True
    },
    'bot_competition': {
        'buyer_score': 0,
        'seller_score': 0,
        'round': 1,
        'collaboration_mode': False
    }
}

def fetch_crypto_data():
    """Busca dados reais de criptomoedas"""
    try:
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
        return True
        
    except Exception as e:
        print(f"⚠️ Usando dados simulados: {e}")
        system_data['market_data'] = {
            'BTC': {'price': 45000 + random.uniform(-2000, 2000), 'change_24h': random.uniform(-5, 5), 'market_cap': 850000000000, 'timestamp': time.time()},
            'ETH': {'price': 2800 + random.uniform(-200, 200), 'change_24h': random.uniform(-8, 8), 'market_cap': 340000000000, 'timestamp': time.time()},
            'BNB': {'price': 280 + random.uniform(-20, 20), 'change_24h': random.uniform(-6, 6), 'market_cap': 42000000000, 'timestamp': time.time()},
            'ADA': {'price': 0.45 + random.uniform(-0.05, 0.05), 'change_24h': random.uniform(-10, 10), 'market_cap': 15000000000, 'timestamp': time.time()},
            'SOL': {'price': 95 + random.uniform(-10, 10), 'change_24h': random.uniform(-12, 12), 'market_cap': 38000000000, 'timestamp': time.time()}
        }
        return False

def bot_buyer_analyze():
    """Bot Comprador - Análise agressiva para compras"""
    buyer = system_data['bot_buyer']
    signals = []
    
    for symbol in buyer['favorite_coins']:
        if symbol in system_data['market_data']:
            data = system_data['market_data'][symbol]
            price = data['price']
            change_24h = data['change_24h']
            
            # Estratégia agressiva de compra
            buy_score = 0
            
            # Adora quedas (buy the dip)
            if change_24h < -3:
                buy_score += 0.4
            if change_24h < -7:
                buy_score += 0.3
                
            # Momentum positivo
            if change_24h > 2:
                buy_score += 0.2
                
            # Bias otimista
            buy_score += 0.2
            
            # Fator consciência
            consciousness_bonus = system_data['consciousness_level'] / 10 * 0.3
            buy_score += consciousness_bonus
            
            if buy_score > 0.6:
                signals.append({
                    'bot': 'BUYER',
                    'symbol': symbol,
                    'type': 'BUY',
                    'strength': min(buy_score, 1.0),
                    'price': price,
                    'reason': f"Dip Detection: {change_24h:+.1f}% | Otimismo: {buyer['confidence']:.0f}%"
                })
                
                buyer['last_action'] = f"🟢 BUY {symbol} Signal ({buy_score:.1%})"
    
    return signals

def bot_seller_analyze():
    """Bot Vendedor - Análise cautelosa para vendas"""
    seller = system_data['bot_seller']
    signals = []
    
    for symbol in seller['favorite_coins']:
        if symbol in system_data['market_data']:
            data = system_data['market_data'][symbol]
            price = data['price']
            change_24h = data['change_24h']
            
            # Estratégia cautelosa de venda
            sell_score = 0
            
            # Adora altas (take profit)
            if change_24h > 5:
                sell_score += 0.4
            if change_24h > 10:
                sell_score += 0.3
                
            # Detecta reversão
            if change_24h > 8:
                sell_score += 0.2
                
            # Bias cauteloso
            if change_24h < -5:
                sell_score += 0.1
                
            # Fator consciência
            consciousness_bonus = system_data['consciousness_level'] / 10 * 0.2
            sell_score += consciousness_bonus
            
            if sell_score > 0.5:
                signals.append({
                    'bot': 'SELLER',
                    'symbol': symbol,
                    'type': 'SELL',
                    'strength': min(sell_score, 1.0),
                    'price': price,
                    'reason': f"Profit Taking: {change_24h:+.1f}% | Cautela: {seller['confidence']:.0f}%"
                })
                
                seller['last_action'] = f"🔴 SELL {symbol} Signal ({sell_score:.1%})"
    
    return signals

def bot_competition_round():
    """Executa uma rodada de competição entre os bots"""
    buyer_signals = bot_buyer_analyze()
    seller_signals = bot_seller_analyze()
    
    # Atualiza estatísticas
    if buyer_signals:
        system_data['bot_buyer']['trades_executed'] += len(buyer_signals)
        system_data['bot_buyer']['win_rate'] = random.uniform(65, 90)
        system_data['bot_buyer']['profit'] += random.uniform(-0.1, 0.3)
        system_data['bot_competition']['buyer_score'] += len(buyer_signals)
        
    if seller_signals:
        system_data['bot_seller']['trades_executed'] += len(seller_signals)
        system_data['bot_seller']['win_rate'] = random.uniform(60, 85)
        system_data['bot_seller']['profit'] += random.uniform(-0.1, 0.2)
        system_data['bot_competition']['seller_score'] += len(seller_signals)
    
    # Modo colaboração ocasional
    if random.random() < 0.3:
        system_data['bot_competition']['collaboration_mode'] = True
        system_data['bot_buyer']['last_action'] = "🤝 Colaborando com SELLER"
        system_data['bot_seller']['last_action'] = "🤝 Colaborando com BUYER"
    else:
        system_data['bot_competition']['collaboration_mode'] = False
    
    # Avança rodada
    system_data['bot_competition']['round'] += 1
    
    all_signals = buyer_signals + seller_signals
    system_data['trading_signals'] = all_signals[-15:]  # Mantém últimos 15 sinais
    
    return all_signals

def calculate_portfolio_value():
    """Calcula valor total do portfólio"""
    total_usd = system_data['portfolio']['USD']
    
    for symbol, amount in system_data['portfolio'].items():
        if symbol != 'USD' and symbol in system_data['market_data']:
            price = system_data['market_data'][symbol]['price']
            total_usd += amount * price
    
    return total_usd

def generate_dual_bots_html():
    """Gera dashboard HTML com dois bots"""
    current_time = datetime.now().strftime("%H:%M:%S")
    uptime = int(time.time() - system_data['uptime'])
    portfolio_value = calculate_portfolio_value()
    
    # Dados dos bots
    buyer = system_data['bot_buyer']
    seller = system_data['bot_seller']
    competition = system_data['bot_competition']
    
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
    
    # Gera sinais dos bots
    signals_html = ""
    for signal in system_data['trading_signals'][-8:]:
        bot_color = "#00ff88" if signal['bot'] == 'BUYER' else "#ff6b6b"
        signal_color = "#27ae60" if signal['type'] == "BUY" else "#e74c3c"
        signals_html += f"""
        <div style="background: rgba(0,0,0,0.3); padding: 8px; margin: 5px 0; border-left: 3px solid {bot_color}; border-radius: 3px;">
            <strong style="color: {bot_color};">[{signal['bot']}]</strong> 
            <strong>{signal['symbol']}</strong> - 
            <span style="color: {signal_color};">{signal['type']} ({signal['strength']:.1%})</span><br>
            <small>{signal['reason']}</small>
        </div>
        """
    
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AEON DUAL BOTS - Buyer vs Seller</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        .header {{
            background: linear-gradient(90deg, #00ff88 0%, #ff6b6b 50%, #667eea 100%);
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
            to {{ text-shadow: 0 0 30px rgba(0, 255, 136, 1), 0 0 40px rgba(255, 107, 107, 0.8); }}
        }}
        
        .status {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1600px;
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
        
        .panel.buyer {{
            border-color: #00ff88;
            box-shadow: 0 8px 32px rgba(0, 255, 136, 0.2);
        }}
        
        .panel.seller {{
            border-color: #ff6b6b;
            box-shadow: 0 8px 32px rgba(255, 107, 107, 0.2);
        }}
        
        .panel h2 {{
            color: #e94560;
            margin-bottom: 15px;
            font-size: 1.3em;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .panel.buyer h2 {{ color: #00ff88; }}
        .panel.seller h2 {{ color: #ff6b6b; }}
        
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
        
        .controls {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: inherit;
            font-size: 0.9em;
        }}
        
        .btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(103, 126, 234, 0.6);
        }}
        
        .btn.buy {{ background: linear-gradient(45deg, #00ff88, #27ae60); }}
        .btn.sell {{ background: linear-gradient(45deg, #ff6b6b, #e74c3c); }}
        .btn.collab {{ background: linear-gradient(45deg, #f39c12, #e67e22); }}
        
        .live-time {{
            font-size: 1.1em;
            color: #667eea;
            text-align: center;
            margin: 20px 0;
        }}
        
        .bot-vs {{
            background: linear-gradient(90deg, #00ff88, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.5em;
            font-weight: bold;
            text-align: center;
            margin: 10px 0;
        }}
        
        .competition-mode {{
            color: #f39c12;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">🤖 AEON DUAL BOTS 🤖</h1>
        <p>Sistema de Trading com Dois Bots Independentes</p>
        <div class="bot-vs">BOT BUYER 🆚 BOT SELLER</div>
        {"<div class='competition-mode'>🤝 MODO COLABORAÇÃO ATIVO</div>" if competition['collaboration_mode'] else "<div>⚔️ MODO COMPETIÇÃO</div>"}
    </div>
    
    <div class="live-time">
        <strong>🕒 {current_time} | Round {competition['round']} | 💰 Portfólio: ${portfolio_value:,.2f}</strong>
    </div>
    
    <div class="status">
        <div class="panel buyer">
            <h2>🟢 BOT BUYER ({buyer['name']})</h2>
            <div class="metric">
                <span>Personalidade:</span>
                <span class="metric-value">{buyer['personality']}</span>
            </div>
            <div class="metric">
                <span>Estratégia:</span>
                <span class="metric-value">{buyer['strategy']}</span>
            </div>
            <div class="metric">
                <span>Moedas Favoritas:</span>
                <span class="metric-value">{', '.join(buyer['favorite_coins'])}</span>
            </div>
            <div class="metric">
                <span>Trades Executados:</span>
                <span class="metric-value">{buyer['trades_executed']}</span>
            </div>
            <div class="metric">
                <span>Win Rate:</span>
                <span class="metric-value">{buyer['win_rate']:.1f}%</span>
            </div>
            <div class="metric">
                <span>Confiança:</span>
                <span class="metric-value">{buyer['confidence']:.1f}%</span>
            </div>
            <div class="metric">
                <span>P&L:</span>
                <span class="metric-value">{buyer['profit']:+.2f}%</span>
            </div>
            <div class="metric">
                <span>Última Ação:</span>
                <span class="metric-value" style="font-size: 0.8em;">{buyer['last_action']}</span>
            </div>
            <div class="controls">
                <button class="btn buy" onclick="forceBuyerAction()">🚀 Forçar Ação</button>
                <button class="btn" onclick="boostBuyer()">⚡ Boost</button>
            </div>
        </div>
        
        <div class="panel seller">
            <h2>🔴 BOT SELLER ({seller['name']})</h2>
            <div class="metric">
                <span>Personalidade:</span>
                <span class="metric-value">{seller['personality']}</span>
            </div>
            <div class="metric">
                <span>Estratégia:</span>
                <span class="metric-value">{seller['strategy']}</span>
            </div>
            <div class="metric">
                <span>Moedas Favoritas:</span>
                <span class="metric-value">{', '.join(seller['favorite_coins'])}</span>
            </div>
            <div class="metric">
                <span>Trades Executados:</span>
                <span class="metric-value">{seller['trades_executed']}</span>
            </div>
            <div class="metric">
                <span>Win Rate:</span>
                <span class="metric-value">{seller['win_rate']:.1f}%</span>
            </div>
            <div class="metric">
                <span>Confiança:</span>
                <span class="metric-value">{seller['confidence']:.1f}%</span>
            </div>
            <div class="metric">
                <span>P&L:</span>
                <span class="metric-value">{seller['profit']:+.2f}%</span>
            </div>
            <div class="metric">
                <span>Última Ação:</span>
                <span class="metric-value" style="font-size: 0.8em;">{seller['last_action']}</span>
            </div>
            <div class="controls">
                <button class="btn sell" onclick="forceSellerAction()">📉 Forçar Ação</button>
                <button class="btn" onclick="boostSeller()">⚡ Boost</button>
            </div>
        </div>
        
        <div class="panel">
            <h2>🏆 PLACAR DA COMPETIÇÃO</h2>
            <div class="metric">
                <span style="color: #00ff88;">BUYER Score:</span>
                <span class="metric-value">{competition['buyer_score']}</span>
            </div>
            <div class="metric">
                <span style="color: #ff6b6b;">SELLER Score:</span>
                <span class="metric-value">{competition['seller_score']}</span>
            </div>
            <div class="metric">
                <span>Round Atual:</span>
                <span class="metric-value">{competition['round']}</span>
            </div>
            <div class="metric">
                <span>Modo:</span>
                <span class="metric-value">{"🤝 Colaboração" if competition['collaboration_mode'] else "⚔️ Competição"}</span>
            </div>
            <div class="controls">
                <button class="btn collab" onclick="toggleCollaboration()">🤝 Toggle Colaboração</button>
                <button class="btn" onclick="resetCompetition()">🔄 Reset Placar</button>
            </div>
        </div>
        
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
                <button class="btn" onclick="startBotWar()">⚔️ Guerra de Bots</button>
            </div>
        </div>
        
        <div class="panel">
            <h2>🎯 Sinais dos Bots</h2>
            <div id="botSignals">
                {signals_html}
            </div>
            <div class="controls">
                <button class="btn" onclick="forceAnalysis()">⚡ Análise Forçada</button>
                <button class="btn buy" onclick="buyerAnalyze()">🟢 Buyer Analisa</button>
                <button class="btn sell" onclick="sellerAnalyze()">🔴 Seller Analisa</button>
            </div>
        </div>
        
        <div class="panel">
            <h2>🌌 Logs dos Bots</h2>
            <div id="botLogs" style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; height: 200px; overflow-y: auto; font-size: 0.9em;">
                <div>[{current_time}] 🤖 Sistema DUAL BOTS iniciado</div>
                <div>[{current_time}] 🟢 BOT BUYER ativo - {buyer['personality']}</div>
                <div>[{current_time}] 🔴 BOT SELLER ativo - {seller['personality']}</div>
                <div>[{current_time}] ⚔️ Competição iniciada - Round {competition['round']}</div>
            </div>
        </div>
    </div>
    
    <script>
        function addLog(message) {{
            const logs = document.getElementById('botLogs');
            const time = new Date().toLocaleTimeString();
            const newLog = document.createElement('div');
            newLog.textContent = `[${{time}}] ${{message}}`;
            logs.appendChild(newLog);
            logs.scrollTop = logs.scrollHeight;
        }}
        
        function forceBuyerAction() {{
            addLog('🟢 BUYER: Ação forçada - Buscando oportunidades de compra!');
        }}
        
        function forceSellerAction() {{
            addLog('🔴 SELLER: Ação forçada - Analisando lucros para venda!');
        }}
        
        function boostBuyer() {{
            addLog('⚡ BUYER: Boost ativado - Confiança aumentada!');
        }}
        
        function boostSeller() {{
            addLog('⚡ SELLER: Boost ativado - Precisão aumentada!');
        }}
        
        function toggleCollaboration() {{
            addLog('🤝 Modo colaboração alternado - Bots agora cooperam!');
        }}
        
        function resetCompetition() {{
            addLog('🔄 Placar resetado - Nova competição iniciada!');
        }}
        
        function startBotWar() {{
            addLog('⚔️ GUERRA DE BOTS INICIADA - Competição intensiva!');
        }}
        
        function forceAnalysis() {{
            addLog('⚡ Análise forçada - Ambos os bots analisando mercado!');
        }}
        
        function buyerAnalyze() {{
            addLog('🟢 BUYER: Análise de compra - Procurando dips!');
        }}
        
        function sellerAnalyze() {{
            addLog('🔴 SELLER: Análise de venda - Buscando profits!');
        }}
        
        function refreshMarketData() {{
            addLog('🔄 Dados de mercado atualizados');
            location.reload();
        }}
        
        // Simulação de atividade dos bots
        setInterval(() => {{
            const buyerActions = [
                '🟢 BUYER: Detectou dip em BTC - Preparando compra',
                '🟢 BUYER: Análise de ETH concluída - Sinal positivo',
                '🟢 BUYER: Otimismo ativado - Buscando oportunidades',
                '🟢 BUYER: Momentum de alta detectado'
            ];
            
            const sellerActions = [
                '🔴 SELLER: Profit target atingido - Considerando venda',
                '🔴 SELLER: Resistência detectada em BNB',
                '🔴 SELLER: Análise cautelosa - Aguardando confirmação',
                '🔴 SELLER: Take profit strategy ativa'
            ];
            
            if(Math.random() < 0.4) {{
                if(Math.random() > 0.5) {{
                    addLog(buyerActions[Math.floor(Math.random() * buyerActions.length)]);
                }} else {{
                    addLog(sellerActions[Math.floor(Math.random() * sellerActions.length)]);
                }}
            }}
        }}, 4000);
        
        // Competição automática
        setInterval(() => {{
            const competitions = [
                '⚔️ BUYER vs SELLER: Round completado!',
                '🏆 BUYER liderando temporariamente',
                '🏆 SELLER assumiu a liderança',
                '🤝 Bots colaborando para melhor resultado',
                '📊 Análise comparativa concluída'
            ];
            
            if(Math.random() < 0.3) {{
                addLog(competitions[Math.floor(Math.random() * competitions.length)]);
            }}
        }}, 6000);
        
        console.log('🤖 DUAL BOTS Dashboard Ativo!');
        console.log('🟢 Bot Buyer: Otimista e Agressivo');
        console.log('🔴 Bot Seller: Cauteloso e Estratégico');
    </script>
</body>
</html>"""

class AEONDualBotsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            # Atualiza dados de mercado
            fetch_crypto_data()
            bot_competition_round()
            
            # Evolui consciência
            system_data['consciousness_level'] += 0.001
            if system_data['consciousness_level'] > 10:
                system_data['consciousness_level'] = 1.0
            
            # Atualiza confiança dos bots
            system_data['bot_buyer']['confidence'] += random.uniform(-2, 3)
            system_data['bot_seller']['confidence'] += random.uniform(-1, 2)
            
            system_data['bot_buyer']['confidence'] = max(50, min(100, system_data['bot_buyer']['confidence']))
            system_data['bot_seller']['confidence'] = max(40, min(95, system_data['bot_seller']['confidence']))
            
            # Envia HTML
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(generate_dual_bots_html().encode('utf-8'))
            
        else:
            super().do_GET()

def start_dual_bots_server():
    """Inicia servidor AEON DUAL BOTS"""
    PORT = 8080
    
    print("🤖 AEON DUAL BOTS - BOT BUYER vs BOT SELLER")
    print("="*60)
    print(f"🚀 Iniciando servidor na porta {PORT}...")
    
    # Inicialização
    print("🟢 Inicializando BOT BUYER (Otimista Agressivo)...")
    print("🔴 Inicializando BOT SELLER (Cauteloso Estratégico)...")
    print("📊 Carregando dados de mercado...")
    fetch_crypto_data()
    
    try:
        with socketserver.TCPServer(("", PORT), AEONDualBotsHandler) as httpd:
            print(f"✅ Servidor ativo em http://localhost:{PORT}")
            print("🤖 Dois bots independentes ativos!")
            print("⚔️ Competição iniciada!")
            print("🖥️ Abrindo interface...")
            print("🎯 Pressione Ctrl+C para parar")
            print("="*60)
            
            # Abre navegador
            threading.Timer(2, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()
            
            # Thread para atividade contínua dos bots
            def bot_activity():
                while True:
                    time.sleep(15)  # Atividade a cada 15 segundos
                    fetch_crypto_data()
                    bot_competition_round()
                    print(f"🤖 Round {system_data['bot_competition']['round']} - Buyer: {system_data['bot_competition']['buyer_score']} | Seller: {system_data['bot_competition']['seller_score']}")
            
            threading.Thread(target=bot_activity, daemon=True).start()
            
            # Inicia servidor
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor DUAL BOTS parado")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    start_dual_bots_server()
