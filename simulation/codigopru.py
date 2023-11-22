import os
import traci

# Función para detectar si un vehículo es eléctrico (puedes personalizarla según tu configuración)
def es_vehiculo_electrico(vehiculo_id):
    # Obtiene la clase del vehículo
    vehicle_class = traci.vehicle.getVehicleClass(vehiculo_id)
    
    # Comprueba si la clase del vehículo es "electric" o similar
    return "electric" in vehicle_class

# Ruta al archivo de configuración SUMO (reemplaza con tu propia ruta)
ruta_archivo_sumo = "C:/Users/karla/Sumo/Pru.sumocfg"

# Ruta al archivo de rutas .rou.xml
ruta_archivo_rutas = "C:/Users/karla/Sumo/Pru/Pru.rou.xml"  # Reemplaza con la ubicación de tu archivo .rou.xml

# Inicia la simulación SUMO
sumo_bin = "sumo-gui"  # Ruta al ejecutable de SUMO
comando = [sumo_bin, "-c", ruta_archivo_sumo, "--route-files", ruta_archivo_rutas]
traci.start(comando)

try:
    # Ejecuta la simulación durante un número determinado de pasos de simulación
    for paso_simulacion in range(1000):  # Cambia el número de pasos según tus necesidades
        traci.simulationStep()

        # Realiza acciones en la simulación, como obtener información de vehículos, semáforos, etc.

        # Detecta vehículos eléctricos cerca de estaciones de recarga y controla la recarga
        for vehiculo_id in traci.vehicle.getIDList():
            if es_vehiculo_electrico(vehiculo_id) and es_cerca_de_estacion_de_recarga(vehiculo_id):
                # Activa la recarga del vehículo eléctrico con una velocidad específica
                traci.vehicle.setChargingParams(vehiculo_id, 1)  # Ajusta la velocidad de recarga según sea necesario

finally:
    # Cierra la simulación SUMO
    traci.close()

# Función para detectar si un vehículo está cerca de una estación de recarga (ajusta las coordenadas)
def es_cerca_de_estacion_de_recarga(vehiculo_id):
    # Obtén la posición del vehículo
    vehicle_position = traci.vehicle.getPosition(vehiculo_id)

    # Compara la posición con la ubicación de las estaciones de recarga (ajusta las coordenadas)
    # En este ejemplo, se considera que está cerca si está a menos de 10 unidades de distancia
    estaciones_de_recarga = [("estacion1", (100.0, 200.0)), ("estacion2", (150.0, 250.0))]
    for estacion, estacion_position in estaciones_de_recarga:
        if traci.simulation.getDistance2D(vehicle_position[0], vehicle_position[1], estacion_position[0], estacion_position[1]) < 10:
            return True
    return False
