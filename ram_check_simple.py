import psutil
import os

# Informações básicas de memória
memory = psutil.virtual_memory()
print("=" * 50)
print("ANÁLISE DE RAM - PROJETO AEON")
print("=" * 50)

print(f"💾 MEMÓRIA TOTAL: {memory.total / (1024**3):.2f} GB")
print(f"📊 MEMÓRIA USADA: {memory.used / (1024**3):.2f} GB ({memory.percent}%)")
print(f"🆓 MEMÓRIA LIVRE: {memory.available / (1024**3):.2f} GB")

print("\n🐍 PROCESSOS PYTHON:")
print("-" * 30)
for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
    try:
        if 'python' in proc.info['name'].lower():
            memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
            print(f"PID {proc.info['pid']:6}: {memory_mb:6.1f} MB - {proc.info['name']}")
    except:
        pass

print(f"\n⚡ PROCESSO ATUAL: {psutil.Process().memory_info().rss / (1024 * 1024):.1f} MB")
print("=" * 50)
