#!/usr/bin/env python3
"""
🚀 AEON Master Launcher
Sistema integrado de lançamento e orquestração para todos os módulos AEON
Controle centralizado de entropia quântica, monitoramento e visualização
"""

import os
import sys
import time
import json
import threading
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse
import webbrowser

# Constantes do sistema
AEON_VERSION = "1.0.0"
AEON_ASCII_LOGO = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ▄▄▄       ▄▄▄ .▒█████  ███▄    █                        ║
║    ▒████▄     ▀▄.▀·▒██▒  ██▒██ ▀█   █                        ║
║    ▒██  ▀█▄   ▐▀▀▪▄▒██░  ██▓██  ▀█ ██▒                       ║
║    ░██▄▄▄▄██  ▐█▄▄▌▒██   ██▓██▒  ▐▌██▒                       ║
║     ▓█   ▓██▒ ▀▀▀ ░ ████▓▒░▒██░   ▓██░                       ║
║     ▒▒   ▓▒█░       ░ ▒░▒░▒░ ░ ▒░   ▒ ▒                        ║
║      ▒   ▒▒ ░         ░ ▒ ▒░ ░ ░░   ░ ▒░                       ║
║      ░   ▒          ░ ░ ░ ▒     ░   ░ ░                        ║
║          ░  ░           ░ ░           ░                        ║
║                                                               ║
║    🌌 Advanced Entropy Optimization Network 🌌                ║
║         Sistema Integrado de Análise Quântica                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""

class AeonModuleStatus:
    """Status de um módulo AEON"""
    def __init__(self, name: str, path: str, description: str, dependencies: List[str] = None):
        self.name = name
        self.path = path
        self.description = description
        self.dependencies = dependencies or []
        self.is_available = self._check_availability()
        self.last_run = None
        self.status = "ready" if self.is_available else "unavailable"
        self.process = None
        
    def _check_availability(self) -> bool:
        """Verifica se o módulo está disponível"""
        file_path = Path(self.path)
        return file_path.exists() and file_path.is_file()
    
    def update_status(self, status: str, last_run: Optional[datetime] = None):
        """Atualiza status do módulo"""
        self.status = status
        if last_run:
            self.last_run = last_run

