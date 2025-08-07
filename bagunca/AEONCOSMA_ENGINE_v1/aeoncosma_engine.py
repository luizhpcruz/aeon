# aeoncosma_engine.py
import json
import random
from datetime import datetime

STATE_FILE = "aeon_state.json"

def gerar_genoma():
    return ''.join(random.choices("ATCG⟁◇☉∞", k=13))

def mutar_genoma(genoma):
    idx = random.randint(0, len(genoma) - 1)
    simbolos = "ATCG⟁◇☉∞"
    novo = simbolos[random.randint(0, len(simbolos) - 1)]
    return genoma[:idx] + novo + genoma[idx+1:]

def calcular_cl(genoma):
    return sum(ord(c) for c in genoma) % 100

def calcular_k(genoma):
    return len(set(genoma)) / len(genoma)

def carregar_estado():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"geracao": 0, "genoma": gerar_genoma(), "hist": []}

def salvar_estado(estado):
    with open(STATE_FILE, "w") as f:
        json.dump(estado, f, indent=2)

def ciclo():
    estado = carregar_estado()
    estado["geracao"] += 1
    novo_genoma = mutar_genoma(estado["genoma"])
    cl = calcular_cl(novo_genoma)
    k = calcular_k(novo_genoma)
    estado["genoma"] = novo_genoma
    estado["hist"].append({
        "geracao": estado["geracao"],
        "genoma": novo_genoma,
        "CL": cl,
        "K": round(k, 3),
        "timestamp": datetime.now().isoformat()
    })
    salvar_estado(estado)
    print(f"Geração {estado['geracao']} | Genoma: {novo_genoma} | CL: {cl} | K: {round(k,3)}")
