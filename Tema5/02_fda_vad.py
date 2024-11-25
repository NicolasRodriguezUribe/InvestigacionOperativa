import numpy as np
import matplotlib.pyplot as plt

# Parámetros del Generador Congruencial Lineal
X0 = 7       # Semilla inicial
a = 5        # Multiplicador
c = 3        # Incremento
m = 16       # Módulo
num_iterations = 1000000  # Número de números a generar

# Generar la secuencia de números pseudoaleatorios
sequence = [X0]
for _ in range(num_iterations):
    Xn = (a * sequence[-1] + c) % m
    sequence.append(Xn)
sequence_array = np.array(sequence[1:])

# Normalizar la secuencia para obtener números en [0,1)
uniform_randoms = sequence_array / m

# Definir la FDP de la variable aleatoria discreta
# Ejemplo: Número de caras al lanzar dos monedas
# X: 0, 1, 2
# P(X=0) = 0.25, P(X=1) = 0.5, P(X=2) = 0.25

# FDA
cdf = np.array([0.25, 0.75, 1.0])

# Valores posibles de X
x_values = np.array([0, 1, 2])

# Generar variables aleatorias discretas usando inverse transform sampling
def generate_discrete_random_variables(u, cdf, x_values):
    """Genera variables aleatorias discretas a partir de números uniformes u."""
    return np.searchsorted(cdf, u)

# Generar la secuencia de X
X_sequence = generate_discrete_random_variables(uniform_randoms, cdf, x_values)

# Mostrar los primeros 10 valores
print("Primeros 10 valores de la variable aleatoria discreta X:")
print(X_sequence[:10])

# Visualizar la distribución
plt.figure(figsize=(8, 5))
plt.hist(X_sequence, bins=np.arange(-0.5, 3.5, 1), density=True, edgecolor='black', alpha=0.7)
plt.title('Distribución de la Variable Aleatoria Discreta X')
plt.xlabel('Valor de X')
plt.ylabel('Frecuencia Relativa')
plt.xticks(x_values)
plt.grid(axis='y')
plt.show()
