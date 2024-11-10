# Importar el módulo gurobipy
from gurobipy import Model, GRB

# Crear un nuevo modelo
modelo = Model("Producción_PET")

# Definir las variables de decisión
# x: Toneladas de PET-envase a producir (>= 0)
# y: Toneladas de PET-fibra a producir (>= 0)
x = modelo.addVar(name="PET_envase", lb=0)
y = modelo.addVar(name="PET_fibra", lb=0)

# Establecer la función objetivo: Maximizar Z = 32x + 38y
modelo.setObjective(32 * x + 38 * y, GRB.MAXIMIZE)

# Agregar las restricciones
# Restricción de PTA: 0.950x + 0.920y ≤ 280
modelo.addConstr(0.950 * x + 0.920 * y <= 280, name="Restricción_PTA")

# Restricción de MEG: 0.370x + 0.340y ≤ 170
modelo.addConstr(0.370 * x + 0.340 * y <= 170, name="Restricción_MEG")

# Optimizar el modelo
modelo.optimize()

# Verificar si se encontró una solución óptima
if modelo.status == GRB.OPTIMAL:
    # Imprimir los resultados
    print(f"Toneladas de PET-envase a producir: {x.X:.2f} toneladas")
    print(f"Toneladas de PET-fibra a producir: {y.X:.2f} toneladas")
    print(f"Beneficio máximo: {modelo.ObjVal:.2f} euros")
else:
    print("No se encontró una solución óptima.")
