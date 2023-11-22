import subprocess

# Ruta al ejecutable de SUMO (reemplaza con la ubicación correcta)
sumo_bin = "sumo-gui", "-c", "C:/Users/karla/Sumo/2023-11-02-02-13-47/Prueba.sumocfg"

# Comando para iniciar SUMO
command = f'"{sumo_bin}"'  # Usa comillas para manejar espacios en la ruta

# Inicia SUMO desde Python
subprocess.Popen(command, shell=True)

