import numpy as np
import matplotlib.pyplot as plt

from core.hybrid_cosmology import HIDEMCosmology

z = np.array([0.1, 0.3, 0.5, 0.7, 1.0, 1.3, 1.5])
H_obs = np.array([69, 75, 82, 90, 95, 102, 110])
sigma = np.array([5, 6, 5, 7, 8, 10, 12])

hidem = HIDEMCosmology()
lcdm_H = lambda z_: 70 * np.sqrt(0.3*(1+z_)**3 + 0.7)  # LCDM simples

H_hidem = np.array([hidem.H(zi) for zi in z])
H_lcdm = np.array([lcdm_H(zi) for zi in z])

resid_hidem = H_obs - H_hidem
resid_lcdm = H_obs - H_lcdm

plt.errorbar(z, resid_hidem, yerr=sigma, fmt='o', label='Resíduo HIDEM', color='green')
plt.errorbar(z, resid_lcdm, yerr=sigma, fmt='s', label='Resíduo ΛCDM', color='black')

plt.axhline(0, color='gray', linestyle='--')
plt.xlabel("Redshift (z)")
plt.ylabel(r"Resíduo $H_{obs} - H_{model}$ [km/s/Mpc]")
plt.legend()
plt.grid()
plt.title("Resíduos dos modelos em relação aos dados observacionais")
plt.savefig("report/figs/residuos_vs_z.png", dpi=300)
plt.show()
