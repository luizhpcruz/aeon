import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ===== Parâmetros cosmológicos =====
H0 = 70.0
Omega_m = 0.3
Omega_r = 9e-5

# ===== Parâmetros da transição gravitacional coletiva =====
a_tr = 0.2              # valor de a em que a transição se inicia (z ~ 4)
gamma = 12.0            # define quão abrupta é a transição
C_grav = 1.0            # amplitude global do efeito coletivo

# ===== Termo QCD/EDE =====
C_QCD = 0.03
n_QCD = 4.0
b_QCD = 2.5

# ===== Termo SMBHs =====
C_SMBH = 290.0
m_SMBH = 14.61
a_c_SMBH = 6.02

# ===== Omega_DE total =====
def Omega_DE(a):
    qcd = C_QCD * a**(-n_QCD) * np.exp(-b_QCD / a)
    smbh = C_SMBH * a**(-m_SMBH) * np.exp(-a_c_SMBH / a)
    trigger = np.tanh(gamma * (a - a_tr))
    return C_grav * trigger * (qcd + smbh)

def H_model(a):
    return H0 * np.sqrt(Omega_m * a**-3 + Omega_r * a**-4 + Omega_DE(a))

# ===== Equação de crescimento linear =====
def dH_da(a, H_func, eps=1e-5):
    return (H_func(a+eps) - H_func(a-eps)) / (2*eps)

def growth_ode(a, y, H_func):
    H_val = H_func(a)
    dH = dH_da(a, H_func)
    dlnH_dln_a = a * dH / H_val
    dydt = [ y[1],
             - (3/a + dlnH_dln_a)*y[1] + (3/2)*Omega_m*H0**2 / (a**5 * H_val**2) * y[0] ]
    return dydt

def solve_growth(H_func, sigma8_0=0.8):
    a_min, a_max = 0.01, 1.0
    sol = solve_ivp(lambda a, y: growth_ode(a, y, H_func),
                    [a_min, a_max], [a_min, 1.0],
                    dense_output=True, rtol=1e-6, atol=1e-8)
    a_vals = np.linspace(a_min, a_max, 500)
    D, dD_da = sol.sol(a_vals)
    D_norm = D / D[-1]
    f = a_vals * dD_da / D
    f_sigma8 = sigma8_0 * D_norm * f
    return a_vals, f_sigma8

# ===== Executar simulação =====
a_vals, fs8 = solve_growth(H_model)
z_vals = 1/a_vals - 1
H_vals = H_model(a_vals)
Omega_de_vals = Omega_DE(a_vals)

# ===== Plot =====
plt.figure(figsize=(13,5))

plt.subplot(1,3,1)
plt.plot(z_vals, H_vals, 'navy')
plt.xlabel("Redshift z")
plt.ylabel("H(z) [km/s/Mpc]")
plt.title("Taxa de Expansão H(z)")
plt.grid(True)

plt.subplot(1,3,2)
plt.plot(z_vals, fs8, 'darkgreen')
plt.xlabel("Redshift z")
plt.ylabel(r"$f\sigma_8(z)$")
plt.title("Crescimento de Estruturas")
plt.grid(True)

plt.subplot(1,3,3)
plt.plot(z_vals, Omega_de_vals, 'crimson')
plt.xlabel("Redshift z")
plt.ylabel(r"$\Omega_{\rm DE}(z)$")
plt.title("Densidade de Energia Escura")
plt.grid(True)

plt.tight_layout()
plt.show()

# ===== Valores específicos =====
print("Comparação numérica:")
for z_check in [0, 0.5, 1.0, 2.0, 3.0]:
    a_check = 1 / (1 + z_check)
    fs8_val = np.interp(a_check, a_vals[::-1], fs8[::-1])
    omega_val = np.interp(a_check, a_vals[::-1], Omega_de_vals[::-1])
    print(f"z = {z_check:.1f}  |  fσ₈ ≈ {fs8_val:6.3f}   |  Ω_DE ≈ {omega_val:6.3f}")