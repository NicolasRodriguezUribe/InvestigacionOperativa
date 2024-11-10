def mm1k_model(lam, mu, K):

    rho = lam / mu

    # Verificar si rho es igual a 1
    if rho == 1:
        S = K + 1
    else:
        S = (1 - rho ** (K + 1)) / (1 - rho)

    # Calcular Pn
    pn_dict = {}
    for n in range(K + 1):
        Pn = (rho ** n) / S
        pn_dict[n] = Pn

    # Probabilidad de que el sistema esté lleno (PK)
    PK = pn_dict[K]

    # Tasa efectiva de llegada
    lam_e = lam * (1 - PK)

    # Número promedio de clientes en el sistema (L)
    L = sum(n * pn_dict[n] for n in range(K + 1))

    # Tiempo promedio en el sistema (W)
    W = L / lam_e if lam_e > 0 else 0

    # Tiempo promedio en cola (Wq)
    Wq = W - (1 / mu)

    # Número promedio de clientes en cola (Lq)
    Lq = L - (1 - pn_dict[0])

    results = {
        'Factor de utilización (rho)': rho,
        'Probabilidad de que el sistema esté lleno (PK)': PK,
        'Tasa efectiva de llegada (λe)': lam_e,
        'Número promedio de clientes en el sistema (L)': L,
        'Número promedio de clientes en cola (Lq)': Lq,
        'Tiempo promedio en el sistema (W)': W,
        'Tiempo promedio en cola (Wq)': Wq
    }
    return results, pn_dict

# Ejemplo para el Modelo M/M/1/K
lam = 4   # λ
mu = 2    # μ
K = 5     # Capacidad máxima

results_mm1k, pn_dict = mm1k_model(lam, mu, K)

print("\nResultados para el Modelo M/M/1/K:")
for key, value in results_mm1k.items():
    if 'Tiempo' in key:
        print(f"{key}: {value:.4f} horas ({value*60:.2f} minutos)")
    elif 'λe' in key:
        print(f"{key}: {value:.4f} clientes/hora")
    else:
        print(f"{key}: {value:.4f}")

print("\nProbabilidades Pn (n = 0 a {0}):".format(K))
for n, pn in pn_dict.items():
    print(f"P_{n}: {pn:.4f}")