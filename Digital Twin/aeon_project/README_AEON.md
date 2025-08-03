# 🚀 AEON Digital Twin Platform

Sistema integrado de comunicação corporativa e simulação industrial para o setor energético.

## 📋 Descrição

O AEON é uma plataforma completa que combina:
- 🧠 **Kernel de IA Simbólica**: Sistema de inteligência artificial para análise e predição
- 💧 **Digital Twin UHE**: Simulação em tempo real de Usinas Hidrelétricas  
- 📄 **Documentos SSMA**: Geração automatizada de documentação ambiental
- 💬 **Chat Corporativo**: Sistema de comunicação empresarial integrado
- 🌐 **Rede P2P**: Comunicação descentralizada entre nós

## 🚀 Como Executar

### Opção 1: Interface Integrada (Recomendado)
```bash
# 1. Ativar ambiente virtual
.\.venv\Scripts\activate

# 2. Executar aplicação integrada
streamlit run aeon_app.py --server.port 8501
```

### Opção 2: Backend + Frontend Separados
```bash
# Terminal 1 - Backend (API REST)
python -m uvicorn simple_backend:app --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend (Interface Web)
streamlit run app.py --server.port 8501
```

### Opção 3: Teste do Sistema
```bash
python test_system.py
```

## 🌐 Acesso

- **Interface Principal**: http://localhost:8501
- **API Backend**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs

## 📊 Funcionalidades

### 🏠 Dashboard
- Monitoramento em tempo real
- Métricas de performance
- Gráficos de geração de energia
- Status dos sistemas

### 🧠 Kernel IA
- Evolução de parâmetros neurais
- Análise de redes simbólicas
- Simulação de atividade neural
- Controle de intensidade e diversidade

### 💧 UHE Digital Twin
- Simulação de usinas hidrelétricas
- Cálculo de geração energética
- Monitoramento de vazão
- Análise de eficiência

### 📄 Documentos SSMA
- Geração automática de licenças ambientais
- Integração com Gov.br
- Controle de versões
- Assinatura digital

### 💬 Chat Corporativo
- Comunicação em tempo real
- Notificações automáticas
- Histórico de mensagens
- Integração com IA

## 🛠️ Tecnologias

- **Python 3.13**: Linguagem principal
- **Streamlit**: Interface web interativa
- **FastAPI**: APIs REST de alta performance
- **Pandas**: Análise de dados
- **NumPy**: Computação científica
- **Uvicorn**: Servidor ASGI

## 📁 Estrutura do Projeto

```
aeon_project/
├── aeon_app.py          # Aplicação integrada principal
├── simple_backend.py    # Backend API simplificado
├── test_system.py       # Testes do sistema
├── start_aeon.bat       # Script de inicialização
├── aeon_kernel/         # Módulo de IA
├── aeon_ops/            # Operações e dados
├── aeon_chat/           # Sistema de chat
├── aeon_cosma/          # Análise cosmológica
├── aeon_chain/          # Rede P2P
├── backend/             # APIs REST
├── frontend/            # Interfaces web
└── tests/               # Testes unitários
```

## 🔧 Configuração de Desenvolvimento

### Dependências
```bash
pip install streamlit fastapi uvicorn pandas numpy requests python-multipart
```

### Variáveis de Ambiente
```bash
export AEON_ENV=development
export AEON_PORT=8501
export AEON_HOST=localhost
```

## 🧪 Testes

```bash
# Teste completo do sistema
python test_system.py

# Testes unitários
python -m pytest tests/

# Teste do kernel
python tests/test_kernel.py
```

## 📝 API Endpoints

### Kernel IA
- `POST /kernel/evolve` - Executa evolução neural
- `GET /kernel/status` - Status do kernel

### UHE Digital Twin
- `POST /ops/simulate` - Simulação de UHE
- `GET /ops/data` - Dados das usinas

### Documentos SSMA
- `POST /ops/generate_and_sign` - Gera documento
- `GET /ops/documents` - Lista documentos

### Chat
- `POST /chat/send` - Envia mensagem
- `GET /chat/messages` - Lista mensagens

## 🔒 Segurança

- Autenticação via Gov.br SSO
- Criptografia de documentos
- Assinatura digital
- Controle de acesso baseado em roles

## 📞 Suporte

Para suporte técnico:
- 📧 Email: suporte@aeon-platform.com
- 💬 Chat: Sistema integrado
- 📖 Docs: /docs na API

## 📄 Licença

Propriedade da AEON Digital Twin Platform.
Todos os direitos reservados.

---

🚀 **AEON Digital Twin Platform** - Transformando a comunicação corporativa no setor energético!
