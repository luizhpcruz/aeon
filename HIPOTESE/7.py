import numpy as np
import collections
import matplotlib.pyplot as plt

# --- Parâmetros Globais ---
N_CELULAS = 32
N_ESTADOS = 4
N_CICLOS = 40
P_ACOP = 0.8

# --- Funções de Memória ---
def inicializar_memoria(num_celulas, num_estados):
    memoria = [None] * num_celulas
    for i in range(0, num_celulas, 2):
        memoria[i] = np.random.randint(num_estados)
    return memoria

def colapsar(memoria):
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

def mutacao_estado(a, b, num_estados):
    if a is None or b is None:
        return None
    base = (2 * a + b) % num_estados
    mut = np.random.choice([0, 1], p=[0.9, 0.1])
    return (base + mut) % num_estados

def ciclo_simbolico(memoria, num_estados, direcao=1):
    nova = list(memoria)
    indices = range(2, len(memoria)) if direcao == 1 else range(len(memoria) - 3, -1, -1)
    for i in indices:
        i1 = (i - direcao) % len(memoria)
        i2 = (i - 2 * direcao) % len(memoria)
        if memoria[i1] is not None and memoria[i2] is not None:
            nova[i] = mutacao_estado(memoria[i1], memoria[i2], num_estados)
    return colapsar(nova)

def calcular_entropia(mem):
    ativos = [v for v in mem if v is not None]
    if not ativos:
        return 0.0
    cnt = collections.Counter(ativos)
    freq = np.array([cnt[k] for k in sorted(cnt)]) / len(ativos)
    return -np.sum(freq * np.log2(freq + 1e-12))

def acoplar_silencios(origem, destino, prob, num_estados):
    for i, v in enumerate(origem):
        if v is None and np.random.rand() < prob:
            destino[i] = num_estados - 1
    return origem, destino

def injetar_ruido(memoria, intensidade=0.3):
    for i in range(len(memoria)):
        if np.random.rand() < intensidade:
            memoria[i] = np.random.randint(N_ESTADOS) if np.random.rand() < 0.5 else None
    return memoria

# --- Execução Principal ---
if __name__ == "__main__":
    A = inicializar_memoria(N_CELULAS, N_ESTADOS)
    B = inicializar_memoria(N_CELULAS, N_ESTADOS)
    historico_A, historico_B = [], []
    ultimas_entropias = []
    direcao = 1

    print("Iniciando simulação com reversão adaptativa e ruído controlado...")

    for ciclo in range(1, N_CICLOS + 1):
        A = ciclo_simbolico(A, N_ESTADOS, direcao)
        B = ciclo_simbolico(B, N_ESTADOS, direcao)
        A, B = acoplar_silencios(B, A, P_ACOP, N_ESTADOS)
        B, A = acoplar_silencios(A, B, P_ACOP, N_ESTADOS)

        HA = calcular_entropia(A)
        HB = calcular_entropia(B)

        historico_A.append(HA)
        historico_B.append(HB)
        media_H = (HA + HB) / 2
        ultimas_entropias.append(media_H)

        # --- Inversão de direção por variação baixa
        if len(ultimas_entropias) > 5:
            ultimas_entropias.pop(0)
            var_H = max(ultimas_entropias) - min(ultimas_entropias)
            if var_H < 0.01:
                direcao *= -1
                print(f"[!] Ciclo {ciclo}: Gargalo detectado. Invertendo direção para {direcao}")

        # --- Ruído adaptativo se entropia congelar
        if ciclo > 5:
            delta_A = abs(historico_A[-1] - historico_A[-2])
            delta_B = abs(historico_B[-1] - historico_B[-2])
            if delta_A < 1e-4:
                A = injetar_ruido(A, 0.2)
                print(f"[~] Ciclo {ciclo}: Injetando ruído em A")
            if delta_B < 1e-4:
                B = injetar_ruido(B, 0.2)
                print(f"[~] Ciclo {ciclo}: Injetando ruído em B")

        # --- Reinicialização total se 10 ciclos com entropia idêntica
        if len(historico_B) >= 10 and all(abs(historico_B[-i] - historico_B[-i-1]) < 1e-6 for i in range(1, 10)):
            B = inicializar_memoria(N_CELULAS, N_ESTADOS)
            print(f"[X] Ciclo {ciclo}: Reinicializando completamente Fita B")

        print(f"Ciclo {ciclo:2d} — Entropia A: {HA:.3f} | Entropia B: {HB:.3f}")

    # --- Plotagem
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, N_CICLOS + 1), historico_A, marker='o', label="Fita A")
    plt.plot(range(1, N_CICLOS + 1), historico_B, marker='s', label="Fita B")
    plt.title("Entropia Simbólica com Recuperação Adaptativa")
    plt.xlabel("Ciclo")
    plt.ylabel("Entropia (bits)")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig("entropia_recuperada.png")
    plt.show()

    print("Simulação finalizada.")
