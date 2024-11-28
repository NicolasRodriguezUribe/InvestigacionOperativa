import numpy as np
import matplotlib.pyplot as plt


def monte_carlo_sphere_volume(num_samples, r=1):
    # Generar puntos aleatorios en el cubo [-r, r]^3
    x = np.random.uniform(-r, r, num_samples)
    y = np.random.uniform(-r, r, num_samples)
    z = np.random.uniform(-r, r, num_samples)
    # Calcular la distancia al origen
    distances = np.sqrt(x**2 + y**2 + z**2)
    # Contar puntos dentro de la esfera
    inside_sphere = np.sum(distances <= r)
    # Calcular el volumen del cubo
    volume_cube = (2 * r) ** 3
    # Estimar el volumen de la esfera
    volume_sphere_estimate = (inside_sphere / num_samples) * volume_cube
    return volume_sphere_estimate, inside_sphere

# Parámetros
num_samples = 100000
r = 1

# Ejecutar la simulación
volume_estimate, inside = monte_carlo_sphere_volume(num_samples, r)

print(f"Estimación del volumen de la esfera con {num_samples} muestras: {volume_estimate:.4f}")
print(f"Número de puntos dentro de la esfera: {inside}")

# Visualizar algunos puntos
def visualize_sphere_samples(r, num_points=1000):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    # Generar puntos aleatorios
    x = np.random.uniform(-r, r, num_points)
    y = np.random.uniform(-r, r, num_points)
    z = np.random.uniform(-r, r, num_points)
    # Filtrar puntos dentro de la esfera
    inside = x**2 + y**2 + z**2 <= r**2
    ax.scatter(x[inside], y[inside], z[inside], color='blue', s=1, alpha=0.5, label='Dentro de la esfera')
    ax.scatter(x[~inside], y[~inside], z[~inside], color='red', s=1, alpha=0.1, label='Fuera de la esfera')
    ax.set_title('Visualización de Puntos dentro y fuera de la Esfera')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.show()

# Visualizar algunos puntos
visualize_sphere_samples(r, num_points=5000)
