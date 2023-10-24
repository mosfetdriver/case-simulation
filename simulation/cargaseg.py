import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Crear un rango de tiempo de un día completo (86400 segundos)
tiempo_dia = np.arange(0, 86400)

# Generar datos de carga ficticios (puedes reemplazar estos datos con datos reales)
carga = np.sin(2 * np.pi * tiempo_dia / 86400) + np.random.normal(0, 0.1, tiempo_dia.shape)

# Crear una función de interpolación cúbica suave
interpolacion_cubica = interp1d(tiempo_dia, carga, kind='cubic')

# Generar puntos intermedios para suavizar la curva
tiempo_interpolado = np.linspace(tiempo_dia.min(), tiempo_dia.max(), 86400)
carga_interpolada = interpolacion_cubica(tiempo_interpolado)

# Crear un gráfico para mostrar los datos originales y suavizados
plt.figure(figsize=(12, 6))

plt.plot(tiempo_dia, carga, 'o', markersize=1, label='Datos originales para la carga con ruido')
plt.plot(tiempo_interpolado, carga_interpolada, '-', label='Datos Suavizados')

plt.xlabel('Tiempo (segundos)')
plt.ylabel('Carga (kW)')
plt.title('Interpolación para el perfil de carga en un día')

plt.legend()
plt.grid(True)
plt.show()
