import numpy as np
import matplotlib.pyplot as plt

from clase import num_iterations

# Generar una secuencia de números pseudoaleatorios
# Utilizaremos el Generador Mersenne Twister para una mejor calidad
num_iterations = 100000
np.random.seed(7)
uniform_randoms = np.random.rand(num_iterations)

# Definir la FDP y FDA de la distribución exponencial
lambda_param = 1  # Parámetro de la distribución exponencial

# Invertir la FDA para generar variables aleatorias continuas
X_continuous = -np.log(1 - uniform_randoms) / lambda_param

# Mostrar los primeros 10 valores
print("Primeros 10 valores de la variable aleatoria continua X (Exponencial):")
print(X_continuous[:10])

# Visualizar la distribución
plt.figure(figsize=(8, 5))
plt.hist(X_continuous, bins=30, density=True, edgecolor='black', alpha=0.7, label='Empírica')

# Dibujar la FDP teórica
x = np.linspace(0, np.max(X_continuous), 1000)
f_x = lambda_param * np.exp(-lambda_param * x)
plt.plot(x, f_x, 'r', label='Teórica')
plt.title('Distribución de la Variable Aleatoria Continua X (Exponencial)')
plt.xlabel('Valor de X')
plt.ylabel('Densidad de Probabilidad')
plt.legend()
plt.grid(axis='y')
plt.show()
