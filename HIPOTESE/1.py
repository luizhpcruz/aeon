import numpy as np
import matplotlib.pyplot as plt

# Função que gera uma sequência binária tipo Fibonacci (L=ativo, S=inativo)
def fibonacci_sequence_cover(n):
    a, b = "L", "S"
    while len(b) < n:
        a, b = b, a + b  # Substituição: L → S, S → LS
    return b[:n]

# Parâmetros do modelo
n_nos = 21  # número de nós na cadeia
fib_seq = fibonacci_sequence_cover(n_nos)

# Vetores: 1 se ativo ("L"), 0 se inativo ("S")
vetores = np.array([1 if c == 'L' else 0 for c in fib_seq])

# Direções aleatórias para visualização vetorial
angles = np.random.uniform(0, 2 * np.pi, n_nos)
u = vetores * np.cos(angles)
v = vetores * np.sin(angles)

# Posições espaciais dos nós
x = np.arange(n_nos)
y = np.zeros(n_nos)

# Visualização com quiver
plt.figure(figsize=(10, 2))
plt.quiver(x, y, u, v, scale=1, scale_units='xy', angles='xy', color='crimson')
plt.title('Cadeia Vetorial com Ativação Fibonacci')
plt.yticks([])
plt.xticks(x)
plt.grid(True, axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()