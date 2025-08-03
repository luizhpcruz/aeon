# 🚀 AEONCOSMA Advanced Components Suite

Suíte completa de componentes avançados para análise, monitoramento e teste da rede AEONCOSMA Digital Twin.

## 📁 Componentes Incluídos

### 1. 🧪 **Stress Test Suite** (`stress_test_suite.py`)
Sistema completo de testes de stress para validação de resiliência da rede.

**Funcionalidades:**
- Testes de ataque DDoS com múltiplas intensidades
- Simulação de falha em cascata de nós
- Ataques ao mecanismo de consenso
- Testes de esgotamento de recursos (CPU, memória, rede)
- Análise de resilência e geração de relatórios

**Uso:**
```bash
# Teste abrangente (recomendado)
python stress_test_suite.py --test comprehensive

# Teste DDoS específico
python stress_test_suite.py --test ddos --intensity 0.8 --duration 120

# Teste de falha em cascata
python stress_test_suite.py --test cascade --intensity 0.3 --duration 90

# Teste de ataque ao consenso
python stress_test_suite.py --test consensus --intensity 0.4 --duration 60

# Teste de esgotamento de recursos
python stress_test_suite.py --test resource --resource cpu --intensity 0.9
```

### 2. 🔍 **Symbolic Detection Engine** (`symbolic_detector.py`)
Motor de detecção simbólica para análise de padrões e anomalias.

**Funcionalidades:**
- Simbolização automática do estado da rede
- Detecção de padrões de ataque conhecidos
- Análise de entropia e anomalias estatísticas
- Aprendizado de padrões comportamentais
- Relatórios de detecção em tempo real

**Uso:**
```bash
# Executar detecção simbólica
python symbolic_detector.py

# Os dados são salvos automaticamente em:
# - symbolic_detection_data.json (dados históricos)
# - symbolic_detection_report.json (relatório de análise)
```

### 3. 📊 **PDF Report Generator** (`report_generator.py`)
Gerador automático de relatórios PDF/LaTeX com métricas de segurança.

**Funcionalidades:**
- Relatórios de segurança detalhados
- Relatórios de performance operacional
- Relatórios abrangentes combinados
- Compilação automática para PDF (se LaTeX disponível)
- Templates personalizáveis

**Uso:**
```bash
# Gerar relatório completo
python report_generator.py

# Os relatórios são gerados em:
# - reports/security_report_TIMESTAMP.tex
# - reports/comprehensive_report_TIMESTAMP.tex
# - reports/*.pdf (se LaTeX disponível)
```

### 4. 🌐 **3D Network Visualizer** (`network_3d_visualizer.py`)
Visualizador 3D em tempo real da rede usando NetworkX + Streamlit.

**Funcionalidades:**
- Visualização 3D interativa da topologia de rede
- Representação em tempo real do status dos nós
- Análise de conectividade e métricas
- Detecção visual de anomalias
- Interface web responsiva

**Uso:**
```bash
# Iniciar visualizador 3D
streamlit run network_3d_visualizer.py --server.port 8505

# Acesse: http://localhost:8505
```

### 5. 🛡️ **Enhanced Security Dashboard** (`streamlit_dashboard.py`)
Dashboard de segurança aprimorado com detecção avançada.

**Funcionalidades:**
- Monitoramento em tempo real
- Detecção de 6 tipos de ataques
- Métricas de segurança avançadas
- Interface multi-tab
- Alertas automáticos

### 6. 🚀 **Suite Launcher** (`aeoncosma_suite_launcher.py`)
Lançador centralizado para todos os componentes.

## 🔧 Instalação e Configuração

### Pré-requisitos
```bash
# Instalar dependências Python
pip install streamlit plotly networkx pandas numpy psutil requests

# Para geração de PDF (opcional)
# Windows: Instalar MiKTeX ou TeX Live
# Linux: sudo apt-get install texlive-full
# macOS: Instalar MacTeX
```

