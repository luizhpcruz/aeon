# AEON Evolution - Simulador Evolutivo

## 🌟 Visão Geral

O **AEON Evolution** é um simulador evolutivo avançado baseado na equação matemática:

```
F(t) = A * sin(Bt + φ) + C * e^(-λt) + D * log(t + 1)
```

Este sistema modela crescimento, interação e mutação com dinâmica caótica controlada, permitindo simulações de:
- 🧬 Evolução de espécies
- 🌱 Ecossistemas complexos
- 🦅 Interações predador-presa
- 🔄 Cadeias evolutivas dinâmicas

**Desenvolvido por Luiz Cruz - 2025**

## 🔬 Componentes da Equação

### Parâmetros Base:
- **A, B, φ**: Oscilação de fase (simula fatores externos)
- **C, λ**: Decaimento ou estabilidade estrutural  
- **D**: Memória/influência acumulativa

### Cadeia Ligada:
```
Fₙ(t) = Fₙ₋₁(t) * αₙ + βₙ * dFₙ₋₁/dt + γₙ
```

## 🚀 Execução Rápida

### Docker (Recomendado)
```bash
docker build -t aeon-evo .
docker run -v $(pwd)/aeon/output:/app/aeon/output aeon-evo
```

### Python Local
```bash
pip install -r requirements.txt
python main.py
```

## 📊 Tipos de Simulação

### 1. Simulação Básica
- 3 espécies com parâmetros diferentes
- Cadeia evolutiva simples
- Análise de estabilidade

### 2. Ecossistema Complexo
- Múltiplas espécies interagindo
- Competição, predação, simbiose
- Evolução de parâmetros adaptativos

### 3. Sistema Predador-Presa
- Dinâmica clássica de Lotka-Volterra adaptada
- Análise de oscilações populacionais
- Estudo de coevolução

### 4. Experimento de Mutação
- Mutação adaptativa baseada em fitness
- Seleção natural automática
- Evolução de longo prazo

## 📁 Estrutura de Saída

```
aeon/output/
├── results.txt           # Resultados numéricos principais
├── logs.txt              # Logs detalhados da simulação
├── ecosystem_results.txt # Dados do ecossistema
├── predator_prey_results.txt # Sistema predador-presa
├── mutation_results.txt  # Experimento evolutivo
└── comprehensive_report.txt # Relatório final
```

## 🔧 Configuração Avançada

### Parâmetros Personalizados
```python
# Exemplo de configuração
params = [
    [A, B, phi, C, lambd, D],  # Espécie 1
    [A, B, phi, C, lambd, D],  # Espécie 2
    # ... mais espécies
]
```

### Interações Customizadas
```python
from aeon.dynamics import InteractionRule

rule = InteractionRule(
    species_a="predator",
    species_b="prey",
    interaction_type="predation",
    strength=0.3
)
```

## 📈 Interpretação dos Resultados

### Métricas de Fitness
- **Estabilidade**: Baixa variância nos valores finais
- **Sustentabilidade**: Consistência ao longo do tempo
- **Crescimento**: Desenvolvimento positivo moderado
- **Robustez**: Resistência a perturbações

### Análise de Rede
- **Densidade**: Conectividade do ecossistema
- **Centralidade**: Importância de cada espécie
- **Diversidade**: Variedade de tipos de interação

## 🧪 Casos de Uso

### Pesquisa Acadêmica
- Modelagem de sistemas complexos
- Estudos de dinâmica populacional
- Teoria de redes ecológicas

### Desenvolvimento de IA
- Algoritmos evolutivos
- Otimização de parâmetros
- Sistemas adaptativos

### Análise Financeira
- Modelagem de mercados
- Evolução de estratégias
- Análise de risco sistêmico

## 🔬 Algoritmos Implementados

### Engine Principal
- Cálculo otimizado da equação AEON
- Derivadas numéricas automáticas
- Análise de estabilidade em tempo real

### Simulador Evolutivo
- Múltiplas estratégias de simulação
- Ensemble methods para confiabilidade
- Análise espectral (FFT)

### Dinâmica de Cadeias
- Redes de interação complexas
- Evolução de parâmetros adaptativa
- Métricas de fitness multi-critério

## 📚 Exemplos de Uso

### Simulação Básica
```python
from aeon.simulator import AeonSimulator

simulator = AeonSimulator()
t, results = simulator.simulate_chain(
    n_species=3,
    t_range=50,
    params_list=[[1,2,0.1,0.5,0.01,1], ...]
)
```

### Ecossistema Personalizado
```python
from aeon.dynamics import ChainDynamics

dynamics = ChainDynamics()
dynamics.create_default_ecosystem(n_species=5)
results = dynamics.run_evolutionary_simulation(generations=20)
```

## 🔍 Validação e Testes

### Testes Automatizados
- Validação numérica da equação
- Testes de convergência
- Verificação de estabilidade

### Benchmarks
- Performance computacional
- Precisão numérica
- Escalabilidade

## 🛠 Desenvolvimento

### Estrutura do Código
```
aeon/
├── __init__.py       # Exportações principais
├── engine.py         # Equação AEON e cálculos base
├── simulator.py      # Simulação evolutiva
├── dynamics.py       # Dinâmicas de interação
└── output/           # Resultados das simulações
```

### Extensibilidade
- Interface modular para novos tipos de interação
- Sistema de plugins para análises customizadas
- API clara para integração externa

## 📄 Licença

Este projeto está licenciado sob a MIT License. Veja `../LICENSE` para detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas, problemas ou sugestões:
- 📧 Email: [contato]
- 🐛 Issues: GitHub Issues
- 📖 Docs: Consulte este README

---

**AEON Evolution** - Onde a matemática encontra a evolução! 🧬✨
