# 📚 AEON ECOSYSTEM - GUIA PASSO A PASSO

## 🎯 VISÃO GERAL

O ecossistema AEON foi dividido em **10 projetos independentes** para facilitar desenvolvimento, manutenção e deployment. Cada projeto tem responsabilidade específica e pode ser desenvolvido/implantado separadamente.

---

## 📁 ESTRUTURA CRIADA

```
📂 aeon-ecosystem/
├── 🔬 aeon-entropy/           # Simulação de entropia e complexidade
├── 🌌 aeon-cosmology/         # Motor cosmológico e observacional  
├── 🧠 aeon-verna/             # Sistema de emergência simbólica V.E.R.N.A.
├── 🤖 aeon-cosma/             # Motor inteligente cosmológico
├── 🕸️ aeon-network/           # Sistema P2P e coordenação de rede
├── 🎯 aeon-coordinator/       # Orquestrador central de serviços
├── 🌐 aeon-api/               # API REST e interfaces de comunicação
├── 🎨 aeon-dashboard/         # Interface web e visualização
├── 🗄️ aeon-data/              # Persistência de dados e analytics
├── ☁️ aeon-deploy/            # Deployment e infraestrutura
├── 📋 docker-compose.json     # Orquestração multi-container
└── 🚀 setup.sh               # Script de configuração automática
```

---

## 🚀 PASSO 1: PREPARAÇÃO DO AMBIENTE

### 1.1 Verificar a Estrutura Criada

```bash
# Navegar para o diretório do ecossistema
cd aeon-ecosystem

# Listar todos os projetos
ls -la
```

### 1.2 Verificar Python e Dependências

```bash
# Verificar versão do Python (recomendado 3.11+)
python --version

# Verificar pip
pip --version

# (Opcional) Criar ambiente virtual global
python -m venv aeon-env
source aeon-env/bin/activate  # Linux/Mac
# ou
aeon-env\Scripts\activate.bat  # Windows
```

---

## 🔧 PASSO 2: CONFIGURAÇÃO INDIVIDUAL DE PROJETOS

### 2.1 Configurar Projeto Específico (Exemplo: aeon-entropy)

```bash
# Navegar para o projeto
cd aeon-entropy

# Verificar estrutura do projeto
ls -la
```

**Estrutura esperada:**
```
aeon-entropy/
├── src/
│   └── entropy_core/
│       ├── __init__.py
│       └── main.py
├── tests/
├── docs/
├── configs/
├── data/
├── logs/
├── requirements.txt
├── Dockerfile
├── pyproject.toml
└── README.md
```

### 2.2 Instalar Dependências

```bash
# Instalar dependências do projeto
pip install -r requirements.txt

# Verificar instalação
pip list
```

### 2.3 Testar Execução

```bash
# Executar o módulo principal
python -m src.entropy_core

# Ou executar main diretamente
python src/entropy_core/main.py
```

---

## 🏗️ PASSO 3: DESENVOLVIMENTO EM PROJETO ESPECÍFICO

### 3.1 Estrutura de Desenvolvimento

```bash
cd aeon-entropy/src/entropy_core/
```

**Arquivo principal:** `main.py`
```python
"""
Entropy and Complexity Simulator - Main Module
"""
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EntropyCore:
    """Main module class"""
    
    def __init__(self):
        self.config = self.load_config()
        self.is_running = False
    
    def load_config(self) -> dict:
        """Load configuration"""
        return {
            "name": "entropy_core",
            "version": "1.0.0",
            "port": 8001
        }
    
    async def start(self):
        """Start the service"""
        logger.info(f"Starting {self.config['name']} v{self.config['version']}")
        self.is_running = True
        
        while self.is_running:
            await self.process()
            await asyncio.sleep(1)
    
    async def process(self):
        """Main processing"""
        logger.debug("Processing entropy calculations...")
        # TODO: Implementar lógica específica de entropia
    
    async def stop(self):
        """Stop the service"""
        logger.info("Stopping service...")
        self.is_running = False

async def main():
    """Main function"""
    service = EntropyCore()
    try:
        await service.start()
    except KeyboardInterrupt:
        await service.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.2 Implementar Lógica Específica

```bash
# Criar módulo adicional para lógica específica
cd src/entropy_core/
touch entropy_simulator.py
```

**Exemplo entropy_simulator.py:**
```python
"""
Simulador de entropia específico
"""
import numpy as np
import matplotlib.pyplot as plt

