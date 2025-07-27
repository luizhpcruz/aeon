#!/usr/bin/env python3
"""
📊 AEONCOSMA SYSTEM MONITOR
Monitor de recursos do sistema usando bibliotecas padrão
Desenvolvido por Luiz Cruz - 2025
"""

import os
import platform
import sys
import time
from datetime import datetime

def get_system_info():
    """Coleta informações básicas do sistema"""
    print("🖥️ AEONCOSMA SYSTEM MONITOR")
    print("=" * 50)
    print(f"🕒 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"💻 Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"⚙️ Arquitetura: {platform.machine()}")
    print(f"💾 Processador: {platform.processor()}")
    
    # Informações de memória (Windows)
    if platform.system() == "Windows":
        try:
            import subprocess
            result = subprocess.run(
                ['wmic', 'OS', 'get', 'TotalVisibleMemorySize,FreePhysicalMemory', '/format:value'],
                capture_output=True, text=True
            )
            
            lines = result.stdout.strip().split('\n')
            memory_data = {}
            
            for line in lines:
                if '=' in line:
                    key, value = line.split('=', 1)
                    if value.strip():
                        memory_data[key] = int(value) * 1024  # Convert KB to bytes
            
            if 'TotalVisibleMemorySize' in memory_data and 'FreePhysicalMemory' in memory_data:
                total_memory = memory_data['TotalVisibleMemorySize']
                free_memory = memory_data['FreePhysicalMemory']
                used_memory = total_memory - free_memory
                usage_percent = (used_memory / total_memory) * 100
                
                print(f"💾 RAM Total: {total_memory / (1024**3):.1f} GB")
                print(f"💾 RAM Usada: {used_memory / (1024**3):.1f} GB")
                print(f"💾 RAM Livre: {free_memory / (1024**3):.1f} GB")
                print(f"💾 RAM Uso: {usage_percent:.1f}%")
            
        except Exception as e:
            print(f"⚠️ Não foi possível obter info de memória: {e}")
    
    # Informações de CPU (aproximada)
    try:
        cpu_count = os.cpu_count()
        print(f"🖥️ CPUs: {cpu_count} cores")
        
        # Teste simples de carga da CPU
        start_time = time.time()
        iterations = 100000
        for i in range(iterations):
            pass
        end_time = time.time()
        
        cpu_test_time = end_time - start_time
        print(f"🔄 Teste CPU: {cpu_test_time:.4f}s para {iterations} iterações")
        
    except Exception as e:
        print(f"⚠️ Erro no teste de CPU: {e}")

def get_process_info():
    """Informações sobre processos Python ativos"""
    print("\n🐍 PROCESSOS PYTHON ATIVOS:")
    print("-" * 50)
    
    try:
        if platform.system() == "Windows":
            import subprocess
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python*', '/FO', 'CSV'],
                capture_output=True, text=True
            )
            
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                for line in lines[1:]:  # Skip header
                    if 'python' in line.lower():
                        parts = line.replace('"', '').split(',')
                        if len(parts) >= 5:
                            name = parts[0]
                            pid = parts[1]
                            memory = parts[4]
                            print(f"   🔹 {name} (PID: {pid}) - Memória: {memory}")
            else:
                print("   ✅ Nenhum processo Python ativo encontrado")
                
    except Exception as e:
        print(f"   ⚠️ Erro ao listar processos: {e}")

def get_network_info():
    """Informações básicas de rede"""
    print("\n🌐 INFORMAÇÕES DE REDE:")
    print("-" * 50)
    
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"   🖥️ Hostname: {hostname}")
        print(f"   🌐 IP Local: {local_ip}")
        
        # Testa se as portas do AEONCOSMA estão livres
        test_ports = [9000, 20000, 25000, 30000]
        print("\n   🔌 Status das Portas AEONCOSMA:")
        
        for port in test_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('127.0.0.1', port))
                
                if result == 0:
                    print(f"      ❌ Porta {port}: EM USO")
                else:
                    print(f"      ✅ Porta {port}: LIVRE")
                
                sock.close()
                
            except Exception as e:
                print(f"      ⚠️ Porta {port}: ERRO - {e}")
                
    except Exception as e:
        print(f"   ⚠️ Erro nas informações de rede: {e}")

def get_test_summary():
    """Resumo dos arquivos de teste gerados"""
    print("\n📁 ARQUIVOS DE TESTE GERADOS:")
    print("-" * 50)
    
    test_files = [
        "simplified_test_report.txt",
        "simplified_test_data.csv", 
        "simplified_ecosystem_test.log",
        "AEONCOSMA_VALIDATION_MILESTONE.md",
        "ecosystem_validation_test.py",
        "final_validation_test.py",
        "realtime_monitoring.py"
    ]
    
    for filename in test_files:
        if os.path.exists(filename):
            try:
                size = os.path.getsize(filename)
                mod_time = os.path.getmtime(filename)
                mod_date = datetime.fromtimestamp(mod_time).strftime('%d/%m/%Y %H:%M:%S')
                
                if size < 1024:
                    size_str = f"{size} bytes"
                elif size < 1024*1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                
                print(f"   ✅ {filename} - {size_str} - {mod_date}")
                
            except Exception as e:
                print(f"   ⚠️ {filename} - Erro: {e}")
        else:
            print(f"   ❌ {filename} - Não encontrado")

def main():
    """Função principal do monitor"""
    get_system_info()
    get_process_info()
    get_network_info()
    get_test_summary()
    
    print("\n" + "=" * 50)
    print("🎯 SISTEMA MONITORADO COM SUCESSO!")
    print("✅ Recursos verificados após teste AEONCOSMA")
    print("📊 Todas as informações coletadas")

if __name__ == "__main__":
    main()
