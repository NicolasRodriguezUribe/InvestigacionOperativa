import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, kstest
from statsmodels.graphics.tsaplots import plot_acf
from scipy.fft import fft, fftfreq

# Parámetros del Generador Congruencial Lineal
X0 = 7  # Semilla inicial
a = 5  # Multiplicador
c = 3  # Incremento
m = 16  # Módulo
num_iterations = 1000  # Número de números a generar

# Generar la secuencia
sequence = [X0]
for _ in range(num_iterations):
    Xn = (a * sequence[-1] + c) % m
    sequence.append(Xn)
sequence_array = np.array(sequence[1:])


# 3.1. Prueba de Chi-Cuadrado para Uniformidad
def chi_squared_test(sequence, m, alpha=0.05):
    k = m  # Número de intervalos igual al módulo
    observed = np.bincount(sequence, minlength=m)
    expected = len(sequence) / m
    chi_squared_stat = np.sum((observed - expected) ** 2 / expected)
    p_value = 1 - chi2.cdf(chi_squared_stat, df=k - 1)
    result = "Rechazar H0 (No Uniforme)" if p_value < alpha else "No Rechazar H0 (Uniforme)"
    return chi_squared_stat, p_value, result


chi_sq_stat, p_val, chi_sq_result = chi_squared_test(sequence_array, m)

print("Prueba de Chi-Cuadrado para Uniformidad:")
print(f"Estadística Chi-Cuadrado: {chi_sq_stat:.4f}")
print(f"Valor p: {p_val:.4f}")
print(f"Resultado: {chi_sq_result}")


# 3.2. Prueba de Autocorrelación
def autocorrelation_test(sequence, lags=10):
    plt.figure(figsize=(10, 6))
    plot_acf(sequence, lags=lags, alpha=0.05)
    plt.title('Función de Autocorrelación de la Secuencia Generada')
    plt.xlabel('Retardo')
    plt.ylabel('Autocorrelación')
    plt.show()


print("\nGenerando gráfico de autocorrelación...")
autocorrelation_test(sequence_array)


# 3.3. Prueba de Runs
def runs_test(sequence, alpha=0.05):
    mean_seq = np.mean(sequence)
    signs = np.where(sequence > mean_seq, 1, 0)
    n1 = np.sum(signs)
    n2 = len(signs) - n1
    if n1 == 0 or n2 == 0:
        return np.nan, 0.0, "No se puede realizar la prueba (solo un tipo de signo)"
    # Calcular número de runs
    runs = 1 + np.sum(signs[:-1] != signs[1:])
    # Calcular la estadística esperada y varianza
    expected_runs = ((2 * n1 * n2) / len(signs)) + 1
    variance_runs = (2 * n1 * n2 * (2 * n1 * n2 - len(signs))) / (len(signs) ** 2 * (len(signs) - 1))
    z = (runs - expected_runs) / np.sqrt(variance_runs)
    # Calcular valor p
    from scipy.stats import norm
    p_value = 2 * (1 - norm.cdf(abs(z)))
    result = "Rechazar H0 (No aleatorio)" if p_value < alpha else "No Rechazar H0 (Aleatorio)"
    return runs, p_value, result


n_runs, p_val_runs, runs_result = runs_test(sequence_array)

print("\nPrueba de Runs:")
print(f"Número de Runs: {n_runs}")
print(f"Valor p: {p_val_runs:.4f}")
print(f"Resultado: {runs_result}")


# 3.4. Prueba de Kolmogorov-Smirnov
def kolmogorov_smirnov_test(sequence):
    # Normalizar la secuencia para que esté en [0,1)
    normalized_sequence = sequence / m
    ks_stat, ks_p_value = kstest(normalized_sequence, 'uniform')
    result = "Rechazar H0 (No uniforme)" if ks_p_value < 0.05 else "No Rechazar H0 (Uniforme)"
    return ks_stat, ks_p_value, result


ks_stat, ks_p_val, ks_result = kolmogorov_smirnov_test(sequence_array)

print("\nPrueba de Kolmogorov-Smirnov:")
print(f"Estadística KS: {ks_stat:.4f}")
print(f"Valor p: {ks_p_val:.4f}")
print(f"Resultado: {ks_result}")


# 3.5. Pruebas de Periodicidad (FFT)
def periodicity_test(sequence):
    # Normalizar la secuencia
    normalized_sequence = (sequence - np.mean(sequence)) / np.std(sequence)
    # Aplicar FFT
    N = len(normalized_sequence)
    yf = fft(normalized_sequence)
    xf = fftfreq(N, 1.0)[:N // 2]
    magnitude = 2.0 / N * np.abs(yf[0:N // 2])

    # Plotear el espectro de frecuencia
    plt.figure(figsize=(12, 6))
    plt.plot(xf, magnitude)
    plt.title('Espectro de Frecuencia de la Secuencia Generada')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid()
    plt.show()


print("\nGenerando espectro de frecuencia para prueba de periodicidad...")
periodicity_test(sequence_array)


# 3.6. Histograma de Distribución
def plot_histogram(sequence, m):
    plt.figure(figsize=(10, 6))
    plt.hist(sequence, bins=np.arange(m + 1) - 0.5, edgecolor='black', density=True)
    plt.title('Histograma de la Distribución de Números Generados')
    plt.xlabel('Número')
    plt.ylabel('Frecuencia Relativa')
    plt.xticks(range(m))
    plt.show()


print("Generando histograma de distribución...")
plot_histogram(sequence_array, m)
