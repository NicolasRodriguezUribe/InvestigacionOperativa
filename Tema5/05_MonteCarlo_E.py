import numpy as np
import matplotlib.pyplot as plt


def monte_carlo_expected_distance(num_samples):
    # Generar coordenadas para el primer punto
    X1 = np.random.uniform(0, 1, num_samples)
    Y1 = np.random.uniform(0, 1, num_samples)

    # Generar coordenadas para el segundo punto
    X2 = np.random.uniform(0, 1, num_samples)
    Y2 = np.random.uniform(0, 1, num_samples)

    # Calcular la distancia Euclidiana entre los pares de puntos
    distances = np.sqrt((X2 - X1) ** 2 + (Y2 - Y1) ** 2)

    # Estimar la distancia esperada
    expected_distance = np.mean(distances)

    return expected_distance, distances


# Parámetros
num_samples = 1000000  # Número de simulaciones

# Ejecutar la simulación
expected_distance, distances = monte_carlo_expected_distance(num_samples)

print(f"Distancia esperada estimada entre dos puntos aleatorios en el cuadrado unitario: {expected_distance:.4f}")

# Visualizar la distribución de las distancias
plt.figure(figsize=(10, 6))
plt.hist(distances, bins=100, density=True, edgecolor='black', alpha=0.7)
plt.title('Distribución de las distancias entre dos puntos aleatorios en un cuadrado unitario')
plt.xlabel('Distancia Euclidiana')
plt.ylabel('Densidad de Probabilidad')
plt.grid(True)
plt.show()
