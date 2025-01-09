# priority_queue_corrected_with_metrics.py

import numpy as np
import matplotlib.pyplot as plt
from collections import deque


def simulate_priority_queue(lambda_rate, mu_rate, num_customers, priority_levels=2):

    # Generar tiempos entre llegadas y tiempos de servicio
    inter_arrival_times = np.random.exponential(1 / lambda_rate, num_customers)
    service_times = np.random.exponential(1 / mu_rate, num_customers)
    priorities = np.random.choice(range(priority_levels), size=num_customers, p=[0.3, 0.7])

    # Calcular tiempos de llegada acumulativos
    arrival_times = np.cumsum(inter_arrival_times)

    # Inicializar matrices para tiempos de servicio
    service_start_times = np.zeros(num_customers)
    service_end_times = np.zeros(num_customers)
    wait_times = np.zeros(num_customers)

    # Inicializar colas para cada nivel de prioridad
    queues = [deque() for _ in range(priority_levels)]

    # Inicializar tiempo de disponibilidad del servidor
    server_free_time = 0

    # Inicializar índice de llegada
    i = 0

    while i < num_customers or any(queues[p] for p in range(priority_levels)):
        if i < num_customers and arrival_times[i] <= server_free_time:
            # Añadir cliente a la cola correspondiente
            queues[priorities[i]].append(i)
            i += 1
        else:
            if any(queues[p] for p in range(priority_levels)):
                # Encontrar la cola con la más alta prioridad disponible
                for p in range(priority_levels):
                    if queues[p]:
                        next_customer = queues[p].popleft()
                        break

                # Asignar tiempos de servicio
                service_start_times[next_customer] = max(arrival_times[next_customer], server_free_time)
                wait_times[next_customer] = service_start_times[next_customer] - arrival_times[next_customer]
                service_end_times[next_customer] = service_start_times[next_customer] + service_times[next_customer]

                # Actualizar tiempo libre del servidor
                server_free_time = service_end_times[next_customer]
            else:
                if i < num_customers:
                    # Avanzar el tiempo al siguiente evento de llegada
                    server_free_time = arrival_times[i]
                else:
                    break

    # Calcular tiempos en el sistema
    system_times = service_end_times - arrival_times

    # Calcular métricas
    #average_wait = np.mean(wait_times)
    #average_system_time = np.mean(system_times)
    t_final = max(service_end_times)  # Máximo tiempo de servicio terminado
    server_utilization = np.sum(service_times) / t_final if t_final > 0 else 0

    return wait_times, system_times, priorities, server_utilization


# Parámetros de la simulación
lambda_rate = 4  # clientes por hora
mu_rate = 5  # clientes por hora
num_customers = 10000
priority_levels = 2  # 0 - Alta, 1 - Baja

# Ejecutar la simulación
wait_times, system_times, priorities, utilization = simulate_priority_queue(
    lambda_rate, mu_rate, num_customers, priority_levels
)

# Separar métricas por prioridad
high_priority_indices = np.where(priorities == 0)[0]
low_priority_indices = np.where(priorities == 1)[0]

wait_times_high = wait_times[high_priority_indices]
system_times_high = system_times[high_priority_indices]

wait_times_low = wait_times[low_priority_indices]
system_times_low = system_times[low_priority_indices]

# Imprimir métricas generales
print(f"Tiempo de espera promedio en cola (General): {np.mean(wait_times):.2f} horas")
print(f"Tiempo promedio en el sistema (General): {np.mean(system_times):.2f} horas")
print(f"Utilización del servidor: {utilization:.2%}\n")

# Imprimir métricas por prioridad
print(f"--- Métricas para Prioridad Alta (0) ---")
print(f"Tiempo de espera promedio en cola (Alta): {np.mean(wait_times_high):.2f} horas")
print(f"Tiempo promedio en el sistema (Alta): {np.mean(system_times_high):.2f} horas\n")

print(f"--- Métricas para Prioridad Baja (1) ---")
print(f"Tiempo de espera promedio en cola (Baja): {np.mean(wait_times_low):.2f} horas")
print(f"Tiempo promedio en el sistema (Baja): {np.mean(system_times_low):.2f} horas\n")

# Visualizar la distribución de tiempos de espera
plt.figure(figsize=(12, 8))
plt.hist(wait_times_high, bins=50, density=True, edgecolor='black', alpha=0.7, label='Prioridad Alta')
plt.hist(wait_times_low, bins=50, density=True, edgecolor='black', alpha=0.5, label='Prioridad Baja')
plt.title('Distribución de tiempos de espera en cola por prioridad')
plt.xlabel('Tiempo de espera (horas)')
plt.ylabel('Densidad de probabilidad')
plt.legend()
plt.grid(True)
plt.show()

# Visualizar la distribución de tiempos en el sistema
plt.figure(figsize=(12, 8))
plt.hist(system_times_high, bins=50, density=True, edgecolor='black', alpha=0.7, label='Prioridad Alta')
plt.hist(system_times_low, bins=50, density=True, edgecolor='black', alpha=0.5, label='Prioridad Baja')
plt.title('Distribución de tiempos en el sistema por prioridad')
plt.xlabel('Tiempo en el sistema (horas)')
plt.ylabel('Densidad de probabilidad')
plt.legend()
plt.grid(True)
plt.show()