class EntropySimulator:
    def __init__(self, n_fitas=5, n_ciclos=40):
        self.n_fitas = n_fitas
        self.n_ciclos = n_ciclos
    
    def simulate(self):
        """Executa simulação de entropia"""
        results = []
        for fita in range(self.n_fitas):
            entropy_values = np.random.exponential(2.0, self.n_ciclos)
            results.append({
                'fita': fita,
                'entropy': entropy_values.tolist(),
                'mean': float(np.mean(entropy_values))
            })
        return results
    
    def visualize(self, results):
        """Cria visualização dos resultados"""
        plt.figure(figsize=(10, 6))
        for result in results:
            plt.plot(result['entropy'], label=f"Fita {result['fita']}")
        plt.xlabel('Ciclos')
        plt.ylabel('Entropia')
        plt.title('Simulação de Entropia por Fita')
        plt.legend()
        plt.savefig('data/entropy_simulation.png')
        plt.close()
```

### 3.3 Atualizar main.py para usar o simulador

```python
# Adicionar no início do main.py
from .entropy_simulator import EntropySimulator

# Modificar o método process
async def process(self):
    """Main processing"""
    simulator = EntropySimulator()
    results = simulator.simulate()
    simulator.visualize(results)
    logger.info(f"Processed {len(results)} entropy simulations")
```

---

## 🧪 PASSO 4: TESTES E VALIDAÇÃO

### 4.1 Criar Testes Unitários

```bash
cd tests/
touch test_entropy_core.py
```

**Exemplo test_entropy_core.py:**
```python
"""
Testes para entropy_core
"""
import pytest
import asyncio
from src.entropy_core.main import EntropyCore
from src.entropy_core.entropy_simulator import EntropySimulator

def test_entropy_core_config():
    """Testa configuração do EntropyCore"""
    core = EntropyCore()
    config = core.load_config()
    assert config['name'] == 'entropy_core'
    assert config['port'] == 8001

def test_entropy_simulator():
    """Testa simulador de entropia"""
    simulator = EntropySimulator(n_fitas=3, n_ciclos=10)
    results = simulator.simulate()
    assert len(results) == 3
    assert all('fita' in r and 'entropy' in r for r in results)

@pytest.mark.asyncio
async def test_entropy_core_lifecycle():
    """Testa ciclo de vida do EntropyCore"""
    core = EntropyCore()
    
    # Simular início e parada rápida
    start_task = asyncio.create_task(core.start())
    await asyncio.sleep(0.1)
    await core.stop()
    
    assert not core.is_running
```

### 4.2 Executar Testes

```bash
# Instalar pytest se necessário
pip install pytest pytest-asyncio

# Executar testes
pytest tests/ -v

# Executar com coverage
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

---

## 🐳 PASSO 5: CONTAINERIZAÇÃO

### 5.1 Testar Docker Build

```bash
# Build da imagem Docker
docker build -t aeon-entropy .

# Verificar imagem criada
docker images | grep aeon-entropy
```

### 5.2 Executar Container

```bash
# Executar container
docker run -p 8001:8001 aeon-entropy

# Executar em background
docker run -d -p 8001:8001 --name entropy-service aeon-entropy

# Verificar logs
docker logs entropy-service

# Parar container
docker stop entropy-service
```

---

## 🌐 PASSO 6: INTEGRAÇÃO MULTI-PROJETOS

### 6.1 Configurar Múltiplos Projetos

```bash
# Voltar para diretório principal
cd ..

# Configurar outro projeto (exemplo: aeon-coordinator)
cd aeon-coordinator
pip install -r requirements.txt
```

### 6.2 Usar Docker Compose

```bash
# Voltar para raiz do ecossistema
cd ..

# Verificar docker-compose.json
cat docker-compose.json

# Iniciar todos os serviços
docker-compose up

# Iniciar em background
docker-compose up -d

# Verificar status
docker-compose ps

# Parar todos os serviços
docker-compose down
```

---

## 🔧 PASSO 7: DESENVOLVIMENTO AVANÇADO

### 7.1 Comunicação Entre Projetos

**Exemplo de API client (aeon-api):**
```python
import requests

class AeonAPIClient:
    def __init__(self, base_url="http://localhost"):
        self.base_url = base_url
    
    def get_entropy_data(self):
        """Obter dados do serviço de entropia"""
        response = requests.get(f"{self.base_url}:8001/entropy")
        return response.json()
    
    def get_cosmology_data(self):
        """Obter dados do serviço de cosmologia"""
        response = requests.get(f"{self.base_url}:8002/cosmology")
        return response.json()
```

