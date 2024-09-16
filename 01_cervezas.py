# Importar el módulo gurobipy
from gurobipy import Model, GRB

# Crear un nuevo modelo
modelo = Model("Produccion_Cerveza")

# Definir las variables de decisión
# x: Miles de litros de cerveza rubia a producir (>= 0)
# y: Miles de litros de cerveza negra a producir (>= 0)
x = modelo.addVar(name="Cerveza_Rubia", lb=0)
y = modelo.addVar(name="Cerveza_Negra", lb=0)

# Establecer la función objetivo: Maximizar Z = 100x + 125y
modelo.setObjective(100 * x + 125 * y, GRB.MAXIMIZE)

# Agregar las restricciones
# Restricción de empleados: 3x + 5y ≤ 15
modelo.addConstr(3 * x + 5 * y <= 15, name="Restriccion_Empleados")

# Restricción de presupuesto para materias primas: 90x + 85y ≤ 350
modelo.addConstr(90 * x + 85 * y <= 350, name="Restriccion_MateriasPrimas")

# Optimizar el modelo
modelo.optimize()

# Verificar si se encontró una solución óptima
if modelo.status == GRB.OPTIMAL:
    # Imprimir los resultados
    print(f"Litros de cerveza rubia a producir: {x.X :.2f} litros")
    print(f"Litros de cerveza negra a producir: {y.X :.2f} litros")
    print(f"Ingresos máximos: {modelo.ObjVal:.2f} euros")
else:
    print("No se encontró una solución óptima.")
