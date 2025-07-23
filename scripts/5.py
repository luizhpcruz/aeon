import numpy as np
import matplotlib.pyplot as plt
import collections

# — Configuração —
N_FITAS = 5
N_CICLOS = 50
N_CELULAS = 32
POS_PULSO = 15
VAL_PULSO = 3

# — Função de entropia por célula —
def calcular_entropia_por_posicao(memorias):
    entropias = []
    matriz = np.array(memorias)
    for col in matriz.T:
        ativos = [v for v in col if v is not None]
        if not ativos:
            entropias.append(0.0)
        else:
            cnt = collections.Counter(ativos)
            freqs = np.array([cnt[k] for k in sorted(cnt)]) / len(ativos)
            entropias.append(-np.sum(freqs * np.log2(freqs + 1e-12)))
    return entropias

# — Inicialização com pulso em posição 15 —
fitas = [[None]*N_CELULAS for _ in range(N_FITAS)]
for i in range(N_FITAS):
    fitas[i][POS_PULSO] = VAL_PULSO

# — Evolução por ciclo —
memorias = [[] for _ in range(N_FITAS)]
for t in range(N_CICLOS):
    for i in range(N_FITAS):
        for j in range(N_CELULAS):
            if j == POS_PULSO:
                continue  # mantém o pulso fixo
            if fitas[i][j] is None or np.random.rand() < 0.05:
                fitas[i][j] = np.random.randint(0, 4)
        memorias[i].append(fitas[i][:])  # guarda o estado da fita

# — Cálculo da entropia por posição final —
entropias_por_posicao = calcular_entropia_por_posicao([f[-1] for f in memorias])

# — Visualização —
plt.figure(figsize=(10,5))
plt.plot(entropias_por_posicao, color='darkmagenta')
plt.axvline(POS_PULSO, color='orange', linestyle='--', label='Pulso na posição 15')
plt.title("Entropia por Célula — Simulação com Pulso Fixo")
plt.xlabel("Posição Genômica")
plt.ylabel("Entropia (bits)")
plt.legend()
plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()