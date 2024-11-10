# Importar la librería gurobipy
from gurobipy import Model, GRB

# Datos del problema
mercancias = [1, 2, 3, 4, 5]
pesos = {1: 5, 2: 8, 3: 3, 4: 2, 5: 7}
volumenes = {1: 1, 2: 8, 3: 6, 4: 5, 5: 4}
valores = {1: 4, 2: 7, 3: 6, 4: 5, 5: 4}
peso_maximo = 112
volumen_maximo = 109

# Crear un nuevo modelo
modelo = Model("Carga_Camion")

# Desactivar la salida de Gurobi (opcional)
modelo.Params.OutputFlag = 0

# Definir las variables de decisión
# x[i] = número de unidades de la mercancía i a cargar
x = {}
for i in mercancias:
    x[i] = modelo.addVar(vtype=GRB.INTEGER, lb=0, name=f"x_{i}")

# Establecer la función objetivo: maximizar el valor total
modelo.setObjective(
    sum(valores[i] * x[i] for i in mercancias),
    GRB.MAXIMIZE
)

# Agregar la restricción de peso máximo
modelo.addConstr(
    sum(pesos[i] * x[i] for i in mercancias) <= peso_maximo,
    name="Restriccion_Peso"
)

# Agregar la restricción de volumen máximo
modelo.addConstr(
    sum(volumenes[i] * x[i] for i in mercancias) <= volumen_maximo,
    name="Restriccion_Volumen"
)

# Optimizar el modelo
modelo.optimize()

# Imprimir la solución
if modelo.status == GRB.OPTIMAL:
    total_valor = modelo.ObjVal
    total_peso = sum(pesos[i] * x[i].X for i in mercancias)
    total_volumen = sum(volumenes[i] * x[i].X for i in mercancias)
    print(f"Valor máximo total de la carga: {total_valor} euros")
    print(f"Peso total de la carga: {total_peso} kg")
    print(f"Volumen total de la carga: {total_volumen} m³")
    print("Unidades de mercancías a cargar:")
    for i in mercancias:
        cantidad = int(round(x[i].X))
        if cantidad > 0:
            print(f" - Mercancía {i}: {cantidad} unidades")
else:
    print("No se encontró una solución óptima.")
