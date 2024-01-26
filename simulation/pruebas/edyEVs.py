import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Curva interpolada de potencia del edificio
building_power_curve = np.array([[0, 10, 20, 30, 40, 50, 60, 70, 80],
                                [0, 5, 15, 25, 35, 45, 55, 65, 75]])

building_power_interpolator = interp1d(building_power_curve[0], building_power_curve[1], kind='linear', fill_value="extrapolate")

# Parámetros iniciales de los vehículos eléctricos
ev_power_demands = np.array([10, 15, 20, 25])  # Consumo de potencia de cada EV

# Límite de potencia total
power_limit = 80

# Definición de intervalo de tiempo
time_steps = np.arange(0, 24, 1)  # Intervalo de tiempo en horas

# Algoritmo de llenado de agua para ajustar los tiempos de carga
def water_pouring_algorithm(target, containers):
    n = len(containers)
    capacities = np.zeros(n)
    fill_levels = np.zeros(n)
    pouring_times = np.zeros(n)

    while True:
        max_container = np.argmax(fill_levels)
        min_container = np.argmin(fill_levels)

        pour_amount = min(containers[min_container], capacities[max_container] - fill_levels[max_container])
        
        fill_levels[min_container] += pour_amount
        fill_levels[max_container] -= pour_amount

        pouring_times[min_container] += pour_amount

        if np.sum(fill_levels) >= target:
            break

    return pouring_times

# Ejecutar el algoritmo de llenado de agua para ajustar los tiempos de carga
adjusted_charging_times = water_pouring_algorithm(power_limit, ev_power_demands)

# Actualizar la simulación con los nuevos tiempos de carga
ev_power_profiles = np.zeros((len(ev_power_demands), len(time_steps)))
for i in range(len(ev_power_demands)):
    charging_time = adjusted_charging_times[i]
    charging_indices = np.where((time_steps >= 0) & (time_steps <= charging_time))[0]
    ev_power_profiles[i, charging_indices] = ev_power_demands[i]

total_power_consumption = building_power_interpolator(time_steps) + np.sum(ev_power_profiles, axis=0)

# Mostrar la simulación
plt.plot(time_steps, building_power_interpolator(time_steps), label="Edificio")
plt.plot(time_steps, total_power_consumption, label="EVs (Ajustado)")
plt.axhline(power_limit, color='r', linestyle='--', label="Límite de 80 kW")
plt.xlabel("Hora del día")
plt.ylabel("Potencia (kW)")
plt.legend()
plt.title("Simulación de Consumo de Edificio y EVs (Ajustado)")
plt.show()
