import numpy as np
import matplotlib.pyplot as plt

from clase import num_iterations

# Generar una secuencia de números pseudoaleatorios
# Utilizaremos el Generador Mersenne Twister para una mejor calidad
num_iterations = 1000
np.random.seed(7)
uniform_randoms_1 = np.random.rand(num_iterations//2)
uniform_randoms_2 = np.random.rand(num_iterations//2)

# Aplicar la Transformación de Box-Muller
Z0 = np.sqrt(-2 * np.log(uniform_randoms_1)) * np.cos(2 * np.pi * uniform_randoms_2)
Z1 = np.sqrt(-2 * np.log(uniform_randoms_1)) * np.sin(2 * np.pi * uniform_randoms_2)

# Concatenar las secuencias
X_normal = np.concatenate((Z0, Z1))

# Mostrar los primeros 10 valores
print("Primeros 10 valores de la variable aleatoria continua X (Normal):")
print(X_normal[:10])

# Visualizar la distribución
plt.figure(figsize=(8, 5))
plt.hist(X_normal, bins=30, density=True, edgecolor='black', alpha=0.7, label='Empírica')

# Dibujar la FDP teórica
x = np.linspace(np.min(X_normal), np.max(X_normal), 1000)
f_x = (1 / np.sqrt(2 * np.pi)) * np.exp(-x**2 / 2)
plt.plot(x, f_x, 'r', label='Teórica')
plt.title('Distribución de la Variable Aleatoria Continua X (Normal)')
plt.xlabel('Valor de X')
plt.ylabel('Densidad de Probabilidad')
plt.legend()
plt.grid(axis='y')
plt.show()
