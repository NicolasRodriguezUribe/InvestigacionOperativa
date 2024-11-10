def mm1_model(lam, mu):
    rho = lam / mu
    if rho >= 1:
        return "El sistema es inestable (rho >= 1)."
    L = rho / (1 - rho)
    Lq = rho**2 / (1 - rho)
    W = 1 / (mu - lam)
    Wq = rho / (mu - lam)
    results = {
        'Utilización (rho)': rho,
        'Número promedio en el sistema (L)': L,
        'Número promedio en cola (Lq)': Lq,
        'Tiempo promedio en el sistema (W)': W,
        'Tiempo promedio en cola (Wq)': Wq
    }
    return results

# Modelo M/M/1
lam = 2  # tasa de llegada
mu = 3   # tasa de servicio
resultado_mm1 = mm1_model(lam, mu)
print("Resultados M/M/1:")
for clave, valor in resultado_mm1.items():
    print(f"{clave}: {valor:.4f}")