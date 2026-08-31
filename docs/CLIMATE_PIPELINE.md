# Pipeline público de CO₂ e temperatura global

O `scripts/climate_pipeline.py` executa um experimento **offline** com duas séries mensais públicas: CO₂ médio de Mauna Loa, da NOAA, e anomalia média global de temperatura Land-Ocean Temperature Index, da NASA GISTEMP v4.

A NOAA fornece o CSV mensal de Mauna Loa com metadados comentados e colunas `year`, `month` e `average` [1]. A NASA fornece o arquivo `GLB.Ts+dSST.csv`, cuja primeira linha identifica a tabela, a segunda contém `Year` e os meses, e as linhas seguintes contêm anomalias mensais relativas à climatologia de 1951–1980 [2]. O leitor do AEON conhece esses dois formatos sem depender de pandas ou de download durante a análise.

## Instalação

Na raiz do repositório, use um ambiente Python isolado:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

O pipeline usa somente a biblioteca padrão e o módulo `ScenarioPredictor` do AEON. O arquivo de entrada deve ser baixado separadamente e armazenado fora do Git.

## Obtenção dos dados

```bash
mkdir -p /srv/aeon/public-data
curl -fsSL \
  'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.csv' \
  -o /srv/aeon/public-data/co2_mm_mlo.csv

curl -fsSL \
  'https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv' \
  -o /srv/aeon/public-data/GLB.Ts+dSST.csv
```

Essa etapa de download deve permanecer separada da análise offline. Registre o SHA-256 de cada arquivo e confira as páginas oficiais antes de substituir uma versão de dados.

## Execução

```bash
python3 scripts/climate_pipeline.py \
  --co2 /srv/aeon/public-data/co2_mm_mlo.csv \
  --temperature /srv/aeon/public-data/GLB.Ts+dSST.csv \
  --holdout 24 \
  --output-dir /srv/aeon/experiments/climate-001
```

O programa alinha as séries por mês, usa somente o período comum, reserva os últimos meses como teste e executa previsão de um passo à frente para cada alvo. Para cada série, compara o AEON com um baseline que repete o último valor.

## Saídas

| Arquivo | Conteúdo |
|---|---|
| `summary.json` | Hashes, período, tamanho, métricas, confiança e limitações |
| `aligned_climate.csv` | Série pública alinhada por mês |
| `co2_predictions.csv` | Previsões e valores observados de CO₂ no holdout |
| `temperature_predictions.csv` | Previsões e valores observados de temperatura no holdout |

Esses artefatos podem conter dados públicos e devem permanecer fora do repositório quando o diretório também for usado para dados privados. O `.gitignore` do projeto já exclui `data/`, `runs/offline/` e `experiments/`.

## Métricas

O relatório inclui MAE, RMSE, viés, MASE, acurácia direcional, taxa de abstinência e confiança média. MASE menor que 1 indica erro inferior ao baseline ingênuo de primeira diferença no treino; ainda assim, a conclusão deve considerar várias janelas temporais.

A confiança do `ScenarioPredictor` é heurística. Ela não deve ser interpretada como probabilidade calibrada. O pipeline não faz inferência causal, não prevê o clima global completo e não executa ações externas.

## Fontes

[1]: https://gml.noaa.gov/ccgg/trends/data.html "NOAA Global Monitoring Laboratory — CO₂ data"
[2]: https://data.giss.nasa.gov/gistemp/data_v4.html "NASA GISS GISTEMP v4 — Data Downloads"
