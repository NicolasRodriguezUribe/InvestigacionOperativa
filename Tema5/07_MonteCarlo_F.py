import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_integration(f, a, b, num_samples):
    # Generar puntos aleatorios en [a, b]
    x = np.random.uniform(a, b, num_samples)
    # Evaluar la función en los puntos generados
    y = f(x)
    # Estimar la integral
    integral_estimate = (b - a) * np.mean(y)
    return integral_estimate, x, y

# Definir la función a integrar, por ejemplo f(x) = sin(x)
def f(x):
    return np.sin(x)

# Parámetros
a = 0
b = np.pi
num_samples = 10000

# Ejecutar la simulación
integral_estimate, x, y = monte_carlo_integration(f, a, b, num_samples)

print(f"Estimación de la integral de sin(x) de {a} a {b}: {integral_estimate:.4f}")

# Visualizar la función y los puntos
plt.figure(figsize=(10, 6))
plt.plot(np.linspace(a, b, 1000), f(np.linspace(a, b, 1000)), label='f(x) = sin(x)')
plt.scatter(x, y, color='red', s=1, alpha=0.3, label='Puntos Aleatorios')
plt.title('Estimación de la Integral usando Monte Carlo')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.show()
