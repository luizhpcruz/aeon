#!/usr/bin/env python3
"""
🚀 IA P2P TRADER - LAUNCHER PRINCIPAL
===================================

Sistema Proprietário de Trading Desenvolvido por Luiz
Ativo Digital Pronto para Monetização

Este é o ponto de entrada principal para todo o sistema.
Execute este arquivo para iniciar sua rede P2P de trading.
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

# Informações do sistema
__version__ = "1.0.0"
__author__ = "Luiz"
__copyright__ = "Copyright 2025, Luiz - Todos os direitos reservados"

def print_banner():
    """Exibir banner do sistema."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                🔮 FRACTAL P2P TRADER 🔮                     ║
    ║                                                              ║
    ║        Sistema Avançado de Trading com Análise Fractal      ║
    ║              + Inteligência Artificial + P2P                ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Verificar se as dependências estão instaladas."""
    print("🔍 Verificando dependências...")
    
    required_packages = [
        'numpy', 'pandas', 'matplotlib', 'scikit-learn', 
        'fastapi', 'uvicorn', 'yfinance'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (não encontrado)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Dependências não encontradas: {', '.join(missing_packages)}")
        print("💡 Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def install_dependencies():
    """Instalar dependências automaticamente."""
    print("📦 Instalando dependências...")
    
    requirements_path = Path("requirements.txt")
    if not requirements_path.exists():
        # Criar requirements.txt básico se não existir
        basic_requirements = """
numpy>=1.24.0
pandas>=2.1.0
matplotlib>=3.7.0
scikit-learn>=1.3.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
yfinance>=0.2.20
websockets>=12.0
asyncio
"""
        with open("requirements.txt", "w") as f:
            f.write(basic_requirements.strip())
        print("📝 Arquivo requirements.txt criado")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso!")
            return True
        else:
            print(f"❌ Erro na instalação: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def run_demo_mode():
    """Executar modo demo com dados simulados."""
    print("🎮 Iniciando modo DEMO...")
    
    demo_script = """
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from utils import generate_fractal_series, plot_series, generate_test_scenarios
    from utils import calculate_fractal_metrics, hurst_exponent_rs
    
    print("🔮 Demonstração de Análise Fractal")
    print("=" * 50)
    
    # Gerar cenários de teste
    scenarios = generate_test_scenarios()
    
    for name, series in scenarios.items():
        print(f"\\n📊 Analisando: {name}")
        
        # Calcular métricas
        metrics = calculate_fractal_metrics(series)
        hurst = hurst_exponent_rs(series)
        
        print(f"  • Expoente de Hurst: {hurst:.3f}")
        print(f"  • Volatilidade: {metrics.get('volatility', 0):.4f}")
        print(f"  • Tendência: {metrics.get('trend', 0):.6f}")
        print(f"  • Auto-correlação: {metrics.get('autocorrelation', 0):.3f}")
        
        # Interpretação
        if hurst > 0.6:
            interpretation = "Série PERSISTENTE - tendência forte"
        elif hurst < 0.4:
            interpretation = "Série ANTI-PERSISTENTE - reversões prováveis"
        else:
            interpretation = "Série ALEATÓRIA - movimento browniano"
        
        print(f"  • Interpretação: {interpretation}")
    
    print("\\n✅ Demonstração concluída!")
    print("💡 Para análise real, use: python start.py --mode real")
    
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("💡 Execute: python start.py --install")

