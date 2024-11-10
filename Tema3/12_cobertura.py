from gurobipy import Model, GRB

# Datos
elementos = [1, 2, 3, 4, 5]
subconjuntos = [1, 2, 3, 4, 5]

# Coste de los subconjuntos
costes = {1: 3, 2: 2, 3: 4, 4: 3, 5: 5}

# Elementos cubiertos por cada subconjunto
cobertura = {
    1: [1, 2],
    2: [2, 3],
    3: [3, 4],
    4: [4, 5],
    5: [1, 5]
}

# Crear modelo
modelo = Model("Problema_de_Cubrimiento")

# Variables de decisión
x = modelo.addVars(subconjuntos, vtype=GRB.BINARY, name="x")

# Función objetivo
modelo.setObjective(
    sum(costes[j] * x[j] for j in subconjuntos),
    GRB.MINIMIZE
)

# Restricciones de cobertura
for i in elementos:
    modelo.addConstr(
        sum(x[j] for j in subconjuntos if i in cobertura[j]) >= 1,
        name=f"Cobertura_{i}"
    )

# Optimizar modelo
modelo.optimize()

# Imprimir solución
if modelo.status == GRB.OPTIMAL:
    print(f"\nCoste mínimo total: {modelo.ObjVal}")
    print("Subconjuntos seleccionados:")
    for j in subconjuntos:
        if x[j].X > 0.5:
            print(f" - Subconjunto {j}: Cubre elementos {cobertura[j]}")
else:
    print("No se encontró una solución óptima.")
