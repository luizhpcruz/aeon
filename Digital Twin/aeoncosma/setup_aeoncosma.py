"""
⚙️ AEONCOSMA Setup Script - Instalação e Configuração Automática
Script para configurar todo o ambiente AEONCOSMA automaticamente
Copyright 2025 - Luiz H. P. Cruz
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
import platform
import shutil
import urllib.request
import zipfile
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AEONCOSMASetup:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.system = platform.system()
        self.python_version = sys.version_info
        self.setup_complete = False
        
        # Requisitos do sistema
        self.requirements = [
            "streamlit>=1.28.0",
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
            "plotly>=5.17.0",
            "pandas>=2.1.0",
            "numpy>=1.24.0",
            "networkx>=3.2.0",
            "asyncio-mqtt>=0.13.0",
            "cryptography>=41.0.0",
            "websockets>=12.0",
            "psutil>=5.9.0",
            "aiohttp>=3.9.0",
            "pydantic>=2.5.0",
            "python-multipart>=0.0.6",
            "jinja2>=3.1.0",
            "seaborn>=0.13.0",
            "matplotlib>=3.8.0",
            "scipy>=1.11.0",
            "jupyter>=1.0.0"
        ]
        
        # Estrutura de diretórios
        self.directory_structure = [
            "logs",
            "data",
            "config",
            "temp",
            "backups",
            "reports",
            "notebooks"
        ]
    
    def display_banner(self):
        """Exibir banner de setup"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                  ⚙️ AEONCOSMA SETUP ⚙️                      ║
║              Instalação e Configuração Automática            ║
║                                                              ║
║  🐍 Python • 📦 Packages • 🗂️ Structure • ⚙️ Config         ║
║                                                              ║
║              Desenvolvido por Luiz H. P. Cruz               ║
║                      Copyright 2025                         ║
╚══════════════════════════════════════════════════════════════╝

