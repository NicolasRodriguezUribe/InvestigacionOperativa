import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, kstest
from statsmodels.graphics.tsaplots import plot_acf
from scipy.fft import fft, fftfreq

from clase import chi_squared_test, autocorrelation_test, kolmogorov_smirnov_test, runs_test, periodicity_test, \
    plot_histogram

# Configurar la semilla para reproducibilidad
np.random.seed(7)

# Parámetros
m = 16
num_iterations = 1000

# Generar la secuencia con Mersenne Twister
sequence_mt = np.random.randint(0, m, size=num_iterations)

# 3.1. Prueba de Chi-Cuadrado para Uniformidad
chi_sq_stat_mt, p_val_mt, chi_sq_result_mt = chi_squared_test(sequence_mt, m)

print("\nPrueba de Chi-Cuadrado para Uniformidad (Mersenne Twister):")
print(f"Estadística Chi-Cuadrado: {chi_sq_stat_mt:.4f}")
print(f"Valor p: {p_val_mt:.4f}")
print(f"Resultado: {chi_sq_result_mt}")

# 3.2. Prueba de Autocorrelación
print("\nGenerando gráfico de autocorrelación (Mersenne Twister)...")
autocorrelation_test(sequence_mt)

# 3.3. Prueba de Runs
n_runs_mt, p_val_runs_mt, runs_result_mt = runs_test(sequence_mt)

print("\nPrueba de Runs (Mersenne Twister):")
print(f"Número de Runs: {n_runs_mt}")
print(f"Valor p: {p_val_runs_mt:.4f}")
print(f"Resultado: {runs_result_mt}")

# 3.4. Prueba de Kolmogorov-Smirnov
ks_stat_mt, ks_p_val_mt, ks_result_mt = kolmogorov_smirnov_test(sequence_mt)

print("\nPrueba de Kolmogorov-Smirnov (Mersenne Twister):")
print(f"Estadística KS: {ks_stat_mt:.4f}")
print(f"Valor p: {ks_p_val_mt:.4f}")
print(f"Resultado: {ks_result_mt}")

# 3.5. Pruebas de Periodicidad (FFT)
print("\nGenerando espectro de frecuencia para prueba de periodicidad (Mersenne Twister)...")
periodicity_test(sequence_mt)

# 3.6. Histograma de Distribución
print("Generando histograma de distribución (Mersenne Twister)...")
plot_histogram(sequence_mt, m)
