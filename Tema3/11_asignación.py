# Importar la librería gurobipy
from gurobipy import Model, GRB

# Definir los datos
abogados = ['Ana', 'Bruno', 'Carmen', 'Domingo']
casos = {
    1: 'Divorcio',
    2: 'Fusión Empresarial',
    3: 'Desfalco',
    4: 'Herencias'
}

# Tasa de efectividad e_{ij}
efectividad = {
    ('Ana', 1): 6,
    ('Ana', 2): 2,
    ('Ana', 3): 8,
    ('Ana', 4): 5,
    ('Bruno', 1): 9,
    ('Bruno', 2): 3,
    ('Bruno', 3): 5,
    ('Bruno', 4): 8,
    ('Carmen', 1): 4,
    ('Carmen', 2): 8,
    ('Carmen', 3): 3,
    ('Carmen', 4): 4,
    ('Domingo', 1): 6,
    ('Domingo', 2): 7,
    ('Domingo', 3): 6,
    ('Domingo', 4): 4
}

# Crear un nuevo modelo
modelo = Model("Asignacion_Abogados_Casos")

# Desactivar la salida de Gurobi (opcional)
modelo.Params.OutputFlag = 0

# Definir las variables de decisión
x = {}
for i in abogados:
    for j in casos:
        x[i, j] = modelo.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

# Actualizar el modelo para integrar las variables
modelo.update()

# Establecer la función objetivo: maximizar la efectividad total
modelo.setObjective(
    sum(efectividad[i, j] * x[i, j] for i in abogados for j in casos),
    GRB.MAXIMIZE
)

# Agregar las restricciones

# 1. Cada abogado debe ser asignado a exactamente un caso
for i in abogados:
    modelo.addConstr(
        sum(x[i, j] for j in casos) == 1,
        name=f"Asignacion_Unica_Abogado_{i}"
    )

# 2. Cada caso debe ser asignado a exactamente un abogado
for j in casos:
    modelo.addConstr(
        sum(x[i, j] for i in abogados) == 1,
        name=f"Asignacion_Unica_Caso_{j}"
    )

# Optimizar el modelo
modelo.optimize()

# Imprimir la solución
if modelo.status == GRB.OPTIMAL:
    total_efectividad = modelo.ObjVal
    print(f"Efectividad total máxima: {total_efectividad}")
    print("Asignaciones óptimas:")
    for i in abogados:
        for j in casos:
            if x[i, j].X > 0.5:
                print(f" - {i} asignado al caso '{casos[j]}' con efectividad {efectividad[i, j]}")
else:
    print("No se encontró una solución óptima.")
