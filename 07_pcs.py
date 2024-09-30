from gurobipy import Model, GRB

# Crear un nuevo modelo
model = Model("PCIngredients_Produccion")

# Definir las variables de decisión
xA = model.addVar(name="xA", lb=0)  # Unidades de Ordenador A
xB = model.addVar(name="xB", lb=0)  # Unidades de Ordenador B
xC = model.addVar(name="xC", lb=0)  # Unidades de Ordenador C

# Establecer la función objetivo
model.setObjective(
    350 * xA + 470 * xB + 610 * xC,
    GRB.MAXIMIZE
)

# Agregar las restricciones

# Restricción 1: Control de Calidad para A y B
model.addConstr(
    xA + xB <= 120,
    name="Control_Calidad_AB"
)

# Restricción 2: Control de Calidad para C
model.addConstr(
    xC <= 48,
    name="Control_Calidad_C"
)

# Restricción 3: Tiempo de Montaje Total
model.addConstr(
    10 * xA + 15 * xB + 20 * xC <= 2000,
    name="Tiempo_Montaje"
)

# Optimizar el modelo
model.optimize()

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