### 7.2 Configuração de Environment

**Criar .env para cada projeto:**
```bash
# aeon-entropy/.env
ENTROPY_PORT=8001
ENTROPY_DEBUG=true
ENTROPY_N_FITAS=5
ENTROPY_N_CICLOS=40

# aeon-coordinator/.env
COORDINATOR_PORT=8006
COORDINATOR_SERVICES=entropy,cosmology,verna,cosma
```

### 7.3 Monitoramento e Logs

```python
# Configuração avançada de logging
import logging
from loguru import logger

# Remover handler padrão
logger.remove()

# Adicionar handler para arquivo
logger.add(
    "logs/entropy_{time}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)

# Adicionar handler para console
logger.add(
    lambda msg: print(msg, end=""),
    colorize=True,
    level="DEBUG"
)
```

---

## 📊 PASSO 8: MONITORAMENTO E DEPLOYMENT

### 8.1 Health Checks

```python
# Adicionar endpoint de health check
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "aeon-entropy",
        "version": "1.0.0"
    }
```

### 8.2 Métricas e Observabilidade

```bash
# Instalar dependências de monitoramento
pip install prometheus-client grafana-api

# Configurar coleta de métricas
# (Implementar em cada projeto conforme necessário)
```

---

## 🎯 PASSO 9: FLUXO DE TRABALHO RECOMENDADO

### 9.1 Desenvolvimento Diário

```bash
# 1. Escolher projeto para trabalhar
cd aeon-entropy

# 2. Ativar ambiente virtual
source ../aeon-env/bin/activate

# 3. Atualizar dependências se necessário
pip install -r requirements.txt

# 4. Executar testes antes de começar
pytest tests/

# 5. Desenvolver funcionalidades
# (editar arquivos em src/)

# 6. Testar durante desenvolvimento
python -m src.entropy_core

# 7. Executar testes após mudanças
pytest tests/

# 8. Commit das mudanças
git add .
git commit -m "feat: implement entropy calculation improvements"
```

### 9.2 Integração e Deploy

```bash
# 1. Testar integração local
docker-compose up

# 2. Executar testes de integração
# (implementar conforme necessário)

# 3. Build para produção
docker build -t aeon-entropy:prod .

# 4. Deploy (exemplo com registry)
docker tag aeon-entropy:prod registry.company.com/aeon-entropy:latest
docker push registry.company.com/aeon-entropy:latest
```

---

## 🆘 TROUBLESHOOTING

### Problemas Comuns:

**1. Erro de import:**
```bash
# Definir PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

**2. Conflito de portas:**
```bash
# Verificar portas em uso
netstat -tulpn | grep :8001

# Matar processo na porta
kill -9 $(lsof -t -i:8001)
```

**3. Dependências não instaladas:**
```bash
# Reinstalar requirements
pip install -r requirements.txt --force-reinstall
```

**4. Problemas com Docker:**
```bash
# Limpar containers e imagens
docker system prune -a

# Rebuild sem cache
docker build --no-cache -t aeon-entropy .
```

---

## 📝 PRÓXIMOS PASSOS

1. **Escolher 2-3 projetos prioritários** para desenvolvimento inicial
2. **Implementar lógica específica** em cada projeto
3. **Definir APIs de comunicação** entre projetos
4. **Configurar CI/CD pipeline** para automação
5. **Implementar monitoramento** e observabilidade
6. **Documentar APIs** com OpenAPI/Swagger
7. **Criar testes de integração** entre serviços
8. **Configurar ambiente de produção** com Kubernetes

---

## 🎉 CONCLUSÃO

O ecossistema AEON está agora estruturado para desenvolvimento modular e escalável. Cada projeto pode evoluir independentemente, permitindo:

- ✅ **Desenvolvimento paralelo** por múltiplas equipes
- ✅ **Deploy independente** de componentes
- ✅ **Tecnologias específicas** otimizadas por funcionalidade
- ✅ **Escalabilidade** granular por serviço
- ✅ **Manutenção simplificada** com responsabilidades isoladas

**🚀 Comece escolhendo um projeto e siga este guia passo a passo para desenvolvimento produtivo!**
