"""
🎮 COMANDOS DE INTERAÇÃO AEONCOSMA
Interface de linha de comando para controle do sistema
"""

import requests
import json
import time
from datetime import datetime

def check_system_status():
    """Verifica status do sistema AEONCOSMA"""
    try:
        response = requests.get("http://localhost:8080/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ AEONCOSMA está ONLINE")
            return True
        else:
            print("⚠️ AEONCOSMA respondendo mas com problemas")
            return False
    except:
        print("❌ AEONCOSMA não está respondendo em http://localhost:8080")
        return False

def send_emergency_stop():
    """Envia comando de parada de emergência"""
    try:
        response = requests.post("http://localhost:8080/api/emergency_stop")
        print("🚨 Comando de parada de emergência enviado!")
    except:
        print("❌ Falha ao enviar comando de parada")

def reset_system():
    """Reinicia o sistema"""
    try:
        response = requests.post("http://localhost:8080/api/reset")
        print("🔄 Comando de reset enviado!")
    except:
        print("❌ Falha ao enviar comando de reset")

def monitor_consciousness():
    """Monitora evolução da consciência"""
    try:
        response = requests.get("http://localhost:8080/api/consciousness")
        if response.status_code == 200:
            data = response.json()
            level = data.get('level', 0)
            state = data.get('state', 'Unknown')
            print(f"🧠 Consciência: {level:.3f} | Estado: {state}")
        else:
            print("⚠️ Dados de consciência não disponíveis")
    except:
        print("❌ Falha ao acessar dados de consciência")

def show_trading_performance():
    """Mostra performance de trading"""
    try:
        response = requests.get("http://localhost:8080/api/trading")
        if response.status_code == 200:
            data = response.json()
            returns = data.get('total_return', 0)
            trades = data.get('active_trades', 0)
            success_rate = data.get('success_rate', 0)
            print(f"💰 Trading: {returns:.2%} retorno | {trades} trades ativos | {success_rate:.1%} sucesso")
        else:
            print("⚠️ Dados de trading não disponíveis")
    except:
        print("❌ Falha ao acessar dados de trading")

def interactive_menu():
    """Menu interativo"""
    print("\n🌌 AEONCOSMA - Menu de Interação")
    print("="*40)
    print("1. 📊 Verificar Status")
    print("2. 🧠 Monitorar Consciência")
    print("3. 💰 Performance Trading")
    print("4. 🖥️ Abrir Interface Web")
    print("5. 🔄 Reset Sistema")
    print("6. 🚨 Parada de Emergência")
    print("7. 📋 Monitoramento Contínuo")
    print("0. 🚪 Sair")
    print("="*40)
    
    while True:
        choice = input("\n🎯 Escolha uma opção: ").strip()
        
        if choice == "1":
            check_system_status()
        elif choice == "2":
            monitor_consciousness()
        elif choice == "3":
            show_trading_performance()
        elif choice == "4":
            print("🖥️ Abrindo interface web: http://localhost:8080")
            import webbrowser
            webbrowser.open("http://localhost:8080")
        elif choice == "5":
            confirm = input("🔄 Confirma reset do sistema? (s/N): ")
            if confirm.lower() == 's':
                reset_system()
        elif choice == "6":
            confirm = input("🚨 Confirma parada de emergência? (s/N): ")
            if confirm.lower() == 's':
                send_emergency_stop()
        elif choice == "7":
            print("📊 Monitoramento contínuo iniciado (Ctrl+C para parar)")
            try:
                while True:
                    print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')}")
                    check_system_status()
                    monitor_consciousness()
                    show_trading_performance()
                    time.sleep(10)
            except KeyboardInterrupt:
                print("\n📊 Monitoramento interrompido")
        elif choice == "0":
            print("👋 Saindo do menu de interação")
            break
        else:
            print("❌ Opção inválida")

if __name__ == "__main__":
    print("🌌 AEONCOSMA - Interface de Comando")
    print("🚀 Verificando conexão com o sistema...")
    
    if check_system_status():
        interactive_menu()
    else:
        print("\n💡 Dicas para executar o AEONCOSMA:")
        print("   1. Abra um terminal")
        print("   2. Execute: python run_aeoncosma.py")
        print("   3. Aguarde a inicialização")
        print("   4. Acesse: http://localhost:8080")