"""
    
    exec(demo_script)

def run_backend():
    """Executar backend FastAPI."""
    print("🚀 Iniciando backend FastAPI...")
    
    backend_path = Path("backend/main.py")
    if backend_path.exists():
        os.chdir("backend")
        subprocess.run([sys.executable, "main.py"])
    else:
        print("❌ Backend não encontrado em backend/main.py")

def run_frontend():
    """Executar frontend React."""
    print("🌐 Iniciando frontend React...")
    
    frontend_path = Path("frontend")
    if frontend_path.exists():
        os.chdir("frontend")
        
        # Verificar se node_modules existe
        if not Path("node_modules").exists():
            print("📦 Instalando dependências do frontend...")
            subprocess.run(["npm", "install"])
        
        subprocess.run(["npm", "start"])
    else:
        print("❌ Frontend não encontrado em frontend/")

def run_dashboard():
    """Executar dashboard Python/Tkinter."""
    print("🖥️  Iniciando dashboard Tkinter...")
    
    dashboard_path = Path("app/main.py")
    if dashboard_path.exists():
        subprocess.run([sys.executable, "app/main.py"])
    else:
        print("❌ Dashboard não encontrado em app/main.py")

def run_p2p_network():
    """Executar rede P2P."""
    print("🌐 Iniciando rede P2P...")
    
    def start_simple_node(port):
        """Iniciar nó P2P simples."""
        node_script = f"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'p2p'))

try:
    from simple_p2p_node import SimpleP2PNode
    
    print(f"🔗 Iniciando nó P2P simples na porta {port}")
    node = SimpleP2PNode(host='localhost', port={port})
    
    if node.start_server():
        print(f"✅ Nó ativo em localhost:{port}")
        
        # Tentar conectar com outros nós
        for other_port in [5000, 5001, 5002]:
            if other_port != {port}:
                try:
                    node.add_peer_manual('localhost', other_port)
                except:
                    pass
        
        # Manter nó ativo
        import time
        while node.running:
            time.sleep(1)
    else:
        print(f"❌ Erro ao iniciar nó na porta {port}")
        
except ImportError as e:
    print(f"❌ Erro ao importar módulos P2P: {{e}}")
except Exception as e:
    print(f"❌ Erro no nó P2P: {{e}}")
"""
        
        exec(node_script)
    
    def start_fractal_trader(port):
        """Iniciar trader fractal com P2P."""
        trader_script = f"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'p2p'))

try:
    from fractal_p2p_demo import FractalP2PTrader
    import time
    
    print(f"🤖 Iniciando Fractal P2P Trader na porta {port}")
    trader = FractalP2PTrader(host='localhost', port={port})
    
    if trader.start():
        print(f"✅ Trader ativo em localhost:{port}")
        
        # Conectar com outros traders
        peers = []
        for other_port in [5000, 5001, 5002]:
            if other_port != {port}:
                peers.append(f"localhost:{{other_port}}")
        
        if peers:
            trader.connect_to_peers(peers)
        
        # Executar análises automáticas
        print("🔄 Iniciando análises automáticas...")
        while trader.node.running:
            try:
                for symbol in ["BTCUSD", "ETHUSD"]:
                    trader.analyze_and_share(symbol)
                    time.sleep(30)
            except Exception as e:
                print(f"❌ Erro na análise: {{e}}")
                time.sleep(60)
    else:
        print(f"❌ Erro ao iniciar trader na porta {port}")
        
except ImportError as e:
    print(f"❌ Erro ao importar trader: {{e}}")
except Exception as e:
    print(f"❌ Erro no trader: {{e}}")
