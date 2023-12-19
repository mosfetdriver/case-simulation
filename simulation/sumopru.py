import os
import shutil
import xml.etree.ElementTree as ET
import traci

# Rutas de los archivos
sumo_cfg_file = 'C:/Users/karla/Sumo/2023-11-23-08-18-39/osm.sumocfg'
sumo_net_file = 'C:/Users/karla/Sumo/2023-11-23-08-18-39/osm.net.xml/osm.net.xml'
charging_station_file = 'C:/Users/karla/Sumo/2023-11-23-08-18-39/charging_station.add.xml'


# Crear una copia del archivo de configuración original
combined_cfg_file = 'combined.sumocfg'
shutil.copy(sumo_cfg_file, combined_cfg_file)

# Agregar la estación de carga al archivo de configuración combinado
tree = ET.parse(combined_cfg_file)
root = tree.getroot()
additional_files = root.find('.//input/additional-files')
if additional_files is not None:
    additional_files.set('value', f"{additional_files.get('value')} {charging_station_file}")

tree.write(combined_cfg_file)

# Iniciar simulación
sumo_binary = 'sumo-gui'  # Cambiar a 'sumo' si no necesitas la interfaz gráfica
sumo_cmd = [sumo_binary, '-c', combined_cfg_file, '--net-file', sumo_net_file]

# Iniciar SUMO
traci.start(sumo_cmd)

# Ejecutar simulación durante 1000 pasos de tiempo
for _ in range(1000):
    traci.simulationStep()

# Detener SUMO al final de la simulación
traci.close()