### Uso Rápido
```bash
# Lançador interativo (recomendado)
python aeoncosma_suite_launcher.py --interactive

# Iniciar todos os dashboards
python aeoncosma_suite_launcher.py --component all

# Executar análise abrangente
python aeoncosma_suite_launcher.py --analysis
```

## 📊 Componentes Web Disponíveis

| Componente | Porta | URL | Descrição |
|------------|-------|-----|-----------|
| Security Dashboard | 8504 | http://localhost:8504 | Dashboard de segurança principal |
| 3D Visualizer | 8505 | http://localhost:8505 | Visualizador 3D da rede |
| P2P Monitor | 8501 | http://localhost:8501 | Monitor P2P básico |

## 🧪 Executando Testes de Stress

### Teste Abrangente (Recomendado)
```bash
python stress_test_suite.py --test comprehensive --output stress_results.json
```

### Testes Específicos
```bash
# Teste DDoS com alta intensidade
python stress_test_suite.py --test ddos --intensity 0.9 --duration 180

# Teste de falha em cascata
python stress_test_suite.py --test cascade --intensity 0.2 --duration 120

# Teste de consenso com 30% de nós maliciosos
python stress_test_suite.py --test consensus --intensity 0.3 --duration 90

# Teste de esgotamento de CPU
python stress_test_suite.py --test resource --resource cpu --intensity 0.8
```

## 🔍 Detecção Simbólica

O motor de detecção simbólica converte o estado da rede em símbolos e detecta padrões:

### Símbolos Detectados
- `HIGH_LATENCY`: Latência elevada (>200ms)
- `CPU_CRITICAL`: CPU crítico (>90%)
- `MEMORY_LEAK`: Vazamento de memória detectado
- `CONSENSUS_FAIL`: Falha no consenso (<51%)
- `NETWORK_PARTITION`: Partição da rede
- `PACKET_LOSS`: Perda significativa de pacotes

### Padrões de Ataque
- **Sequência de Ataque**: `HIGH_LATENCY → PACKET_LOSS → NODE_FAILURE`
- **Manipulação de Consenso**: `DOUBLE_VOTING → FORK_ATTEMPT → CHAIN_REORGANIZATION`
- **Intrusão de Rede**: `UNAUTHORIZED_NODE → IDENTITY_SPOOFING → CERT_INVALID`

## 📄 Geração de Relatórios

### Tipos de Relatório

1. **Relatório de Segurança**: Foco em ameaças e vulnerabilidades
2. **Relatório de Performance**: Análise de métricas operacionais
3. **Relatório Abrangente**: Combinação completa com todas as análises

### Dados Incluídos
- Métricas de segurança e performance
- Análise de tendências temporais
- Detecções de anomalias
- Resultados de testes de stress
- Recomendações de melhoria

## 🌐 Visualização 3D

### Características
- **Nós**: Representados como esferas coloridas por tipo
- **Conexões**: Linhas conectando nós relacionados
- **Cores**:
  - 🔴 Master: Vermelho
  - 🔵 AI: Azul
  - 🟢 Crypto: Verde
  - 🟡 Quantum: Amarelo
  - 🟣 Cosmos: Roxo
  - 🔵 Energy: Azul-verde
  - 🟢 Validator: Verde claro

### Interações
- Rotação 3D com mouse
- Zoom com scroll
- Hover para informações detalhadas
- Filtros por tipo de nó
- Atualização em tempo real

## 🚀 Menu Interativo

Execute o lançador interativo para acesso fácil:

```bash
python aeoncosma_suite_launcher.py --interactive
```

### Opções do Menu
1. Verificar dependências
2. Iniciar todos os dashboards
3. Executar análise abrangente
4. Iniciar dashboard de segurança
5. Iniciar visualizador 3D
6. Executar testes de stress
7. Executar detecção simbólica
8. Gerar relatórios
9. Mostrar status dos componentes
10. Parar todos os componentes

## 📊 Métricas Coletadas

### Métricas de Segurança
- Nível geral de segurança (0-100%)
- Ameaças detectadas por categoria
- Score de anomalia por nó
- Taxa de participação no consenso