🚀 Configurando ambiente AEONCOSMA...
"""
        print(banner)
        logger.info("AEONCOSMA Setup - Iniciado")
    
    def check_system_requirements(self) -> bool:
        """Verificar requisitos do sistema"""
        logger.info("🔍 Verificando requisitos do sistema...")
        
        # Verificar versão do Python
        if self.python_version < (3, 8):
            logger.error(f"❌ Python 3.8+ necessário. Atual: {sys.version}")
            return False
        
        logger.info(f"✅ Python {sys.version} - OK")
        
        # Verificar sistema operacional
        logger.info(f"✅ Sistema: {self.system} - OK")
        
        # Verificar espaço em disco (mínimo 1GB)
        try:
            disk_usage = shutil.disk_usage(self.base_path)
            free_gb = disk_usage.free / (1024**3)
            
            if free_gb < 1.0:
                logger.error(f"❌ Espaço insuficiente em disco. Necessário: 1GB, Disponível: {free_gb:.2f}GB")
                return False
            
            logger.info(f"✅ Espaço em disco: {free_gb:.2f}GB - OK")
            
        except Exception as e:
            logger.warning(f"⚠️ Não foi possível verificar espaço em disco: {e}")
        
        # Verificar conectividade com internet
        try:
            urllib.request.urlopen('https://pypi.org', timeout=10)
            logger.info("✅ Conectividade com internet - OK")
        except:
            logger.warning("⚠️ Sem conectividade com internet - Modo offline")
        
        return True
    
    def create_directory_structure(self):
        """Criar estrutura de diretórios"""
        logger.info("📁 Criando estrutura de diretórios...")
        
        for directory in self.directory_structure:
            dir_path = self.base_path / directory
            try:
                dir_path.mkdir(exist_ok=True)
                logger.info(f"✅ Diretório criado: {directory}")
            except Exception as e:
                logger.error(f"❌ Erro criando {directory}: {e}")
        
        # Criar subdiretórios específicos
        subdirs = [
            "data/p2p_network",
            "data/blockchain",
            "data/ai_models",
            "data/crypto_keys",
            "data/quantum_states",
            "data/cosmos_data",
            "logs/p2p",
            "logs/api",
            "logs/tests",
            "config/nodes",
            "config/network",
            "notebooks/examples",
            "reports/tests",
            "reports/performance"
        ]
        
        for subdir in subdirs:
            sub_path = self.base_path / subdir
            try:
                sub_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"✅ Subdiretório criado: {subdir}")
            except Exception as e:
                logger.error(f"❌ Erro criando {subdir}: {e}")
    
    def install_python_packages(self) -> bool:
        """Instalar pacotes Python necessários"""
        logger.info("📦 Instalando pacotes Python...")
        
        # Atualizar pip primeiro
        try:
            logger.info("⬆️ Atualizando pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True, text=True)
            logger.info("✅ Pip atualizado")
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ Erro atualizando pip: {e}")
        
        # Criar requirements.txt
        requirements_file = self.base_path / "requirements.txt"
        with open(requirements_file, 'w') as f:
            for req in self.requirements:
                f.write(f"{req}\n")
        
        logger.info(f"📄 Arquivo requirements.txt criado com {len(self.requirements)} pacotes")
        
        # Instalar pacotes
        try:
            logger.info("⏳ Instalando pacotes (isso pode demorar alguns minutos)...")
            
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], capture_output=True, text=True, timeout=600)  # 10 minutos timeout
            
            if result.returncode == 0:
                logger.info("✅ Todos os pacotes instalados com sucesso")
                return True
            else:
                logger.error(f"❌ Erro na instalação: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Timeout na instalação de pacotes")
            return False
        except Exception as e:
            logger.error(f"❌ Erro instalando pacotes: {e}")
            return False
    
    def create_configuration_files(self):
        """Criar arquivos de configuração"""
        logger.info("⚙️ Criando arquivos de configuração...")
        
        # Configuração principal
        main_config = {
            "system": {
                "name": "AEONCOSMA",
                "version": "1.0.0",
                "author": "Luiz H. P. Cruz",
                "installation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": platform.platform()
            },
            "network": {
                "max_nodes": 100,
                "default_port_range": [8000, 9000],
                "connection_timeout": 30,
                "heartbeat_interval": 10,
                "max_connections_per_node": 20
            },
            "services": {
                "streamlit_port": 8501,
                "fastapi_port": 8000,
                "p2p_network_port": 8002,
                "jupyter_port": 8888,
                "auto_start": ["p2p_network", "streamlit_monitor"],
                "auto_open_browser": True
            },
            "security": {
                "encryption_algorithm": "AES-256-GCM",
                "key_exchange": "RSA-4096",
                "hash_algorithm": "SHA3-256",
                "enable_quantum_security": True
            },
            "performance": {
                "max_memory_usage_mb": 4096,
                "max_cpu_usage_percent": 80,
                "max_disk_usage_gb": 10,
                "cleanup_interval_hours": 24
            },
            "logging": {
                "level": "INFO",
                "max_file_size_mb": 100,
                "backup_count": 5,
                "enable_console_logging": True
            }
        }
        
        config_file = self.base_path / "config" / "aeoncosma_config.json"
        with open(config_file, 'w') as f:
            json.dump(main_config, f, indent=2)
        
        logger.info("✅ Configuração principal criada")
        
        # Configuração de rede P2P
        p2p_config = {
            "network_topology": "mesh",
            "discovery_protocol": "mdns",
            "routing_algorithm": "shortest_path",
            "consensus_algorithm": "pbft",
            "block_time_seconds": 30,
            "transaction_pool_size": 1000,
            "node_types": {
                "master": {"max_instances": 3, "capabilities": ["coordination", "consensus"]},
                "energy": {"max_instances": 20, "capabilities": ["monitoring", "data_collection"]},
                "ai": {"max_instances": 10, "capabilities": ["training", "inference"]},
                "crypto": {"max_instances": 8, "capabilities": ["encryption", "signing"]},
                "quantum": {"max_instances": 5, "capabilities": ["quantum_comm", "entanglement"]},
                "cosmos": {"max_instances": 3, "capabilities": ["analysis", "modeling"]},
                "backup": {"max_instances": 10, "capabilities": ["replication", "recovery"]},
                "edge": {"max_instances": 15, "capabilities": ["local_processing", "caching"]}
            }
        }
        
        p2p_config_file = self.base_path / "config" / "p2p_network_config.json"
        with open(p2p_config_file, 'w') as f:
            json.dump(p2p_config, f, indent=2)
        
        logger.info("✅ Configuração P2P criada")
        
        # Configuração de testes
        test_config = {
            "test_suites": {
                "latency": {"enabled": True, "timeout": 300, "samples": 100},
                "throughput": {"enabled": True, "duration": 60, "concurrent_threads": 10},
                "scalability": {"enabled": True, "max_nodes": 500, "step_size": 25},
                "failure_recovery": {"enabled": True, "scenarios": 7, "recovery_timeout": 60},
                "stress": {"enabled": True, "multipliers": [5, 10, 15, 20], "duration": 30},
                "security": {"enabled": True, "vulnerability_scan": True, "penetration_test": False}
            },
            "reporting": {
                "generate_html": True,
                "generate_json": True,
                "generate_csv": True,
                "auto_upload": False
            },
            "thresholds": {
                "latency_ms": 100,
                "throughput_msgs_sec": 1000,
                "success_rate": 0.95,
                "availability": 0.99,
                "security_score": 80
            }
        }
        
        test_config_file = self.base_path / "config" / "testing_config.json"
        with open(test_config_file, 'w') as f:
            json.dump(test_config, f, indent=2)
        
        logger.info("✅ Configuração de testes criada")
    
    def create_sample_notebooks(self):
        """Criar notebooks de exemplo"""
        logger.info("📓 Criando notebooks de exemplo...")
        
        # Notebook de introdução
        intro_notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# 🌐 AEONCOSMA Network - Introdução\n",
                        "\n",
                        "Este notebook demonstra como usar a rede P2P AEONCOSMA.\n",
                        "\n",
                        "**Desenvolvido por:** Luiz H. P. Cruz  \n",
                        "**Data:** " + time.strftime("%Y-%m-%d") + "\n",
                        "\n",
                        "## 🚀 Primeiros Passos\n",
                        "\n",
                        "1. Inicialize a rede P2P\n",
                        "2. Conecte nós\n",
                        "3. Envie mensagens\n",
                        "4. Monitore performance"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Importar bibliotecas necessárias\n",
                        "import sys\n",
                        "import os\n",
                        "sys.path.append('..')\n",
                        "\n",
                        "from expanded_p2p_network import ExpandedP2PNetwork\n",
                        "from network_testing_suite import NetworkTestSuite\n",
                        "import asyncio\n",
                        "import pandas as pd\n",
                        "import plotly.express as px\n",
                        "\n",
                        "print('✅ Bibliotecas importadas com sucesso')"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# Criar e inicializar rede P2P\n",
                        "network = ExpandedP2PNetwork()\n",
                        "network.create_node_fleet(count=10)\n",
                        "\n",
                        "print(f'🌐 Rede criada com {len(network.nodes)} nós')\n",
                        "print('✅ Pronto para usar!')"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "name": "python",
                    "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        intro_file = self.base_path / "notebooks" / "01_introducao_aeoncosma.ipynb"
        with open(intro_file, 'w') as f:
            json.dump(intro_notebook, f, indent=2)
        
        logger.info("✅ Notebook de introdução criado")
    
    def create_startup_scripts(self):
        """Criar scripts de inicialização"""
        logger.info("🚀 Criando scripts de inicialização...")
        
        # Script para Windows
        if self.system == "Windows":
            bat_script = f"""@echo off
