# Importar módulos necesarios
import math

# Datos del sistema
# Tasa de llegada externa al departamento A
lambda_A = 5  # clientes/hora

# Probabilidades de enrutamiento desde A
P_AB = 0.5  # De A a B
P_AC = 0.3  # De A a C
P_A0 = 0.2  # De A a salida

# Tasa de servicio de cada departamento
mu_A = 6  # clientes/hora
mu_B = 5  # clientes/hora
mu_C = 4  # clientes/hora

# Cálculo de las tasas de llegada a cada departamento
lambda_B = lambda_A * P_AB
lambda_C = lambda_A * P_AC

# Cálculo de las utilizaciones
rho_A = lambda_A / mu_A
rho_B = lambda_B / mu_B
rho_C = lambda_C / mu_C

# Funciones para calcular medidas en M/M/1
def mm1_measures(lam, mu):
    rho = lam / mu
    L = rho / (1 - rho)
    Lq = rho**2 / (1 - rho)
    W = 1 / (mu - lam)
    Wq = rho / (mu - lam)
    return {
        'lambda': lam,
        'mu': mu,
        'rho': rho,
        'L': L,
        'Lq': Lq,
        'W': W,
        'Wq': Wq
    }

# Cálculo de medidas para cada departamento
measures_A = mm1_measures(lambda_A, mu_A)
measures_B = mm1_measures(lambda_B, mu_B)
measures_C = mm1_measures(lambda_C, mu_C)

# Función para imprimir resultados
def print_results(department, measures):
    print(f"\nResultados para el Departamento {department}:")
    print(f"Tasa de llegada (lambda): {measures['lambda']:.4f} clientes/hora")
    print(f"Tasa de servicio (mu): {measures['mu']:.4f} clientes/hora")
    print(f"Utilización (rho): {measures['rho']:.4f}")
    print(f"Número promedio en el sistema (L): {measures['L']:.4f} clientes")
    print(f"Número promedio en cola (Lq): {measures['Lq']:.4f} clientes")
    print(f"Tiempo promedio en el sistema (W): {measures['W']:.4f} horas ({measures['W']*60:.2f} minutos)")
    print(f"Tiempo promedio en cola (Wq): {measures['Wq']:.4f} horas ({measures['Wq']*60:.2f} minutos)")

# Imprimir resultados
print_results('A', measures_A)
print_results('B', measures_B)
print_results('C', measures_C)
