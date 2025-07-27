#!/usr/bin/env python3
"""
🔧 AEONCOSMA ECOSYSTEM SETUP
Configuração Completa do Ambiente de Teste
Desenvolvido por Luiz Cruz - 2025
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def install_package(package):
    """Instala um pacote Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ requerido")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def setup_ecosystem_environment():
    """Configura ambiente completo para teste de ecossistema"""
    print("🔧 AEONCOSMA ECOSYSTEM SETUP")
    print("=" * 50)
    
    # Verifica Python
    if not check_python_version():
        return False
    
    print("\n📦 Instalando dependências...")
    
    # Dependências essenciais
    packages = [
        "psutil",           # Monitoramento de sistema
        "prometheus_client", # Métricas Prometheus
        "requests",         # HTTP requests
        "websockets",       # WebSocket support
        "aiohttp",          # Async HTTP
        "asyncio",          # Async support
        "numpy",            # Computação numérica
        "pandas",           # Análise de dados
    ]
    
    failed_packages = []
    for package in packages:
        print(f"   📥 Instalando {package}...")
        if install_package(package):
            print(f"   ✅ {package} instalado")
        else:
            print(f"   ❌ Falha ao instalar {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️ Pacotes não instalados: {', '.join(failed_packages)}")
        print("💡 Execute manualmente: pip install " + " ".join(failed_packages))
    
    # Cria estrutura de diretórios
    print("\n📁 Criando estrutura de diretórios...")
    
    directories = [
        "logs",
        "metrics", 
        "reports",
        "data/ecosystem",
        "data/monitoring",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}/")
    
    # Cria arquivos de configuração
    print("\n⚙️ Criando arquivos de configuração...")
    
    # Configuração do Prometheus
    prometheus_config = """
# AEONCOSMA Prometheus Configuration
global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: 'aeoncosma-ecosystem'
    static_configs:
      - targets: ['localhost:8001']
    scrape_interval: 2s
    metrics_path: /metrics

  - job_name: 'system-metrics'
    static_configs:
      - targets: ['localhost:8002']
    scrape_interval: 5s
"""
    
    with open("config/prometheus.yml", "w") as f:
        f.write(prometheus_config)
    print("   ✅ config/prometheus.yml")
    
    # Configuração do teste de ecossistema
    ecosystem_config = {
        "test_settings": {
            "max_nodes": 1000,
            "base_port": 20000,
            "monitoring_port": 8001,
            "test_duration_seconds": 1800,
            "phases": {
                "bootstrap": 10,
                "early_network": 50,
                "growth_phase": 200,
                "mature_network": 500,
                "stress_test": 1000
            }
        },
        "monitoring": {
            "prometheus_enabled": True,
            "real_time_dashboard": True,
            "log_level": "INFO",
            "metrics_retention_hours": 24
        },
        "network_settings": {
            "connection_timeout": 3,
            "max_connections_per_node": 8,
            "peer_discovery_interval": 10,
            "consensus_threshold": 0.51
        },
        "business_metrics": {
            "target_arr_usd": 5000000,
            "scalability_threshold": 500,
            "commercial_validation_nodes": 100
        }
    }
    
    with open("config/ecosystem_config.json", "w") as f:
        json.dump(ecosystem_config, f, indent=2)
    print("   ✅ config/ecosystem_config.json")
    
    # Script de inicialização rápida
    quick_start_script = """@echo off
echo 🚀 AEONCOSMA ECOSYSTEM QUICK START
echo ================================

echo 📊 Iniciando monitoramento em tempo real...
start python realtime_monitoring.py

timeout /t 3 /nobreak >nul

echo 🌐 Iniciando teste de validação do ecossistema...
python ecosystem_validation_test.py

echo ✅ Teste concluído!
pause
"""
    
    with open("start_ecosystem_test.bat", "w") as f:
        f.write(quick_start_script)
    print("   ✅ start_ecosystem_test.bat")
    
    # README para o teste
    readme_content = """# 🌟 AEONCOSMA ECOSYSTEM VALIDATION

## Visão Geral
Este é o teste definitivo de escalabilidade do AEONCOSMA - uma simulação completa de ecossistema de mercado descentralizado com até 1000 nós P2P.

## Objetivo
Validar a tese central de que o AEONCOSMA pode operar como uma arquitetura verdadeiramente escalável e descentralizada, transformando alegações em fatos auditáveis.

## Componentes do Teste

### 1. ecosystem_validation_test.py
- **Propósito**: Teste principal de validação do ecossistema
- **Capacidade**: Até 1000 nós simultâneos
- **Duração**: 30 minutos de teste contínuo
- **Métricas**: Escalabilidade, performance, consenso, trading

### 2. realtime_monitoring.py  
- **Propósito**: Monitoramento em tempo real com Prometheus
- **Dashboard**: Terminal interativo + métricas web
- **Métricas**: Sistema, rede, negócio, performance
- **Port**: http://localhost:8001/metrics

## Execução Rápida

### Opção 1: Script Automático
```cmd
start_ecosystem_test.bat
```

### Opção 2: Manual
```cmd
# Terminal 1 - Monitoramento
python realtime_monitoring.py

# Terminal 2 - Teste de Ecossistema  
python ecosystem_validation_test.py
```

## Métricas Críticas a Observar

### 📊 Escalabilidade
- Máximo de nós simultâneos alcançado
- Taxa de sucesso de conexões P2P
- Tempo de propagação de mensagens
- Estabilidade da rede sob carga

### 💻 Performance  
- Uso de CPU e memória por nó
- Latência de rede P2P
- Throughput de transações
- Tempo de consenso

### 💰 Valor Comercial
- ARR estimado baseado na escala
- Score de escalabilidade (0-100)
- Validação de deployment enterprise
- Métricas auditáveis para investidores

## Critérios de Sucesso

### 🥇 EXCELENTE (500+ nós)
- Arquitetura altamente escalável validada
- Pronto para deployment global
- $5M+ ARR potencial comprovado
- **TESE DE ESCALABILIDADE COMPROVADA**

### 🥈 MUITO BOM (200+ nós)  
- Escalável para médias empresas
- Adequado para redes regionais
- $2M+ ARR potencial

### 🥉 BOM (100+ nós)
- Adequado para empresas
- Proof of concept validado
- $1M+ ARR potencial

## Arquivos Gerados

### Logs e Relatórios
- `ecosystem_test.log` - Log detalhado do teste
- `ecosystem_validation_report.txt` - Relatório final
- `ecosystem_metrics.csv` - Dados CSV para análise
- `realtime_monitoring.log` - Log do monitoramento

### Métricas
- `logs/` - Logs detalhados por componente
- `metrics/` - Dados de métricas coletadas  
- `reports/` - Relatórios gerados

## Impacto Comercial

Um teste bem-sucedido transforma o projeto de "promessa tecnológica" para "solução comprovada em escala", com impacto direto em:

- **Validação Técnica**: Prova inquestionável da arquitetura
- **Valor Comercial**: ARR defensável baseado em métricas
- **Atração de Investimento**: Dados auditáveis para VCs
- **Vantagem Competitiva**: Diferencial técnico massivo

## Desenvolvido por Luiz Cruz - 2025
Sistema Proprietário - Todos os Direitos Reservados
"""
    
    with open("ECOSYSTEM_TEST_README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("   ✅ ECOSYSTEM_TEST_README.md")
    
    print("\n🎯 Setup concluído com sucesso!")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("   1. Execute: start_ecosystem_test.bat")
    print("   2. Ou manualmente:")
    print("      - Terminal 1: python realtime_monitoring.py")
    print("      - Terminal 2: python ecosystem_validation_test.py")
    print("   3. Monitore: http://localhost:8001/metrics")
    print("   4. Aguarde relatórios finais")
    
    print(f"\n🌟 PRONTO PARA VALIDAR A TESE DE ESCALABILIDADE!")
    print("   Este teste pode transformar AEONCOSMA de promessa em realidade comprovada.")
    
    return True

if __name__ == "__main__":
    setup_ecosystem_environment()
