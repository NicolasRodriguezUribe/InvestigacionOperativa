# Importar la librería gurobipy
from gurobipy import Model, GRB

# Datos
K = [1, 2, 3, 4, 5]  # Conjunto de aceites
V = [1, 2]           # Aceites vegetales
NV = [3, 4, 5]       # Aceites no vegetales

# Costos variables por tonelada de cada aceite
c = {1: 110, 2: 120, 3: 130, 4: 110, 5: 115}

# Coeficientes de consumo
a = {1: 8.8, 2: 6.1, 3: 2, 4: 4.2, 5: 5}

# Costes fijos y capacidades de los depósitos
f_I = 750    # Coste del depósito tipo I
f_II = 450   # Coste del depósito tipo II

C_I = 200    # Capacidad del depósito tipo I
C_II = 100   # Capacidad del depósito tipo II

# Crear el modelo
model = Model("Modelo_Con_Nuevas_Variables_Delta")

# Desactivar la salida de Gurobi (opcional)
model.Params.OutputFlag = 1  # Cambia a 0 para desactivar la salida

# Variables de decisión
x = model.addVars(K, vtype=GRB.INTEGER, lb=0, name="x")
delta = model.addVars(K, vtype=GRB.BINARY, name="delta")
delta_I = model.addVars(K, vtype=GRB.BINARY, name="delta_I")
delta_II = model.addVars(K, vtype=GRB.BINARY, name="delta_II")
t = model.addVar(vtype=GRB.INTEGER, lb=0, name="t")

# Función objetivo
model.setObjective(
    150 * t - sum(c[i] * x[i] + f_I * delta_I[i] + f_II * delta_II[i] for i in K),
    GRB.MAXIMIZE
)

# Restricciones

# 1. Capacidad de aceites vegetales
model.addConstr(sum(x[i] for i in V) <= 200, name="Capacidad_Vegetal")

# 2. Capacidad de aceites no vegetales
model.addConstr(sum(x[i] for i in NV) <= 250, name="Capacidad_No_Vegetal")

# 3. Restricciones de consumo

# Dureza máxima
model.addConstr(sum(a[i] * x[i] for i in K) <= 6 * t, name="Consumo_Maximo")

# Dureza mínima
model.addConstr(sum(a[i] * x[i] for i in K) >= 3 * t, name="Consumo_Minimo")

# 4. Relación entre x_i y t
model.addConstr(sum(x[i] for i in K) == t, name="Produccion_Total")

# 5. Mínimo de producción si el aceite es utilizado
for i in K:
    model.addConstr(x[i] >= 20 * delta[i], name=f"Produccion_Min_{i}")

# 6. Capacidad de los depósitos
for i in K:
    model.addConstr(x[i] <= C_I * delta_I[i] + C_II * delta_II[i], name=f"Capacidad_Deposito_{i}")

# 7. Elección única de depósito por aceite
for i in K:
    model.addConstr(delta_I[i] + delta_II[i] == delta[i], name=f"Deposito_Unico_{i}")

# 8. Restricción en el número máximo de aceites utilizados
model.addConstr(sum(delta[i] for i in K) <= 3, name="Max_Aceites_Usados")

# 9. Restricciones lógicas
model.addConstr(delta[1] <= delta[5], name="Logica_delta1_delta5")
model.addConstr(delta[2] <= delta[5], name="Logica_delta2_delta5")

# Optimizar el modelo
model.optimize()

# Imprimir la solución
if model.status == GRB.OPTIMAL:
    print(f"\nValor óptimo de la función objetivo: {model.ObjVal}")
    print("Valores de las variables de decisión:")
    for i in K:
        print(f"Aceite {i}: x_{i} = {x[i].X}, delta_{i} = {int(delta[i].X)}, delta_I_{i} = {int(delta_I[i].X)}, delta_II_{i} = {int(delta_II[i].X)}")
    print(f"Producción total (t): {t.X}")
else:
    print("No se encontró una solución óptima.")
