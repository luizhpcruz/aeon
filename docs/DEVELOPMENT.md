# Guia de Desenvolvimento - AEON

## Configuração do Ambiente

### 1. Primeira execução

```bash
# Windows
setup.bat

# Linux/macOS
./setup.sh
```

### 2. Execução rápida

```bash
# Windows
run.bat

# Linux/macOS
./run.sh
```

## Estrutura de Arquivos

### Scripts Principais

- `scripts/4.py` - **Análise completa de entropia** (mais importante)
  - Gera visualizações de entropia temporal
  - Cria heatmaps e gráficos comparativos
  - Exporta dados em CSV

### Módulos Especializados

- `bagunça/AEONCOSMA_ENGINE_v1/` - Motor principal do sistema AEON
- `teoria/verna.py` - Sistema V.E.R.N.A. de consciência emergente
- `frontend/` - Interface web React com trading viewer

## Comandos Git Úteis

### Workflow básico

```bash
# Criar nova feature
git checkout -b feature/nova-funcionalidade

# Fazer mudanças
git add .
git commit -m "feat: descrição da mudança"

# Atualizar branch
git push origin feature/nova-funcionalidade

# Voltar para develop
git checkout develop
git merge feature/nova-funcionalidade
```

### Sincronização

```bash
# Atualizar repositório local
git pull origin develop

# Enviar mudanças
git push origin develop
```

## Tasks do VS Code

Use `Ctrl+Shift+P` e digite "Tasks: Run Task" para executar:

1. **🔬 Executar Análise de Entropia** - Roda o script principal
2. **🌌 Executar Modelo Cosmológico** - Análise cosmológica
3. **🤖 Executar Motor AEON Cosma** - Sistema AEON completo
4. **🧠 Executar Sistema V.E.R.N.A.** - Consciência emergente
5. **🚀 Instalar Dependências** - Setup automático

## Debugging

### Problemas comuns

1. **ModuleNotFoundError**: Execute `pip install -r requirements.txt`
2. **Python não encontrado**: Verifique se Python está no PATH
3. **Git erro**: Configure `git config --global user.name` e `user.email`

### Logs e outputs

- Gráficos salvos em `visualizations/`
- Dados em `data/`
- Estados do AEON em `bagunça/AEONCOSMA_ENGINE_v1/aeon_state.json`

## Extensões VS Code Recomendadas

- **Python** (ms-python.python)
- **GitLens** (eamodio.gitlens)
- **ES7+ React/Redux/React-Native** (dsznajder.es7-react-js-snippets)
- **Tailwind CSS IntelliSense** (bradlc.vscode-tailwindcss)

## Parâmetros de Configuração

### Simulação de Entropia

```python
N_CICLOS_TESTE = 50    # Ciclos de evolução
N_FITAS = 5           # Fitas paralelas
N_CELULAS = 32        # Células por fita
N_ESTADOS = 4         # Estados possíveis
```

### Motor AEON

- Genomas de 13 caracteres
- Mutação baseada em regras específicas
- Estado persistente em JSON

## Próximos Passos

1. **Configurar GitHub Actions** para CI/CD
2. **Implementar testes automatizados**
3. **Expandir frontend** com mais visualizações
4. **Integrar APIs externas** (AlphaVantage, Hugging Face)
5. **Documentar APIs** com FastAPI/Swagger

---

Para dúvidas, consulte o README.md principal ou abra uma issue no GitHub.
