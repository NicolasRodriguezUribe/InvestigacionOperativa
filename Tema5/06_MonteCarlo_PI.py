import numpy as np
import matplotlib.pyplot as plt


def estimate_pi(num_samples):
    # Generar puntos aleatorios en el rango [-1, 1]
    x = np.random.uniform(-1, 1, num_samples)
    y = np.random.uniform(-1, 1, num_samples)

    # Calcular la distancia al origen
    distance = np.sqrt(x ** 2 + y ** 2)

    # Contar puntos dentro del círculo
    inside_circle = np.sum(distance <= 1)

    # Estimar pi
    pi_estimate = (inside_circle / num_samples) * 4

    return pi_estimate, x, y, distance


# Número de muestras
num_samples = 1000000

# Estimar pi
pi_estimate, x, y, distance = estimate_pi(num_samples)

print(f"Estimación de π con {num_samples} muestras: {pi_estimate}")

# Visualizar los puntos
plt.figure(figsize=(6, 6))
plt.scatter(x[distance <= 1], y[distance <= 1], color='blue', s=1, label='Dentro del círculo')
plt.scatter(x[distance > 1], y[distance > 1], color='red', s=1, label='Fuera del círculo')
plt.legend()
plt.title('Estimación de π mediante Simulación de Monte Carlo')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.show()
