# 🌌 AEONCOSMA P2P NETWORK - Fase 1

## 🚀 Sistema Distribuído de Trading com Validação Backend

Sistema P2P descentralizado para trading com inteligência artificial, implementando validação sequencial de nós e feedback centralizado através de backend AEON.

## 📋 Visão Geral

### Componentes Principais

1. **🌐 Nós P2P** (`aeoncosma/networking/p2p_node.py`)
   - Comunicação peer-to-peer via sockets
   - Validação sequencial de novos nós
   - Sistema de estatísticas e monitoramento
   - Threading para múltiplas conexões simultâneas

2. **🔍 Sistema de Validação** (`aeoncosma/networking/validation_logic.py`)
   - Validação estrutural de dados
   - Verificação de duplicatas
   - Ordem sequencial de entrada na rede
   - Consulta ao backend AEON para validação final

3. **🚀 Backend FastAPI** (`aeoncosma/backend/api_feedback.py`)
   - API REST para validação centralizada
   - Sistema de pontuação AEON inteligente
   - Estatísticas da rede em tempo real
   - Histórico de validações

## 🎯 Funcionalidades

### ✅ Implementado

- [x] Nós P2P com comunicação socket
- [x] Validação sequencial de nós
- [x] Backend API com sistema de pontuação
- [x] Sistema de estatísticas em tempo real
- [x] Fallback para modo mock (sem dependências externas)
- [x] Threading para múltiplas conexões
- [x] Validação estrutural e de duplicatas
- [x] Interface de linha de comando interativa

### 🔄 Em Desenvolvimento

- [ ] Interface web para monitoramento
- [ ] Persistência de dados em banco
- [ ] Criptografia de comunicação
- [ ] Sistema de reputação de nós
- [ ] Balanceamento de carga
- [ ] Recuperação automática de falhas

## 🚀 Como Usar

### Execução Rápida

```bash
# Windows
start_p2p_network.bat

# Linux/Mac
./start_p2p_system.py
```

### Execução Manual

```bash
# Ative o ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Execute o sistema
python start_p2p_system.py
```

### Teste Simples

```bash
python test_p2p_network.py
```

## 🌐 Arquitetura da Rede

### Topologia

```
Backend AEON (port 8000)
       |
   [Validação]
       |
Nó Genesis (port 9001)
       |
Nó 002 (port 9002)
       |
Nó 003 (port 9003)
```

### Fluxo de Validação

1. **Novo nó** se conecta ao nó anterior
2. **Nó anterior** valida estrutura e duplicatas
3. **Consulta AEON** para validação final
4. **Aceita/Rejeita** baseado na pontuação
5. **Atualiza rede** com novo peer

## 📡 API Endpoints

### Backend (porta 8000)

- `GET /` - Informações da API
- `POST /validate` - Validação de nós
- `GET /network/stats` - Estatísticas da rede
- `GET /network/nodes` - Lista de nós validados
- `GET /network/node/{id}` - Informações específicas
- `DELETE /network/node/{id}` - Remove nó (manutenção)
- `GET /health` - Status do sistema

### Exemplo de Validação

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "node_data": {
      "node_id": "new_node_001",
      "host": "127.0.0.1",
      "port": 9004,
      "timestamp": "2025-01-27T12:00:00",
      "previous": "node_003"
    },
    "validator_id": "validator_001"
  }'
```

## 🔧 Configuração

### Dependências Básicas (Incluídas no Python)

- `socket` - Comunicação de rede
- `threading` - Processamento concorrente
- `json` - Serialização de dados
- `datetime` - Timestamps

### Dependências Opcionais

- `fastapi` - Backend API (fallback para mock)
- `uvicorn` - Servidor ASGI
- `requests` - Cliente HTTP (fallback para socket)

### Instalação Completa

```bash
pip install fastapi uvicorn requests
```

## 🎮 Modo Interativo

Após iniciar o sistema, comandos disponíveis:

- `status` - Mostra status da rede
- `test` - Executa teste de conectividade  
- `broadcast` - Envia mensagem broadcast
- `quit` - Para o sistema
- `help` - Lista comandos

## 📊 Sistema de Pontuação AEON

### Critérios de Validação (Total: 100 pontos)

1. **Estrutura dos Dados (25 pts)**
   - Campos obrigatórios presentes
   - Tipos de dados corretos

2. **Qualidade do Node ID (20 pts)**
   - Comprimento adequado (≥8 chars = 20pts)
   - Unicidade na rede

3. **Timestamp (20 pts)**
   - Frescor dos dados (<1min = 20pts)
   - Validez do formato

4. **Contexto/Metadados (20 pts)**
   - Riqueza de informações
   - 5 pontos por campo relevante

5. **Conectividade (15 pts)**
   - Host válido e acessível
   - Porta no range correto

### Aprovação

- **≥70%** - Nó aprovado
- **<70%** - Nó rejeitado

## 🔍 Monitoramento

### Logs do Sistema

```
✅ [genesis_node] Nó validado: node_002
📊 [genesis_node] Stats - Peers: 1, Validados: 1, Rejeitados: 0, Uptime: 30s
🔗 [node_002] Conectando a 127.0.0.1:9001
```

### Métricas Disponíveis

- Total de nós na rede
- Taxa de aprovação de validações
- Tempo de atividade de cada nó
- Histórico de validações
- Estatísticas de conectividade

## 🛠️ Troubleshooting

### Problemas Comuns

1. **"Nenhuma conexão pôde ser feita"**
   - Verifique se o backend está rodando
   - Sistema fallback para mock automaticamente

2. **"Módulos P2P não disponíveis"**
   - Verifique estrutura de diretórios
   - Execute teste simples: `python -c "import socket"`

3. **"Porta já em uso"**
   - Mude a porta no código
   - Pare processos conflitantes

### Debug Mode

```bash
# Execução com logs detalhados
python -u start_p2p_system.py
```

## 🔒 Segurança

### Implementado

- Validação de estrutura de dados
- Verificação de duplicatas
- Timeouts de conexão
- Sanitização de entradas

### Planejado

- [ ] Criptografia TLS/SSL
- [ ] Autenticação de nós
- [ ] Rate limiting
- [ ] Assinatura digital de mensagens

## 📈 Performance

### Otimizações

- Threading para conexões simultâneas
- Timeouts configuráveis
- Limpeza automática de recursos
- Cache de validações

### Limites Atuais

- **Nós simultâneos**: ~50 (limitado por SO)
- **Conexões/nó**: 5 simultâneas
- **Timeout**: 10 segundos
- **Histórico**: 1000 validações em memória

## 🤝 Contribuição

### Estrutura do Código

```
aeoncosma/
├── networking/
│   ├── p2p_node.py          # Lógica principal do nó
│   └── validation_logic.py   # Sistema de validação
├── backend/
│   └── api_feedback.py      # Backend FastAPI
└── config/
    └── settings.py          # Configurações (futuro)
```

### Guidelines

- Seguir padrões PEP 8
- Documentar funções com docstrings
- Implementar tratamento de erros
- Adicionar logs informativos
- Testar em ambiente local

## 📄 Licença

Sistema proprietário AEONCOSMA - Desenvolvido por Luiz Cruz - 2025
Todos os direitos reservados.

---

🌌 **AEONCOSMA P2P Network** - Construindo o futuro do trading descentralizado com IA
