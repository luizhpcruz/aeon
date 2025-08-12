#!/usr/bin/env python3
"""
Script para verificar uso de RAM do sistema e processos Python
"""
import psutil
import sys
import os
from datetime import datetime

def get_size(bytes_size):
    """Converte bytes para formato legível"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def check_system_memory():
    """Verifica memória do sistema"""
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    print("🖥️  MEMÓRIA DO SISTEMA")
    print("=" * 50)
    print(f"Total RAM: {get_size(memory.total)}")
    print(f"Disponível: {get_size(memory.available)}")
    print(f"Usado: {get_size(memory.used)}")
    print(f"Percentual usado: {memory.percent}%")
    print(f"Livre: {get_size(memory.free)}")
    print()
    
    print(f"💾 SWAP/VIRTUAL")
    print("=" * 50)
    print(f"Total Swap: {get_size(swap.total)}")
    print(f"Usado Swap: {get_size(swap.used)}")
    print(f"Percentual Swap: {swap.percent}%")
    print()

def check_python_processes():
    """Verifica processos Python ativos"""
    print("🐍 PROCESSOS PYTHON")
    print("=" * 50)
    
    python_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent', 'cmdline']):
        try:
            if 'python' in proc.info['name'].lower():
                memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                cmdline = ' '.join(proc.info['cmdline'][:3]) if proc.info['cmdline'] else "N/A"
                python_processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'memory_mb': memory_mb,
                    'cpu_percent': proc.info['cpu_percent'],
                    'cmdline': cmdline
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if python_processes:
        python_processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        for proc in python_processes:
            print(f"PID: {proc['pid']:6} | RAM: {proc['memory_mb']:6.1f} MB | {proc['name']} | {proc['cmdline'][:60]}")
    else:
        print("Nenhum processo Python ativo encontrado")
    print()

def check_vscode_processes():
    """Verifica processos do VS Code"""
    print("💻 PROCESSOS VS CODE")
    print("=" * 50)
    
    vscode_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
        try:
            if 'code' in proc.info['name'].lower() or 'electron' in proc.info['name'].lower():
                memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                vscode_processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'memory_mb': memory_mb,
                    'cpu_percent': proc.info['cpu_percent']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if vscode_processes:
        vscode_processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        total_vscode_memory = sum(proc['memory_mb'] for proc in vscode_processes)
        
        for proc in vscode_processes[:10]:  # Top 10
            print(f"PID: {proc['pid']:6} | RAM: {proc['memory_mb']:6.1f} MB | {proc['name']}")
        
        if len(vscode_processes) > 10:
            print(f"... e mais {len(vscode_processes) - 10} processos")
        
        print(f"\n🎯 Total VS Code: {total_vscode_memory:.1f} MB")
    else:
        print("Nenhum processo VS Code encontrado")
    print()

def check_current_process():
    """Verifica o processo atual"""
    current_proc = psutil.Process()
    memory_mb = current_proc.memory_info().rss / (1024 * 1024)
    
    print("⚡ PROCESSO ATUAL")
    print("=" * 50)
    print(f"PID: {current_proc.pid}")
    print(f"Nome: {current_proc.name()}")
    print(f"Memória: {memory_mb:.2f} MB")
    print(f"CPU: {current_proc.cpu_percent()}%")
    print()

def estimate_aeon_impact():
    """Estima impacto do projeto AEON na memória"""
    print("🧬 ESTIMATIVA IMPACTO AEON")
    print("=" * 50)
    
    # Processo atual (este script)
    current_memory = psutil.Process().memory_info().rss / (1024 * 1024)
    
    print(f"📊 Impacto estimado:")
    print(f"• Script atual: {current_memory:.2f} MB")
    print(f"• VS Code (estimado): 200-400 MB")
    print(f"• Python interpretador: 10-20 MB")
    print(f"• Bibliotecas carregadas: 50-100 MB")
    print(f"• Total estimado AEON: 260-520 MB")
    print()
    
    memory = psutil.virtual_memory()
    impact_percent = ((260 + 520) / 2) / (memory.total / (1024**2)) * 100
    print(f"🎯 Impacto médio no sistema: ~{impact_percent:.2f}%")

def main():
    print(f"🔍 ANÁLISE DE MEMÓRIA RAM - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    try:
        check_system_memory()
        check_python_processes()
        check_vscode_processes()
        check_current_process()
        estimate_aeon_impact()
        
        print("✅ Análise completa!")
        
    except Exception as e:
        print(f"❌ Erro durante análise: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
