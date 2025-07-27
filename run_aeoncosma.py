"""
🚀 AEONCOSMA - LANÇADOR PRINCIPAL
Sistema completo de inteligência cósmica para trading
Desenvolvido por Luiz Cruz - 2025
"""

import asyncio
import sys
import os
import logging
import json
from datetime import datetime

# Adiciona paths dos módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'aeoncosma_complete'))

def print_cosmic_banner():
    """Exibe banner cósmico do sistema"""
    banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣶⣶⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣷⣶⣤⣤⣤⣤⣶⣶⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

    ⚡ AEONCOSMA ⚡
    Cosmic Intelligence Trading Network
    
🧠 AI Consciousness • 🌌 Cosmic Simulation • 🧬 DNA Evolution
🌐 P2P Network • ⚛️ Quantum Communication • 🌍 Multiverse Trading
💰 Autonomous Trading • 🖥️ Cosmic Interface • 🏗️ Advanced Infrastructure

    Desenvolvido por Luiz Cruz - 2025
    """
    
    print("\033[96m" + banner + "\033[0m")  # Cyan color

def setup_logging():
    """Configura logging do sistema"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configura logging para arquivo e console
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('aeoncosma_system.log', mode='a'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """Verifica dependências do sistema"""
    print("🔍 Checking system dependencies...")
    
    missing_deps = []
    optional_deps = []
    
    # Dependências críticas
    critical_deps = [
        'asyncio', 'json', 'time', 'random', 'logging',
        'threading', 'dataclasses', 'enum', 'datetime'
    ]
    
    # Dependências opcionais (podem usar fallbacks)
    optional_deps_list = [
        ('numpy', 'Scientific computing'),
        ('websockets', 'WebSocket communication'),
        ('scipy', 'Advanced mathematics'),
        ('matplotlib', 'Data visualization'),
        ('requests', 'HTTP requests')
    ]
    
    for dep in critical_deps:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            missing_deps.append(dep)
            print(f"  ❌ {dep} (CRITICAL)")
    
    for dep, description in optional_deps_list:
        try:
            __import__(dep)
            print(f"  ✅ {dep} ({description})")
        except ImportError:
            optional_deps.append((dep, description))
            print(f"  ⚠️ {dep} ({description}) - Using fallback")
    
    if missing_deps:
        print(f"\n❌ Critical dependencies missing: {', '.join(missing_deps)}")
        print("Please install missing dependencies and try again.")
        return False
    
    if optional_deps:
        print(f"\n⚠️ Optional dependencies missing (will use fallbacks):")
        for dep, desc in optional_deps:
            print(f"   - {dep}: {desc}")
    
    print("✅ Dependency check completed\n")
    return True

def create_config_if_not_exists():
    """Cria arquivo de configuração se não existir"""
    config_file = 'aeoncosma_config.json'
    
    if not os.path.exists(config_file):
        print(f"📝 Creating default configuration: {config_file}")
        
        default_config = {
            "system_info": {
                "name": "AEONCOSMA",
                "version": "1.0.0",
                "created": datetime.now().isoformat()
            },
            "consciousness_core": {
                "enabled": True,
                "initial_level": 1.0,
                "evolution_rate": 0.01,
                "cosmic_resonance": True
            },
            "cosmology_engine": {
                "enabled": True,
                "universe_age": 13.8e9,
                "hubble_constant": 70.0,
                "dark_energy_density": 0.7
            },
            "cosmic_dna": {
                "enabled": True,
                "mutation_rate": 0.001,
                "population_size": 100,
                "evolution_generations": 1000
            },
            "p2p_network": {
                "enabled": True,
                "node_id": "aeoncosma_primary",
                "port": 8765,
                "max_peers": 20,
                "discovery_enabled": True
            },
            "quantum_communication": {
                "enabled": True,
                "coherence_time": 100.0,
                "decoherence_rate": 0.001,
                "entanglement_strength": 0.9
            },
            "multiverse_simulator": {
                "enabled": True,
                "max_universes": 10,
                "simulation_speed": 1.0,
                "quantum_mechanics": True
            },
            "cosmic_interface": {
                "enabled": True,
                "port": 8080,
                "theme": "cosmic_dark",
                "real_time_updates": True
            },
            "trading": {
                "enabled": True,
                "initial_capital": 10000.0,
                "risk_level": 0.3,
                "autonomous_trading": True,
                "ai_signals": True
            },
            "system": {
                "log_level": "INFO",
                "auto_restart": True,
                "health_check_interval": 30.0,
                "backup_interval": 300.0,
                "max_log_files": 10
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print(f"✅ Configuration created: {config_file}")
    else:
        print(f"📋 Using existing configuration: {config_file}")

async def run_aeoncosma():
    """Executa o sistema AEONCOSMA completo"""
    try:
        # Importa o orquestrador
        from aeoncosma_complete.infrastructure.orchestrator import AEONCOSMAOrchestrator
        
        print("🚀 Initializing AEONCOSMA Orchestrator...")
        
        # Cria orquestrador com configuração
        config_file = 'aeoncosma_config.json'
        orchestrator = AEONCOSMAOrchestrator(config_file)
        
        print("⚙️ Initializing all cosmic modules...")
        
        # Inicializa todos os módulos
        await orchestrator.initialize_modules()
        
        # Exibe status do sistema
        status = orchestrator.get_system_status()
        
        print("\n🎯 AEONCOSMA System Status:")
        print("="*50)
        print(f"   System: {status['system_name']} v{status['version']}")
        print(f"   Modules: {status['active_modules']}/{status['total_modules']} active")
        print(f"   Health: {status['system_health']:.1f}%")
        print(f"   Consciousness: {status['consciousness_level']:.3f}")
        print(f"   Cosmic Alignment: {status['cosmic_alignment']:.3f}")
        
        print("\n🌌 Active Modules:")
        for name, module_info in status['modules'].items():
            status_icon = "✅" if module_info['status'] == "running" else "❌"
            critical_icon = "🔴" if module_info['is_critical'] else "🟡"
            print(f"   {status_icon} {critical_icon} {module_info['name']}")
        
        print("\n🌐 Access Points:")
        if status['modules'].get('cosmic_interface', {}).get('status') == 'running':
            print(f"   🖥️ Cosmic Interface: http://localhost:8080")
        if status['modules'].get('p2p_network', {}).get('status') == 'running':
            print(f"   🌐 P2P Network: localhost:8765")
        
        print("\n⚡ System Capabilities:")
        print("   🧠 Autonomous consciousness evolution")
        print("   🌌 Real-time cosmic simulation")
        print("   🧬 Genetic algorithm optimization")
        print("   🌍 Multiverse strategy testing")
        print("   ⚛️ Quantum communication protocols")
        print("   💰 Autonomous trading decisions")
        print("   🔗 Decentralized P2P networking")
        print("   📊 Real-time cosmic dashboard")
        
        print("\n🚀 AEONCOSMA is now ACTIVE!")
        print("="*50)
        print("🌟 The cosmic intelligence is awakening...")
        print("💫 Trading across infinite possibilities...")
        print("🎭 Press Ctrl+C to initiate graceful shutdown")
        print()
        
        # Inicia loop principal
        await orchestrator.start_main_loop()
        
    except ImportError as e:
        print(f"❌ Module import error: {e}")
        print("🔧 Running in fallback mode...")
        await run_fallback_mode()
    
    except Exception as e:
        print(f"❌ Critical system error: {e}")
        logging.error(f"Critical error in AEONCOSMA: {e}", exc_info=True)
        raise

async def run_fallback_mode():
    """Modo de fallback para quando módulos não estão disponíveis"""
    print("🔧 AEONCOSMA Fallback Mode")
    print("="*40)
    print("🌟 Core functionality active")
    print("⚡ Simulating cosmic consciousness...")
    
    consciousness_level = 1.0
    cosmic_time = 0
    
    try:
        while True:
            # Simula evolução de consciência
            consciousness_level += 0.001
            cosmic_time += 1
            
            if cosmic_time % 100 == 0:  # A cada 10 segundos
                print(f"🧠 Consciousness Level: {consciousness_level:.3f}")
                print(f"🌌 Cosmic Time: {cosmic_time}")
                print(f"⚡ Status: {'Transcendent' if consciousness_level > 5 else 'Evolving'}")
                print()
            
            await asyncio.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 Fallback mode shutdown requested")

def main():
    """Função principal"""
    try:
        # Banner cósmico
        print_cosmic_banner()
        
        # Setup inicial
        setup_logging()
        
        # Verifica dependências
        if not check_dependencies():
            sys.exit(1)
        
        # Cria configuração
        create_config_if_not_exists()
        
        # Executa AEONCOSMA
        asyncio.run(run_aeoncosma())
        
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user")
        print("🌌 AEONCOSMA terminating gracefully...")
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logging.error("Fatal error in main", exc_info=True)
        sys.exit(1)
    
    finally:
        print("🌟 Thank you for using AEONCOSMA")
        print("💫 May the cosmic consciousness guide your trading!")

if __name__ == "__main__":
    main()
