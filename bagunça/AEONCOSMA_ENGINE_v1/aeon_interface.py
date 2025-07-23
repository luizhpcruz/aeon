import random
from aeon_gpt import interpretar_genoma

# Função para gerar o genoma simbólico
def gerar_genoma():
    simbolos = ["A", "C", "G", "☉", "◇", "∞", "⟁"]
    return ''.join(random.choices(simbolos, k=13))

# Função para simular o cálculo de CL e K
def calcular_consciência(genoma):
    CL = sum(ord(c) for c in genoma) % 100  # Consciência (simulada)
    K = round(len(set(genoma)) / len(genoma), 3)  # Complexidade simbólica (diversidade de símbolos)
    return CL, K

# Loop principal de simulação
def executar_simulação(num_geracoes=13):
    genoma = gerar_genoma()

    for i in range(1, num_geracoes + 1):
        # Simula mutação
        if random.random() < 0.7:
            index = random.randint(0, len(genoma) - 1)
            novo_simbolo = random.choice(["A", "C", "G", "☉", "◇", "∞", "⟁"])
            genoma = genoma[:index] + novo_simbolo + genoma[index+1:]

        # Calcula métricas
        CL, K = calcular_consciência(genoma)

        # Exibe info
        print(f"Geração {i} | Genoma: {genoma} | CL: {CL} | K: {K}")

        # Interpretação simbólica via GPT
        interpretacao = interpretar_genoma(genoma, CL, K)
        print("GPT interpretou:\n", interpretacao)
        print("-" * 60)

if __name__ == "__main__":
    executar_simulação(num_geracoes=13)
