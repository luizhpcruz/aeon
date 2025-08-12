import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parâmetros da simulação
n_bubbles = 21             # Número de bolhas
timesteps = 100            # Número de frames
max_radius = 1.5           # Raio máximo da bolha
growth_rate = 0.015        # Velocidade de expansão
rotation_speed = 0.2       # Velocidade de rotação vetorial

# Geração da sequência de ativação tipo Fibonacci
def fibonacci_sequence_cover(n):
    a, b = "L", "S"
    while len(b) < n:
        a, b = b, a + b  # L → S, S → LS
    return b[:n]

fib_seq = fibonacci_sequence_cover(n_bubbles)
active = np.array([1 if c == 'L' else 0 for c in fib_seq])

# Posições das bolhas (em círculo)
angles_init = np.linspace(0, 2 * np.pi, n_bubbles, endpoint=False)
x_init = np.cos(angles_init) * 5
y_init = np.sin(angles_init) * 5

# Criar a figura
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_aspect('equal')
ax.axis('off')

# Função de atualização por frame
def update(frame):
    ax.cla()
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal')
    ax.axis('off')

    for i in range(n_bubbles):
        if active[i] == 0:
            continue
        radius = min(frame * growth_rate, max_radius)
        angle = angles_init[i] + frame * rotation_speed
        x = x_init[i]
        y = y_init[i]
        # Desenha bolha
        bubble = plt.Circle((x, y), radius, color='deepskyblue', alpha=0.4)
        ax.add_patch(bubble)
        # Desenha vetor girando
        dx = np.cos(angle) * radius
        dy = np.sin(angle) * radius
        ax.arrow(x, y, dx, dy, head_width=0.15, head_length=0.3, fc='crimson', ec='crimson')

    return ax.patches

# Criar animação
ani = animation.FuncAnimation(fig, update, frames=timesteps, interval=100, blit=True)

# Salvar como GIF
ani.save("bolhas_vetoriais.gif", writer=animation.PillowWriter(fps=20))
print("GIF gerado com sucesso: bolhas_vetoriais.gif")
