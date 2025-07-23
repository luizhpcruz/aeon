# AEON - Sistema de Simulação Complexa

## Descrição
AEON é um sistema de simulação avançado que combina elementos de:
- **Bioinformática computacional** com genomas simbólicos
- **Cosmologia teórica** com modelos alternativos
- **Sistemas dinâmicos** e análise de entropia
- **Inteligência artificial emergente** com o sistema V.E.R.N.A.

## Estrutura do Projeto

```
aeon/
├── scripts/           # Scripts Python de simulação
├── data/             # Dados gerados (CSV, JSON)
├── visualizations/   # Gráficos e imagens geradas
├── frontend/         # Interface web (React)
├── bagunça/          # Protótipos e experimentos
├── teoria/           # Modelos teóricos
└── docs/             # Documentação
```

## Scripts Principais

### Simulações de Entropia
- **1.py**: Simulação básica com genomas simbólicos
- **2.py**: Simulação multi-fita
- **3.py**: Simulação com estímulos variáveis
- **4.py**: Análise completa de entropia com visualizações
- **5.py**: Simulação com pulso fixo

### Modelos Especializados
- **NMD.py**: Modelo cosmológico de deflexão vetorial
- **yu.py**: Análises adicionais

### Sistema AEON Cosma
- **bagunça/AEONCOSMA_ENGINE_v1/**: Motor principal do AEON
- **bagunça/aeoncosma_hf/**: Integração com Hugging Face

### Sistema V.E.R.N.A.
- **teoria/verna.py**: Vector of Emergent Recursive Neuro-Awareness
- **teoria/comparador_modelos.py**: Comparação de modelos cosmológicos

## Pré-requisitos

### Python
```bash
pip install numpy matplotlib seaborn pandas scipy
```

### Dependências específicas
- FastAPI (para backend)
- Requests (para APIs)
- Collections, JSON (bibliotecas padrão)

## Como Usar

### Executar Simulação Básica
```bash
cd scripts
python 4.py
```

### Motor AEON Cosma
```bash
cd bagunça/AEONCOSMA_ENGINE_v1
python aeon_interface.py
```

### Frontend (React)
```bash
cd frontend
npm install
npm start
```

## Configuração de API

### Hugging Face (Opcional)
1. Crie conta em https://huggingface.co/join
2. Gere token de acesso
3. Configure variável de ambiente:
   ```bash
   setx HF_API_TOKEN "seu_token_aqui"
   ```

### AlphaVantage (Trading)
1. Obtenha chave em https://www.alphavantage.co/
2. Substitua no código React

## Parâmetros de Simulação

### Configurações Padrão
- **N_CICLOS_TESTE**: 50 ciclos de evolução
- **N_FITAS**: 5 fitas paralelas
- **N_CELULAS**: 32 células por fita
- **N_ESTADOS**: 4 estados possíveis

### Tipos de Entrada
- **aleatoria**: Distribuição uniforme
- **pulso**: Sinal concentrado no centro
- **ruido**: Distribuição com alta proporção de nulos

## Análises Disponíveis

### Métricas de Entropia
- Entropia de Shannon por fita
- Entropia temporal segmentada
- Entropia por posição genômica
- Heatmaps entrópicos

### Visualizações
- Gráficos temporais de entropia
- Análise posicional
- Comparações entre tipos de entrada
- Mapas de calor

## Resultados

Os resultados são salvos automaticamente em:
- **data/**: Arquivos CSV com dados numéricos
- **visualizations/**: Gráficos em PNG
- **bagunça/AEONCOSMA_ENGINE_v1/aeon_state.json**: Estado do motor AEON

## Desenvolvimento

### Git Workflow
```bash
git checkout -b develop
# fazer mudanças
git add .
git commit -m "feat: descrição da mudança"
git push origin develop
```

### Estrutura de Commits
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `style:` formatação
- `refactor:` refatoração
- `test:` testes

## Autor
Luiz F. + GitHub Copilot

## Data
Julho/2025

---

**Nota**: Este é um projeto experimental que explora conceitos avançados de sistemas complexos, simulação computacional e emergência de padrões em sistemas dinâmicos.