echo 🌐 Iniciando AEONCOSMA Engine...
cd /d "{self.base_path}"
python aeoncosma_launcher.py
pause
"""
            
            bat_file = self.base_path / "start_aeoncosma.bat"
            with open(bat_file, 'w') as f:
                f.write(bat_script)
            
            logger.info("✅ Script Windows (.bat) criado")
        
        # Script para Unix/Linux/Mac
        if self.system in ["Linux", "Darwin"]:
            sh_script = f"""#!/bin/bash
echo "🌐 Iniciando AEONCOSMA Engine..."
cd "{self.base_path}"
python3 aeoncosma_launcher.py
"""
            
            sh_file = self.base_path / "start_aeoncosma.sh"
            with open(sh_file, 'w') as f:
                f.write(sh_script)
            
            # Tornar executável
            os.chmod(sh_file, 0o755)
            
            logger.info("✅ Script Unix (.sh) criado")
        
        # Script Python universal
        py_script = f'''#!/usr/bin/env python3
"""
🚀 AEONCOSMA Quick Start Script
Script de inicialização rápida do sistema
"""

import sys
import os
from pathlib import Path

# Adicionar diretório base ao path
base_path = Path(__file__).parent
sys.path.insert(0, str(base_path))

try:
    from aeoncosma_launcher import AEONCOSMALauncher
    import asyncio
    
    if __name__ == "__main__":
        print("🌐 AEONCOSMA Quick Start")
        launcher = AEONCOSMALauncher()
        asyncio.run(launcher.run())
        
except ImportError as e:
    print(f"❌ Erro de importação: {{e}}")
    print("Execute primeiro: python setup_aeoncosma.py")
except Exception as e:
    print(f"❌ Erro: {{e}}")
'''
        
        py_file = self.base_path / "quick_start.py"
        with open(py_file, 'w') as f:
            f.write(py_script)
        
        logger.info("✅ Script Python universal criado")
    
    def create_readme_files(self):
        """Criar arquivos README"""
        logger.info("📚 Criando documentação...")
        
        main_readme = f"""# 🌐 AEONCOSMA Engine

