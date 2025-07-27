# 🧠 AEONCOSMA - Sistema P2P Inteligente

> **Arquitetura de 5 Pilares com Segurança Ultra-Avançada**  
> Sistema proprietário de trading P2P com inteligência artificial e análise fractal  
> Desenvolvido por Luiz Cruz - 2025

## 🎯 Visão Geral

AEONCOSMA é um sistema revolucionário que combina:
- **🧠 Inteligência Cognitiva** - Interface com LLMs e base de conhecimento
- **🛡️ Segurança Adaptativa** - Reputação dinâmica e políticas inteligentes  
- **🌐 Comunicação P2P** - Protocolo simbólico descentralizado
- **🎯 Raciocínio Distribuído** - Motor de coordenação inteligente
- **🌍 Integração Empresarial** - Tentáculos para dados externos

## 🏗️ Arquitetura dos 5 Pilares

### 1. 🧠 GPT Node - O Sentido Cognitivo
```
aeoncosma/cognitive/gpt_node.py
```
- **KnowledgeBase**: SQLite com busca por relevância
- **LLMInterface**: OpenAI/Local/Fallback
- **Security Integration**: Filtros e sanitização
- **Context Enrichment**: Enriquecimento inteligente

### 2. 🛡️ AEON Kernel - O Guardião da Identidade  
```
aeoncosma/core/aeon_kernel.py
```
- **ReputationEngine**: Sistema adaptativo com aprendizado temporal
- **SecurityPolicy**: Políticas dinâmicas configuráveis
- **Access Control**: Quarentena e banimento automático
- **Configuration**: YAML com hot-reload

### 3. 🌐 P2P Interface - O Meio de Comunicação
```
aeoncosma/communication/p2p_interface.py
```
- **SymbolicProtocol**: Comunicação de alto nível
- **WebSocket Handling**: Conexões assíncronas
- **Message Queuing**: Filas com prioridades
- **Handshake Validation**: Autenticação segura

### 4. 🎯 Interaction Engine - O Motor de Raciocínio
```
aeoncosma/reasoning/interaction_engine.py
```
- **SymbolicTranslator**: Natural → Formal
- **Reasoning Coordination**: Distribuído/Consenso/Local
- **Audit Trail**: Trilha imutável com hashing
- **Performance Metrics**: Monitoramento completo

### 5. 🌍 Enterprise Adapter - Os Tentáculos no Mundo
```
aeoncosma/adapters/enterprise_adapter.py
```
- **Universal Connectors**: API/File/Document
- **NLP Processing**: Entidades, sentiment, keywords
- **Intelligent Cache**: TTL com limpeza automática
- **Insights Database**: SQLite com indexação

## 🛡️ Sistema de Segurança

### AeonSecurityLock
```
security/aeoncosma_security_lock.py
```
- **✅ Localhost Only**: Força execução local
- **✅ Root Prevention**: Bloqueia privilégios elevados
- **✅ Argument Filtering**: Detecta argumentos perigosos
- **✅ Fingerprint Check**: Validação de usuário/sistema
- **✅ Integrity Verification**: Verificação de arquivos críticos
- **✅ Network Security**: Monitoramento de configurações
- **✅ Audit Database**: SQLite com logs completos

## 🚀 Quick Start

### 1. Teste de Segurança
```bash
python test_security_quick.py
```

### 2. Demo Enterprise Adapter
```bash
python demo_enterprise_adapter.py
```

### 3. Sistema Completo
```bash
python aeoncosma_launcher.py
```

## 📂 Estrutura do Projeto

```
aeoncosma/
├── cognitive/              # 🧠 Inteligência e Conhecimento
│   └── gpt_node.py        # Interface cognitiva principal
├── core/                  # 🛡️ Núcleo e Identidade
│   └── aeon_kernel.py     # Guardião da identidade
├── communication/         # 🌐 Comunicação P2P
│   └── p2p_interface.py   # Interface de comunicação
├── reasoning/             # 🎯 Motor de Raciocínio
│   └── interaction_engine.py # Coordenação distribuída
└── adapters/              # 🌍 Integração Externa
    └── enterprise_adapter.py # Conectores empresariais

security/                  # 🔒 Sistema de Segurança
├── aeoncosma_security_lock.py # Lock principal
└── security_audit.db     # Base de auditoria

config/                    # ⚙️ Configurações
└── enterprise_sources.json # Fontes de dados

data/                      # 📊 Dados de Exemplo
├── sample_document.txt    # Documento de demonstração
└── trading_history.csv    # Histórico de trading
```

## 🔧 Configuração

