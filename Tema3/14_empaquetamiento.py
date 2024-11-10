# Importar la librería gurobipy
from gurobipy import Model, GRB

elementos = ['A', 'B', 'C', 'D', 'E']

# Conjunto de subconjuntos y sus elementos
subconjuntos = {
    1: {'elementos': ['A', 'B'], 'beneficio': 5},
    2: {'elementos': ['C', 'D'], 'beneficio': 7},
    3: {'elementos': ['B', 'D'], 'beneficio': 4},
    4: {'elementos': ['E'], 'beneficio': 3},
    5: {'elementos': ['A', 'E'], 'beneficio': 6},
}

# Crear el modelo
modelo = Model("Problema_de_Conjunto_de_Empaquetamiento")

# Desactivar la salida de Gurobi (opcional)
modelo.Params.OutputFlag = 0

# Variables de decisión: x_j = 1 si el subconjunto j es seleccionado
x = modelo.addVars(subconjuntos.keys(), vtype=GRB.BINARY, name="x")

# Función objetivo: maximizar el beneficio total
modelo.setObjective(
    sum(subconjuntos[j]['beneficio'] * x[j] for j in subconjuntos),
    GRB.MAXIMIZE
)

# Restricciones: cada elemento puede pertenecer a como máximo un subconjunto seleccionado
for e in elementos:
    modelo.addConstr(
        sum(x[j] for j in subconjuntos if e in subconjuntos[j]['elementos']) <= 1,
        name=f"Elemento_{e}"
    )

# Optimizar el modelo
modelo.optimize()

# Verificar si se encontró una solución óptima
if modelo.status == GRB.OPTIMAL:
    print(f"\nBeneficio máximo total: {modelo.ObjVal}")
    print("Subconjuntos seleccionados:")
    for j in subconjuntos:
        if x[j].X > 0.5:
            elems = subconjuntos[j]['elementos']
            ben = subconjuntos[j]['beneficio']
            print(f" - Subconjunto {j}: Elementos {elems}, Beneficio {ben}")
else:
    print("No se encontró una solución óptima.")
