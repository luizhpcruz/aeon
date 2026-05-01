# AEON + JANUS (Monorepo de Pesquisa)

Este repositório agora integra dois núcleos:

- **AEON**: simulação complexa (entropia, modelos evolutivos, cosmologia, componentes experimentais)
- **JANUS Engine**: detecção de mudança de regime de mercado (sem previsão de preço/sinal de trade)

## Estrutura principal

- `scripts/` e módulos AEON
- `janus/` motor JANUS (core, adapters, services, analytics, visual)
- `tests/` testes do JANUS e testes gerais
- `data/` e `logs/` artefatos de execução

## Princípios

- AEON: exploração computacional de sistemas dinâmicos complexos
- JANUS: sensor estrutural de regime, não oráculo de preço

## Setup rápido

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

## Execução

### AEON

Use os scripts já existentes do projeto (ex.: análises de entropia e simulações) conforme o fluxo do repositório.

### JANUS

```bash
python -m janus.services.runner AAPL
python -m janus.services.runner AAPL --log
python -m janus.analytics.analyze_logs
python -m janus.visual.plot_price_score
```

## Observações

- O merge foi feito com `--allow-unrelated-histories` para preservar os dois históricos.
- Ajustes finos de documentação podem ser feitos em seguida, mas o código de ambos os projetos está unificado neste repositório.
