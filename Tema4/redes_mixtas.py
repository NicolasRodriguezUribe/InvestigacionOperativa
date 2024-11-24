# Datos del sistema

# Tasa de llegada de UE
lambda_UE = 4  # tareas/minuto

# Número de PI
N_PI = 5

# Recursos
resources = ['SP', 'DA', 'RC']

# Tiempos de servicio para UE (en minutos)
S_UE = {
    'SP': 0.1,
    'DA': 0.05,
    'RC': 0.02
}

# Tiempos de servicio para PI (en minutos)
S_PI = {
    'SP': 0.2,
    'DA': 0.15,
    'RC': 0  # PI no usan RC
}

# Tasas de visita para UE
V_UE = {
    'SP': 1,
    'DA': 0.7,
    'RC': 2
}

# Tasas de visita para PI
V_PI = {
    'SP': 1,
    'DA': 1,
    'RC': 0
}

# Número de servidores en cada recurso (asumimos 1)
m = {
    'SP': 1,
    'DA': 1,
    'RC': 1
}

# Inicialización de Q_i para PI y UE
Q_PI = {res: [0] * (N_PI + 1) for res in resources}
Q_UE = {res: 0 for res in resources}

# Inicialización de R_i para PI y UE
R_i_PI = {res: [0] * (N_PI + 1) for res in resources}
R_i_UE = {res: 0 for res in resources}

# Inicialización de R_PI(n) y X_PI(n)
R_PI = [0] * (N_PI + 1)
X_PI = [0] * (N_PI + 1)

# Número promedio de UE en el sistema
Q_UE_total = 0

# Iterativo MVA para PI
for n in range(1, N_PI + 1):
    # Calcular R_i(n) para PI
    for res in resources:
        # Evitar división por cero
        m_i = m[res]
        if S_PI[res] > 0:
            R_i_PI[res][n] = S_PI[res] * (1 + (Q_PI[res][n - 1] + Q_UE[res]) / m_i)
        else:
            R_i_PI[res][n] = 0
    # Calcular R_PI(n)
    R_PI[n] = sum(V_PI[res] * R_i_PI[res][n] for res in resources)
    # Calcular X_PI(n)
    X_PI[n] = n / R_PI[n]
    # Actualizar Q_i(n) para PI
    for res in resources:
        Q_PI[res][n] = X_PI[n] * V_PI[res] * R_i_PI[res][n]
    # Actualizar Q_i para el siguiente paso
    for res in resources:
        Q_PI[res][n] = Q_PI[res][n]

# Calcular R_i para UE considerando carga de PI
for res in resources:
    # Evitar división por cero
    m_i = m[res]
    if S_UE[res] > 0:
        Q_PI_last = Q_PI[res][N_PI]
        R_i_UE[res] = S_UE[res] * (1 + (Q_PI_last + Q_UE[res]) / m_i)
    else:
        R_i_UE[res] = 0

# Calcular tiempo de respuesta total para UE
R_UE = sum(V_UE[res] * R_i_UE[res] for res in resources)

# Throughput efectivo para UE
X_UE = lambda_UE

# Calcular Q_i para UE
for res in resources:
    Q_UE[res] = X_UE * V_UE[res] * R_i_UE[res]

# Calcular número promedio total de UE en el sistema
Q_UE_total = sum(Q_UE[res] for res in resources)

# Calcular utilizaciones
utilization = {}
for res in resources:
    total_service_rate = m[res] / S_UE[res] if S_UE[res] > 0 else 0
    arrival_rate = X_UE * V_UE[res] + X_PI[N_PI] * V_PI[res]
    utilization[res] = arrival_rate / total_service_rate if total_service_rate > 0 else 0

# Imprimir resultados
print("\nResultados del Análisis:")
print(f"Tiempo de respuesta promedio para UE: {R_UE:.4f} minutos")
print(f"Número promedio de UE en el sistema: {Q_UE_total:.4f}")
print("\nNúmero promedio de UE en cada recurso:")
for res in resources:
    print(f"{res}: {Q_UE[res]:.4f}")

print("\nNúmero promedio de PI en cada recurso:")
for res in resources:
    print(f"{res}: {Q_PI[res][N_PI]:.4f}")

print("\nUtilización de los recursos:")
for res in resources:
    print(f"{res}: {utilization[res]*100:.2f}%")