class AeonMasterLauncher:
    """Launcher principal do sistema AEON"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.modules = {}
        self.active_processes = {}
        self.log_file = Path("aeon_launcher.log")
        self.config_file = Path("aeon_config.json")
        
        # Inicializa sistema
        self._initialize_logging()
        self._discover_modules()
        self._load_config()
        
        print(AEON_ASCII_LOGO)
        print(f"🚀 AEON Master Launcher v{AEON_VERSION}")
        print(f"📅 Iniciado em: {self.start_time.strftime('%d/%m/%Y às %H:%M:%S')}")
        print("=" * 65)
        
    def _initialize_logging(self):
        """Inicializa sistema de logging"""
        self.log_entries = []
        self._log("🚀 AEON Master Launcher iniciado")
        
    def _log(self, message: str, level: str = "INFO"):
        """Adiciona entrada ao log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {level}: {message}"
        self.log_entries.append(log_entry)
        
        # Salva no arquivo
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
        
        # Imprime se não for DEBUG
        if level != "DEBUG":
            print(log_entry)
    
    def _discover_modules(self):
        """Descobre módulos AEON disponíveis"""
        self._log("🔍 Descobrindo módulos AEON...")
        
        # Define módulos conhecidos
        known_modules = {
            "quantum_analyzer": AeonModuleStatus(
                "Analisador de Entropia Quântica",
                "quantum_entropy_analyzer.py",
                "Sistema avançado de análise de entropia quântica",
                ["numpy", "random", "math"]
            ),
            "visualizer": AeonModuleStatus(
                "Visualizador Quântico",
                "aeon_quantum_visualizer.py",
                "Dashboard e visualizações para dados quânticos",
                ["quantum_entropy_analyzer"]
            ),
            "ram_dashboard": AeonModuleStatus(
                "Dashboard RAM",
                "aeon_ram_dashboard.py",
                "Monitoramento avançado de RAM em tempo real",
                ["psutil"]
            ),
            "resource_monitor": AeonModuleStatus(
                "Monitor de Recursos",
                "aeon_resource_monitor.py",
                "Análise completa de recursos do sistema",
                ["psutil"]
            ),
            "entropy_script": AeonModuleStatus(
                "Script de Entropia",
                "scripts/4.py",
                "Análise específica de entropia",
                []
            ),
            "cosmology_model": AeonModuleStatus(
                "Modelo Cosmológico",
                "scripts/NMD.py",
                "Simulação de modelo cosmológico avançado",
                []
            ),
            "verna_system": AeonModuleStatus(
                "Sistema V.E.R.N.A.",
                "teoria/verna.py",
                "Sistema de inteligência V.E.R.N.A.",
                []
            )
        }
        
        # Adiciona módulos descobertos
        for key, module in known_modules.items():
            self.modules[key] = module
            status = "✅" if module.is_available else "❌"
            self._log(f"  {status} {module.name}: {module.status}", "DEBUG")
        
        available_count = sum(1 for m in self.modules.values() if m.is_available)
        self._log(f"📦 {available_count}/{len(self.modules)} módulos disponíveis")
    
    def _load_config(self):
        """Carrega configuração do launcher"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self._log("⚙️ Configuração carregada")
            except Exception as e:
                self._log(f"⚠️ Erro ao carregar config: {e}", "WARN")
                self.config = self._default_config()
        else:
            self.config = self._default_config()
            self._save_config()
    
    def _default_config(self) -> Dict:
        """Retorna configuração padrão"""
        return {
            "auto_start": [],
            "update_interval": 5,
            "log_level": "INFO",
            "max_log_entries": 1000,
            "dashboard_port": 8080,
            "enable_notifications": True,
            "quantum_params": {
                "dimensions": 4,
                "system_size": 1000,
                "time_step": 0.1
            },
            "monitoring": {
                "enable_ram_monitoring": True,
                "ram_alert_threshold": 85,
                "enable_auto_cleanup": True
            }
        }
    
    def _save_config(self):
        """Salva configuração atual"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self._log("💾 Configuração salva")
        except Exception as e:
            self._log(f"❌ Erro ao salvar config: {e}", "ERROR")
    
    def list_modules(self):
        """Lista todos os módulos disponíveis"""
        print("\n📦 MÓDULOS AEON DISPONÍVEIS:")
        print("=" * 50)
        
        for key, module in self.modules.items():
            status_icon = "✅" if module.is_available else "❌"
            status_text = module.status.upper()
            
            print(f"{status_icon} {module.name}")
            print(f"   📄 Arquivo: {module.path}")
            print(f"   📝 Descrição: {module.description}")
            print(f"   🔄 Status: {status_text}")
            
            if module.last_run:
                print(f"   ⏰ Última execução: {module.last_run.strftime('%H:%M:%S')}")
            
            if module.dependencies:
                deps_status = []
                for dep in module.dependencies:
                    if dep in self.modules:
                        dep_available = self.modules[dep].is_available
                        deps_status.append(f"{dep}({'✓' if dep_available else '✗'})")
                    else:
                        deps_status.append(f"{dep}(?)")
                print(f"   🔗 Dependências: {', '.join(deps_status)}")
            
            print()
    
    def run_module(self, module_key: str, args: List[str] = None, background: bool = False) -> bool:
        """Executa um módulo específico"""
        if module_key not in self.modules:
            self._log(f"❌ Módulo '{module_key}' não encontrado", "ERROR")
            return False
        
        module = self.modules[module_key]
        
        if not module.is_available:
            self._log(f"❌ Módulo '{module.name}' não disponível", "ERROR")
            return False
        
        # Verifica dependências
        missing_deps = self._check_dependencies(module)
        if missing_deps:
            self._log(f"⚠️ Dependências ausentes para '{module.name}': {missing_deps}", "WARN")
        
        try:
            self._log(f"🚀 Executando: {module.name}")
            
            # Prepara comando
            cmd = [sys.executable, module.path]
            if args:
                cmd.extend(args)
            
            # Executa processo
            if background:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=os.getcwd()
                )
                self.active_processes[module_key] = process
                module.process = process
                module.update_status("running", datetime.now())
                self._log(f"🔄 '{module.name}' executando em background (PID: {process.pid})")
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
                
                if result.returncode == 0:
                    self._log(f"✅ '{module.name}' executado com sucesso")
                    module.update_status("completed", datetime.now())
                    
                    # Mostra output se houver
                    if result.stdout.strip():
                        print("\n📋 Saída do módulo:")
                        print("-" * 30)
                        print(result.stdout)
                else:
                    self._log(f"❌ '{module.name}' falhou (código: {result.returncode})", "ERROR")
                    module.update_status("failed", datetime.now())
                    
                    if result.stderr.strip():
                        print("\n❌ Erro do módulo:")
                        print("-" * 30)
                        print(result.stderr)
            
            return True
            
        except Exception as e:
            self._log(f"❌ Erro ao executar '{module.name}': {e}", "ERROR")
            module.update_status("error", datetime.now())
            return False
    
    def _check_dependencies(self, module: AeonModuleStatus) -> List[str]:
        """Verifica dependências de um módulo"""
        missing = []
        
        for dep in module.dependencies:
            if dep in self.modules:
                # Dependência é outro módulo AEON
                if not self.modules[dep].is_available:
                    missing.append(dep)
            else:
                # Dependência é biblioteca Python
                try:
                    __import__(dep)
                except ImportError:
                    missing.append(dep)
        
        return missing
    
    def run_sequence(self, sequence: List[str], delay: float = 1.0):
        """Executa sequência de módulos com delay"""
        self._log(f"🔄 Executando sequência: {' → '.join(sequence)}")
        
        for i, module_key in enumerate(sequence):
            if i > 0:
                time.sleep(delay)
            
            success = self.run_module(module_key)
            if not success:
                self._log(f"❌ Sequência interrompida em '{module_key}'", "ERROR")
                break
        
        self._log("✅ Sequência concluída")
    
    def start_monitoring_suite(self):
        """Inicia conjunto completo de monitoramento"""
        self._log("🔍 Iniciando suite de monitoramento...")
        
        monitoring_modules = ["ram_dashboard", "resource_monitor"]
        
        for module_key in monitoring_modules:
            if module_key in self.modules and self.modules[module_key].is_available:
                self.run_module(module_key, background=True)
            else:
                self._log(f"⚠️ Módulo de monitoramento '{module_key}' não disponível", "WARN")
        
        self._log("📊 Suite de monitoramento iniciada")
    
    def start_quantum_analysis(self, evolution_time: int = 60):
        """Inicia análise quântica completa"""
        self._log("🌌 Iniciando análise quântica completa...")
        
        # Parâmetros da análise
        params = [
            "--dimensions", str(self.config["quantum_params"]["dimensions"]),
            "--system-size", str(self.config["quantum_params"]["system_size"]),
            "--evolution-time", str(evolution_time)
        ]
        
        # Executa analisador quântico
        if "quantum_analyzer" in self.modules:
            success = self.run_module("quantum_analyzer", params, background=True)
            
            if success:
                # Aguarda um pouco e inicia visualizador
                time.sleep(5)
                if "visualizer" in self.modules:
                    self.run_module("visualizer", background=True)
        
        self._log("🔬 Análise quântica iniciada")
    
    def generate_system_report(self) -> str:
        """Gera relatório completo do sistema"""
        report_time = datetime.now()
        report_file = f"aeon_system_report_{report_time.strftime('%Y%m%d_%H%M%S')}.json"
        
        # Coleta informações do sistema
        active_processes = {}
        for key, process in self.active_processes.items():
            if process and process.poll() is None:  # Processo ainda rodando
                active_processes[key] = {
                    "pid": process.pid,
                    "status": "running"
                }
        
        # Compila relatório
        report = {
            "metadata": {
                "generated_at": report_time.isoformat(),
                "launcher_version": AEON_VERSION,
                "uptime_seconds": (report_time - self.start_time).total_seconds(),
                "total_modules": len(self.modules),
                "available_modules": sum(1 for m in self.modules.values() if m.is_available)
            },
            "modules_status": {
                key: {
                    "name": module.name,
                    "available": module.is_available,
                    "status": module.status,
                    "last_run": module.last_run.isoformat() if module.last_run else None,
                    "dependencies": module.dependencies
                }
                for key, module in self.modules.items()
            },
            "active_processes": active_processes,
            "configuration": self.config,
            "recent_logs": self.log_entries[-50:],  # Últimas 50 entradas
            "system_health": self._assess_system_health()
        }
        
        # Salva relatório
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        self._log(f"📋 Relatório do sistema gerado: {report_file}")
        return report_file
    
    def _assess_system_health(self) -> Dict:
        """Avalia saúde geral do sistema"""
        available_modules = sum(1 for m in self.modules.values() if m.is_available)
        total_modules = len(self.modules)
        availability_ratio = available_modules / total_modules if total_modules > 0 else 0
        
        running_processes = sum(1 for p in self.active_processes.values() 
                              if p and p.poll() is None)
        
        # Critérios de saúde
        health_score = 0
        max_score = 5
        
        # 1. Disponibilidade de módulos
        if availability_ratio >= 0.8:
            health_score += 2
        elif availability_ratio >= 0.6:
            health_score += 1
        
        # 2. Processos ativos
        if running_processes >= 2:
            health_score += 1
        
        # 3. Tempo de atividade
        uptime_hours = (datetime.now() - self.start_time).total_seconds() / 3600
        if uptime_hours >= 1:
            health_score += 1
        
        # 4. Logs de erro
        error_logs = sum(1 for log in self.log_entries[-20:] if "ERROR" in log)
        if error_logs == 0:
            health_score += 1
        
        health_percentage = (health_score / max_score) * 100
        
        if health_percentage >= 80:
            status = "excellent"
        elif health_percentage >= 60:
            status = "good"
        elif health_percentage >= 40:
            status = "moderate"
        else:
            status = "poor"
        
        return {
            "overall_status": status,
            "health_percentage": health_percentage,
            "available_modules": available_modules,
            "total_modules": total_modules,
            "running_processes": running_processes,
            "uptime_hours": uptime_hours,
            "recent_errors": error_logs
        }
    
    def stop_all_processes(self):
        """Para todos os processos ativos"""
        self._log("🛑 Parando todos os processos...")
        
        stopped_count = 0
        for key, process in list(self.active_processes.items()):
            if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    stopped_count += 1
                    self._log(f"✅ Processo '{key}' parado")
                except subprocess.TimeoutExpired:
                    process.kill()
                    stopped_count += 1
                    self._log(f"⚡ Processo '{key}' finalizado forçadamente")
                except Exception as e:
                    self._log(f"❌ Erro ao parar '{key}': {e}", "ERROR")
                
                # Atualiza status do módulo
                if key in self.modules:
                    self.modules[key].update_status("stopped")
        
        self.active_processes.clear()
        self._log(f"🔄 {stopped_count} processos parados")
    
    def interactive_menu(self):
        """Interface interativa do launcher"""
        while True:
            print("\n" + "=" * 50)
            print("🌌 AEON MASTER LAUNCHER - MENU PRINCIPAL")
            print("=" * 50)
            print("1. 📦 Listar módulos")
            print("2. 🚀 Executar módulo")
            print("3. 🔄 Executar sequência")
            print("4. 📊 Iniciar monitoramento")
            print("5. 🌌 Análise quântica completa")
            print("6. 📋 Gerar relatório do sistema")
            print("7. ⚙️ Configurações")
            print("8. 📊 Status dos processos")
            print("9. 🛑 Parar todos os processos")
            print("0. 🚪 Sair")
            print()
            
            try:
                choice = input("🎯 Escolha uma opção: ").strip()
                
                if choice == "1":
                    self.list_modules()
                
                elif choice == "2":
                    self._interactive_run_module()
                
                elif choice == "3":
                    self._interactive_sequence()
                
                elif choice == "4":
                    self.start_monitoring_suite()
                
                elif choice == "5":
                    evolution_time = input("⏰ Tempo de evolução (segundos) [60]: ").strip()
                    evolution_time = int(evolution_time) if evolution_time else 60
                    self.start_quantum_analysis(evolution_time)
                
                elif choice == "6":
                    report_file = self.generate_system_report()
                    print(f"📋 Relatório gerado: {report_file}")
                
                elif choice == "7":
                    self._interactive_config()
                
                elif choice == "8":
                    self._show_process_status()
                
                elif choice == "9":
                    self.stop_all_processes()
                
                elif choice == "0":
                    print("👋 Encerrando AEON Master Launcher...")
                    self.stop_all_processes()
                    break
                
                else:
                    print("❌ Opção inválida!")
            
            except KeyboardInterrupt:
                print("\n\n🛑 Interrompido pelo usuário")
                self.stop_all_processes()
                break
            except Exception as e:
                self._log(f"❌ Erro no menu: {e}", "ERROR")
    
    def _interactive_run_module(self):
        """Interface para executar módulo"""
        print("\n📦 Módulos disponíveis:")
        available = [(k, v) for k, v in self.modules.items() if v.is_available]
        
        for i, (key, module) in enumerate(available, 1):
            print(f"{i}. {module.name}")
        
        try:
            choice = int(input("\n🎯 Escolha um módulo (número): "))
            if 1 <= choice <= len(available):
                key, module = available[choice - 1]
                
                background = input("🔄 Executar em background? (s/N): ").lower().startswith('s')
                args_input = input("📝 Argumentos (opcional): ").strip()
                args = args_input.split() if args_input else None
                
                self.run_module(key, args, background)
            else:
                print("❌ Número inválido!")
        except (ValueError, IndexError):
            print("❌ Entrada inválida!")
    
    def _interactive_sequence(self):
        """Interface para executar sequência"""
        print("\n🔄 Criar sequência de execução:")
        available = [(k, v) for k, v in self.modules.items() if v.is_available]
        
        for i, (key, module) in enumerate(available, 1):
            print(f"{i}. {module.name}")
        
        sequence = []
        print("\nEscolha módulos (números separados por espaço):")
        
        try:
            choices = input("🎯 Sequência: ").split()
            for choice in choices:
                idx = int(choice) - 1
                if 0 <= idx < len(available):
                    sequence.append(available[idx][0])
            
            if sequence:
                delay = float(input("⏱️ Delay entre módulos (segundos) [1.0]: ") or "1.0")
                self.run_sequence(sequence, delay)
            else:
                print("❌ Sequência vazia!")
        except (ValueError, IndexError):
            print("❌ Entrada inválida!")
    
    def _interactive_config(self):
        """Interface para configurações"""
        print("\n⚙️ Configurações atuais:")
        print(json.dumps(self.config, indent=2, ensure_ascii=False))
        
        print("\nOpções de configuração:")
        print("1. 🔄 Modificar intervalo de atualização")
        print("2. 🌌 Parâmetros quânticos")
        print("3. 📊 Configurações de monitoramento")
        print("4. 💾 Salvar configuração")
        print("5. 🔙 Voltar")
        
        choice = input("\n🎯 Escolha: ")
        
        if choice == "1":
            try:
                interval = int(input("Novo intervalo (segundos): "))
                self.config["update_interval"] = interval
                print("✅ Intervalo atualizado")
            except ValueError:
                print("❌ Valor inválido")
        
        elif choice == "2":
            try:
                dims = int(input(f"Dimensões [{self.config['quantum_params']['dimensions']}]: ") or self.config['quantum_params']['dimensions'])
                size = int(input(f"Tamanho do sistema [{self.config['quantum_params']['system_size']}]: ") or self.config['quantum_params']['system_size'])
                
                self.config["quantum_params"]["dimensions"] = dims
                self.config["quantum_params"]["system_size"] = size
                print("✅ Parâmetros quânticos atualizados")
            except ValueError:
                print("❌ Valores inválidos")
        
        elif choice == "4":
            self._save_config()
    
    def _show_process_status(self):
        """Mostra status dos processos ativos"""
        print("\n📊 STATUS DOS PROCESSOS:")
        print("=" * 40)
        
        if not self.active_processes:
            print("💤 Nenhum processo ativo")
            return
        
        for key, process in self.active_processes.items():
            if process:
                status = "🟢 Rodando" if process.poll() is None else "🔴 Parado"
                print(f"{status} {key} (PID: {process.pid})")
                
                # Mostra informações do módulo
                if key in self.modules:
                    module = self.modules[key]
                    print(f"   📝 {module.name}")
                    if module.last_run:
                        uptime = datetime.now() - module.last_run
                        print(f"   ⏰ Ativo há: {uptime}")
        
        print(f"\n📈 Total: {len(self.active_processes)} processos")

