import numpy as np
import matplotlib.pyplot as plt

from core.hybrid_cosmology import HIDEMCosmology

def w_eff(hidem, z):
    # Definir uma aproximação do w_eff(z) — exemplo simples
    # Geralmente: w_eff = -1 + (1/3)(d ln ρ_DE / d ln a)
    a = 1/(1+z)
    delta = 1e-4
    rho = lambda a_: hidem.Omega_halo(a_)
    dlnrho_dlnA = (np.log(rho(a + delta)) - np.log(rho(a - delta))) / (np.log(a + delta) - np.log(a - delta))
    return -1 + dlnrho_dlnA / 3

hidem = HIDEMCosmology()
z_vals = np.linspace(0, 3, 100)
w_vals = np.array([w_eff(hidem, z) for z in z_vals])

plt.plot(z_vals, w_vals, label=r'$w_\mathrm{eff}(z)$')
plt.axhline(-1, color='gray', linestyle='--', label='ΛCDM (w = -1)')
plt.xlabel("Redshift (z)")
plt.ylabel(r"$w_\mathrm{eff}(z)$")
plt.legend()
plt.grid()
plt.title("Evolução do Equation of State efetivo do HIDEM")
plt.savefig("report/figs/w_eff_z.png", dpi=300)
plt.show()
