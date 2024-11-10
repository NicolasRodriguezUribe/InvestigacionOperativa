import math
def mminf_model(lam, mu, n_max=10):
    
    rho = lam / mu
    L = rho
    W = 1 / mu

    # Cálculo de Pn para n = 0 hasta n_max
    pn_dict = {}
    for n in range(n_max + 1):
        Pn = (rho ** n) * math.exp(-rho) / math.factorial(n)
        pn_dict[n] = Pn

    results = {
        'Factor de utilización (rho)': rho,
        'Número promedio de clientes en el sistema (L)': L,
        'Tiempo promedio en el sistema (W)': W,
        'Tiempo promedio en cola (Wq)': 0,
        'Número promedio de clientes en cola (Lq)': 0
    }
    return results, pn_dict

# Datos de entrada
lam = 1000  # λ
mu = 500    # μ
n_max = 5   # Calcularemos Pn para n = 0 a 5

# Llamar a la función mminf_model
results_mminf, pn_dict = mminf_model(lam, mu, n_max)

# Imprimir resultados
print("Resultados para el Modelo M/M/∞:")
for key, value in results_mminf.items():
    if 'Tiempo' in key:
        print(f"{key}: {value:.6f} segundos")
    else:
        print(f"{key}: {value:.6f}")

print("\nProbabilidades Pn (n = 0 a {0}):".format(n_max))
for n, pn in pn_dict.items():
    print(f"P_{n}: {pn:.6f}")
# Resultados para el Modelo M/M/∞:

