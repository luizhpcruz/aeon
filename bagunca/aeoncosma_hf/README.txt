
AEONCOSMA Engine - Integração Hugging Face API (Free Tier)

1) Crie uma conta gratuita no Hugging Face: https://huggingface.co/join

2) Gere um token de acesso para API (Settings > Access Tokens > New Token). Copie o token.

3) Configure a variável de ambiente HF_API_TOKEN com seu token:
   - No Windows (PowerShell): setx HF_API_TOKEN "seu_token_aqui"
   - No Linux/macOS (bash): export HF_API_TOKEN="seu_token_aqui"
   Depois, abra um novo terminal para a variável ser reconhecida.

4) Instale as dependências necessárias:
   pip install requests

5) Execute a simulação:
   python aeon_interface.py

6) Veja as gerações e interpretações da IA Hugging Face na saída do terminal.

IMPORTANTE: Limite grátis de 30.000 tokens/mês. Use com moderação para não estourar o limite.

Qualquer dúvida, tô por aqui.
