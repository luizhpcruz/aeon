import numpy as np
import pandas as pd
import emcee

def load_pantheon(path):
    df = pd.read_csv(path, delim_whitespace=True, comment='#')
    return df.z, df.distance_modulus, np.loadtxt(path.replace(".txt","_cov.txt"))

def lnlike(theta, z, mu, cov_inv):
    H0, Omega_m = theta
    mu_model = 5*np.log10(299792.458 * z / H0 * (1 + 0.5*(1-Omega_m)*z))
    diff = mu - mu_model
    return -0.5 * diff.dot(cov_inv.dot(diff))

def run_mcmc(z, mu, cov, nwalkers=50, steps=2000):
    ndim = 2
    cov_inv = np.linalg.inv(cov)
    initial = np.array([70, 0.3]) + 0.1 * np.random.randn(nwalkers, ndim)
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnlike, args=(z, mu, cov_inv))
    sampler.run_mcmc(initial, steps, progress=True)
    return sampler.get_chain(discard=500, flat=True)
