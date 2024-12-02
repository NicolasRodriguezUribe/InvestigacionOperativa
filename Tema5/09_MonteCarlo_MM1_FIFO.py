import numpy as np
import matplotlib.pyplot as plt

def simulate_fifo_queue(lambda_rate, mu_rate, num_customers):
    # Generar tiempos entre llegadas y tiempos de servicio
    inter_arrival_times = np.random.exponential(1 / lambda_rate, num_customers)
    service_times = np.random.exponential(1 / mu_rate, num_customers)

    # Inicializar variables
    arrival_times = np.cumsum(inter_arrival_times)
    service_start_times = np.zeros(num_customers)
    service_end_times = np.zeros(num_customers)
    wait_times = np.zeros(num_customers)

    # Simulación del sistema de colas
    for i in range(num_customers):
        if i == 0:
            service_start_times[i] = arrival_times[i]
        else:
            service_start_times[i] = max(arrival_times[i], service_end_times[i - 1])
        wait_times[i] = service_start_times[i] - arrival_times[i]
        service_end_times[i] = service_start_times[i] + service_times[i]

    # Calcular tiempos en el sistema
    system_times = service_end_times - arrival_times

    # Métricas
    #average_wait = np.mean(wait_times)
    #average_system_time = np.mean(system_times)
    server_utilization = np.sum(service_times) / service_end_times[-1]

    return wait_times, system_times, server_utilization


# Parámetros
lambda_rate = 4  # clientes por hora
mu_rate = 5      # clientes por hora
num_customers = 10000

# Ejecutar la simulación
wait_times, system_times, utilization = simulate_fifo_queue(lambda_rate, mu_rate, num_customers)

print(f"Tiempo de espera promedio en cola (FIFO): {np.mean(wait_times):.2f} horas")
print(f"Tiempo promedio en el sistema (FIFO): {np.mean(system_times):.2f} horas")
print(f"Utilización del servidor (FIFO): {utilization:.2%}")

# Visualizar la distribución de tiempos de espera
plt.figure(figsize=(10, 6))
plt.hist(wait_times, bins=50, density=True, edgecolor='black', alpha=0.7)
plt.title('Distribución de tiempos de espera en cola (FIFO)')
plt.xlabel('Tiempo de espera (horas)')
plt.ylabel('Densidad de probabilidad')
plt.grid(True)
plt.show()

# Visualizar la distribución de tiempos en el sistema
plt.figure(figsize=(10, 6))
plt.hist(system_times, bins=50, density=True, edgecolor='black', alpha=0.7)
plt.title('Distribución de tiempos en el sistema (FIFO)')
plt.xlabel('Tiempo en el sistema (horas)')
plt.ylabel('Densidad de probabilidad')
plt.grid(True)
plt.show()


