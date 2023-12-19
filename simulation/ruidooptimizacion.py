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

# En estas listas se almacena la energía cargada en cada instante de tiempo
ev0 = []
ev1 = []
ev2 = []
ev3 = []

# Estas listas definen a qué hora llegan y se van los vehículos eléctricos
ev0_stay = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ev1_stay = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ev2_stay = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
ev3_stay = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Se definen las horas de llegada y de salida de los vehículos eléctricos a la estación de carga
ev0_arr_time = 6
ev0_dep_time = 11 
ev1_arr_time = 8
ev1_dep_time = 11 
ev2_arr_time = 10
ev2_dep_time = 17
ev3_arr_time = 14
ev3_dep_time = 23 

# Se transforma el perfil de carga del edificio a una lista
Pl = profiles['Load'].tolist()

# Interpolación con ruido gaussiano solo para la carga del edificio
x_interp = np.arange(0, 24, 1/60)  # 1/60 representa el paso de tiempo de 1 minuto en horas
load_interp = interp1d(np.arange(24), Pl, kind='cubic', fill_value="extrapolate")
Pl_interp = load_interp(x_interp) + np.random.normal(0, 1, len(x_interp))  # Ajusta la desviación estándar según sea necesario

# Se ejecuta el algoritmo de optimización una vez cada hora
for i in range(24):
    Pch1 = mdl.continuous_var(name="Pch1")
    Pch2 = mdl.continuous_var(name="Pch2")
    Pch3 = mdl.continuous_var(name="Pch3")
    Pch4 = mdl.continuous_var(name="Pch4")

    # Se utiliza la carga interpolada con ruido solo para la carga del edificio en la optimización
    mdl.minimize(weight * Ce * (Pch1 + Pch2 + Pch3 + Pch4 + Pl_interp[i]) \
        + (ev0_dep_time - i) * ev0_stay[i] * (ev_dem[0] - (Pch1 + ev_ch[0]))**2 \
        + (ev1_dep_time - i) * ev1_stay[i] * (ev_dem[1] - (Pch2 + ev_ch[1]))**2 \
        + (ev2_dep_time - i) * ev2_stay[i] * (ev_dem[2] - (Pch3 + ev_ch[2]))**2 \
        + (ev3_dep_time - i) * ev3_stay[i] * (ev_dem[3] - (Pch4 + ev_ch[3]))**2 \
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

    ev0.append(sol[Pch1])
    ev1.append(sol[Pch2])
    ev2.append(sol[Pch3])
    ev3.append(sol[Pch4])

    ev_ch[0] += sol[Pch1]
    ev_ch[1] += sol[Pch2]
    ev_ch[2] += sol[Pch3]
    ev_ch[3] += sol[Pch4]

# Se muestran los resultados del algoritmo de optimización para cada vehículo
print(ev_dem)
print(ev_ch)

# Se obtiene la potencia de la estación de carga y de la combinación entre el edificio y la estación de carga
Pcs = []
PcsPl = []
x = []
for i in range(24):
    Pcs.append(ev0[i] + ev1[i] + ev2[i] + ev3[i])
    PcsPl.append(Pcs[i] + Pl[i])
    x.append(i)

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
plt.step(x, Pl)

plt.tight_layout()
plt.show()