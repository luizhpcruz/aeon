#!/usr/bin/env python3
"""
🚀 AEONCOSMA Suite Launcher
Script de inicialização para todos os componentes avançados
Autor: Luiz H. P. Cruz
Copyright 2025
"""

import os
import sys
import time
import subprocess
import threading
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aeoncosma_suite.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AEONCOSMASuiteLauncher:
    """Lançador da suíte completa AEONCOSMA"""
    
    def __init__(self):
        self.running_processes = {}
        self.available_components = {
            "dashboard": {
                "name": "Security Dashboard",
                "script": "streamlit_dashboard.py",
                "port": 8504,
                "description": "Dashboard de segurança com detecção de ataques"
            },
            "3d_visualizer": {
                "name": "3D Network Visualizer",
                "script": "network_3d_visualizer.py",
                "port": 8505,
                "description": "Visualizador 3D da rede em tempo real"
            },
            "stress_test": {
                "name": "Stress Test Suite",
                "script": "stress_test_suite.py",
                "port": None,
                "description": "Suíte de testes de stress da rede"
            },
            "symbolic_detector": {
                "name": "Symbolic Detection Engine",
                "script": "symbolic_detector.py",
                "port": None,
                "description": "Motor de detecção simbólica de anomalias"
            },
            "report_generator": {
                "name": "PDF Report Generator",
                "script": "report_generator.py",
                "port": None,
                "description": "Gerador automático de relatórios PDF/LaTeX"
            },
            "integrity_backend": {
                "name": "Integrity Backend",
                "script": "integrity_ascii.py",
                "port": None,
                "description": "Backend de validação de integridade"
            }
        }
    
    def check_dependencies(self) -> bool:
        """Verifica dependências necessárias"""
        required_packages = [
            'streamlit', 'plotly', 'networkx', 'pandas', 
            'numpy', 'psutil', 'requests'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"Pacotes ausentes: {', '.join(missing_packages)}")
            logger.info("Execute: pip install " + " ".join(missing_packages))
            return False
        
        return True
    
    def launch_component(self, component_key: str, **kwargs) -> bool:
        """Lança um componente específico"""
        if component_key not in self.available_components:
            logger.error(f"Componente '{component_key}' não encontrado")
            return False
        
        component = self.available_components[component_key]
        script_path = component["script"]
        
        if not os.path.exists(script_path):
            logger.error(f"Script não encontrado: {script_path}")
            return False
        
        try:
            if component["port"]:
                # Componente web (Streamlit)
                cmd = [
                    sys.executable, "-m", "streamlit", "run", script_path,
                    "--server.port", str(component["port"]),
                    "--server.headless", "true",
                    "--browser.gatherUsageStats", "false"
                ]
                
                logger.info(f"Iniciando {component['name']} na porta {component['port']}")
            else:
                # Componente de linha de comando
                cmd = [sys.executable, script_path]
                
                # Adicionar argumentos específicos
                if component_key == "stress_test":
                    cmd.extend(["--test", kwargs.get("test_type", "comprehensive")])
                    if "duration" in kwargs:
                        cmd.extend(["--duration", str(kwargs["duration"])])
                    if "intensity" in kwargs:
                        cmd.extend(["--intensity", str(kwargs["intensity"])])
                
                logger.info(f"Iniciando {component['name']}")
            
            # Executar o processo
            if component["port"]:
                # Para componentes web, executar em background
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                self.running_processes[component_key] = process
                
                # Aguardar inicialização
                time.sleep(3)
                
                if process.poll() is None:
                    logger.info(f"✅ {component['name']} iniciado com sucesso")
                    logger.info(f"🌐 Acesse: http://localhost:{component['port']}")
                    return True
                else:
                    logger.error(f"❌ Falha ao iniciar {component['name']}")
                    return False
            else:
                # Para componentes CLI, executar e aguardar
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"✅ {component['name']} executado com sucesso")
                    if result.stdout:
                        print(result.stdout)
                    return True
                else:
                    logger.error(f"❌ Erro em {component['name']}: {result.stderr}")
                    return False
        
        except Exception as e:
            logger.error(f"Erro ao lançar {component['name']}: {e}")
            return False
    
    def launch_dashboard_suite(self) -> bool:
        """Lança todos os dashboards web"""
        logger.info("🚀 Iniciando suíte de dashboards...")
        
        web_components = [key for key, comp in self.available_components.items() if comp["port"]]
        
        success_count = 0
        for component_key in web_components:
            if self.launch_component(component_key):
                success_count += 1
                time.sleep(2)  # Delay entre inicializações
        
        if success_count > 0:
            logger.info(f"✅ {success_count}/{len(web_components)} dashboards iniciados")
            self._print_access_urls()
            return True
        else:
            logger.error("❌ Nenhum dashboard foi iniciado com sucesso")
            return False
    
    def run_comprehensive_analysis(self) -> bool:
        """Executa análise abrangente do sistema"""
        logger.info("🔍 Iniciando análise abrangente...")
        
        # 1. Executar detecção simbólica
        logger.info("Executando detecção simbólica...")
        if not self.launch_component("symbolic_detector"):
            logger.warning("Falha na detecção simbólica")
        
        time.sleep(2)
        
        # 2. Executar testes de stress
        logger.info("Executando testes de stress...")
        if not self.launch_component("stress_test", test_type="comprehensive", duration=120):
            logger.warning("Falha nos testes de stress")
        
        time.sleep(2)
        
        # 3. Executar backend de integridade
        logger.info("Executando verificação de integridade...")
        if not self.launch_component("integrity_backend"):
            logger.warning("Falha na verificação de integridade")
        
        time.sleep(2)
        
        # 4. Gerar relatórios
        logger.info("Gerando relatórios...")
        if not self.launch_component("report_generator"):
            logger.warning("Falha na geração de relatórios")
        
        logger.info("✅ Análise abrangente concluída")
        return True
    
    def stop_all_components(self) -> bool:
        """Para todos os componentes em execução"""
        logger.info("🛑 Parando todos os componentes...")
        
        stopped_count = 0
        for component_key, process in self.running_processes.items():
            try:
                if process.poll() is None:  # Processo ainda rodando
                    process.terminate()
                    process.wait(timeout=5)
                    logger.info(f"✅ {self.available_components[component_key]['name']} parado")
                    stopped_count += 1
            except subprocess.TimeoutExpired:
                process.kill()
                logger.warning(f"⚠️ {self.available_components[component_key]['name']} forçadamente encerrado")
                stopped_count += 1
            except Exception as e:
                logger.error(f"❌ Erro ao parar {component_key}: {e}")
        
        self.running_processes.clear()
        logger.info(f"🛑 {stopped_count} componentes parados")
        return stopped_count > 0
    
    def show_status(self):
        """Mostra status dos componentes"""
        print("\n" + "="*80)
        print("STATUS DOS COMPONENTES AEONCOSMA")
        print("="*80)
        
        for key, component in self.available_components.items():
            if key in self.running_processes:
                process = self.running_processes[key]
                if process.poll() is None:
                    status = "🟢 RODANDO"
                    if component["port"]:
                        status += f" - http://localhost:{component['port']}"
                else:
                    status = "🔴 PARADO"
            else:
                status = "⚪ NÃO INICIADO"
            
            print(f"{component['name']:25} | {status}")
            print(f"{'':25} | {component['description']}")
            print("-" * 80)
    
    def _print_access_urls(self):
        """Imprime URLs de acesso"""
        print("\n" + "="*60)
        print("DASHBOARDS DISPONÍVEIS")
        print("="*60)
        
        for key, component in self.available_components.items():
            if component["port"] and key in self.running_processes:
                process = self.running_processes[key]
                if process.poll() is None:
                    print(f"🌐 {component['name']}: http://localhost:{component['port']}")
        
        print("="*60)
    
    def interactive_menu(self):
        """Menu interativo para seleção de componentes"""
        while True:
            print("\n" + "="*80)
            print("🚀 AEONCOSMA SUITE LAUNCHER")
            print("="*80)
            
            print("1. 🔄 Verificar dependências")
            print("2. 🌐 Iniciar todos os dashboards")
            print("3. 🔍 Executar análise abrangente")
            print("4. 📊 Iniciar dashboard de segurança")
            print("5. 🌐 Iniciar visualizador 3D")
            print("6. 🧪 Executar testes de stress")
            print("7. 🔍 Executar detecção simbólica")
            print("8. 📄 Gerar relatórios")
            print("9. 📊 Mostrar status dos componentes")
            print("10. 🛑 Parar todos os componentes")
            print("0. ❌ Sair")
            
            try:
                choice = input("\nEscolha uma opção: ").strip()
                
                if choice == "0":
                    self.stop_all_components()
                    print("👋 Até logo!")
                    break
                elif choice == "1":
                    if self.check_dependencies():
                        print("✅ Todas as dependências estão instaladas")
                    else:
                        print("❌ Dependências ausentes")
                elif choice == "2":
                    self.launch_dashboard_suite()
                elif choice == "3":
                    self.run_comprehensive_analysis()
                elif choice == "4":
                    self.launch_component("dashboard")
                elif choice == "5":
                    self.launch_component("3d_visualizer")
                elif choice == "6":
                    print("Tipos de teste disponíveis: ddos, cascade, consensus, resource, comprehensive")
                    test_type = input("Tipo de teste (Enter para comprehensive): ").strip() or "comprehensive"
                    duration = input("Duração em segundos (Enter para 60): ").strip() or "60"
                    self.launch_component("stress_test", test_type=test_type, duration=int(duration))
                elif choice == "7":
                    self.launch_component("symbolic_detector")
                elif choice == "8":
                    self.launch_component("report_generator")
                elif choice == "9":
                    self.show_status()
                elif choice == "10":
                    self.stop_all_components()
                else:
                    print("❌ Opção inválida")
                
                if choice != "0":
                    input("\nPressione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Interrompido pelo usuário")
                self.stop_all_components()
                break
            except Exception as e:
                logger.error(f"Erro no menu: {e}")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="AEONCOSMA Suite Launcher")
    parser.add_argument("--component", "-c", 
                       choices=["dashboard", "3d_visualizer", "stress_test", "symbolic_detector", "report_generator", "all"],
                       help="Componente específico para iniciar")
    parser.add_argument("--interactive", "-i", action="store_true", help="Modo interativo")
    parser.add_argument("--analysis", "-a", action="store_true", help="Executar análise abrangente")
    parser.add_argument("--test-type", "-t", default="comprehensive", help="Tipo de teste de stress")
    parser.add_argument("--duration", "-d", type=int, default=60, help="Duração do teste em segundos")
    
    args = parser.parse_args()
    
    launcher = AEONCOSMASuiteLauncher()
    
    # Verificar dependências primeiro
    if not launcher.check_dependencies():
        logger.error("❌ Dependências ausentes. Instale os pacotes necessários antes de continuar.")
        return 1
    
    try:
        if args.interactive:
            launcher.interactive_menu()
        elif args.analysis:
            launcher.run_comprehensive_analysis()
        elif args.component:
            if args.component == "all":
                launcher.launch_dashboard_suite()
                input("\nPressione Enter para parar todos os componentes...")
                launcher.stop_all_components()
            elif args.component == "stress_test":
                launcher.launch_component(args.component, test_type=args.test_type, duration=args.duration)
            else:
                launcher.launch_component(args.component)
                if launcher.available_components[args.component]["port"]:
                    input("\nPressione Enter para parar o componente...")
                    launcher.stop_all_components()
        else:
            # Modo padrão: menu interativo
            launcher.interactive_menu()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário")
        launcher.stop_all_components()
        return 1
    except Exception as e:
        logger.error(f"Erro na execução: {e}")
        launcher.stop_all_components()
        return 1

if __name__ == "__main__":
    exit(main())
