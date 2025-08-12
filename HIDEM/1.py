import numpy as np
import matplotlib.pyplot as plt

# --- 1) Constantes cosmológicas ---
H0 = 70.0                       # km/s/Mpc
c  = 299792.458                 # km/s
Omega_m = 0.295
Omega_r = 9e-5
Omega_L = 1 - Omega_m - Omega_r

# --- 2) Parâmetros HIDEM ---
Omega_seed = 0.672
m          = -0.822
a_c        = 1.312

# --- 3) Parâmetro de acoplamento buracos-negros ---
def rho_BH_z(z):
    return np.exp(-0.5*((z - 1.5)/0.5)**2)  # pico em z~1.5

alpha = 0.1  # força de acoplamento SMBH→energia escura

# --- 4) Termo f(R) simples ---
fR0 = 1e-5
n   = 1.0

# --- 5) Funções ---
def Omega_halo(a):
    return Omega_seed * a**(-m) * np.exp(-a_c / a)

def Omega_BH(a):
    z = 1/a - 1
    return alpha * rho_BH_z(z) / rho_BH_z(0) * Omega_L

def Omega_fR(a):
    return fR0 * a**(-n)

def H2_mix(a):
    bkg = Omega_m * a**(-3) + Omega_r * a**(-4)
    de  = Omega_L + Omega_halo(a) + Omega_BH(a) + Omega_fR(a)
    return bkg + de

# --- 6) Dados observacionais H(z) ---
z_obs = np.array([0.07, 0.12, 0.17, 0.27, 0.4, 0.48, 0.9, 1.3, 1.43, 1.75])
Hz_obs = np.array([69, 68.6, 83, 77, 95, 97, 117, 168, 177, 202])
Hz_err = np.array([19.6, 26.2, 8.0, 14, 17, 60, 23, 17, 18, 40])

# --- 7) Avaliação no grid ---
z = np.linspace(0, 4, 400)
a = 1 / (1 + z)
Hz_mix = H0 * np.sqrt(H2_mix(a))
Hz_LCDM = H0 * np.sqrt(Omega_m * (1 + z)**3 + Omega_L)

# --- 8) Plot: Curvas com dados ---
plt.figure(figsize=(8.5,5.5))
plt.errorbar(z_obs, Hz_obs, yerr=Hz_err, fmt='o', label='Dados H(z)', color='k', capsize=3)
plt.plot(z, Hz_mix, label='HIDEM + BH + f(R)', color='C1', lw=2)
plt.plot(z, Hz_LCDM, '--', label='ΛCDM', color='gray')
plt.xlabel('Redshift z')
plt.ylabel('H(z) [km/s/Mpc]')
plt.title('Comparação de H(z) com dados reais')
plt.legend()
plt.grid(True)
plt.gca().invert_xaxis()
plt.tight_layout()
plt.show()

# --- 9) Plot: Resíduos (model - obs) / erro ---
def Hz_model_interp(z_points, Hz_array, z_array):
    return np.interp(z_points, z_array, Hz_array)

Hz_model_eval = Hz_model_interp(z_obs, Hz_mix, z)
resid = (Hz_obs - Hz_model_eval) / Hz_err

plt.figure(figsize=(8.5,4.5))
plt.axhline(0, color='gray', ls='--')
plt.errorbar(z_obs, resid, yerr=1, fmt='o', capsize=4, color='C3')
plt.xlabel('Redshift z')
plt.ylabel('Resíduo Normalizado')
plt.title(r'Resíduos: $(H_{\rm obs} - H_{\rm model}) / \sigma$')
plt.grid(True)
plt.gca().invert_xaxis()
plt.tight_layout()
plt.show()