"""
        
        exec(trader_script)
    
    # Opções de rede P2P
    network_menu = """
    🌐 OPÇÕES DE REDE P2P:
    
    1. Nós Simples      - 3 nós P2P básicos (portas 5000-5002)
    2. Traders Fractais - 3 traders com análise fractal
    3. Rede Mista       - Nós simples + traders fractais
    4. Nó Único         - Apenas 1 nó para teste
    5. Voltar
    """
    
    print(network_menu)
    
    try:
        choice = input("🎯 Escolha o tipo de rede (1-5): ").strip()
        
        if choice == "1":
            # Nós simples
            ports = [5000, 5001, 5002]
            threads = []
            
            for port in ports:
                thread = threading.Thread(target=start_simple_node, args=(port,))
                thread.daemon = True
                thread.start()
                threads.append(thread)
                time.sleep(2)  # Delay entre nós
            
            print(f"🎯 {len(ports)} nós P2P iniciados nas portas: {ports}")
            print("⏳ Pressione Ctrl+C para parar...")
            
            try:
                for thread in threads:
                    thread.join()
            except KeyboardInterrupt:
                print("\n🛑 Parando rede P2P...")
                
        elif choice == "2":
            # Traders fractais
            ports = [5000, 5001, 5002]
            threads = []
            
            for port in ports:
                thread = threading.Thread(target=start_fractal_trader, args=(port,))
                thread.daemon = True
                thread.start()
                threads.append(thread)
                time.sleep(3)  # Delay maior para traders
            
            print(f"🤖 {len(ports)} traders fractais iniciados nas portas: {ports}")
            print("⏳ Pressione Ctrl+C para parar...")
            
            try:
                for thread in threads:
                    thread.join()
            except KeyboardInterrupt:
                print("\n🛑 Parando traders...")
                
        elif choice == "3":
            # Rede mista
            print("🔄 Iniciando rede mista...")
            
            # Nós simples
            simple_ports = [5000, 5001]
            for port in simple_ports:
                thread = threading.Thread(target=start_simple_node, args=(port,))
                thread.daemon = True
                thread.start()
                time.sleep(2)
            
            # Traders fractais
            trader_ports = [5002, 5003]
            for port in trader_ports:
                thread = threading.Thread(target=start_fractal_trader, args=(port,))
                thread.daemon = True
                thread.start()
                time.sleep(3)
            
            print(f"🌐 Rede mista iniciada:")
            print(f"   Nós simples: {simple_ports}")
            print(f"   Traders fractais: {trader_ports}")
            print("⏳ Pressione Ctrl+C para parar...")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Parando rede mista...")
                
        elif choice == "4":
            # Nó único
            port = 5000
            print(f"🔗 Iniciando nó único na porta {port}")
            start_simple_node(port)
            
        elif choice == "5":
            return
        else:
            print("❌ Opção inválida")
            
    except KeyboardInterrupt:
        print("\n🛑 Parando rede P2P...")
    except Exception as e:
        print(f"❌ Erro na rede P2P: {e}")

def show_menu():
    """Exibir menu de opções."""
    menu = """
    🚀 OPÇÕES DE EXECUÇÃO:
    
    1. 🎮 Demo Mode        - Demonstração com dados simulados
    2. 🖥️  Dashboard       - Interface gráfica Tkinter
    3. 🌐 Web App         - Frontend React + Backend FastAPI
    4. 🔗 P2P Network     - Rede distribuída peer-to-peer
    5. 🛠️  Backend Only    - Apenas API FastAPI
    6. 🎨 Frontend Only   - Apenas interface React
    7. 🤖 P2P Demo        - Demonstração P2P com 1 trader
    8. 📦 Install Deps    - Instalar dependências
    9. ❌ Sair
    
    """
    print(menu)

def main():
    """Função principal."""
    print_banner()
    
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "--install":
            install_dependencies()
            return
        elif mode == "--demo":
            run_demo_mode()
            return
        elif mode == "--dashboard":
            run_dashboard()
            return
        elif mode == "--webapp":
            # Executar backend e frontend em paralelo
            backend_thread = threading.Thread(target=run_backend)
            frontend_thread = threading.Thread(target=run_frontend)
            
            backend_thread.start()
            time.sleep(3)  # Dar tempo para backend iniciar
            frontend_thread.start()
            
            backend_thread.join()
            frontend_thread.join()
            return
        elif mode == "--p2p":
            run_p2p_network()
            return
    
    # Menu interativo
    while True:
        show_menu()
        
        try:
            choice = input("🎯 Escolha uma opção (1-9): ").strip()
            
            if choice == "1":
                run_demo_mode()
            elif choice == "2":
                run_dashboard()
            elif choice == "3":
                # Web App - executar backend e frontend
                print("🌐 Iniciando aplicação web completa...")
                backend_thread = threading.Thread(target=run_backend)
                frontend_thread = threading.Thread(target=run_frontend)
                
                backend_thread.start()
                time.sleep(3)
                frontend_thread.start()
                
                print("✅ Aplicação web iniciada!")
                print("🔗 Backend: http://localhost:8000")
                print("🔗 Frontend: http://localhost:3000")
                
                try:
                    backend_thread.join()
                    frontend_thread.join()
                except KeyboardInterrupt:
                    print("\n🛑 Parando aplicação web...")
                    
            elif choice == "4":
                run_p2p_network()
            elif choice == "5":
                run_backend()
            elif choice == "6":
                run_frontend()
            elif choice == "7":
                # Demo P2P rápido
                print("🤖 Iniciando demo P2P...")
                demo_script = """
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'p2p'))

try:
    from fractal_p2p_demo import main as p2p_main
    p2p_main()
except ImportError as e:
    print(f"❌ Erro ao importar demo P2P: {e}")
    print("💡 Executando versão simplificada...")
    
    from simple_p2p_node import main as simple_main
    simple_main()
except Exception as e:
    print(f"❌ Erro no demo P2P: {e}")
"""
                exec(demo_script)
            elif choice == "8":
                install_dependencies()
            elif choice == "9":
                print("👋 Saindo... Até logo!")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo... Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
