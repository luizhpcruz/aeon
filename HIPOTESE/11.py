# classificador_entropia.py

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report

# — Geração de séries sintéticas de entropia —

def gerar_aleatoria(n_fitas, n_ciclos):
    base = 1.98
    return base + np.random.normal(0, 0.005, size=(n_fitas, n_ciclos))

def gerar_pulso(n_fitas, n_ciclos):
    arr = np.zeros((n_fitas, n_ciclos))
    for i in range(n_fitas):
        for t in range(n_ciclos):
            if 20 <= t <= 22:
                arr[i, t] = 1.5 + 0.1 * np.random.rand()
            else:
                arr[i, t] = 0.5 + 1.0 * np.exp(-0.1 * abs(t - 21)) + 0.02 * np.random.randn()
    return arr

def gerar_ruido(n_fitas, n_ciclos):
    return np.random.uniform(0.8, 1.5, size=(n_fitas, n_ciclos))

# — Constantes —
N_FITAS  = 5
N_CICLOS = 50

# — Montagem dos dados —
resultados = {
    "aleatoria": gerar_aleatoria(N_FITAS, N_CICLOS),
    "pulso":     gerar_pulso(N_FITAS, N_CICLOS),
    "ruido":     gerar_ruido(N_FITAS, N_CICLOS),
}

# — Extração de features: média e desvio em janelas de 10 ciclos —
X, y = [], []
for label, hist in resultados.items():
    for fita in hist:
        feats = []
        for j in range(5):
            bloco = fita[j*10:(j+1)*10]
            feats += [bloco.mean(), bloco.std()]
        X.append(feats)
        y.append(label)

X = np.array(X)  # shape (15, 10)
y = np.array(y)

# — Treino/Teste e Avaliação —
Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, random_state=42)
clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(Xtr, ytr)
y_pred = clf.predict(Xte)

print("Acurácia:", clf.score(Xte, yte))
print("\nMatriz de Confusão:")
print(confusion_matrix(yte, y_pred, labels=list(resultados.keys())))
print("\nRelatório de Classificação:")
print(classification_report(yte, y_pred, target_names=list(resultados.keys())))