#!/usr/bin/env python3
"""
🚀 AEON Resource Monitor - Integração completa
Monitora RAM, CPU e recursos do sistema para otimização do projeto AEON
"""

import time
import json
import threading
from datetime import datetime
from pathlib import Path
import subprocess
import sys

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ psutil não instalado. Algumas funcionalidades limitadas.")

from aeon_ram_dashboard import AeonRAMDashboard

class AeonResourceMonitor:
    """Monitor completo de recursos para AEON"""
    
    def __init__(self):
        self.ram_dashboard = AeonRAMDashboard() if PSUTIL_AVAILABLE else None
        self.monitoring_active = False
        self.log_file = Path("aeon_resources.log")
        
    def check_system_requirements(self):
        """Verifica se o sistema atende aos requisitos mínimos para AEON"""
        requirements = {
            'ram_gb_minimum': 4,
            'ram_gb_recommended': 8,
            'python_version_minimum': (3, 8),
            'disk_space_gb': 2
        }
        
        results = {}
        
        if PSUTIL_AVAILABLE:
            # Verificação de RAM
            total_ram = psutil.virtual_memory().total / (1024**3)
            results['ram_check'] = {
                'current_gb': round(total_ram, 1),
                'meets_minimum': total_ram >= requirements['ram_gb_minimum'],
                'meets_recommended': total_ram >= requirements['ram_gb_recommended'],
                'status': 'excellent' if total_ram >= 16 else 'good' if total_ram >= 8 else 'adequate' if total_ram >= 4 else 'insufficient'
            }
            
            # Verificação de espaço em disco
            disk_usage = psutil.disk_usage('.')
            free_gb = disk_usage.free / (1024**3)
            results['disk_check'] = {
                'free_gb': round(free_gb, 1),
                'meets_requirement': free_gb >= requirements['disk_space_gb'],
                'status': 'excellent' if free_gb >= 10 else 'good' if free_gb >= 5 else 'adequate' if free_gb >= 2 else 'insufficient'
            }
        
        # Verificação de Python
        python_version = sys.version_info[:2]
        results['python_check'] = {
            'current_version': f"{python_version[0]}.{python_version[1]}",
            'meets_requirement': python_version >= requirements['python_version_minimum'],
            'status': 'excellent' if python_version >= (3, 11) else 'good' if python_version >= (3, 9) else 'adequate'
        }
        
        return results
    
    def optimize_system_for_aeon(self):
        """Aplica otimizações no sistema para melhor performance do AEON"""
        optimizations = []
        
        if PSUTIL_AVAILABLE:
            # Limpa cache de memória se possível
            try:
                if sys.platform == "win32":
                    # Windows: Sugestões de otimização
                    optimizations.append("🔧 Execute 'cleanmgr' para limpar arquivos temporários")
                    optimizations.append("💾 Considere aumentar arquivo de paginação")
                    optimizations.append("🔄 Reinicie aplicações pesadas se necessário")
                else:
                    # Linux/Mac: Comandos de otimização
                    optimizations.append("🔧 Execute 'sudo sync && sudo sysctl vm.drop_caches=3' para limpar cache")
                    optimizations.append("💾 Verifique swap com 'free -h'")
            except Exception as e:
                optimizations.append(f"⚠️ Erro ao aplicar otimizações: {e}")
        
        # Otimizações Python específicas
        optimizations.extend([
            "🐍 Execute 'pip cache purge' para limpar cache do pip",
            "🧹 Use 'python -m py_compile' para pré-compilar scripts críticos",
            "📊 Configure PYTHONOPTIMIZE=1 para bytecode otimizado"
        ])
        
        return optimizations
    
    def analyze_aeon_performance(self):
        """Analisa performance específica dos módulos AEON"""
        if not PSUTIL_AVAILABLE:
            return {"error": "psutil necessário para análise"}
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'aeon_processes': [],
            'performance_metrics': {},
            'recommendations': []
        }
        
        # Detecta processos AEON e analisa performance
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'cmdline']):
            try:
                if proc.info['name'].lower() in ['python.exe', 'python3.exe', 'pythonw.exe']:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    
                    if any(keyword in cmdline.lower() for keyword in ['aeon', 'p2p', 'entropy', 'cosma', 'verna']):
                        # Coleta métricas de performance
                        cpu_percent = proc.cpu_percent(interval=1)
                        memory_mb = proc.info['memory_info'].rss / (1024*1024)
                        
                        process_info = {
                            'pid': proc.info['pid'],
                            'script': self._extract_script_name(cmdline),
                            'cpu_percent': round(cpu_percent, 1),
                            'memory_mb': round(memory_mb, 1),
                            'efficiency_score': self._calculate_efficiency(cpu_percent, memory_mb)
                        }
                        
                        analysis['aeon_processes'].append(process_info)
            
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Gera recomendações de performance
        analysis['recommendations'] = self._generate_performance_recommendations(analysis['aeon_processes'])
        
        return analysis
    
    def _extract_script_name(self, cmdline: str) -> str:
        """Extrai nome do script da linha de comando"""
        parts = cmdline.split()
        for part in parts:
            if part.endswith('.py') or 'aeon' in part.lower():
                return Path(part).name
        return "unknown_script"
    
    def _calculate_efficiency(self, cpu: float, memory_mb: float) -> str:
        """Calcula score de eficiência do processo"""
        # Score baseado em uso equilibrado de CPU e memória
        if cpu < 5 and memory_mb < 50:
            return "excellent"
        elif cpu < 15 and memory_mb < 100:
            return "good"
        elif cpu < 30 and memory_mb < 200:
            return "moderate"
        else:
            return "needs_optimization"
    
    def _generate_performance_recommendations(self, processes: list) -> list:
        """Gera recomendações de performance baseadas nos processos"""
        recommendations = []
        
        if not processes:
            recommendations.append("✅ Nenhum processo AEON detectado no momento")
            return recommendations
        
        # Analisa processos com alto uso de CPU
        high_cpu = [p for p in processes if p['cpu_percent'] > 20]
        if high_cpu:
            recommendations.append(f"🔥 {len(high_cpu)} processo(s) com alto uso de CPU. Considere otimização")
        
        # Analisa processos com alto uso de memória
        high_memory = [p for p in processes if p['memory_mb'] > 100]
        if high_memory:
            recommendations.append(f"💾 {len(high_memory)} processo(s) usando >100MB RAM. Monitore vazamentos de memória")
        
        # Processos que precisam otimização
        need_optimization = [p for p in processes if p['efficiency_score'] == 'needs_optimization']
        if need_optimization:
            recommendations.append(f"⚡ {len(need_optimization)} processo(s) precisam otimização")
        
        # Recomendações gerais
        total_memory = sum(p['memory_mb'] for p in processes)
        if total_memory > 500:
            recommendations.append("🧬 Uso total AEON >500MB. Considere executar módulos sequencialmente")
        
        if len(processes) > 5:
            recommendations.append("🔄 Muitos processos AEON simultâneos. Verifique necessidade de todos")
        
        return recommendations or ["✅ Performance AEON dentro dos parâmetros normais"]
    
    def generate_health_report(self) -> dict:
        """Gera relatório completo de saúde do sistema para AEON"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_requirements': self.check_system_requirements(),
            'current_resources': {},
            'aeon_performance': {},
            'optimizations': self.optimize_system_for_aeon(),
            'overall_health': 'unknown'
        }
        
        if PSUTIL_AVAILABLE and self.ram_dashboard:
            report['current_resources'] = self.ram_dashboard.generate_report()
            report['aeon_performance'] = self.analyze_aeon_performance()
        
        # Calcula saúde geral do sistema
        report['overall_health'] = self._calculate_overall_health(report)
        
        return report
    
    def _calculate_overall_health(self, report: dict) -> str:
        """Calcula saúde geral baseada em múltricos fatores"""
        score = 0
        max_score = 0
        
        # Score baseado em requisitos do sistema
        req = report['system_requirements']
        
        if 'ram_check' in req:
            max_score += 3
            if req['ram_check']['meets_recommended']:
                score += 3
            elif req['ram_check']['meets_minimum']:
                score += 2
            else:
                score += 0
        
        if 'python_check' in req:
            max_score += 2
            if req['python_check']['meets_requirement']:
                score += 2
        
        if 'disk_check' in req:
            max_score += 1
            if req['disk_check']['meets_requirement']:
                score += 1
        
        # Score baseado em recursos atuais
        if 'current_resources' in report and 'current_status' in report['current_resources']:
            max_score += 2
            ram_percent = report['current_resources']['current_status']['ram_usage_percent']
            if ram_percent < 70:
                score += 2
            elif ram_percent < 85:
                score += 1
        
        # Calcula percentual final
        if max_score > 0:
            health_percent = (score / max_score) * 100
            
            if health_percent >= 90:
                return "excellent"
            elif health_percent >= 75:
                return "good"
            elif health_percent >= 60:
                return "moderate"
            else:
                return "needs_attention"
        
        return "unknown"
    
    def start_continuous_monitoring(self, interval: int = 60):
        """Inicia monitoramento contínuo com relatórios periódicos"""
        print("🚀 Iniciando monitoramento contínuo AEON...")
        
        if PSUTIL_AVAILABLE and self.ram_dashboard:
            self.ram_dashboard.start_monitoring(30)
        
        self.monitoring_active = True
        
        def monitoring_loop():
            while self.monitoring_active:
                try:
                    report = self.generate_health_report()
                    
                    # Log do relatório
                    self._log_health_report(report)
                    
                    # Exibe status resumido
                    self._display_monitoring_summary(report)
                    
                    time.sleep(interval)
                    
                except KeyboardInterrupt:
                    print("\n👋 Monitoramento interrompido pelo usuário")
                    break
                except Exception as e:
                    print(f"❌ Erro no monitoramento: {e}")
                    time.sleep(10)
        
        monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitor_thread.start()
        
        return monitor_thread
    
    def _log_health_report(self, report: dict):
        """Registra relatório de saúde em arquivo"""
        log_entry = {
            'timestamp': report['timestamp'],
            'health': report['overall_health'],
            'ram_percent': report.get('current_resources', {}).get('current_status', {}).get('ram_usage_percent', 0),
            'aeon_processes': len(report.get('aeon_performance', {}).get('aeon_processes', []))
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def _display_monitoring_summary(self, report: dict):
        """Exibe resumo do monitoramento na tela"""
        health_icons = {
            'excellent': '🟢',
            'good': '🟡', 
            'moderate': '🟠',
            'needs_attention': '🔴',
            'unknown': '⚪'
        }
        
        health = report['overall_health']
        icon = health_icons.get(health, '❓')
        
        print(f"\r{icon} AEON Health: {health.upper()} | ", end='', flush=True)
        
        if 'current_resources' in report:
            ram_percent = report['current_resources']['current_status']['ram_usage_percent']
            print(f"RAM: {ram_percent}% | ", end='', flush=True)
        
        if 'aeon_performance' in report:
            process_count = len(report['aeon_performance']['aeon_processes'])
            print(f"Processos: {process_count} | ", end='', flush=True)
        
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}", flush=True)

def main():
    """Função principal - interface de linha de comando"""
    monitor = AeonResourceMonitor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--health':
            report = monitor.generate_health_report()
            print(json.dumps(report, indent=2, ensure_ascii=False))
            
        elif command == '--requirements':
            req = monitor.check_system_requirements()
            print("🔍 VERIFICAÇÃO DE REQUISITOS AEON:")
            print(json.dumps(req, indent=2, ensure_ascii=False))
            
        elif command == '--optimize':
            opts = monitor.optimize_system_for_aeon()
            print("⚡ OTIMIZAÇÕES SUGERIDAS:")
            for opt in opts:
                print(f"  {opt}")
                
        elif command == '--monitor':
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            thread = monitor.start_continuous_monitoring(interval)
            
            try:
                thread.join()
            except KeyboardInterrupt:
                print("\n👋 Monitoramento finalizado!")
                
        else:
            print("❌ Comando inválido. Use: --health, --requirements, --optimize, --monitor")
    else:
        # Modo interativo padrão
        print("🧬 AEON Resource Monitor")
        print("=" * 40)
        
        report = monitor.generate_health_report()
        health = report['overall_health']
        
        print(f"🎯 Saúde geral: {health.upper()}")
        
        if PSUTIL_AVAILABLE:
            print(f"💾 RAM: {report['current_resources']['current_status']['ram_usage_percent']}%")
            print(f"🧬 Processos AEON: {len(report['aeon_performance']['aeon_processes'])}")
        
        print("\n📋 Use os seguintes comandos:")
        print("  python aeon_resource_monitor.py --health      # Relatório completo")
        print("  python aeon_resource_monitor.py --monitor     # Monitoramento contínuo")
        print("  python aeon_resource_monitor.py --optimize    # Sugestões de otimização")

if __name__ == "__main__":
    main()
