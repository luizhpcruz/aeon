import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Densidade relativa dos SMBHs observados (normalizada)
def rho_BH_z(z):
    return np.exp(-0.5*((z - 1.5)/0.6)**2)

# Inverter para função de a
def rho_BH_a(a):
    z = 1/a - 1
    return rho_BH_z(z)

# Normalizar para comparar com Ω_halo
a_vals = np.linspace(0.1, 1.0, 300)
rho_norm = rho_BH_a(a_vals) / rho_BH_a(1.0)  # normaliza no presente

# Ajustar com Ω_halo(a) = Ω₀·a^{-m}·exp(–a_c/a)
def omega_halo_like(a, Omega0, m, a_c):
    return Omega0 * a**(-m) * np.exp(-a_c / a)

popt, _ = curve_fit(omega_halo_like, a_vals, rho_norm, p0=[0.7, 0.8, 1.0])

# Parâmetros ajustados
Omega0_fit, m_fit, ac_fit = popt

# Plotando comparação
plt.figure(figsize=(8,5))
plt.plot(1/a_vals - 1, rho_norm, 'k', lw=2, label='ρ_BH(z) normalizado')
plt.plot(1/a_vals - 1, omega_halo_like(a_vals, *popt), 'C1--', lw=2,
         label=f'Ajuste: Ω₀={Omega0_fit:.2f}, m={m_fit:.2f}, a_c={ac_fit:.2f}')
plt.xlabel('Redshift z')
plt.ylabel('Densidade relativa')
plt.title('Pode o perfil de SMBHs gerar Ω_halo(a)?')
plt.legend()
plt.gca().invert_xaxis()
plt.grid()
plt.tight_layout()
plt.show()