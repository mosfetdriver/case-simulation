import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Crear un DataFrame de ejemplo
data = {'x': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        #'y1': [0, 0, 0, 0, 0, 0, 0, 40.37, 156.89, 233.49, 426.3, 991.48, 917.5, 1100.5, 491.2, 298.37, 340.74, 446.79, 180.62, 10.5, 0, 0, 0, 0],
        'y2': [0.3, 0.3, 0.25, 0.35, 0.3, 0.4, 0.5, 0.6, 0.63, 0.54, 0.56, 0.8, 0.85, 0.8, 0.4, 0.3, 0.4, 0.45, 0.55, 0.88, 1, 0.9, 0.6, 0.4]}

df = pd.DataFrame(data)

# Especificar los valores de "x" donde se desea realizar la interpolación
x_interpolados = np.linspace(df['x'].min(), df['x'].max(), num=200)  # Rango continuo de valores de "x"

# Realizar la interpolación lineal para "y1"
#y1_interpolados = np.interp(x_interpolados, df['x'], df['y1'])

# Realizar la interpolación lineal para "y2"
y2_interpolados = np.interp(x_interpolados, df['x'], df['y2'])

# Crear un gráfico
plt.figure(figsize=(8, 6))

# Graficar los datos originales
#plt.plot(df['x'], df['y1'], label='y1 (Original)', marker='o')
plt.plot(df['x'], df['y2'], label='y2 (Original)', marker='o')

# Graficar los valores interpolados
#plt.plot(x_interpolados, y1_interpolados, 'ro', label='y1 (Interpolado)')
plt.plot(x_interpolados, y2_interpolados, 'go', label='y2 (Interpolado)')

# Personalizar el gráfico
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interpolación Lineal de y1 y y2')
plt.legend()

# Mostrar el gráfico
plt.grid(True)
plt.show()
