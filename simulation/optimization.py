# Se importan las librerías a utilizar para la simulación
from docplex.mp.model import Model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import traci

# Se importa el perfil de carga del edificio y la generación fotovoltaica
profiles = pd.read_excel('C:/Users/karla/OneDrive/Documentos/GitHub/case-simulation/datos_interpolados.xlsx')
results = pd.DataFrame()

# Se cambian los nombres a las columnas del dataframe para mayor legibilidad
profiles.rename(columns = {'Fecha/Hora' : 'Timestamp', 'glb (W/m2)' : 'Irradiance', 'Carga (pu)' : 'Load'}, inplace = True)
profiles['Load'] = profiles['Load'] * 80.00

# Se crea el modelo de optimización a resolver
mdl = Model("EV Charging Station")

# Se definen las constantes como el precio de la energía eléctrica y el peso de la misma en el algoritmo de optimización
Ce = 150 # [CLP/kWh]
weight = 0 #0.001

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

# Se ejecuta el algoritmo de optimización una vez cada hora
for i in range(24):
    Pch1       = mdl.continuous_var(name = "Pch1")
    Pch2       = mdl.continuous_var(name = "Pch2")
    Pch3       = mdl.continuous_var(name = "Pch3")
    Pch4       = mdl.continuous_var(name = "Pch4")
    
    mdl.minimize(weight * Ce * (Pch1 + Pch2 + Pch3 + Pch4 + Pl[i]) \
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
    
    mdl.add_constraint(Pch1 + Pch2 + Pch3 + Pch4 + Pl[i] <= Pmax)


    sol = mdl.solve()
    print("*******")
    print("h =", i)
    print("Pch1 =", sol[Pch1])
    print("Pch2 =", sol[Pch2])
    print("Pch3 =", sol[Pch3])
    print("Pch4 =", sol[Pch4])
    print("Pl =", Pl[i])
    print("ev_ch =", ev_ch[3])
    print("Pmax =", Pmax)
    print("obj =", sol.objective_value)

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

# Se grafican los resultados de simulación obtenidos para los vehículos eléctricos
plt.title('Potencia de carga de los vehículos eléctricos')
plt.axhline(y=22, color = 'r', linestyle = '--')
plt.step(x, ev0)
plt.step(x, ev1)
plt.step(x, ev2)
plt.step(x, ev3)
plt.show()

# Se grafican los resultados obtenidos para la saturación del empalme
plt.title('Potencia de la EC, del Edificio y del Empalme')
plt.axhline(y=80, color = 'r', linestyle = '--')
plt.step(x, PcsPl)
plt.step(x, Pcs)
plt.step(x, Pl)
plt.show()