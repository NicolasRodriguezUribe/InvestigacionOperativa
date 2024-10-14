# Importar la librería gurobipy
from gurobipy import Model, GRB

# Crear un nuevo modelo
model = Model("Problema_de_Optimización")

# Desactivar la salida de Gurobi (opcional)
model.Params.OutputFlag = 1  # Puedes cambiar a 0 para desactivar la salida

# Variables enteras
v1 = model.addVar(vtype=GRB.INTEGER, name="v1")
v2 = model.addVar(vtype=GRB.INTEGER, name="v2")
nv1 = model.addVar(vtype=GRB.INTEGER, name="nv1")
nv2 = model.addVar(vtype=GRB.INTEGER, name="nv2")
nv3 = model.addVar(vtype=GRB.INTEGER, name="nv3")
t = model.addVar(vtype=GRB.INTEGER, name="t")

# Variables binarias
delta1 = model.addVar(vtype=GRB.BINARY, name="delta1")
delta2 = model.addVar(vtype=GRB.BINARY, name="delta2")
delta3 = model.addVar(vtype=GRB.BINARY, name="delta3")
delta4 = model.addVar(vtype=GRB.BINARY, name="delta4")
delta5 = model.addVar(vtype=GRB.BINARY, name="delta5")

# Actualizar el modelo para integrar las variables
model.update()

# Establecer la función objetivo
model.setObjective(
    150 * t - 110 * v1 - 120 * v2 - 130 * nv1 - 110 * nv2 - 115 * nv3,
    GRB.MAXIMIZE
)

# Agregar las restricciones

# Restricción 1
model.addConstr(v1 + v2 <= 200, name="R_Vegetal")

# Restricción 2
model.addConstr(nv1 + nv2 + nv3 <= 250, name="R_NoVegetal")

# Restricción 3
model.addConstr(
    8.8 * v1 + 6.1 * v2 + 2 * nv1 + 4.2 * nv2 + 5 * nv3 <= 6 * t,
    name="Dureza_Max"
)

# Restricción 4
model.addConstr(
    8.8 * v1 + 6.1 * v2 + 2 * nv1 + 4.2 * nv2 + 5 * nv3 >= 3 * t,
    name="Dureza_Min"
)

# Restricción 5
model.addConstr(
    v1 + v2 + nv1 + nv2 + nv3 == t,
    name="Total_Aceite"
)

# Restricciones 6 a 10 (Vinculación con variables binarias)
model.addConstr(v1 >= 20 * delta1, name="V1_inferior")
model.addConstr(v1 <= 200 * delta1, name="V1_superior")

model.addConstr(v2 >= 20 * delta2, name="V2_inferior")
model.addConstr(v2 <= 200 * delta2, name="V2_superior")

model.addConstr(nv1 >= 20 * delta3, name="NV1_inferior")
model.addConstr(nv1 <= 250 * delta3, name="NV1_superior")

model.addConstr(nv2 >= 20 * delta4, name="NV2_inferior")
model.addConstr(nv2 <= 250 * delta4, name="NV2_superior")

model.addConstr(nv3 >= 20 * delta5, name="NV3_inferior")
model.addConstr(nv3 <= 250 * delta5, name="NV3_superior")

# Restricción 11
model.addConstr(
    delta1 + delta2 + delta3 + delta4 + delta5 <= 3,
    name="Total_Aceite_Max"
)

# Restricciones 12 y 13
model.addConstr(delta1 <= delta5, name="Si_vegetal1_no_vegetal")
model.addConstr(delta2 <= delta5, name="Si_vegetal2_no_vegetal")

# Optimizar el modelo
model.optimize()

# Imprimir la solución
if model.status == GRB.OPTIMAL:
    print(f"\nValor óptimo de la función objetivo: {model.ObjVal}")
    print("Valores de las variables de decisión:")
    print(f"v1 = {v1.X}")
    print(f"v2 = {v2.X}")
    print(f"nv1 = {nv1.X}")
    print(f"nv2 = {nv2.X}")
    print(f"nv3 = {nv3.X}")
    print(f"t = {t.X}")
    print(f"delta1 = {delta1.X}")
    print(f"delta2 = {delta2.X}")
    print(f"delta3 = {delta3.X}")
    print(f"delta4 = {delta4.X}")
    print(f"delta5 = {delta5.X}")
else:
    print("No se encontró una solución óptima.")
