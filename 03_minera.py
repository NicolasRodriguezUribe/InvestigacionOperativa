# Importar el módulo gurobipy
from gurobipy import Model, GRB

# Crear un nuevo modelo
modelo = Model("Explotación minera")

# Definir las variables de decisión
# x: Toneladas de Lignito (>= 0)
# y: Toneladas de Antracita (>= 0)
x = modelo.addVar(name="PET_envase", lb=0)
y = modelo.addVar(name="PET_fibra", lb=0)

# Establecer la función objetivo: Maximizar Z = 24x + 18y
modelo.setObjective(24 * x + 18 * y, GRB.MAXIMIZE)

# Agregar las restricciones
# Restricción del corte: 3x + 4y ≤ 12
modelo.addConstr(3 * x + 4 * y <= 12, name="Restricción_Corte")

# Restricción del tamizado 3x + 3y ≤ 10
modelo.addConstr(3 * x + 3 * y <= 10, name="Restricción_Tamizado")

#Restricción del lavado 4x + 2y ≤ 8
modelo.addConstr(4 * x + 2 * y <= 8, name="Restricción_Lavado")

# Optimizar el modelo
modelo.optimize()

# Verificar si se encontró una solución óptima
if modelo.status == GRB.OPTIMAL:
    # Imprimir los resultados
    print(f"Toneladas de Lignito a producir: {x.X:.2f} toneladas")
    print(f"Toneladas de Antracita a producir: {y.X:.2f} toneladas")
    print(f"Beneficio máximo: {modelo.ObjVal:.2f} euros")
else:
    print("No se encontró una solución óptima.")
