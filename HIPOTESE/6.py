import numpy as np
import collections
import matplotlib.pyplot as plt

# --- Parâmetros Globais ---
N_CELULAS = 32    # Tamanho da RAM simbólica
N_ESTADOS = 4     # Número de estados vetoriais (0, 1, 2, 3)
N_CICLOS  = 40    # Número de ciclos de evolução
P_ACOP    = 0.8   # Probabilidade de acoplamento nos silêncios

# --- Funções de Manipulação da Memória ---
def inicializar_memoria(num_celulas: int, num_estados: int) -> list:
    memoria = [None] * num_celulas
    for i in range(0, num_celulas, 2):
        memoria[i] = np.random.randint(num_estados)
    return memoria

def colapsar(memoria: list) -> list:
    memoria_colapsada = []
    i = 0
    while i < len(memoria):
        a = memoria[i]
        b = memoria[i+1] if i + 1 < len(memoria) else None
        if a == 0 and b == 1:
            memoria_colapsada.extend([None, None])
            i += 2
        else:
            memoria_colapsada.append(a)
            i += 1
    return memoria_colapsada

def mutacao_estado(estado_anterior: int | None, estado_atual: int | None, num_estados: int) -> int | None:
    if estado_anterior is None or estado_atual is None:
        return None
    base = (2 * estado_atual + estado_anterior) % num_estados
    mut = np.random.choice([0, 1], p=[0.9, 0.1])
    return (base + mut) % num_estados

def ciclo_simbolico(memoria: list, num_estados: int, direcao=1) -> list:
    nova_memoria = list(memoria)
    if direcao == 1:
        indices = range(2, len(memoria))
    else:
        indices = range(len(memoria)-3, -1, -1)
    for i in indices:
        idx1 = (i - direcao) % len(memoria)
        idx2 = (i - 2*direcao) % len(memoria)
        if memoria[idx2] is not None and memoria[idx1] is not None:
            nova_memoria[i] = mutacao_estado(memoria[idx1], memoria[idx2], num_estados)
    return colapsar(nova_memoria)

def calcular_entropia(memoria: list) -> float:
    ativos = [v for v in memoria if v is not None]
    if not ativos:
        return 0.0
    contagem = collections.Counter(ativos)
    frequencias = np.array([contagem[k] for k in sorted(contagem)]) / len(ativos)
    return -np.sum(frequencias * np.log2(frequencias + 1e-12))

def acoplar_silencios(memoria_origem: list, memoria_destino: list, prob_acoplamento: float, num_estados: int) -> tuple[list, list]:
    for i, valor in enumerate(memoria_origem):
        if valor is None and np.random.rand() < prob_acoplamento:
            memoria_destino[i] = num_estados - 1
    return memoria_origem, memoria_destino

# --- Execução Principal ---
if __name__ == "__main__":
    A = inicializar_memoria(N_CELULAS, N_ESTADOS)
    B = inicializar_memoria(N_CELULAS, N_ESTADOS)
    
    historico_A = []
    historico_B = []
    ultimas_entropias = []
    direcao = 1

    print("Iniciando simulação de RAM Acoplada com Inversão de Direção...")
    for ciclo in range(1, N_CICLOS + 1):
        A = ciclo_simbolico(A, N_ESTADOS, direcao)
        B = ciclo_simbolico(B, N_ESTADOS, direcao)

        A, B = acoplar_silencios(B, A, P_ACOP, N_ESTADOS)
        B, A = acoplar_silencios(A, B, P_ACOP, N_ESTADOS)

        entropia_A = calcular_entropia(A)
        entropia_B = calcular_entropia(B)

        historico_A.append(entropia_A)
        historico_B.append(entropia_B)

        ultimas_entropias.append((entropia_A + entropia_B) / 2)
        if len(ultimas_entropias) > 5:
            ultimas_entropias.pop(0)
            var_entropia = max(ultimas_entropias) - min(ultimas_entropias)
            if var_entropia < 0.01:
                direcao *= -1
                print(f"Gargalo detectado no ciclo {ciclo}, invertendo direção para {direcao}")

        print(f"Ciclo {ciclo:2d} — Entropia A: {entropia_A:.3f} | Entropia B: {entropia_B:.3f}")

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, N_CICLOS + 1), historico_A, marker='o', linestyle='-', label="Fita A")
    plt.plot(range(1, N_CICLOS + 1), historico_B, marker='s', linestyle='--', label="Fita B")
    plt.title("Entropia Simbólica com Direção Adaptativa")
    plt.xlabel("Ciclo")
    plt.ylabel("Entropia (bits)")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig("entropia_direcao_adaptativa.png")
    plt.show()

    print("Simulação concluída.")
