# 🚀 GUIA DE INSTALAÇÃO E EXECUÇÃO - AEON COSMOS

## 📋 Pré-requisitos

- Python 3.9 ou superior
- Node.js 16+ (para o frontend)
- Git
- Docker e Docker Compose (opcional, para deploy)

## 🔧 Instalação Passo a Passo

### 1. Clonar o Repositório
```bash
git clone https://github.com/luizcruz/aeon-cosmos.git
cd aeon-cosmos
```

### 2. Configurar Ambiente Python
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Frontend (Opcional)
```bash
cd frontend
npm install
cd ..
```

### 4. Validar Instalação
```bash
python validate_project.py
```

## 🏃‍♂️ Executando o Projeto

### Opção 1: Execução Simples
```bash
# Executar o launcher principal
python start.py
```

### Opção 2: Componentes Individuais

#### Backend API
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Simulação AEON
```bash
python aeoncosma/main.py
```

#### Simulação Núcleo Hive
```bash
python -m aeoncosma.core.simulate_aeon
```

#### Frontend (se configurado)
```bash
cd frontend
npm start
```

### Opção 3: Docker (Recomendado para Produção)
```bash
# Build e execução com Docker Compose
docker-compose up --build

# Ou usar o script automatizado
bash scripts/docker_deploy.sh
```

## 🌐 Acessando os Serviços

Após a execução, os serviços estarão disponíveis em:

- **API Backend**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000 (se configurado)
- **P2P Network**: Porta 8888

## 🧪 Testando o Sistema

### Testes Automatizados
```bash
# Executar todos os testes
pytest

# Testes específicos
python tests/test_aeon_hive_core.py
python tests/test_backend_api.py
```

### Teste Manual da API
```bash
# Testar endpoint de saúde
curl http://localhost:8000/api/health

# Testar análise de mercado
curl http://localhost:8000/api/analyze/AAPL
```

## 🐛 Solução de Problemas

### Erro de Import
```bash
# Instalar dependências faltantes
pip install -r requirements.txt

# Verificar versão do Python
python --version
```

### Erro de Porta Ocupada
```bash
# Verificar portas em uso
netstat -an | findstr :8000
```

### Problemas com Docker
```bash
# Limpar containers e imagens
docker-compose down
docker system prune -f
```

## 📚 Documentação Adicional

- **Arquitetura**: Consulte `docs/architecture.md`
- **API Reference**: http://localhost:8000/docs
- **Exemplos**: Diretório `examples/`

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique os logs em `logs/`
2. Execute o validador: `python validate_project.py`
3. Consulte a documentação
4. Abra uma issue no GitHub

---

**Desenvolvido por Luiz Cruz** | **AEON COSMOS - 2025**