### Métricas de Performance
- Latência média/máxima da rede
- Utilização de CPU/memória
- Taxa de uptime dos nós
- Throughput de transações

### Métricas de Rede
- Número de nós online/offline
- Conectividade entre nós
- Taxa de perda de pacotes
- Largura de banda utilizada

## 🛡️ Detecção de Ataques

### Tipos de Ataque Detectados
1. **Ataques DDoS**: Sobrecarga de tráfego
2. **Sabotagem**: Comportamento malicioso intencional
3. **Falhas de Hardware**: Degradação de componentes
4. **Problemas de Rede**: Conectividade instável
5. **Dessincronização**: Problemas de sincronização blockchain
6. **Ataques ao Consenso**: Manipulação do mecanismo de acordo

### Níveis de Severidade
- 🔴 **CRÍTICO**: Ameaça imediata à rede
- 🟠 **ALTO**: Requer atenção urgente
- 🟡 **MÉDIO**: Monitoramento necessário
- 🟢 **BAIXO**: Situação normal

## 📈 Análise de Tendências

### Métricas Temporais
- Evolução da latência ao longo do tempo
- Padrões de utilização de recursos
- Histórico de participação no consenso
- Frequência de detecção de anomalias

### Previsões
- Identificação de tendências de degradação
- Predição de falhas potenciais
- Recomendações preventivas

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro "pdflatex not found"**
   - Instalar distribuição LaTeX (MiKTeX, TeX Live, MacTeX)
   - Apenas arquivos .tex serão gerados sem LaTeX

2. **Porta já em uso**
   - Verificar processos em execução
   - Usar ports alternativos: `--server.port XXXX`

3. **Dependências ausentes**
   - Executar: `pip install -r requirements.txt`

4. **Performance lenta**
   - Reduzir número de nós na visualização 3D
   - Aumentar intervalo de atualização

### Logs
Todos os componentes geram logs em:
- `aeoncosma_suite.log`: Log principal do launcher
- `symbolic_detector.log`: Log da detecção simbólica
- `report_generator.log`: Log da geração de relatórios
- `stress_test_suite.log`: Log dos testes de stress

## 📚 Estrutura de Arquivos

```
aeoncosma/ui/
├── streamlit_dashboard.py          # Dashboard principal
├── network_3d_visualizer.py        # Visualizador 3D
├── stress_test_suite.py            # Testes de stress
├── symbolic_detector.py            # Detecção simbólica
├── report_generator.py             # Gerador de relatórios
├── integrity_ascii.py              # Backend de integridade
├── aeoncosma_suite_launcher.py     # Lançador da suíte
├── README_ADVANCED_COMPONENTS.md   # Este arquivo
├── integrity_data/                 # Dados de integridade
├── reports/                        # Relatórios gerados
│   ├── images/                     # Imagens dos relatórios
│   └── data/                       # Dados dos relatórios
└── logs/                           # Arquivos de log
```

## 🚀 Próximos Passos

1. **Executar análise inicial**:
   ```bash
   python aeoncosma_suite_launcher.py --analysis
   ```

2. **Iniciar monitoramento contínuo**:
   ```bash
   python aeoncosma_suite_launcher.py --component all
   ```

3. **Revisar relatórios gerados** na pasta `reports/`

4. **Configurar alertas automáticos** baseados nas métricas

5. **Implementar ações corretivas** baseadas nas recomendações

## 🎯 Objetivos dos Componentes

### Segurança
- Detectar ameaças em tempo real
- Validar integridade da rede
- Monitorar comportamentos anômalos

### Performance
- Otimizar recursos da rede
- Identificar gargalos
- Prever falhas potenciais

### Resilência
- Testar limites do sistema
- Validar capacidade de recuperação
- Melhorar robustez geral

---

**Desenvolvido por:** Luiz H. P. Cruz  
**Projeto:** AEONCOSMA Digital Twin Network  
**Versão:** 1.0.0  
**Data:** 2025
