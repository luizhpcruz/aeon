
import os
import requests

# Substitua pelo seu token de acesso Hugging Face (grátis após criar conta)
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

if not HF_API_TOKEN:
    raise RuntimeError("Variável de ambiente HF_API_TOKEN não configurada")

API_URL = "https://api-inference.huggingface.co/models/distilgpt2"

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def interpretar_genoma(genoma, CL, K):
    prompt = f"Genoma: {genoma}\nConsciência: {CL}\nComplexidade: {K}\nInterprete filosoficamente, poeticamente:"

    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 50, "temperature": 0.7}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # O resultado é uma lista com texto gerado na chave 'generated_text'
        texto_gerado = result[0]['generated_text'] if isinstance(result, list) else str(result)

        # Limpa e retorna só a parte da geração após o prompt
        texto = texto_gerado.replace(prompt, "").strip()
        return texto or "[Sem resposta do modelo]"
    except Exception as e:
        return f"[ERRO HF] {e}"
