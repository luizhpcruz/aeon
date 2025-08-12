#!/usr/bin/env python3
"""
🖥️ MONITOR DE RAM PARA PROJETO AEON
Monitora uso de memória em tempo real e gera alertas
"""

import psutil
import time
import os
import sys
from datetime import datetime
import json

class AeonRAMMonitor:
    def __init__(self):
        self.log_file = "ram_monitor.log"
        self.config = {
            "alert_threshold": 85,  # % de RAM para alerta
            "critical_threshold": 90,  # % de RAM crítico
            "check_interval": 30,  # segundos entre verificações
            "log_enabled": True
        }
        
    def get_ram_info(self):
        """Coleta informações detalhadas de RAM"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "percent": mem.percent,
            "swap_percent": swap.percent,
            "free_gb": round(mem.free / (1024**3), 2)
        }
    
    def get_aeon_processes(self):
        """Identifica processos relacionados ao AEON"""
        aeon_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cmdline']):
            try:
                # Procura por processos Python executando scripts AEON
                if proc.info['name'].lower() in ['python.exe', 'python3.exe', 'pythonw.exe']:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if any(keyword in cmdline.lower() for keyword in ['aeon', 'p2p', 'entropy', 'cosma', 'verna']):
                        memory_mb = proc.info['memory_info'].rss / (1024*1024)
                        aeon_processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'memory_mb': round(memory_mb, 1),
                            'cmdline': cmdline[:100] + '...' if len(cmdline) > 100 else cmdline
                        })
                        
                # Procura por VS Code
                elif 'code' in proc.info['name'].lower():
                    memory_mb = proc.info['memory_info'].rss / (1024*1024)
                    aeon_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'memory_mb': round(memory_mb, 1),
                        'cmdline': 'VS Code'
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return aeon_processes
    
    def log_info(self, ram_info, processes):
        """Log das informações para arquivo"""
        if not self.config["log_enabled"]:
            return
            
        log_entry = {
            "ram": ram_info,
            "aeon_processes": processes,
            "total_aeon_memory": sum(p['memory_mb'] for p in processes)
        }
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def display_status(self, ram_info, processes):
        """Exibe status atual no console"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("🧬 AEON RAM MONITOR")
        print("=" * 50)
        print(f"⏰ {ram_info['timestamp']}")
        print()
        
        # Status da RAM
        status_icon = "🟢" if ram_info['percent'] < 70 else "🟡" if ram_info['percent'] < 85 else "🔴"
        print(f"{status_icon} RAM Status: {ram_info['percent']:.1f}%")
        print(f"💾 Total: {ram_info['total_gb']} GB")
        print(f"✅ Disponível: {ram_info['available_gb']} GB")
        print(f"🔥 Em uso: {ram_info['used_gb']} GB")
        
        if ram_info['swap_percent'] > 0:
            print(f"💿 Swap: {ram_info['swap_percent']:.1f}%")
        
        print()
        
        # Processos AEON
        if processes:
            total_aeon = sum(p['memory_mb'] for p in processes)
            print(f"🧬 PROCESSOS AEON: {len(processes)} processos, {total_aeon:.1f} MB total")
            print("-" * 50)
            
            for proc in sorted(processes, key=lambda x: x['memory_mb'], reverse=True):
                print(f"🔹 PID {proc['pid']:5} | {proc['memory_mb']:6.1f} MB | {proc['name']}")
                if proc['cmdline'] != 'VS Code':
                    print(f"   └─ {proc['cmdline']}")
        else:
            print("🧬 Nenhum processo AEON detectado")
        
        print()
        print("Pressione Ctrl+C para sair")
    
    def check_alerts(self, ram_info):
        """Verifica e emite alertas"""
        if ram_info['percent'] >= self.config['critical_threshold']:
            print(f"\n🚨 ALERTA CRÍTICO: RAM em {ram_info['percent']:.1f}%!")
            print("💡 Considere fechar aplicações desnecessárias")
            
        elif ram_info['percent'] >= self.config['alert_threshold']:
            print(f"\n⚠️ ALERTA: RAM em {ram_info['percent']:.1f}%")
            print("📊 Monitorando de perto...")
    
    def run(self):
        """Loop principal do monitor"""
        print("🚀 Iniciando AEON RAM Monitor...")
        print(f"📊 Verificações a cada {self.config['check_interval']} segundos")
        print("🔍 Monitorando processos AEON automaticamente")
        print()
        
        try:
            while True:
                ram_info = self.get_ram_info()
                processes = self.get_aeon_processes()
                
                self.display_status(ram_info, processes)
                self.check_alerts(ram_info)
                self.log_info(ram_info, processes)
                
                time.sleep(self.config['check_interval'])
                
        except KeyboardInterrupt:
            print("\n\n👋 Monitor AEON encerrado!")
            print(f"📝 Log salvo em: {self.log_file}")

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--quick':
            # Modo rápido - apenas uma verificação
            monitor = AeonRAMMonitor()
            ram_info = monitor.get_ram_info()
            processes = monitor.get_aeon_processes()
            monitor.display_status(ram_info, processes)
            return
        elif sys.argv[1] == '--help':
            print("🧬 AEON RAM Monitor")
            print("Uso:")
            print("  python monitor_ram.py          - Monitor contínuo")
            print("  python monitor_ram.py --quick  - Verificação única")
            print("  python monitor_ram.py --help   - Esta ajuda")
            return
    
    # Monitor contínuo
    monitor = AeonRAMMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
