# Predição experimental e privacidade

O módulo `src/core/prediction.py` fornece um baseline determinístico para prever o próximo ponto de uma série numérica. Ele usa a média das primeiras diferenças como tendência e retorna uma previsão central, cenários baixo/central/alto, confiança aproximada e uma indicação explícita de abstinência.

O módulo é deliberadamente **local, explicável e sem efeitos externos**. Não coleta dados, não acessa APIs, não grava informações pessoais e não executa ações. Ele deve ser usado como referência para comparar modelos mais sofisticados, inclusive modelos quântico-inspirados.

## Uso

```python
from core.prediction import PrivacyFilter, ScenarioPredictor

record = {"email": "remover", "energia": 0.7, "foco": 0.8}
clean_record = PrivacyFilter().remove_sensitive_fields(record)

result = ScenarioPredictor().predict([0.40, 0.45, 0.48, 0.55, 0.59])
print(result.forecast)
print(result.scenarios)
print(result.confidence)
print(result.abstained)
```

O `PrivacyFilter` remove identificadores e credenciais conhecidos antes da preparação dos dados. Ele não substitui anonimização completa, controle de acesso, criptografia ou revisão de privacidade. Para dados pessoais reais, recomenda-se trabalhar com uma cópia minimizada e anonimizada.

## Política de abstinência

O preditor se abstém quando há poucas observações, valores não finitos ou volatilidade relativa acima do limite configurado. A abstinência deve ser tratada como uma saída válida do sistema, não como uma falha a ser contornada automaticamente.

```python
predictor = ScenarioPredictor(
    minimum_observations=8,
    max_relative_volatility=1.0,
)
```

A saída não é diagnóstico médico, aconselhamento financeiro, previsão garantida nem autorização para executar ações. A camada de decisão deve comparar o resultado com um baseline clássico, avaliar dados fora da amostra e aplicar limites independentes antes de qualquer automação.

## Próxima etapa

O uso recomendado é comparar este baseline com o módulo quântico simulado e medir ganho real em dados históricos anonimizados. As métricas devem incluir erro de previsão, calibração, estabilidade, falsos positivos, custo computacional e taxa de abstinência. Nenhum modelo deve acessar execução real enquanto não houver evidência reproduzível e supervisão operacional.
