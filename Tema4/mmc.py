import math

def mmc_model(lam, mu, c):
    rho = lam / (c * mu)
    if rho >= 1:
        return "El sistema es inestable (rho >= 1)."
    # Calcular P0
    sumatoria = sum((lam / mu)**n / math.factorial(n) for n in range(c))
    pnumerator = (lam / mu)**c / (math.factorial(c) * (1 - rho))
    P0 = 1 / (sumatoria + pnumerator)
    # Calcular Lq
    Lq = (P0 * (lam / mu)**c * rho) / (math.factorial(c) * (1 - rho)**2)
    L = Lq + (lam / mu)
    Wq = Lq / lam
    W = Wq + (1 / mu)
    results = {
        'Utilización (rho)': rho,
        'Probabilidad de cero clientes (P0)': P0,
        'Número promedio en el sistema (L)': L,
        'Número promedio en cola (Lq)': Lq,
        'Tiempo promedio en el sistema (W)': W,
        'Tiempo promedio en cola (Wq)': Wq
    }
    return results

# Modelo M/M/c
lam = 6
mu = 3
c = 3
resultado_mmc = mmc_model(lam, mu, c)
print("\nResultados M/M/c:")
for clave, valor in resultado_mmc.items():
    print(f"{clave}: {valor:.4f}")