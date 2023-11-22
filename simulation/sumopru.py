import os
import traci


# Ruta al archivo de configuración SUMO (reemplaza con tu propia ruta)
ruta_archivo_sumo = "C:/Users/karla/Sumo/2023-11-14-11-44-14/Prueba.sumocfg"

# Inicia la simulación SUMO
sumo_bin = "sumo-gui"  # Ruta al ejecutable de SUMO
comando = [sumo_bin, "-c", ruta_archivo_sumo]
traci.start(comando)

try:
    # Ejecuta la simulación durante un número determinado de pasos de simulación
    for paso_simulacion in range(1000):  # Cambia el número de pasos según tus necesidades
        traci.simulationStep()

finally:
    # Cierra la simulación SUMO
    traci.close()