Sistema integrado de rede P2P com módulos avançados de IA, Criptografia, Quantum e Cosmos.

**Desenvolvido por:** Luiz H. P. Cruz  
**Data de Instalação:** {time.strftime("%Y-%m-%d %H:%M:%S")}  
**Versão:** 1.0.0

## 🚀 Início Rápido

### Windows
```bash
start_aeoncosma.bat
```

### Linux/Mac
```bash
./start_aeoncosma.sh
```

### Python Universal
```bash
python quick_start.py
```

## 📊 Interfaces Disponíveis

- **Monitor P2P:** http://localhost:8501
- **API Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Jupyter Notebooks:** http://localhost:8888

## 🛠️ Comandos Principais

- `s` - Status dos serviços
- `r` - Reiniciar serviços  
- `t` - Executar testes
- `b` - Abrir navegador
- `q` - Parar sistema

## 📁 Estrutura do Projeto

```
aeoncosma/
├── 🚀 aeoncosma_launcher.py      # Launcher principal
├── 🌐 expanded_p2p_network.py    # Rede P2P expandida
├── 📊 p2p_monitor_dashboard.py   # Dashboard Streamlit
├── 🧪 network_testing_suite.py   # Suite de testes
├── ⚙️ setup_aeoncosma.py         # Script de instalação
├── 📁 config/                    # Configurações
├── 📁 data/                      # Dados da rede
├── 📁 logs/                      # Logs do sistema
├── 📁 notebooks/                 # Jupyter notebooks
└── 📁 reports/                   # Relatórios de testes
```

## 🔧 Módulos Integrados

- **🧠 IA Module:** Treinamento e inferência
- **🔐 Crypto Module:** Criptografia enterprise  
- **📡 Quantum Module:** Comunicação quântica
- **🌌 Cosmos Module:** Análise cosmológica
- **⛓️ Blockchain Module:** Sistema VERITAS

## 🧪 Testes Disponíveis

- Latência de rede
- Throughput e performance
- Escalabilidade 
- Recuperação de falhas
- Testes de stress
- Balanceamento de carga
- Consenso distribuído
- Segurança e vulnerabilidades

## 🆘 Suporte

Para problemas ou dúvidas:
- 📧 Email: luiz@aeon.energy.br
- 🐛 Issues: GitHub repository
- 📚 Docs: `/notebooks/` directory

---

