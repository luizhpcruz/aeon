import numpy as np
import collections
import copy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# — Função ciclo não simbólico —
def ciclo_nao_simbolico(mem, est, p_mut=0.1):
    nova = mem[:]
    for i in range(len(mem)):
        if mem[i] is not None:
            if np.random.rand() < p_mut:
                nova[i] = np.random.randint(est)
    return nova

# — Função entropia —
def calcular_entropia(mem):
    ativos = [v for v in mem if v is not None]
    if not ativos:
        return 0.0
    cnt = collections.Counter(ativos)
    freqs = np.array([cnt[k] for k in sorted(cnt)]) / len(ativos)
    return -np.sum(freqs * np.log2(freqs + 1e-12))

# — Geração de entrada —
def gerar_entrada(tipo, tamanho):
    if tipo == "aleatoria":
        return np.random.choice([None,0,1,2,3], tamanho)
    elif tipo == "pulso":
        arr = [None]*tamanho
        meio = tamanho//2
        arr[meio:meio+3] = [3,3,3]
        return arr
    elif tipo == "ruido":
        base = [0,1,2,3,None]
        return np.random.choice(base, tamanho, p=[0.1,0.1,0.1,0.1,0.6])
    else:
        return [None]*tamanho

# — Segmentação por janela —
def segmentar_e_medir(fitas_hist, janela=5):
    n_fitas, n_ciclos = fitas_hist.shape
    n_janelas = n_ciclos // janela
    ent_medias = np.zeros((n_fitas, n_janelas))
    for j in range(n_janelas):
        ent_medias[:, j] = np.mean(fitas_hist[:, j*janela:(j+1)*janela], axis=1)
    return ent_medias

# — Parâmetros —
N_CICLOS_TESTE = 50
N_FITAS = 5
N_CELULAS = 32
N_ESTADOS = 4

# — Simulação —
entradas_testes = ["aleatoria", "pulso", "ruido"]
resultados = {}

for tipo in entradas_testes:
    fitas = [[None]*N_CELULAS for _ in range(N_FITAS)]
    entrada = gerar_entrada(tipo, N_CELULAS)
    print(f"Testando entrada: {tipo}")
    
    hist_ent = np.zeros((N_FITAS, N_CICLOS_TESTE))
    
    for t in range(N_CICLOS_TESTE):
        for i in range(N_FITAS):
            for idx in range(N_CELULAS):
                fitas[i][idx] = entrada[idx]
            fitas[i] = ciclo_nao_simbolico(fitas[i], N_ESTADOS, p_mut=0.1)
        for i in range(N_FITAS):
            hist_ent[i, t] = calcular_entropia(fitas[i])
    
    resultados[tipo] = hist_ent.copy()

# — Gráfico de entropia por fita —
plt.figure(figsize=(15,10))
for idx, tipo in enumerate(entradas_testes):
    plt.subplot(3,1,idx+1)
    for i in range(N_FITAS):
        plt.plot(resultados[tipo][i], label=f"Fita {i}")
    plt.title(f"Entropia - Entrada: {tipo}")
    plt.xlabel("Ciclo")
    plt.ylabel("Entropia (bits)")
    plt.legend()
    plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()

# — Segmentação temporal —
ent_segmentada = segmentar_e_medir(resultados["aleatoria"], janela=10)
plt.figure(figsize=(8,5))
for i in range(N_FITAS):
    plt.plot(ent_segmentada[i], label=f"Fita {i}")
plt.title("Entropia Média por Janela (entrada aleatória, janela=10 ciclos)")
plt.xlabel("Janela Temporal")
plt.ylabel("Entropia Média")
plt.legend()
plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()

# — Heatmap visual —
plt.figure(figsize=(10,6))
sns.heatmap(resultados["pulso"], cmap="magma", cbar_kws={'label': 'Entropia (bits)'})
plt.title("Heatmap Entrópico — Entrada: pulso")
plt.xlabel("Ciclo Temporal")
plt.ylabel("Fita")
plt.tight_layout()
plt.show()

# — Entropia por posição genômica —
final_memorias = {tipo: [] for tipo in entradas_testes}
for tipo in entradas_testes:
    fitas_final = [[None]*N_CELULAS for _ in range(N_FITAS)]
    entrada = gerar_entrada(tipo, N_CELULAS)
    for i in range(N_FITAS):
        fitas_final[i] = entrada.copy()
        for _ in range(N_CICLOS_TESTE):
            fitas_final[i] = ciclo_nao_simbolico(fitas_final[i], N_ESTADOS, p_mut=0.1)
    final_memorias[tipo] = fitas_final

plt.figure(figsize=(12, 4))
for idx, tipo in enumerate(entradas_testes):
    matriz = np.array(final_memorias[tipo])
    entropias_por_posicao = []
    for col in matriz.T:
        ativos = [v for v in col if v is not None]
        if not ativos:
            entropias_por_posicao.append(0.0)
        else:
            cnt = collections.Counter(ativos)
            freqs = np.array([cnt[k] for k in sorted(cnt)]) / len(ativos)
            entropias_por_posicao.append(-np.sum(freqs * np.log2(freqs + 1e-12)))
    plt.subplot(1, 3, idx + 1)
    plt.plot(entropias_por_posicao, color='indigo')
    plt.title(f"Entropia por Célula — {tipo}")
    plt.xlabel("Posição Genômica")
    plt.ylabel("Entropia")
    plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()

# — Exportação opcional —
df = pd.DataFrame(resultados["pulso"].T, columns=[f"Fita {i}" for i in range(N_FITAS)])
df.to_csv("entropia_pulso.csv", index=False)