# Se importan las librerías a utilizar para la simulación 
from docplex.mp.model import Model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Se importa el perfil de carga del edificio y la generación fotovoltaica
profiles = pd.read_excel('data/data.xlsx')
results = pd.DataFrame()

# Se cambian los nombres a las columnas del dataframe para mayor legibilidad
profiles.rename(columns={'Fecha/Hora': 'Timestamp', 'glb (W/m2)': 'Irradiance', 'Carga (pu)': 'Load'}, inplace=True)
profiles['Load'] = profiles['Load'] * 80.00

# Asegurémonos de que la longitud de Pl sea al menos 24
Pl = profiles['Load'].tolist()
while len(Pl) < 24:
    Pl += Pl  # Duplicamos la carga para asegurarnos de tener suficientes datos

# Asegurémonos de que la longitud de Pl sea exactamente 24
Pl = Pl[:24]

# Interpolación con ruido gaussiano para la carga del edificio y la demanda de los vehículos eléctricos
x_interp = np.arange(0, 24, 1/60)
load_interp = interp1d(np.arange(24), Pl, kind='cubic', fill_value="extrapolate")
Pl_interp = load_interp(x_interp) + np.random.normal(0, 1, len(x_interp))

# Definimos las horas de llegada y de salida de los vehículos eléctricos a la estación de carga
ev_arr_time = [6, 8, 10, 14]
ev_dep_time = [11, 11, 17, 23]

# Asegurémonos de que la longitud de Pl sea exactamente 24
Pl = Pl[:24]

# Se crea el modelo de optimización a resolver
mdl = Model("EV Charging Station")

# Se definen las constantes como el precio de la energía eléctrica y el peso de la misma en el algoritmo de optimización
Ce = 150  # [CLP/kWh]
weight = 0  # 0.001

# Se define la potencia máxima que puede entregar la estación de carga y la potencia máxima que puede entregar cada punto de carga
Pmax = 80.0
Pchmax = 22.0

# Se crean dos listas que contienen la demanda de energía y otra que almacena la carga hasta el tiempo t
ev_dem = [60, 50, 80, 150]      # [kWh]
ev_ch = [0, 0, 0, 0]           # [kWh]

# Asegurémonos de que la longitud de Pl sea exactamente 24
Pl = Pl[:24]

# Se ejecuta el algoritmo de optimización una vez cada hora
for i in range(24):
    Pch1 = mdl.continuous_var(name="Pch1")
    Pch2 = mdl.continuous_var(name="Pch2")
    Pch3 = mdl.continuous_var(name="Pch3")
    Pch4 = mdl.continuous_var(name="Pch4")

    # Se utiliza la carga interpolada con ruido solo para la carga del edificio en la optimización
    mdl.minimize(weight * Ce * (Pch1 + Pch2 + Pch3 + Pch4 + Pl_interp[i]) \
        + (ev_dep_time[0] - ev_arr_time[0]) * (ev_dem[0] - (Pch1 + ev_ch[0]))**2 \
        + (ev_dep_time[1] - ev_arr_time[1]) * (ev_dem[1] - (Pch2 + ev_ch[1]))**2 \
        + (ev_dep_time[2] - ev_arr_time[2]) * (ev_dem[2] - (Pch3 + ev_ch[2]))**2 \
        + (ev_dep_time[3] - ev_arr_time[3]) * (ev_dem[3] - (Pch4 + ev_ch[3]))**2 \
        )

    mdl.add_constraint(Pch1 <= Pchmax)
    mdl.add_constraint(Pch2 <= Pchmax)
    mdl.add_constraint(Pch3 <= Pchmax)
    mdl.add_constraint(Pch4 <= Pchmax)

    mdl.add_constraint(Pch1 >= 0)
    mdl.add_constraint(Pch2 >= 0)
    mdl.add_constraint(Pch3 >= 0)
    mdl.add_constraint(Pch4 >= 0)
    
    mdl.add_constraint(Pch1 + Pch2 + Pch3 + Pch4 + Pl_interp[i] <= Pmax)

    sol = mdl.solve()

    if sol is not None:
        ev_ch[0] += sol[Pch1]
        ev_ch[1] += sol[Pch2]
        ev_ch[2] += sol[Pch3]
        ev_ch[3] += sol[Pch4]
    else:
        print(f"Optimization failed at hour {i}")

# Se muestran los resultados del algoritmo de optimización para cada vehículo
print("Demanda de energía de los vehículos eléctricos:", ev_dem)
print("Energía cargada por cada vehículo eléctrico:", ev_ch)

# Asegurémonos de que la longitud de Pl sea al menos 24
if len(Pl) < 24:
    print("La longitud de la lista Pl es menor que 24. Ajusta los datos de entrada.")
else:
    PcsPl = [ev_ch[i] + Pl[i] for i in range(24)]
    x = [i for i in range(24)]

    # Gráficos con interpolación y ruido gaussiano para la carga del edificio
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.title('Potencia de carga del Edificio (Interpolación con ruido)')
    plt.axhline(y=80, color='b', linestyle='--', label='Pmax del empalme')
    plt.plot(x_interp, Pl_interp, label='Pl (Interpolación con ruido)', linestyle='dashed', color='orange')
    plt.legend()

    # Se grafican los resultados obtenidos para la saturación del empalme
    plt.subplot(2, 1, 2)
    plt.title('Potencia del Edificio')
    plt.axhline(y=80, color='r', linestyle='--', label='Pmax del empalme')
    plt.step(x, Pl, label='Perfil de carga del edificio')
    plt.plot(x, PcsPl, label='Potencia de carga de vehículos eléctricos y edificio', linestyle='dashed', color='green')
    plt.legend()

    plt.tight_layout()
    plt.show()
