# Importar el módulo gurobipy
from gurobipy import Model, GRB

# Crear un nuevo modelo
model = Model("Optimization_Model")

# Definir las variables de decisión (todas no negativas)
v1 = model.addVar(name="v1", lb=0)
v2 = model.addVar(name="v2", lb=0)
nv1 = model.addVar(name="nv1", lb=0)
nv2 = model.addVar(name="nv2", lb=0)
nv3 = model.addVar(name="nv3", lb=0)
y = model.addVar(name="y", lb=0)

# Establecer la función objetivo
model.setObjective(
    150 * y - 110 * v1 - 120 * v2 - 130 * nv1 - 110 * nv2 - 115 * nv3,
    GRB.MAXIMIZE
)

# Agregar las restricciones

# Restricción 1: v1 + v2 <= 200
model.addConstr(v1 + v2 <= 200, name="Capacidad_Vegetal")

# Restricción 2: nv1 + nv2 + nv3 <= 250
model.addConstr(nv1 + nv2 + nv3 <= 250, name="Capacidad_NoVegetal")

# Restricción 3: 8.8*v1 + 6.1*v2 + 2*nv1 + 4.2*nv2 + 5*nv3 <= 6*y
model.addConstr(
    8.8 * v1 + 6.1 * v2 + 2 * nv1 + 4.2 * nv2 + 5 * nv3 <= 6 * y,
    name="Dureza_Superior"
)

# Restricción 4: 8.8*v1 + 6.1*v2 + 2*nv1 + 4.2*nv2 + 5*nv3 >= 3*y
model.addConstr(
    8.8 * v1 + 6.1 * v2 + 2 * nv1 + 4.2 * nv2 + 5 * nv3 >= 3 * y,
    name="Dureza_Inferior"
)

# Restricción 5: v1 + v2 + nv1 + nv2 + nv3 == y
model.addConstr(v1 + v2 + nv1 + nv2 + nv3 == y, name="Produccion_Total")

# Optimizar el modelo
model.optimize()

# Verificar si se encontró una solución óptima
if model.status == GRB.OPTIMAL:
    print("\nSolución Óptima:")
    print(f"v1 = {v1.X:.2f}")
    print(f"v2 = {v2.X:.2f}")
    print(f"nv1 = {nv1.X:.2f}")
    print(f"nv2 = {nv2.X:.2f}")
    print(f"nv3 = {nv3.X:.2f}")
    print(f"y  = {y.X:.2f}")
    print(f"Valor óptimo de la función objetivo Z = {model.ObjVal:.2f}")
else:
    print("No se encontró una solución óptima.")
