from docplex.mp.model import Model
import numpy as np

mdl = Model("EV Charging Station")

Ce = 150
weight = 1.0
ev1_dem = 20
ev2_dem = 10
ev3_dem = 30
ev4_dem = 40

Pres = 0
Pcs = 0
Pl = 0
Pmax = 80

ev1 = mdl.continuous_var(name = "ev1")
ev2 = mdl.continuous_var(name = "ev2")
ev3 = mdl.continuous_var(name = "ev3")
ev4 = mdl.continuous_var(name = "ev4")
Pg  = mdl.continuous_var(name = "pg") 

mdl.minimize(weight * Ce * Pg + (ev1_dem - ev1)**2 + (ev2_dem - ev2)**2 + (ev3_dem - ev3)**2 + (ev4_dem - ev4)**2)

mdl.add_constraint(Pg + Pres - Pcs - Pl <= Pmax)

sol = mdl.solve()

if sol:
    print("Solution found: ")
    print("EV1: ", sol[ev1])
    print("EV2: ", sol[ev2])
    print("EV3: ", sol[ev3])
    print("EV4: ", sol[ev4])
    print("Pg: ", sol[Pg])

else:
    print("Solution not found")
