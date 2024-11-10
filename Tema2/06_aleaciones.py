# Importar el módulo gurobipy
from gurobipy import Model, GRB

# Crear un nuevo modelo
model = Model("Mezcla_Hierros")

# Definir las variables de decisión (cantidades en libras de cada tipo de hierro)
x1 = model.addVar(name="x1", lb=0)  # Hierro Tipo 1
x2 = model.addVar(name="x2", lb=0)  # Hierro Tipo 2
x3 = model.addVar(name="x3", lb=0)  # Hierro Tipo 3
x4 = model.addVar(name="x4", lb=0)  # Hierro Tipo 4

# Actualizar el modelo para integrar las nuevas variables
model.update()

# Establecer la función objetivo (minimizar el costo total)
model.setObjective(
    0.05 * x1 +   # Costo por libra de Hierro Tipo 1
    0.04 * x2 +   # Costo por libra de Hierro Tipo 2
    0.25 * x3 +   # Costo por libra de Hierro Tipo 3
    0.35 * x4,    # Costo por libra de Hierro Tipo 4
    GRB.MINIMIZE
)

# Agregar las restricciones

# Restricción 1: Producción total de 1000 libras
model.addConstr(
    x1 + x2 + x3 + x4 == 1000,
    name="Produccion_Total"
)

# Restricciones de Carbono
# Restricción 2: Contenido mínimo de Carbono (2% de 1000 libras = 20 libras)
model.addConstr(
    0.02 * x1 + 0.05 * x2 >= 12,
    name="Carbono_Minimo"
)

# Restricción 3: Contenido máximo de Carbono (4% de 1000 libras = 40 libras)
model.addConstr(
    0.02 * x1 + 0.05 * x2 <= 40,
    name="Carbono_Maximo"
)

# Restricciones de Silicio
# Restricción 4: Contenido mínimo de Silicio (2% de 1000 libras = 20 libras)
model.addConstr(
    0.01 * x1 + 0.60 * x3 + 0.20 * x4 >= 20,
    name="Silicio_Minimo"
)

# Restricción 5: Contenido máximo de Silicio (5% de 1000 libras = 50 libras)
model.addConstr(
    0.01 * x1 + 0.60 * x3 + 0.20 * x4 <= 50,
    name="Silicio_Maximo"
)

# Restricción 6: Contenido máximo de Manganeso (1% de 1000 libras = 10 libras)
model.addConstr(
    0.01 * x2 + 0.40 * x3 + 0.80 * x4 <= 10,
    name="Manganeso_Maximo"
)

# Optimizar el modelo
model.optimize()

# # Imprimir los resultados
# if model.status == GRB.OPTIMAL:
#     print("\nSolución Óptima:")
#     print(f"x1 (Hierro Tipo 1) = {x1.X:.2f} libras")
#     print(f"x2 (Hierro Tipo 2) = {x2.X:.2f} libras")
#     print(f"x3 (Hierro Tipo 3) = {x3.X:.2f} libras")
#     print(f"x4 (Hierro Tipo 4) = {x4.X:.2f} libras")
#     print(f"Costo Mínimo Total = ${model.ObjVal:.2f}")
# else:
#     print("No se encontró una solución óptima.")

# Imprimir los valores sombra de las restricciones
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