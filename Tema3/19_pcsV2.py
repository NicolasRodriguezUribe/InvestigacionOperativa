# Importar la librería gurobipy
from gurobipy import Model, GRB

# Crear el modelo
model = Model("PCIngredients_Actualizado")

# Desactivar la salida de Gurobi (opcional)
model.Params.OutputFlag = 0

# Conjuntos
productos = ['a', 'b', 'c']

# Parámetros
beneficio = {'a': 350, 'b': 470, 'c': 610}
coste_fijo = {'a': 1000, 'b': 1000, 'c': 1000}
coste_ext = {'a': 800, 'b': 800, 'c': 800}
horas_montaje = {'a': 10, 'b': 15, 'c': 20}
horas_calidad = {'a': 1, 'b': 1, 'c': 1}
capacidad_int = {'a': 80, 'b': 80, 'c': 80}
produccion_min = {'a': 10, 'b': 10, 'c': 10}

# Horas disponibles
H_montaje = 2000
H_calidad_ab = 120
H_calidad_c = 48

# Número grande M
M = 10000

# Variables de decisión
x = model.addVars(productos, vtype=GRB.INTEGER, lb=0, name="x")
x_int = model.addVars(productos, vtype=GRB.INTEGER, lb=0, name="x_int")
x_ext = model.addVars(productos, vtype=GRB.INTEGER, lb=0, name="x_ext")
y = model.addVars(productos, vtype=GRB.BINARY, name="y")
y_ext = model.addVars(productos, vtype=GRB.BINARY, name="y_ext")

# Actualizar el modelo para integrar las variables
model.update()

# Función objetivo
model.setObjective(
    sum(beneficio[i] * x[i] - coste_fijo[i] * y[i] - coste_ext[i] * y_ext[i] for i in productos),
    GRB.MAXIMIZE
)

# Restricciones

# 1. Relación entre producción total y producción en instalaciones
for i in productos:
    model.addConstr(x[i] == x_int[i] + x_ext[i], name=f"Produccion_total_{i}")

# 2. Producción mínima
for i in productos:
    model.addConstr(x[i] >= produccion_min[i] * y[i], name=f"Produccion_minima_{i}")
    model.addConstr(x[i] <= M * y[i], name=f"Produccion_maxima_{i}")

# 3. Capacidad de instalaciones internas
for i in productos:
    model.addConstr(x_int[i] <= capacidad_int[i] * y[i], name=f"Capacidad_interna_{i}")

# 4. Uso de instalaciones externas
for i in productos:
    model.addConstr(x_ext[i] >= x[i] - capacidad_int[i] * y[i], name=f"Produccion_externa_min_{i}")
    model.addConstr(x_ext[i] <= M * y_ext[i], name=f"Produccion_externa_max_{i}")

# 5. Si no se produce el tipo de ordenador, no hay producción interna ni externa
for i in productos:
    model.addConstr(x_int[i] <= M * y[i], name=f"Produccion_interna_si_se_produce_{i}")
    model.addConstr(x_ext[i] <= M * y[i], name=f"Produccion_externa_si_se_produce_{i}")

# 6. Horas de control de calidad
model.addConstr(sum(horas_calidad[i] * x[i] for i in ['a', 'b']) <= H_calidad_ab, name="Control_Calidad_AB")
model.addConstr(horas_calidad['c'] * x['c'] <= H_calidad_c, name="Control_Calidad_C")

# 7. Horas de montaje
model.addConstr(sum(horas_montaje[i] * x[i] for i in productos) <= H_montaje, name="Horas_Montaje")

# Optimizar el modelo
model.optimize()

# Imprimir la solución
if model.status == GRB.OPTIMAL:
    print(f"\nBeneficio máximo total: {model.ObjVal} euros")
    print("Plan de producción óptimo:")
    for i in productos:
        print(f" - Ordenadores {i}: {x[i].X} unidades")
        print(f"   - Producción interna ({i}_int): {x_int[i].X} unidades")
        print(f"   - Producción externa ({i}_ext): {x_ext[i].X} unidades")
        print(f"   - Se produce ({i}): {int(y[i].X)}")
        print(f"   - Se usan instalaciones externas ({i}_ext): {int(y_ext[i].X)}")
else:
    print("No se encontró una solución óptima.")
