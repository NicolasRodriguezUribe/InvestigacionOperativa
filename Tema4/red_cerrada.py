# Datos del sistema

N = 5  # Número total de procesos

# Recursos
resources = ['CPU', 'I/O', 'Terminal']

# Tiempos de servicio (S_i) en segundos
S = {
    'CPU': 0.04,
    'I/O': 0.1,
    'Terminal': 12
}

# Tasas de visita (V_i)
V = {
    'CPU': 2,
    'I/O': 1,
    'Terminal': 1
}

# Inicialización de Q_i(0)
Q = {resource: [0] * (N + 1) for resource in resources}

# Inicialización de R_i(n)
R_i = {resource: [0] * (N + 1) for resource in resources}

# Inicialización de R(n) y X(n)
R = [0] * (N + 1)
X = [0] * (N + 1)

# Mean Value Analysis
for n in range(1, N + 1):
    # Calcular R_i(n)
    for res in resources:
        R_i[res][n] = S[res] * (1 + Q[res][n - 1])
    # Calcular R(n)
    R_n = sum(V[res] * R_i[res][n] for res in resources)
    R[n] = R_n
    # Calcular X(n)
    X[n] = n / R[n]
    # Calcular Q_i(n)
    for res in resources:
        Q[res][n] = X[n] * V[res] * R_i[res][n]

# Imprimir resultados
print(f"\nResultados para N = {N} procesos:")
print(f"Tiempo de respuesta del sistema (R): {R[N]:.4f} segundos")
print(f"Throughput del sistema (X): {X[N]:.4f} procesos/segundo")
print("\nNúmero promedio de procesos en cada recurso:")
for res in resources:
    print(f"{res}: {Q[res][N]:.4f} procesos")
