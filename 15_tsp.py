from gurobipy import Model, GRB, quicksum

# Datos
n = 5  # Número de ciudades
ciudades = range(1, n + 1)

# Distancias entre ciudades (matriz c_{ij})
c = {
    (1, 2): 10, (1, 3): 8,  (1, 4): 9,  (1, 5): 7,
    (2, 1): 10, (2, 3): 10, (2, 4): 5,  (2, 5): 6,
    (3, 1): 8,  (3, 2): 10, (3, 4): 8,  (3, 5): 9,
    (4, 1): 9,  (4, 2): 5,  (4, 3): 8,  (4, 5): 6,
    (5, 1): 7,  (5, 2): 6,  (5, 3): 9,  (5, 4): 6
}

# Crear el modelo
modelo = Model("Problema_del_Viajero")

# Variables de decisión: x[i,j] = 1 si se viaja de ciudad i a ciudad j
x = modelo.addVars(ciudades, ciudades, vtype=GRB.BINARY, name="x")

# Variables auxiliares para eliminar subtours (MTZ)
u = modelo.addVars(ciudades, vtype=GRB.CONTINUOUS, lb=1, ub=n, name="u")

# Establecer la función objetivo
modelo.setObjective(
    quicksum(c[i, j] * x[i, j] for i in ciudades for j in ciudades if i != j),
    GRB.MINIMIZE
)

# Restricciones de flujo

# 1. Sale exactamente una vez de cada ciudad
for i in ciudades:
    modelo.addConstr(
        quicksum(x[i, j] for j in ciudades if j != i) == 1,
        name=f"Salida_{i}"
    )

# 2. Entra exactamente una vez a cada ciudad
for j in ciudades:
    modelo.addConstr(
        quicksum(x[i, j] for i in ciudades if i != j) == 1,
        name=f"Entrada_{j}"
    )

# Restricciones de eliminación de subtours (MTZ)
for i in ciudades:
    if i != 1:
        modelo.addConstr(u[i] >= 2, name=f"u_min_{i}")
        modelo.addConstr(u[i] <= n, name=f"u_max_{i}")

for i in ciudades:
    for j in ciudades:
        if i != j and i != 1 and j != 1:
            modelo.addConstr(
                u[i] - u[j] + n * x[i, j] <= n - 1,
                name=f"MTZ_{i}_{j}"
            )

# Optimizar el modelo
modelo.optimize()

# Imprimir la solución
if modelo.status == GRB.OPTIMAL:
    print(f"\nCosto mínimo del recorrido: {modelo.ObjVal}")
    ruta = []
    ciudad_actual = 1
    while True:
        ruta.append(ciudad_actual)
        for j in ciudades:
            if j != ciudad_actual and x[ciudad_actual, j].X > 0.5:
                siguiente_ciudad = j
                break
        if siguiente_ciudad == 1:
            ruta.append(1)
            break
        else:
            ciudad_actual = siguiente_ciudad
    print("Ruta óptima:")
    print(" -> ".join(map(str, ruta)))
else:
    print("No se encontró una solución óptima.")
