from fastapi import APIRouter
from aeon_kernel.kernel import AEONKernel

router = APIRouter()
kernel = AEONKernel()

@router.post("/evolve")
async def evolve_kernel(I: float, omega_info: float, omega_caos: float, S: float, Phi: float):
    result = kernel.evolve(I, omega_info, omega_caos, S, Phi)
    return {"evolved_value": result, "symbol_strength": kernel.symbol_net.network_strength()}
