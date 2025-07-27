# 🌌 AEONCOSMA PREDICTOR

## Sistema Avançado de Trading com IA e Backup Criptografado

### 🚀 Visão Geral

O **AEONCOSMA PREDICTOR** é um sistema proprietário de análise de mercado e predições que combina:

- **IA Avançada** para análise técnica e predições
- **Interface Web Interativa** com gráficos em tempo real
- **Sistema de Backup Criptografado** para segurança de dados
- **Monitoramento Contínuo** de mercados de criptomoedas
- **Logs Detalhados** com criptografia automática

---

## 📁 Estrutura do Projeto

```
aeoncosma/
├── backup/
│   ├── aeon_backup.py      # Sistema de backup criptografado
│   ├── keys/               # Chaves de criptografia
│   ├── logs/               # Logs criptografados
│   └── full/               # Backups completos
├── config.yaml             # Configurações do sistema
├── main.py                 # Módulo principal original
├── system.py               # Sistema integrado
└── README.md               # Esta documentação

Arquivos principais:
├── test_server.py          # Servidor web com interface
├── predictor_simple.py     # Versão simplificada
├── aeoncosma_trading.py    # Sistema completo original
└── start_aeoncosma.bat     # Script de inicialização
```

---

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- Biblioteca `cryptography` para criptografia
- Conexão com internet para dados de mercado

### Instalação
```bash
# Clone ou baixe o projeto
cd "IA p2p trader"

# Instale dependências
pip install cryptography requests

# Execute o sistema
py test_server.py
```

---

## 🚀 Como Usar

### 1. Inicialização Rápida
```bash
# Método 1: Via arquivo .bat
start_aeoncosma.bat

# Método 2: Direto via Python
py test_server.py

# Método 3: Sistema completo
py aeoncosma_trading.py
```

### 2. Acesso à Interface
- Abra seu navegador
- Acesse: `http://localhost:8080`
- A interface carregará automaticamente

### 3. Funcionalidades Disponíveis
- 📊 **Dados de Mercado**: Preços em tempo real de 5 criptomoedas
- 🔮 **Predições IA**: Análises para 1 hora e 24 horas
- 💹 **Gráficos Interativos**: Visualização de tendências
- 🔐 **Backup Automático**: Logs criptografados em tempo real
- 📋 **Monitoramento**: Logs detalhados de atividades

---

## 🔐 Sistema de Backup

### Características
- **Criptografia Fernet**: Proteção avançada de dados
- **Chaves de Sessão**: Nova chave para cada execução
- **Backup Automático**: Salva logs a cada 10 eventos
- **Múltiplos Tipos**: Logs, backups completos, incrementais

### Uso do Sistema de Backup
```python
from backup.aeon_backup import AeonBackupManager

# Inicializa sistema
backup = AeonBackupManager()

# Salva log
backup.save_log("Evento importante", "system")

# Backup completo
backup.save_full_backup(dados_sistema)

# Relatório
print(backup.generate_report())
```

### Estrutura de Arquivos de Backup
```
backup/
├── keys/
│   └── session_YYYYMMDD_HHMMSS.key
├── logs/
│   └── system_YYYYMMDD_HHMMSS.aeon
├── full/
│   └── aeon_full_YYYYMMDD_HHMMSS.aeon
└── incremental/
    └── aeon_inc_YYYYMMDD_HHMMSS.aeon
```

---

## 📊 APIs e Endpoints

### Interface Principal
- `GET /` - Interface web principal
- `GET /api/backup` - Executa backup manual
- `GET /api/logs` - Obtém logs atuais

### Dados de Mercado
- Fonte primária: **CoinGecko API**
- Fallback: Dados simulados realísticos
- Atualização: A cada 30 segundos

---

## 🤖 Sistema de IA

### Algoritmo AEON
O sistema utiliza algoritmos proprietários que combinam:

1. **Análise Técnica**
   - RSI (Relative Strength Index)
   - MACD (Moving Average Convergence Divergence)
   - Bandas de Bollinger
   - Médias móveis (SMA/EMA)

2. **Fatores de Consciência**
   - Nível de consciência evolutivo
   - Análise de momentum
   - Detecção de padrões
   - Correlações quânticas

3. **Predições Multi-Timeframe**
   - Curto prazo (1 hora)
   - Médio prazo (24 horas)
   - Níveis de confiança
   - Análise de volatilidade

---

## 🔧 Configuração Avançada

### Arquivo config.yaml
```yaml
system:
  name: "AEONCOSMA PREDICTOR"
  version: "2.0.1"

server:
  port: 8080
  auto_open_browser: true

backup:
  enabled: true
  encryption: true
  auto_backup_interval: 300

market:
  symbols: [BTC, ETH, BNB, ADA, SOL]
  update_interval: 30

prediction:
  confidence_threshold: 0.6
  timeframes: ["1h", "24h"]
```

---

## 🛡️ Segurança

### Medidas Implementadas
- ✅ **Criptografia Fernet** para todos os backups
- ✅ **Chaves de sessão** únicas
- ✅ **Logs criptografados** automaticamente
- ✅ **Validação de dados** de entrada
- ✅ **Isolation de processos**

### Boas Práticas
- Mantenha as chaves de sessão seguras
- Faça backup regular das chaves
- Monitore logs para atividades suspeitas
- Use HTTPS em produção

---

## 📈 Monitoramento e Logs

### Tipos de Log
- `SYSTEM`: Eventos do sistema
- `ACCESS`: Acessos à interface
- `MARKET`: Dados de mercado
- `PREDICTION`: Predições geradas
- `BACKUP`: Operações de backup
- `ERROR`: Erros e exceções
- `SECURITY`: Eventos de segurança

### Visualização
- Interface web mostra logs em tempo real
- Arquivo de logs criptografados para análise
- Relatórios automáticos de atividades

---

## 🚀 Desenvolvimento

### Extensibilidade
O sistema foi projetado para ser facilmente extensível:

- **Novos indicadores técnicos**
- **Diferentes fontes de dados**
- **Algoritmos de IA personalizados**
- **Interfaces alternativas**

### Contribuição
1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente e teste
4. Submeta um pull request

---

## 📝 Changelog

### v2.0.1 (2025-07-26)
- ✅ Sistema de backup criptografado implementado
- ✅ Interface web melhorada com logs em tempo real
- ✅ Algoritmos de predição aprimorados
- ✅ Estrutura modular reorganizada
- ✅ Documentação completa adicionada

### v2.0.0 (2025-07-26)
- ✅ Primeira versão com IA avançada
- ✅ Interface web interativa
- ✅ Integração com APIs de mercado
- ✅ Sistema básico de logs

---

## 📞 Suporte

Para suporte técnico ou dúvidas:

- **Desenvolvedor**: Luiz Cruz
- **Ano**: 2025
- **Projeto**: AEONCOSMA PREDICTOR
- **Status**: Ativo e em desenvolvimento

---

## ⚖️ Licença

Sistema proprietário desenvolvido por Luiz Cruz.
Todos os direitos reservados - 2025.

---

**🌌 AEONCOSMA PREDICTOR - Onde IA encontra o futuro dos mercados! 🚀**
