import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import heapq

def simulate_round_robin_queue(lambda_rate, mu_rate, num_customers, priority_levels=2, time_slice=1.0):

    # Generar tiempos entre llegadas y tiempos de servicio
    inter_arrival_times = np.random.exponential(1 / lambda_rate, num_customers)
    service_times = np.random.exponential(1 / mu_rate, num_customers)
    priorities = np.random.choice(range(priority_levels), size=num_customers, p=[0.3, 0.7])

    # Calcular tiempos de llegada acumulativos
    arrival_times = np.cumsum(inter_arrival_times)

    # Inicializar matrices para tiempos de servicio
    service_remaining = service_times.copy()  # Tiempo de servicio restante para cada cliente
    wait_times = np.zeros(num_customers)
    system_times = np.zeros(num_customers)

    # Inicializar colas para cada nivel de prioridad
    queues = [deque() for _ in range(priority_levels)]

    # Inicializar eventos
    event_queue = []
    for i in range(num_customers):
        heapq.heappush(event_queue, (arrival_times[i], 'arrival', i))

    # Estado del servidor
    server_busy = False
    current_time = 0

    # Variables para seguimiento
    last_event_time = 0
    server_utilization_time = 0  # Tiempo total que el servidor está ocupado

    while event_queue or any(queues[p] for p in range(priority_levels)):

        if event_queue:
            event_time, event_type, customer_id = heapq.heappop(event_queue)
            current_time = event_time
        else:
            # No hay más eventos, pero aún hay clientes en cola
            if any(queues[p] for p in range(priority_levels)):
                current_time = last_event_time
            else:
                break

        if event_type == 'arrival':
            # Añadir cliente a su cola de prioridad
            priority = priorities[customer_id]
            queues[priority].append(customer_id)
        else:
            # Evento de finalización de servicio
            server_busy = False
            # Si el cliente aún necesita servicio, reinsertarlo en la cola
            if service_remaining[customer_id] > 0:
                priority = priorities[customer_id]
                queues[priority].append(customer_id)
            else:
                # Cliente finaliza y sale del sistema
                system_times[customer_id] = current_time - arrival_times[customer_id]

        # Procesar clientes si el servidor está libre y hay clientes en cola
        while not server_busy and any(queues[p] for p in range(priority_levels)):
            for p in range(priority_levels):
                if queues[p]:
                    next_customer = queues[p].popleft()
                    # Determinar el tiempo de servicio asignado en este ciclo
                    service_time = min(time_slice, service_remaining[next_customer])

                    # Calcular el tiempo de espera si es la primera vez que se atiende
                    if service_times[next_customer] == service_remaining[next_customer]:
                        wait_times[next_customer] = current_time - arrival_times[next_customer]

                    # Actualizar tiempos
                    service_remaining[next_customer] -= service_time
                    server_utilization_time += service_time

                    # Programar evento de finalización de servicio
                    heapq.heappush(event_queue, (current_time + service_time, 'departure', next_customer))
                    server_busy = True
                    last_event_time = current_time + service_time
                    break  # Salir después de atender un cliente

    # Calcular utilización del servidor
    total_simulation_time = current_time
    server_utilization = server_utilization_time / total_simulation_time if total_simulation_time > 0 else 0

    return wait_times, system_times, priorities, server_utilization



# Parámetros de la simulación
lambda_rate = 4  # clientes por hora
mu_rate = 5  # clientes por hora
num_customers = 10000
priority_levels = 2  # 0 - Alta, 1 - Baja
time_slice = 0.5  # Tiempo asignado a cada cliente por ciclo (horas)

# Ejecutar la simulación de Round Robin
wait_times_rr, system_times_rr, priorities_rr, utilization_rr = simulate_round_robin_queue(
    lambda_rate, mu_rate, num_customers, priority_levels, time_slice
)

# Separar métricas por prioridad
high_priority_indices = np.where(priorities_rr == 0)[0]
low_priority_indices = np.where(priorities_rr == 1)[0]

wait_times_high = wait_times_rr[high_priority_indices]
system_times_high = system_times_rr[high_priority_indices]

wait_times_low = wait_times_rr[low_priority_indices]
system_times_low = system_times_rr[low_priority_indices]

# Imprimir métricas generales
print(f"--- Métricas Generales ---")
print(f"Tiempo de espera promedio en cola: {np.mean(wait_times_rr):.2f} horas")
print(f"Tiempo promedio en el sistema: {np.mean(system_times_rr):.2f} horas")
print(f"Utilización del servidor: {utilization_rr:.2%}\n")

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
plt.title('Distribución de tiempos de espera en cola por prioridad (Round Robin)')
plt.xlabel('Tiempo de espera (horas)')
plt.ylabel('Densidad de probabilidad')
plt.legend()
plt.grid(True)
plt.show()

# Visualizar la distribución de tiempos en el sistema
plt.figure(figsize=(12, 8))
plt.hist(system_times_high, bins=50, density=True, edgecolor='black', alpha=0.7, label='Prioridad Alta')
plt.hist(system_times_low, bins=50, density=True, edgecolor='black', alpha=0.5, label='Prioridad Baja')
plt.title('Distribución de tiempos en el sistema por prioridad (Round Robin)')
plt.xlabel('Tiempo en el sistema (horas)')
plt.ylabel('Densidad de probabilidad')
plt.legend()
plt.grid(True)
plt.show()