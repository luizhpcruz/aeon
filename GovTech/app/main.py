from fastapi import FastAPI
from aeon_kernel.kernel import AEONKernel

app = FastAPI(title="AEON‑GPT Orchestrator")

@app.post("/kernel/evolve")
def evolve_kernel(I: float, Omega_info: float, Omega_caos: float, S: float, Phi: float):
    kernel = AEONKernel(alpha=1.0, beta=1.0, gamma=1.0, delta=1.0)
    result = kernel.evolve(I, Omega_info, Omega_caos, S, Phi)
    return {"result": result}
