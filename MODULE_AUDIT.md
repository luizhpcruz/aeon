# AEON Module Audit (Proposta de Limpeza)

Data: 2025-08-10
Estado atual: Repositório disperso, redundâncias, versões antigas, bundles pesados.
Objetivo: Reduzir à espinha dorsal mínima + manter histórico em arquivo.

## Critérios de Valor

- CORE: Necessário para demo mínima integrada (entropia, consciência simbólica, cosmologia simples, launcher, dashboards).
- SUPPORT: Útil para evolução futura (docs, modelos avançados digital_twin, P2P, PINN, Bayesian) mas não obrigatório no MVP.
- LEGACY: Versões antigas/duplicadas, protótipos brutos, arquivos gerados, dumps, pacotes zip.
- GENERATED: Artefatos de execução (png, json de relatórios, .dxf, .csv) que podem ser regenerados.
- HEAVY_ENV: Ambientes ou libs vendorizadas dentro do repo (evitar).

## Classificação por Diretório (Resumo)

| Caminho | Classe | Observação |
|---------|--------|------------|
| scripts/1.py..5.py | LEGACY | Evolutivas antigas (sobrepostas por teste_entropia.py) |
| scripts/4.py | CORE | Análise de entropia original |
| scripts/NMD.py | SUPPORT | Cosmologia completa (avançado) |
| teste_entropia.py | CORE | Entropia simplificada preferencial |
| teste_simples.py | CORE | V.E.R.N.A. minimal |
| teste_cosmologia.py | CORE | Cosmologia demo rápida |
| teste_aeon_cosma.py | CORE | Motor Cosma simplificado |
| aeon_dashboard.py | CORE | Dashboard web |
| aeon_dashboard_simples.py | CORE | Dashboard console |
| aeon_launcher.py | CORE | Orquestrador |
| start_dashboard.bat | CORE | Launch helper |
| bagunca/ (soltos) | LEGACY | Protótipos redundantes |
| bagunca/AEONCOSMA_ENGINE_v1/ | SUPPORT | Engine legado arquivar |
| digital_twin/ | SUPPORT | Suite avançada (P2P, PINN, Bayesian) |
| digital_twin/aeoncosma/ | SUPPORT | Rede/P2P avançada |
| digital_twin/ (arquivos .json/.png/.dxf) | GENERATED | Relatórios/diagramas |
| aeoncosma/ (raiz) | LEGACY | Possível duplicado |
| aeoncosma_simulation_bundle/ | LEGACY | Bundle empacotado |
| AEONCOSMA_WINDOWS_PACKAGE/ | LEGACY | Pacote antigo |
| frontend/ | SUPPORT | React trading UI |
| IA p2p trader/ | HEAVY_ENV | Ambiente vendorizado |
| GovTech/ | HEAVY_ENV | Ambiente vendorizado |
| visualizations/ | GENERATED | Saídas gráficas |
| data/ | GENERATED | Dados regeneráveis |
| docs/ + *.md | SUPPORT | Documentação |
| symbolic_core.py | SUPPORT | Núcleo potencial |
| deepseek_python_*.py | LEGACY | Script isolado |
| equacao_aeon_simulacao_evolutiva_informacional.* | SUPPORT | Material explicativo |
| venv/ | HEAVY_ENV | Não versionar |

aeon/
## MVP Proposto (Pasta Limpa)

```text
aeon/
  README.md
  requirements.txt  # mínimo
  aeon_launcher.py
  aeon_dashboard.py
  aeon_dashboard_simples.py
  start_dashboard.bat
  teste_entropia.py
  teste_simples.py
  teste_cosmologia.py
  teste_aeon_cosma.py
```

## Ações Sugeridas (Etapas)

1. Criar pasta `archive/` e mover LEGACY e bundles pesados.
2. Criar pasta `advanced/` para `digital_twin/` e `frontend/` (ou separar em outro repo).
3. Remover do git (git rm) diretórios com ambientes (`IA p2p trader/`, `GovTech/`, `venv/`).
4. Ajustar `.gitignore` (já parcialmente feito) para reforçar exclusões.
5. Requirements reduzido (feito nesta etapa).
6. Adicionar script `cleanup_plan.py` que lista e pede confirmação antes de mover.

## Lista de Caminhos para Arquivar (LEGACY)

```text
bagunca/AEON.py
bagunca/AEON1.py
bagunca/AEON12.py
bagunca/AEON3.py
bagunca/AEONCOSMA_ENGINE_v1/
AEONCOSMA_WINDOWS_PACKAGE/
aeoncosma_simulation_bundle/
aeoncosma/
frontend/
IA p2p trader/
GovTech/
digital_twin/ (-> advanced/)
visualizations/
data/
```

(Manter `digital_twin/` fora do MVP mas não perder – mover para `advanced/`).

## Próximos Passos

- Gerar `cleanup_plan.py`.
- Executar e revisar lista.
- Mover arquivos após confirmação.
- Commit: `chore: modular cleanup and archive legacy components`.

Confirme com "aplicar plano" para eu gerar o script de limpeza.
