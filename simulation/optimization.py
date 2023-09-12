from docplex.mp.model import Model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

profiles = pd.read_excel('C:/Users/cmsan/OneDrive/Documents/GitHub/case-simulation/simulation/data.xlsx')
results = pd.DataFrame()

profiles.rename(columns = {'Fecha/Hora' : 'Timestamp', 'glb (W/m2)' : 'Irradiance', 'Carga (pu)' : 'Load'}, inplace = True)
profiles['Load'] = profiles['Load'] * 80.00

mdl = Model("EV Charging Station")

Ce = 150 # [CLP/kWh]

weight = 0.001

ev_dem = [40, 30, 50, 60]      # [kWh]
ev_ch = [0, 0, 0, 0]           # [kWh]
ev_stay_time = [6, 4, 8, 10]   # [hrs.]
ev_status = [0, 0, 0, 0]       # [CONNECTED]
Pch_k_1 = [0, 0, 0, 0]         # [kW]

ev0 = []
ev1 = []
ev2 = []
ev3 = []

ev0_stay = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ev1_stay = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ev2_stay = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
ev3_stay = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]



Pl = profiles['Load'].tolist()
Pmax = 80.0
Pchmax = 22.0

Pcs        = mdl.continuous_var(name = "Pcs")
Pch1       = mdl.continuous_var(name = "Pch1")
Pch2       = mdl.continuous_var(name = "Pch2")
Pch3       = mdl.continuous_var(name = "Pch3")
Pch4       = mdl.continuous_var(name = "Pch4")

#cp1_status = mdl.binary_var(name = "cp1_status")
#cp2_status = mdl.binary_var(name = "cp2_status")
#cp3_status = mdl.binary_var(name = "cp3_status")
#cp4_status = mdl.binary_var(name = "cp4_status")

for i in range(24):
    mdl.minimize(weight * Ce * (Pcs + Pl[i]) + ev0_stay[i]*(ev_dem[0] - (Pch1 + ev_ch[0]))**2 + ev1_stay[i]*(ev_dem[1] - (Pch2 + ev_ch[1]))**2 + ev2_stay[i]*(ev_dem[2] - (Pch3 + ev_ch[2]))**2 + ev3_stay[i]*(ev_dem[3] - (Pch4 + ev_ch[3]))**2)

    mdl.add_constraint(Pcs == Pch1 + Pch2 + Pch3 + Pch4)
    mdl.add_constraint(Pch1 <= Pchmax)
    mdl.add_constraint(Pch2 <= Pchmax)
    mdl.add_constraint(Pch3 <= Pchmax)
    mdl.add_constraint(Pch4 <= Pchmax)
    mdl.add_constraint(Pch1 >= 0)
    mdl.add_constraint(Pch2 >= 0)
    mdl.add_constraint(Pch3 >= 0)
    mdl.add_constraint(Pch4 >= 0)
    mdl.add_constraint(Pcs + Pl[i] <= Pmax)

    print(profiles['Load'][i])

    sol = mdl.solve()
#    if sol:
    ev0.append(sol[Pch1])
    ev1.append(sol[Pch2])
    ev2.append(sol[Pch3])
    ev3.append(sol[Pch4])

    ev_ch[0] += sol[Pch1]
    ev_ch[1] += sol[Pch2]
    ev_ch[2] += sol[Pch3]
    ev_ch[3] += sol[Pch4]


print(ev_ch)

#if sol:
#    print("Solution found: ")
#    print("EV1: ", sol[Pch1])
#    print("EV2: ", sol[Pch2])
#    print("EV3: ", sol[Pch3])
#    print("EV4: ", sol[Pch4])
#    print("Pcs: ", sol[Pcs])

#else:
#    print("Solution not found")