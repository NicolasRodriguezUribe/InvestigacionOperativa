# Importar el módulo gurobipy
from gurobipy import Model, GRB

# Crear un nuevo modelo
model = Model("Mezcla_Whiskies")

# Definir las variables de decisión (todas no negativas)
we = model.addVar(name="we", lb=0)     # Barriles de whisky escocés
wi1 = model.addVar(name="wi1", lb=0)   # Barriles de whisky irlandés tipo 1
wi2 = model.addVar(name="wi2", lb=0)   # Barriles de whisky irlandés tipo 2
B = model.addVar(name="B", lb=0)       # Producción total de whisky

# Establecer la función objetivo
model.setObjective(
    500 * B - 300 * we - 250 * wi1 - 270 * wi2,
    GRB.MAXIMIZE
)

# Agregar las restricciones

# Restricción 1: we <= 200
model.addConstr(we <= 200, name="Capacidad_Escoces")

# Restricción 2: wi1 + wi2 <= 250
model.addConstr(wi1 + wi2 <= 250, name="Capacidad_Irlandes")

# Restricción 3: Graduación alcohólica mínima
model.addConstr(
    48 * we + 38 * wi1 + 42 * wi2 >= 40 * B,
    name="Graduacion_Minima"
)

# Restricción 4: Graduación alcohólica máxima
model.addConstr(
    48 * we + 38 * wi1 + 42 * wi2 <= 46 * B,
    name="Graduacion_Maxima"
)

# Restricción 5: Producción total
model.addConstr(we + wi1 + wi2 == B, name="Produccion_Total")

# Optimizar el modelo
model.optimize()

# Verificar si se encontró una solución óptima
if model.status == GRB.OPTIMAL:
    print("\nSolución Óptima:")
    print(f"we (Whisky Escocés)          = {we.X:.2f} barriles")
    print(f"wi1 (Whisky Irlandés Tipo 1) = {wi1.X:.2f} barriles")
    print(f"wi2 (Whisky Irlandés Tipo 2) = {wi2.X:.2f} barriles")
    print(f"B (Producción Total)         = {B.X:.2f} barriles")
    print(f"Beneficio Máximo Z           = {model.ObjVal:.2f} euros")
else:
    print("No se encontró una solución óptima.")


print("\nValores sombra (dual) de las restricciones:")
for constr in model.getConstrs():
    print(f"{constr.ConstrName}: {constr.Pi:.4f}")

# Imprimir los costes reducidos de las variables
print("\nCostes reducidos de las variables:")
for var in model.getVars():
    print(f"{var.VarName}: {var.RC:.4f}")

# Imprimir las holguras de las restricciones
print("\nHolguras de las restricciones:")
for constr in model.getConstrs():
    print(f"{constr.ConstrName}: {constr.Slack:.4f}")

# Verificar si se encontró una solución óptima
if model.status == GRB.OPTIMAL:
    print("\nSolución óptima:")
    for var in model.getVars():
        print(f"{var.VarName} = {var.X:.2f} libras")
    print(f"Costo mínimo total = ${model.ObjVal:.2f}")
else:
    print("No se encontró una solución óptima.")