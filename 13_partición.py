from gurobipy import Model, GRB

# # Datos
# elementos = [1, 2, 3, 4, 5]
# subconjuntos = [1, 2, 3, 4, 5]
#
# # Coste de los subconjuntos
# costes = {1: 3, 2: 2, 3: 4, 4: 3, 5: 5}
#
# # Elementos cubiertos por cada subconjunto
# cobertura = {
#     1: [1, 2],
#     2: [2, 3],
#     3: [3, 4],
#     4: [4, 5],
#     5: [1, 5]
# }

# Datos
elementos = [1, 2, 3, 4, 5]
subconjuntos = [1, 2, 3, 4, 5, 6]

# Coste de los subconjuntos
costes = {1: 3, 2: 2, 3: 4, 4: 3, 5: 5, 6: 2}

# Elementos cubiertos por cada subconjunto
cobertura = {
    1: [1, 2],
    2: [2, 3],
    3: [3, 4],
    4: [4, 5],
    5: [1, 5],
    6: [5]  # Nuevo subconjunto que cubre solo el elemento 5
}

# Crear modelo
modelo_particion = Model("Problema_de_Particion")

# Variables de decisión
x = modelo_particion.addVars(subconjuntos, vtype=GRB.BINARY, name="x")

# Función objetivo
modelo_particion.setObjective(
    sum(costes[j] * x[j] for j in subconjuntos),
    GRB.MINIMIZE
)

# Restricciones de partición
for i in elementos:
    modelo_particion.addConstr(
        sum(x[j] for j in subconjuntos if i in cobertura[j]) == 1,
        name=f"Particion_{i}"
    )

# Optimizar modelo
modelo_particion.optimize()

# Imprimir solución
if modelo_particion.status == GRB.OPTIMAL:
    print(f"\nCoste mínimo total: {modelo_particion.ObjVal}")
    print("Subconjuntos seleccionados:")
    for j in subconjuntos:
        if x[j].X > 0.5:
            print(f" - Subconjunto {j}: Cubre elementos {cobertura[j]}")
else:
    print("No se encontró una solución óptima.")
