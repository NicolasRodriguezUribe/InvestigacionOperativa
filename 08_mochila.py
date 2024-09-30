# Importar la librería gurobipy
from gurobipy import Model, GRB

# Datos del problema
objetos = [1, 2, 3]
valores = {1: 60, 2: 100, 3: 120}
pesos = {1: 10, 2: 20, 3: 30}
capacidad = 50

# Crear un nuevo modelo
modelo = Model("Mochila_0-1")

# Definir las variables de decisión
# x[i] = 1 si el objeto i es incluido en la mochila, 0 en caso contrario
x = {}
for i in objetos:
    x[i] = modelo.addVar(vtype=GRB.BINARY, name=f"x_{i}")

# Establecer la función objetivo: maximizar el valor total
modelo.setObjective(
    sum(valores[i] * x[i] for i in objetos),
    GRB.MAXIMIZE
)

# Agregar la restricción de capacidad
modelo.addConstr(
    sum(pesos[i] * x[i] for i in objetos) <= capacidad,
    name="Restriccion_Capacidad"
)

# Optimizar el modelo
modelo.optimize()

# Imprimir la solución
if modelo.status == GRB.OPTIMAL:
    print(f"\nValor óptimo total: ${modelo.ObjVal}")
    print("Objetos seleccionados:")
    for i in objetos:
        if x[i].X > 0.5:
            print(f" - Objeto {i}: Valor = ${valores[i]}, Peso = {pesos[i]} kg")
else:
    print("No se encontró una solución óptima.")
