# Importar el módulo gurobipy
from gurobipy import Model, GRB

# Crear un nuevo modelo
modelo = Model("Asignación de recursos")

# Definir las variables de decisión
# x: miles de litros de cerveza rubia a producir (>= 0)
# y: miles de litros de cerveza negra a producir (>= 0)
# z: miles de litros de cerveza baja a producir (>= 0)
x = modelo.addVar(name="Cerveza_Rubia", lb=0)
y = modelo.addVar(name="Cerveza_Negra", lb=0)
z = modelo.addVar(name="Cerveza_Baja", lb=0)

# Establecer la función objetivo: Maximizar Z = 7x + 4y + 3z
modelo.setObjective(7 * x + 4 * y + 3 * z, GRB.MAXIMIZE)

# Agregar las restricciones

# Restricción de presupuesto para materias primas: x + 2y + 2z ≤ 30
modelo.addConstr(x + 2 * y + 2 * z <= 30, name="Restricción_Malta")
modelo.addConstr(2 * x + y + 2 * z <= 45, name="Restricción_Levadura")

# Optimizar el modelo
modelo.optimize()

# Verificar si se encontró una solución óptima
if modelo.status == GRB.OPTIMAL:
    # Imprimir los resultados
    print(f"Litros de cerveza rubia a producir: {x.X:.2f} litros")
    print(f"Litros de cerveza negra a producir: {y.X:.2f} litros")
    print(f"Litros de cerveza baja a producir: {z.X:.2f} litros")
    print(f"Beneficio máximo: {modelo.ObjVal:.2f} euros")
else:
    print("No se encontró una solución óptima.")
