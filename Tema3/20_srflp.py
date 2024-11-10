# Importar la librería gurobipy
from gurobipy import Model, GRB, quicksum


# Función para leer los datos desde un archivo
def leer_datos_desde_archivo(nombre_archivo):
    # Abrir el archivo y leer las líneas
    with open(nombre_archivo, 'r') as f:
        lines = f.readlines()

    # Remover saltos de línea y espacios en blanco
    lines = [line.strip() for line in lines if line.strip() != '']

    # Línea 0: Número de instalaciones
    n = int(lines[0])

    # Línea 1: Anchos de las instalaciones
    l = list(map(float, lines[1].split()))

    # Verificar que el número de anchos coincide con n
    if len(l) != n:
        raise ValueError("El número de anchos proporcionados no coincide con el número de instalaciones.")

    # Matriz de costes: líneas desde la tercera hasta el final
    w = []
    for line in lines[2:]:
        row = list(map(float, line.split()))
        w.append(row)

    # Convertir la matriz de costes a una matriz completa
    # Asumiendo que la matriz proporcionada es triangular inferior
    W = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(len(w)):
        for j in range(len(w[i])):
            W[i][j] = w[i][j]
            W[j][i] = W[i][j]  # Matriz simétrica
    return n, l, W


def main():
    # Nombre del archivo con los datos
    nombre_archivo = 'S9.txt'
    # nombre_archivo = 'Am12a.txt'
    # nombre_archivo = 'Am15.txt'
    # nombre_archivo = 'H20.txt'

    # Leer los datos desde el archivo
    n, l, w = leer_datos_desde_archivo(nombre_archivo)
    I = range(n)

    # Número grande M
    M = sum(l) * 2  # Un valor suficientemente grande

    # Crear el modelo
    model = Model("SRFLP")
    model.Params.OutputFlag = 0

    # Variables de decisión
    x = model.addVars(n, lb=0, vtype=GRB.CONTINUOUS, name="x")
    y = model.addVars(n, n, vtype=GRB.BINARY, name="y")

    # Variables auxiliares para las distancias
    d = model.addVars(n, n, lb=0, vtype=GRB.CONTINUOUS, name="d")

    # Función objetivo
    model.setObjective(
        quicksum(
            w[i][j] * d[i, j]
            for i in I for j in I if i < j
        ),
        GRB.MINIMIZE
    )

    # Restricciones

    # 1. No superposición de instalaciones
    for i in I:
        for j in I:
            if i != j:
                # Si y_ij = 1, entonces x_i + l_i <= x_j
                model.addConstr(
                    x[i] + l[i] <= x[j] + M * (1 - y[i, j]),
                    name=f"NoOverlap_{i}_{j}"
                )
                # Si y_ij = 0, entonces x_j + l_j <= x_i
                model.addConstr(
                    x[j] + l[j] <= x[i] + M * y[i, j],
                    name=f"NoOverlap_{j}_{i}"
                )
                # Relación entre y_ij y y_ji
                model.addConstr(
                    y[i, j] + y[j, i] == 1,
                    name=f"Order_{i}_{j}"
                )

    # 2. Cálculo de distancias
    for i in I:
        for j in I:
            if i < j:
                # d_ij >= (x_j + l_j/2) - (x_i + l_i/2)
                model.addConstr(
                    d[i, j] >= (x[j] + l[j] / 2) - (x[i] + l[i] / 2),
                    name=f"Dist1_{i}_{j}"
                )
                # d_ij >= (x_i + l_i/2) - (x_j + l_j/2)
                model.addConstr(
                    d[i, j] >= (x[i] + l[i] / 2) - (x[j] + l[j] / 2),
                    name=f"Dist2_{i}_{j}"
                )

    # Optimizar el modelo
    model.optimize()

    # Imprimir la solución
    if model.status == GRB.OPTIMAL:
        print("\nPosiciones óptimas de las instalaciones:")
        for i in I:
            inicio = x[i].X
            fin = x[i].X + l[i]
            print(f"Instalación {i + 1}: Inicio en {inicio:.2f}, Fin en {fin:.2f}, Longitud: {l[i]}")
        print("\nOrden de las instalaciones:")
        sorted_facilities = sorted(I, key=lambda i: x[i].X)
        for idx, i in enumerate(sorted_facilities):
            print(f"Posición {idx + 1}: Instalación {i + 1}")
    else:
        print("No se encontró una solución óptima.")


if __name__ == "__main__":
    main()
