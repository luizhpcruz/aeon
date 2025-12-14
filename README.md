# JANUS Engine

JANUS é um motor de análise de mercado focado em **detecção de mudança de regime**.
Ele não prevê preços, não gera sinais de compra/venda e não otimiza trades.
Seu objetivo é identificar **transições estruturais no comportamento do ativo**.

> Pense em JANUS como um sensor de estado do mercado, não como um oráculo.

---

## 📌 O que o JANUS faz

- Analisa séries de preço ponto a ponto
- Calcula um **score de tensão/instabilidade**
- Classifica o mercado em regimes:
  - `Normal`
  - `Attention`
- Detecta **mudanças de regime**
- Registra eventos em CSV para análise posterior

---

## ❌ O que o JANUS NÃO faz

- ❌ Não prevê preço
- ❌ Não gera sinais de trade
- ❌ Não substitui análise humana
- ❌ Não promete lucro

Isso é intencional.

---

## 🧠 Filosofia do Projeto

O mercado é tratado como um **sistema dinâmico**, não como uma sequência aleatória.
O foco está em **mudança de comportamento**, não em previsão pontual.

JANUS observa:
- aceleração
- dissipação
- persistência
- ruptura de padrão

---

## 📂 Estrutura do Projeto

janus/
├── adapters/ # Fontes de dados (ex: Yahoo Finance)
├── core/ # Engine principal (lógica de regime)
├── logging/ # Registro de eventos (CSV)
├── services/ # CLI / execução
├── analytics/ # Pós-análise dos logs
├── visual/ # Visualizações (plots)
tests/
data/

yaml
Copiar código

---

## ⚙️ Instalação

### 1. Clone o repositório
```bash
git clone git@github.com:luizhpcruz/janus-engine.git
cd janus-engine
2. Crie e ative o ambiente virtual
bash
Copiar código
python -m venv venv
venv\Scripts\activate   # Windows
3. Instale as dependências
bash
Copiar código
pip install -r requirements.txt
▶️ Uso Básico
Rodar análise simples
bash
Copiar código
python -m janus.services.runner AAPL
Saída:

perl
Copiar código
timestamp | price | score | state
Rodar com log em CSV
bash
Copiar código
python -m janus.services.runner AAPL --log
Gera:

bash
Copiar código
data/janus_log.csv
Analisar o comportamento do ativo
bash
Copiar código
python -m janus.analytics.analyze_logs
Exemplo de saída:

Tempo em cada regime (%)

Número de mudanças de regime

Estatísticas de score

Eventos relevantes

📊 Visualização (opcional)
bash
Copiar código
python -m janus.visual.plot_price_score
Gera gráfico de:

Preço

Score

Regimes ao longo do tempo

🧪 Testes
bash
Copiar código
python -m tests.test_synthetic
📈 Casos de Uso Reais
Monitoramento de risco

Detecção de instabilidade

Análise estrutural de ativos

Input para sistemas maiores (APIs, dashboards, IA)

🚧 Status do Projeto
✔ Core funcional

✔ CLI estável

✔ Logging validado

✔ Analytics básico

🔄 Visual em evolução

🔄 API planejada

📜 Licença
MIT