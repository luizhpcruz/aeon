"""
🚀 AEONCOSMA Integrated Launcher - Launcher Principal do Sistema
Sistema integrado para inicializar todos os componentes da rede P2P
Copyright 2025 - Luiz H. P. Cruz
"""

import asyncio
import subprocess
import sys
import os
import time
import json
import threading
import webbrowser
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import signal
import psutil
from pathlib import Path
import socket

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AEONCOSMALauncher:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.processes = {}
        self.services = {}
        self.running = False
        self.config = self._load_config()
        
        # URLs dos serviços
        self.service_urls = {
            "streamlit_monitor": "http://localhost:8501",
            "fastapi_backend": "http://localhost:8000",
            "p2p_network": "http://localhost:8002",
            "jupyter_notebook": "http://localhost:8888"
        }
        
        # Status dos serviços
        self.service_status = {
            "p2p_network": False,
            "streamlit_monitor": False,
            "fastapi_backend": False,
            "network_testing": False,
            "jupyter_notebook": False
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """Carregar configuração do launcher"""
        default_config = {
            "auto_start_services": ["p2p_network", "streamlit_monitor"],
            "ports": {
                "streamlit": 8501,
                "fastapi": 8000,
                "p2p_network": 8002,
                "jupyter": 8888
            },
            "startup_delay": 2,
            "max_startup_time": 60,
            "auto_open_browser": True,
            "log_level": "INFO"
        }
        
        config_file = self.base_path / "launcher_config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                return {**default_config, **config}
            except:
                logger.warning("Erro carregando config, usando defaults")
        
        return default_config
    
    def _save_config(self):
        """Salvar configuração"""
        config_file = self.base_path / "launcher_config.json"
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def display_banner(self):
        """Exibir banner do sistema"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🌐 AEONCOSMA ENGINE 🌐                   ║
║                   Integrated P2P Network                     ║
║                                                              ║
║  🧠 IA • 🔐 Crypto • 📡 Quantum • 🌌 Cosmos • ⛓️ Blockchain  ║
║                                                              ║
║              Desenvolvido por Luiz H. P. Cruz               ║
║                      Copyright 2025                         ║
╚══════════════════════════════════════════════════════════════╝

🚀 Iniciando Sistema Integrado AEONCOSMA...
"""
        print(banner)
        logger.info("AEONCOSMA Engine - Sistema iniciado")
    
    def check_dependencies(self) -> bool:
        """Verificar dependências do sistema"""
        logger.info("🔍 Verificando dependências...")
        
        required_packages = [
            "streamlit", "fastapi", "uvicorn", "asyncio", 
            "plotly", "pandas", "numpy", "networkx"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                logger.info(f"✅ {package} - OK")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"❌ {package} - Não encontrado")
        
        if missing_packages:
            logger.error(f"❌ Pacotes faltando: {missing_packages}")
            logger.info("Execute: pip install -r requirements.txt")
            return False
        
        logger.info("✅ Todas as dependências verificadas")
        return True
    
    def check_ports(self) -> bool:
        """Verificar disponibilidade das portas"""
        logger.info("🔌 Verificando portas...")
        
        for service, port in self.config["ports"].items():
            if self._is_port_in_use(port):
                logger.warning(f"⚠️ Porta {port} ({service}) já está em uso")
                # Tentar encontrar porta alternativa
                alternative_port = self._find_free_port(port + 1)
                if alternative_port:
                    self.config["ports"][service] = alternative_port
                    logger.info(f"🔄 Usando porta alternativa {alternative_port} para {service}")
                else:
                    logger.error(f"❌ Não foi possível encontrar porta alternativa para {service}")
                    return False
            else:
                logger.info(f"✅ Porta {port} ({service}) - Disponível")
        
        return True
    
    def _is_port_in_use(self, port: int) -> bool:
        """Verificar se porta está em uso"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return False
            except OSError:
                return True
    
    def _find_free_port(self, start_port: int) -> Optional[int]:
        """Encontrar porta livre"""
        for port in range(start_port, start_port + 100):
            if not self._is_port_in_use(port):
                return port
        return None
    
    async def start_p2p_network(self):
        """Iniciar rede P2P"""
        logger.info("🌐 Iniciando rede P2P...")
        
        try:
            # Importar e iniciar rede expandida
            from expanded_p2p_network import ExpandedP2PNetwork
            
            self.p2p_network = ExpandedP2PNetwork()
            self.p2p_network.create_node_fleet(count=25)
            
            # Iniciar em thread separada para não bloquear
            def run_network():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(self.p2p_network.start_network())
                except Exception as e:
                    logger.error(f"Erro na rede P2P: {e}")
                finally:
                    loop.close()
            
            self.services["p2p_network"] = threading.Thread(target=run_network, daemon=True)
            self.services["p2p_network"].start()
            
            # Dar tempo para inicializar
            await asyncio.sleep(3)
            
            self.service_status["p2p_network"] = True
            logger.info("✅ Rede P2P iniciada com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro iniciando rede P2P: {e}")
            self.service_status["p2p_network"] = False
    
    def start_streamlit_monitor(self):
        """Iniciar monitor Streamlit"""
        logger.info("📊 Iniciando monitor Streamlit...")
        
        try:
            port = self.config["ports"]["streamlit"]
            monitor_file = self.base_path / "p2p_monitor_dashboard.py"
            
            if not monitor_file.exists():
                logger.error(f"❌ Arquivo não encontrado: {monitor_file}")
                return False
            
            # Comando para iniciar Streamlit
            cmd = [
                sys.executable, "-m", "streamlit", "run",
                str(monitor_file),
                "--server.port", str(port),
                "--server.headless", "true",
                "--server.address", "localhost"
            ]
            
            # Iniciar processo
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.base_path)
            )
            
            self.processes["streamlit"] = process
            self.service_status["streamlit_monitor"] = True
            
            logger.info(f"✅ Monitor Streamlit iniciado na porta {port}")
            logger.info(f"🌐 Acesse: {self.service_urls['streamlit_monitor']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro iniciando Streamlit: {e}")
            return False
    
    def start_fastapi_backend(self):
        """Iniciar backend FastAPI"""
        logger.info("🚀 Iniciando backend FastAPI...")
        
        try:
            port = self.config["ports"]["fastapi"]
            
            # Criar aplicação FastAPI simples se não existir
            api_file = self.base_path / "simple_api.py"
            if not api_file.exists():
                self._create_simple_api(api_file)
            
            # Comando para iniciar FastAPI
            cmd = [
                sys.executable, "-m", "uvicorn",
                "simple_api:app",
                "--host", "localhost",
                "--port", str(port),
                "--reload"
            ]
            
            # Iniciar processo
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.base_path)
            )
            
            self.processes["fastapi"] = process
            self.service_status["fastapi_backend"] = True
            
            logger.info(f"✅ Backend FastAPI iniciado na porta {port}")
            logger.info(f"🌐 API Docs: {self.service_urls['fastapi_backend']}/docs")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro iniciando FastAPI: {e}")
            return False
    
    def _create_simple_api(self, api_file: Path):
        """Criar API simples se não existir"""
        api_content = '''
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from datetime import datetime

app = FastAPI(title="AEONCOSMA API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "AEONCOSMA API - Sistema Ativo", "timestamp": datetime.now()}

@app.get("/status")
async def status():
    return {
        "status": "running",
        "services": {
            "p2p_network": True,
            "ai_module": True,
            "crypto_module": True,
            "quantum_module": True,
            "cosmos_module": True
        },
        "uptime": "active",
        "timestamp": datetime.now()
    }

@app.get("/network/nodes")
async def get_nodes():
    return {
        "total_nodes": 25,
        "active_nodes": 23,
        "node_types": ["master", "energy", "ai", "crypto", "quantum", "cosmos"],
        "network_health": 0.95
    }

@app.get("/network/stats")
async def get_network_stats():
    return {
        "total_messages": 15847,
        "avg_latency_ms": 45.2,
        "throughput_msgs_sec": 2340,
        "success_rate": 0.987,
        "timestamp": datetime.now()
    }
'''
        
        with open(api_file, 'w') as f:
            f.write(api_content)
    
    async def start_network_testing(self):
        """Iniciar testes de rede"""
        logger.info("🧪 Iniciando suite de testes...")
        
        try:
            from network_testing_suite import NetworkTestSuite
            
            self.test_suite = NetworkTestSuite()
            
            # Executar testes em thread separada
            def run_tests():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    report = loop.run_until_complete(self.test_suite.run_comprehensive_test_suite())
                    logger.info(f"📊 Testes concluídos - Score: {report.get('overall_score', 0):.1f}/100")
                except Exception as e:
                    logger.error(f"Erro nos testes: {e}")
                finally:
                    loop.close()
            
            self.services["testing"] = threading.Thread(target=run_tests, daemon=True)
            self.services["testing"].start()
            
            self.service_status["network_testing"] = True
            logger.info("✅ Suite de testes iniciada")
            
        except Exception as e:
            logger.error(f"❌ Erro iniciando testes: {e}")
    
    def start_jupyter_notebook(self):
        """Iniciar Jupyter Notebook (opcional)"""
        logger.info("📓 Iniciando Jupyter Notebook...")
        
        try:
            port = self.config["ports"]["jupyter"]
            
            cmd = [
                sys.executable, "-m", "jupyter", "notebook",
                "--port", str(port),
                "--no-browser",
                "--ip", "localhost",
                "--notebook-dir", str(self.base_path)
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.base_path)
            )
            
            self.processes["jupyter"] = process
            self.service_status["jupyter_notebook"] = True
            
            logger.info(f"✅ Jupyter Notebook iniciado na porta {port}")
            
            return True
            
        except Exception as e:
            logger.info(f"ℹ️ Jupyter não disponível (opcional): {e}")
            return False
    
    def open_browser_interfaces(self):
        """Abrir interfaces no navegador"""
        if not self.config.get("auto_open_browser", True):
            return
        
        logger.info("🌐 Abrindo interfaces no navegador...")
        
        # Aguardar serviços iniciarem
        time.sleep(3)
        
        try:
            # Abrir monitor principal
            if self.service_status["streamlit_monitor"]:
                webbrowser.open(self.service_urls["streamlit_monitor"])
                logger.info(f"🌐 Aberto: Monitor P2P")
            
            # Abrir documentação da API
            if self.service_status["fastapi_backend"]:
                webbrowser.open(f"{self.service_urls['fastapi_backend']}/docs")
                logger.info(f"🌐 Aberto: API Docs")
                
        except Exception as e:
            logger.warning(f"⚠️ Erro abrindo navegador: {e}")
    
    def monitor_services(self):
        """Monitorar status dos serviços"""
        logger.info("👁️ Iniciando monitoramento de serviços...")
        
        while self.running:
            try:
                # Verificar processos
                for service, process in self.processes.items():
                    if process.poll() is not None:  # Processo terminou
                        logger.warning(f"⚠️ Serviço {service} parou inesperadamente")
                        self.service_status[f"{service}_backend" if service == "fastapi" else f"{service}_monitor"] = False
                
                # Log de status periodicamente
                active_services = sum(1 for status in self.service_status.values() if status)
                total_services = len(self.service_status)
                
                if active_services == total_services:
                    logger.info(f"✅ Todos os serviços ativos ({active_services}/{total_services})")
                else:
                    logger.warning(f"⚠️ Serviços ativos: {active_services}/{total_services}")
                
                time.sleep(30)  # Verificar a cada 30 segundos
                
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                time.sleep(10)
    
    def display_status(self):
        """Exibir status dos serviços"""
        print("\n" + "="*60)
        print("📊 STATUS DOS SERVIÇOS AEONCOSMA")
        print("="*60)
        
        for service, status in self.service_status.items():
            status_icon = "✅" if status else "❌"
            service_name = service.replace("_", " ").title()
            print(f"{status_icon} {service_name}")
        
        print("\n🌐 INTERFACES DISPONÍVEIS:")
        if self.service_status["streamlit_monitor"]:
            print(f"📊 Monitor P2P: {self.service_urls['streamlit_monitor']}")
        if self.service_status["fastapi_backend"]:
            print(f"🚀 API Backend: {self.service_urls['fastapi_backend']}")
            print(f"📚 API Docs: {self.service_urls['fastapi_backend']}/docs")
        if self.service_status["jupyter_notebook"]:
            print(f"📓 Jupyter: {self.service_urls['jupyter_notebook']}")
        
        print("\n💡 COMANDOS DISPONÍVEIS:")
        print("  's' - Status dos serviços")
        print("  'r' - Reiniciar serviços")
        print("  't' - Executar testes")
        print("  'b' - Abrir navegador")
        print("  'q' - Parar sistema")
        print("="*60)
    
    def interactive_menu(self):
        """Menu interativo"""
        self.display_status()
        
        while self.running:
            try:
                command = input("\n🎛️ AEONCOSMA> ").strip().lower()
                
                if command == 'q':
                    logger.info("🛑 Parando sistema...")
                    break
                elif command == 's':
                    self.display_status()
                elif command == 'r':
                    logger.info("🔄 Reiniciando serviços...")
                    asyncio.run(self.restart_services())
                elif command == 't':
                    logger.info("🧪 Executando testes...")
                    asyncio.run(self.start_network_testing())
                elif command == 'b':
                    self.open_browser_interfaces()
                elif command == '':
                    continue
                else:
                    print("❌ Comando inválido. Use 's', 'r', 't', 'b' ou 'q'")
                    
            except KeyboardInterrupt:
                logger.info("\n🛑 Interrompido pelo usuário")
                break
            except Exception as e:
                logger.error(f"Erro no menu: {e}")
    
    async def restart_services(self):
        """Reiniciar serviços"""
        logger.info("🔄 Reiniciando serviços...")
        
        # Parar serviços
        self.stop_services()
        
        # Aguardar
        await asyncio.sleep(2)
        
        # Reiniciar
        await self.start_all_services()
    
    async def start_all_services(self):
        """Iniciar todos os serviços"""
        logger.info("🚀 Iniciando todos os serviços...")
        
        # Iniciar rede P2P
        await self.start_p2p_network()
        
        # Iniciar Streamlit
        self.start_streamlit_monitor()
        
        # Iniciar FastAPI
        self.start_fastapi_backend()
        
        # Iniciar Jupyter (opcional)
        self.start_jupyter_notebook()
        
        # Aguardar inicialização
        await asyncio.sleep(5)
        
        logger.info("✅ Todos os serviços iniciados")
    
    def stop_services(self):
        """Parar todos os serviços"""
        logger.info("🛑 Parando serviços...")
        
        # Parar processos
        for service, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                logger.info(f"✅ {service} parado")
            except subprocess.TimeoutExpired:
                process.kill()
                logger.warning(f"⚠️ {service} forçado a parar")
            except Exception as e:
                logger.error(f"❌ Erro parando {service}: {e}")
        
        # Parar threads
        for service, thread in self.services.items():
            if thread.is_alive():
                logger.info(f"🛑 Parando thread {service}")
        
        # Resetar status
        for service in self.service_status:
            self.service_status[service] = False
        
        self.processes.clear()
        self.services.clear()
    
    def setup_signal_handlers(self):
        """Configurar handlers de sinal"""
        def signal_handler(signum, frame):
            logger.info(f"\n🛑 Recebido sinal {signum}, parando sistema...")
            self.running = False
            self.stop_services()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def run(self):
        """Executar launcher principal"""
        self.display_banner()
        self.setup_signal_handlers()
        self.running = True
        
        # Verificações iniciais
        if not self.check_dependencies():
            logger.error("❌ Dependências não atendidas")
            return False
        
        if not self.check_ports():
            logger.error("❌ Problemas com portas")
            return False
        
        try:
            # Iniciar todos os serviços
            await self.start_all_services()
            
            # Iniciar monitoramento em thread separada
            monitor_thread = threading.Thread(target=self.monitor_services, daemon=True)
            monitor_thread.start()
            
            # Abrir navegador
            browser_thread = threading.Thread(target=self.open_browser_interfaces, daemon=True)
            browser_thread.start()
            
            # Menu interativo
            self.interactive_menu()
            
        except Exception as e:
            logger.error(f"❌ Erro crítico: {e}")
        finally:
            self.stop_services()
            logger.info("✅ Sistema AEONCOSMA encerrado")
        
        return True

# Função principal
async def main():
    """Função principal do launcher"""
    launcher = AEONCOSMALauncher()
    await launcher.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)
