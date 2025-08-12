import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Constantes naturais (em unidades normalizadas onde Mpl = 1 e H0 = 1)
Mpl = 1.0        # Massa de Planck reduzida (normalizada)
H0 = 1.0         # Hubble normalizado (define a unidade de tempo)
mA = 0.1         # Massa do campo vetorial (em unidades de H0)

# Parâmetros de densidade padrão (valores aproximados do Planck 2018)
# Omega_m inclui matéria bariônica e matéria escura fria
Omega_m = 0.315  # Parâmetro de densidade de matéria (observacional) [4, 5, 6]
Omega_r = 9.2e-5 # Parâmetro de densidade de radiação (observacional)
Omega_L = 0.0    # Aqui o campo vetorial pode fazer papel da constante cosmológica

# Tempo de integração
t_span = (0, 10)
t_eval = np.linspace(t_span, t_span[1], 1000)

# Equações diferenciais:
# y = [a, A0, dA0/dt]
def deriv(t, y):
    a, A, dA = y
    # Calcula o parâmetro de Hubble H
    # A densidade total inclui matéria, radiação e o campo escalar (que o código chama de campo vetorial)
    H = np.sqrt((Omega_m / a**3 + Omega_r / a**4 + 0.5 * (dA**2 + mA**2 * A**2)) / (3 * Mpl**2))
    dadt = H * a
    # Equação de Klein-Gordon para o campo escalar massivo
    d2A = -3 * H * dA - mA**2 * A
    return [dadt, dA, d2A]

# Condições iniciais
a0 = 1e-3  # Fator de escala inicial (universo muito jovem)
A0 = 1.0   # Amplitude inicial do campo
dA0 = 0.0  # Derivada inicial do campo
y0 = [a0, A0, dA0]

# Integração
sol = solve_ivp(deriv, t_span, y0, t_eval=t_eval, rtol=1e-8)

# Recupera variáveis
a = sol.y
A = sol.y[1]
dA = sol.y[2]
t = sol.t
H = np.sqrt((Omega_m / a**3 + Omega_r / a**4 + 0.5 * (dA**2 + mA**2 * A**2)) / (3 * Mpl**2))
rhoA = 0.5 * (dA**2 + mA**2 * A**2)
pA = 0.5 * (dA**2 - mA**2 * A**2)
wA = pA / rhoA

# Plot resultados
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, a, label="Fator de escala $a(t)$")
plt.plot(t, A, label="Campo $A_0(t)$")
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t, rhoA, label="Densidade $\\rho_A$")
plt.plot(t, wA, label="Parâmetro de estado $w_A$")
plt.grid()
plt.legend()

plt.xlabel("Tempo (unid. normalizada)")
plt.tight_layout()
plt.show()