def main():
    """Função principal do launcher"""
    parser = argparse.ArgumentParser(description="🚀 AEON Master Launcher")
    parser.add_argument("--module", "-m", help="Executar módulo específico")
    parser.add_argument("--list", "-l", action="store_true", help="Listar módulos")
    parser.add_argument("--sequence", "-s", nargs="+", help="Executar sequência de módulos")
    parser.add_argument("--monitoring", action="store_true", help="Iniciar suite de monitoramento")
    parser.add_argument("--quantum", "-q", type=int, default=60, help="Análise quântica (tempo em segundos)")
    parser.add_argument("--report", "-r", action="store_true", help="Gerar relatório do sistema")
    parser.add_argument("--background", "-b", action="store_true", help="Executar em background")
    parser.add_argument("--interactive", "-i", action="store_true", help="Modo interativo")
    
    args = parser.parse_args()
    
    # Inicializa launcher
    launcher = AeonMasterLauncher()
    
    try:
        # Processa argumentos
        if args.list:
            launcher.list_modules()
        
        elif args.module:
            launcher.run_module(args.module, background=args.background)
        
        elif args.sequence:
            launcher.run_sequence(args.sequence)
        
        elif args.monitoring:
            launcher.start_monitoring_suite()
            print("📊 Suite de monitoramento iniciada. Pressione Ctrl+C para parar.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                launcher.stop_all_processes()
        
        elif args.quantum:
            launcher.start_quantum_analysis(args.quantum)
            print(f"🌌 Análise quântica iniciada ({args.quantum}s). Pressione Ctrl+C para parar.")
            try:
                time.sleep(args.quantum)
            except KeyboardInterrupt:
                pass
            launcher.stop_all_processes()
        
        elif args.report:
            report_file = launcher.generate_system_report()
            print(f"📋 Relatório gerado: {report_file}")
        
        elif args.interactive:
            launcher.interactive_menu()
        
        else:
            # Modo padrão: menu interativo
            launcher.interactive_menu()
    
    except KeyboardInterrupt:
        print("\n🛑 Launcher interrompido")
        launcher.stop_all_processes()
    
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        launcher._log(f"CRITICAL: {e}", "CRITICAL")
    
    finally:
        launcher._log("🔄 AEON Master Launcher finalizado")
        print("👋 Até logo!")

if __name__ == "__main__":
    main()
