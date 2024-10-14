# Importar la librería gurobipy
from gurobipy import Model, GRB

# Datos
K = [1, 2, 3, 4, 5]  # Conjunto de aceites
V = [1, 2]           # Aceites vegetales
NV = [3, 4, 5]       # Aceites no vegetales

# Costes asociados a cada aceite
c = {1: 110, 2: 120, 3: 130, 4: 110, 5: 115}

# Coeficientes de consumo
a = {1: 8.8, 2: 6.1, 3: 2, 4: 4.2, 5: 5}

# Límites superiores de producción
U = {1: 200, 2: 200, 3: 250, 4: 250, 5: 250}

# Crear el modelo
model = Model("Modelo_Simplificado")

# Desactivar la salida de Gurobi (opcional)
model.Params.OutputFlag = 1  # Cambia a 0 para desactivar la salida

# Variables de decisión
x = model.addVars(K, vtype=GRB.INTEGER, lb=0, name="x")
delta = model.addVars(K, vtype=GRB.BINARY, name="delta")
t = model.addVar(vtype=GRB.INTEGER, lb=0, name="t")

# Función objetivo
model.setObjective(150 * t - sum(c[k] * x[k] for k in K), GRB.MAXIMIZE)

# Restricciones

# 1. Capacidad de aceites vegetales
model.addConstr(sum(x[i] for i in V) <= 200, name="Capacidad_Vegetal")

# 2. Capacidad de aceites no vegetales
model.addConstr(sum(x[j] for j in NV) <= 250, name="Capacidad_No_Vegetal")

# 3. Restricciones de consumo

# Consumo máximo
model.addConstr(sum(a[k] * x[k] for k in K) <= 6 * t, name="Consumo_Maximo")

# Consumo mínimo
model.addConstr(sum(a[k] * x[k] for k in K) >= 3 * t, name="Consumo_Minimo")

# 4. Relación entre x_k y t
model.addConstr(sum(x[k] for k in K) == t, name="Produccion_Total")

# 5. Vinculación con variables binarias
for k in K:
    model.addConstr(x[k] >= 20 * delta[k], name=f"Vinculacion_Min_{k}")
    model.addConstr(x[k] <= U[k] * delta[k], name=f"Vinculacion_Max_{k}")

# 6. Restricción en el número máximo de aceites utilizados
model.addConstr(sum(delta[k] for k in K) <= 3, name="Max_Aceites_Usados")

# 7. Restricciones lógicas
model.addConstr(delta[1] <= delta[5], name="Logica_delta1_delta5")
model.addConstr(delta[2] <= delta[5], name="Logica_delta2_delta5")

# Optimizar el modelo
model.optimize()

# Imprimir la solución
if model.status == GRB.OPTIMAL:
    print(f"\nValor óptimo de la función objetivo: {model.ObjVal}")
    print("Valores de las variables de decisión:")
    for k in K:
        print(f"Aceite {k}: x_{k} = {x[k].X}, delta_{k} = {int(delta[k].X)}")
    print(f"Producción total (t): {t.X}")
else:
    print("No se encontró una solución óptima.")
