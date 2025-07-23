import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros ---
H0 = 70  # Hubble inicial [km/s/Mpc]
Mpc = 3.0857e19  # Mpc em km
H0_SI = H0 * 1e3 / Mpc  # H0 em s⁻¹

# --- Função H(t) e amortecimento ---
def H(t): return H0_SI / (1 + t / 1e17)
def Amortecedor(t): return 3 * H(t)

# --- Intervalo de tempo (até 3 Giga-anos) ---
t = np.linspace(0, 3e17, 1000)  # em segundos
t_Gyr = t / (3.154e7 * 1e9)  # em Giga-anos

# --- Plot ---
plt.figure(figsize=(10, 5))
plt.plot(t_Gyr, Amortecedor(t), color='crimson')
plt.xlabel('Tempo (Giga-anos)')
plt.ylabel('Coeficiente Amortecedor  3H(t) [s⁻¹]')
plt.title('📉 Resistência Métrica: Quem silenciou o AEON')
plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()