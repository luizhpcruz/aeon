# Fase 2 — Predição offline

A Fase 2 executa um experimento local e reproduzível sobre uma série numérica. O processo não coleta dados, não acessa a rede e não executa ações externas. O arquivo de entrada permanece no computador do usuário; apenas seu nome e hash são registrados no resumo.

## Preparação

Use um ambiente Python isolado e instale as dependências já adotadas pelo projeto. O CSV precisa ter uma coluna temporal e uma coluna numérica. Um esquema mínimo é:

```csv
date,measure
2026-01-01,0.40
2026-02-01,0.45
2026-03-01,0.48
2026-04-01,0.55
```

Para dados comportamentais, prepare uma cópia minimizada. Remova nome, e-mail, telefone, endereço, localização precisa, texto livre e qualquer credencial. Use somente a medida necessária para a pergunta definida no experimento. Não coloque o CSV no repositório; as regras de exclusão já cobrem `data/`, `runs/offline/`, CSVs e JSONs.

## Execução

A partir da raiz do repositório:

```bash
PYTHONPATH=src python3 scripts/offline_predict.py \
  --input /srv/aeon/processed/serie.csv \
  --date-column date \
  --value-column measure \
  --holdout 12 \
  --output-dir /srv/aeon/experiments/run-001
```

O script ordena a série temporal, ignora linhas vazias, rejeita colunas ausentes e rejeita valores inválidos. Os últimos pontos ficam fora do treino. Em cada ponto de teste, o AEON prevê usando somente o histórico disponível até aquele momento.

## Artefatos

O diretório de saída contém `summary.json`, com hash do arquivo, período, quantidade de registros, métricas, confiança média, taxa de abstinência e indicação de execução offline. O arquivo `predictions.csv` contém a comparação ponto a ponto; por isso deve permanecer em armazenamento privado e não deve ser enviado ao GitHub quando contiver dados pessoais.

As métricas principais são MAE e RMSE para o AEON e para o baseline que repete o último valor. O resultado só deve ser considerado uma melhoria se superar o baseline em múltiplas janelas temporais. Confiança alta não equivale a certeza; a confiança atual é heurística e deve ser calibrada em uma etapa posterior.

## Procedimento de revisão

Antes de aceitar o resultado, confirme a origem e o hash do arquivo, revise a amostra minimizada, confira se a divisão temporal não vazou o futuro e examine os casos de maior erro. Se houver poucos registros, valores não finitos ou volatilidade excessiva, o sistema pode se abster. A abstinência é uma saída segura e não deve ser contornada automaticamente.

Este pipeline deve permanecer em predição offline. Não ligar a saída diretamente a mensagens, contas, publicação, operações financeiras ou mudanças de configuração. Para uma etapa posterior, o módulo quântico deve consumir somente dados processados e ser comparado ao mesmo baseline, na mesma divisão temporal.