**💎 "O futuro da energia é descentralizado, inteligente e brasileiro!" 🇧🇷**
"""
        
        readme_file = self.base_path / "README_AEONCOSMA.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(main_readme)
        
        logger.info("✅ README principal criado")
    
    def verify_installation(self) -> bool:
        """Verificar instalação"""
        logger.info("✅ Verificando instalação...")
        
        # Verificar arquivos principais
        required_files = [
            "aeoncosma_launcher.py",
            "expanded_p2p_network.py", 
            "p2p_monitor_dashboard.py",
            "network_testing_suite.py",
            "config/aeoncosma_config.json",
            "requirements.txt",
            "README_AEONCOSMA.md"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.base_path / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            logger.error(f"❌ Arquivos faltando: {missing_files}")
            return False
        
        logger.info("✅ Todos os arquivos principais encontrados")
        
        # Verificar diretórios
        missing_dirs = []
        for directory in self.directory_structure:
            dir_path = self.base_path / directory
            if not dir_path.exists():
                missing_dirs.append(directory)
        
        if missing_dirs:
            logger.error(f"❌ Diretórios faltando: {missing_dirs}")
            return False
        
        logger.info("✅ Estrutura de diretórios OK")
        
        # Teste de importação
        try:
            import streamlit
            import fastapi
            import plotly
            import pandas
            import numpy
            import networkx
            logger.info("✅ Importações principais OK")
        except ImportError as e:
            logger.error(f"❌ Erro de importação: {e}")
            return False
        
        return True
    
    def display_completion_message(self):
        """Exibir mensagem de conclusão"""
        completion = f"""
╔══════════════════════════════════════════════════════════════╗
║                   ✅ INSTALAÇÃO CONCLUÍDA ✅                ║
║                                                              ║
║  🎉 AEONCOSMA Engine foi instalado com sucesso!             ║
║                                                              ║
║  📋 PRÓXIMOS PASSOS:                                         ║
║                                                              ║
║  1️⃣  Execute o launcher:                                     ║
║      python aeoncosma_launcher.py                           ║
║                                                              ║
║  2️⃣  Ou use os scripts de início:                           ║
║      • Windows: start_aeoncosma.bat                         ║
║      • Linux/Mac: ./start_aeoncosma.sh                      ║
║      • Universal: python quick_start.py                     ║
║                                                              ║
║  3️⃣  Acesse as interfaces:                                  ║
║      • Monitor: http://localhost:8501                       ║
║      • API: http://localhost:8000/docs                      ║
║                                                              ║
║  📚 Documentação completa em README_AEONCOSMA.md            ║
║  📓 Exemplos em notebooks/                                  ║
║                                                              ║
║              Desenvolvido por Luiz H. P. Cruz               ║
║                      Copyright 2025                         ║
╚══════════════════════════════════════════════════════════════╝

🚀 Pronto para revolucionar a rede P2P brasileira!
"""
        print(completion)
        logger.info("🎉 Setup AEONCOSMA concluído com sucesso!")
    
    def run_setup(self) -> bool:
        """Executar setup completo"""
        self.display_banner()
        
        try:
            # Verificar requisitos
            if not self.check_system_requirements():
                return False
            
            # Criar estrutura
            self.create_directory_structure()
            
            # Instalar pacotes
            if not self.install_python_packages():
                logger.error("❌ Falha na instalação de pacotes")
                return False
            
            # Criar configurações
            self.create_configuration_files()
            
            # Criar notebooks
            self.create_sample_notebooks()
            
            # Criar scripts
            self.create_startup_scripts()
            
            # Criar documentação
            self.create_readme_files()
            
            # Verificar instalação
            if not self.verify_installation():
                return False
            
            # Conclusão
            self.display_completion_message()
            self.setup_complete = True
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro crítico no setup: {e}")
            return False

def main():
    """Função principal do setup"""
    try:
        setup = AEONCOSMASetup()
        success = setup.run_setup()
        
        if success:
            print("\n🎯 Quer iniciar o sistema agora? (s/n): ", end="")
            choice = input().strip().lower()
            
            if choice in ['s', 'sim', 'y', 'yes']:
                print("\n🚀 Iniciando AEONCOSMA...")
                time.sleep(2)
                
                # Tentar importar e executar o launcher
                try:
                    from aeoncosma_launcher import AEONCOSMALauncher
                    import asyncio
                    
                    launcher = AEONCOSMALauncher()
                    asyncio.run(launcher.run())
                    
                except ImportError:
                    print("Execute: python aeoncosma_launcher.py")
                except Exception as e:
                    print(f"Erro: {e}")
            else:
                print("\n👋 Execute 'python aeoncosma_launcher.py' quando quiser iniciar!")
        
        return success
        
    except KeyboardInterrupt:
        print("\n🛑 Setup interrompido pelo usuário")
        return False
    except Exception as e:
        print(f"❌ Erro fatal no setup: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