### Fontes de Dados Empresariais
Edite `config/enterprise_sources.json` para configurar:
- APIs externas
- Arquivos locais
- Documentos (PDF, Word)
- Bases de dados

### Exemplo de Fonte API:
```json
{
  "source_id": "crypto_api",
  "source_type": "api",
  "name": "CoinGecko API",
  "endpoint_url": "https://api.coingecko.com/api/v3/simple/price",
  "auth_config": {"type": "none"},
  "data_format": "json",
  "is_active": true
}
```

## 🎪 Funcionalidades Principais

### 🧠 Processamento Cognitivo
- Consultas em linguagem natural
- Base de conhecimento inteligente
- Integração com LLMs (OpenAI/Local)
- Filtragem de segurança automática

### 🛡️ Segurança Adaptativa
- Reputação dinâmica de peers
- Políticas de segurança evolutivas
- Detecção de padrões suspeitos
- Sistema de quarentena automático

### 🌐 Comunicação Simbólica
- Protocolo de alto nível
- Handshake seguro
- Sistema de filas inteligente
- Broadcast coordenado

### 🎯 Raciocínio Distribuído
- Coordenação multi-nó
- Algoritmos de consenso
- Trilha de auditoria imutável
- Métricas de performance

### 🌍 Integração Empresarial
- Conectores universais
- Processamento NLP avançado
- Cache inteligente
- Extração de insights automática

## 📊 Monitoramento

### Status do Sistema
```python
# Via API
status = await system.get_system_status()

# Via Enterprise Adapter
report = adapter.get_security_report(24)  # últimas 24h
```

### Métricas Disponíveis
- **Conexões**: Sucesso/falha por fonte
- **Cache**: Hit/miss ratios
- **Segurança**: Eventos por severidade
- **Performance**: Tempos de resposta
- **Insights**: Confiança e categorias

## 🔒 Segurança e Compliance

- **✅ Zero Execução Remota**: Apenas localhost
- **✅ Privilege Minimization**: Sem root/admin
- **✅ Argument Validation**: Filtragem automática
- **✅ User Authentication**: Fingerprint checking
- **✅ File Integrity**: Verificação contínua
- **✅ Network Monitoring**: Configurações seguras
- **✅ Audit Logging**: Trilha completa

## 🛠️ Desenvolvimento

### Dependências
```bash
pip install -r requirements.txt
```

### Dependências Opcionais
```bash
# Para NLP avançado
pip install nltk

# Para conectores PDF
pip install PyPDF2

# Para conectores Word
pip install python-docx
```

### Testes
```bash
# Teste de segurança
python test_security_quick.py

# Teste de components
python -m pytest tests/

# Demo completa
python aeoncosma_launcher.py
```

## 🎯 Casos de Uso

### 1. Trading Automatizado
- Análise de mercado em tempo real
- Decisões baseadas em IA
- Execução coordenada P2P
- Auditoria completa de operações

### 2. Análise Empresarial
- Extração de insights de documentos
- Processamento de APIs externas
- Análise de sentimento automática
- Relatórios inteligentes

### 3. Rede P2P Segura
- Comunicação descentralizada
- Reputação adaptativa
- Consenso distribuído
- Resistência a ataques

### 4. Sistema de Conhecimento
- Base de conhecimento evolutiva
- Busca semântica inteligente
- Integração com LLMs
- Aprendizado contínuo

## 📈 Roadmap

### v1.1 - GPU Acceleration
- [ ] Integração com CUDA
- [ ] Processamento paralelo
- [ ] Análise fractal GPU
- [ ] ML models acceleration

### v1.2 - Advanced NLP
- [ ] Modelos customizados
- [ ] Multi-idioma suporte
- [ ] Entity linking
- [ ] Knowledge graphs

### v1.3 - Enterprise Features
- [ ] Dashboard web
- [ ] API REST completa
- [ ] Integrações corporativas
- [ ] Compliance reporting

## 📝 Licença

Sistema proprietário desenvolvido por Luiz Cruz.  
Todos os direitos reservados - 2025.

## 🤝 Contribuição

Para contribuir com o projeto:
1. Fork do repositório
2. Branch para feature (`git checkout -b feature/AmazingFeature`)
3. Commit das mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para branch (`git push origin feature/AmazingFeature`)
5. Pull Request

## 📞 Suporte

- **Email**: luiz@aeoncosma.ai
- **Documentação**: [docs.aeoncosma.ai](https://docs.aeoncosma.ai)
- **Issues**: [GitHub Issues](https://github.com/luizcruz/aeoncosma/issues)

---

**🎯 AEONCOSMA - Onde Inteligência Artificial encontra Segurança de Nível Enterprise**
