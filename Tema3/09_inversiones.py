# Importar la librería gurobipy
from gurobipy import Model, GRB

# Datos del problema
inversiones = [1, 2, 3, 4]
beneficios = {
    1: 16000,
    2: 22000,
    3: 12000,
    4: 8000
}
capital_requerido = {
    1: 5000,
    2: 7000,
    3: 4000,
    4: 3000
}
capital_disponible = 14000

# Crear un nuevo modelo
modelo = Model("Seleccion_Inversiones")

# Desactivar la salida de Gurobi (opcional)
modelo.Params.OutputFlag = 0

# Definir las variables de decisión
# x[i] = 1 si se realiza la inversión i, 0 en caso contrario
x = {}
for i in inversiones:
    x[i] = modelo.addVar(vtype=GRB.BINARY, name=f"x_{i}")

# Actualizar el modelo para integrar las variables
modelo.update()

# Establecer la función objetivo: maximizar el beneficio total
modelo.setObjective(
    sum(beneficios[i] * x[i] for i in inversiones),
    GRB.MAXIMIZE
)

# Agregar la restricción de capital disponible
modelo.addConstr(
    sum(capital_requerido[i] * x[i] for i in inversiones) <= capital_disponible,
    name="Restriccion_Capital"
)

# Optimizar el modelo
modelo.optimize()

# Imprimir la solución
if modelo.status == GRB.OPTIMAL:
    total_beneficio = modelo.ObjVal
    total_capital = sum(capital_requerido[i] * x[i].X for i in inversiones)
    print(f"Beneficio máximo total: {total_beneficio} euros")
    print(f"Capital invertido total: {total_capital} euros")
    print("Inversiones seleccionadas:")
    for i in inversiones:
        if x[i].X > 0.5:
            print(f" - Inversión {i}: Beneficio = {beneficios[i]} euros, Capital = {capital_requerido[i]} euros")
else:
    print("No se encontró una solución óptima.")
