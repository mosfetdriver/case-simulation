import cvxpy
import powercomponents

cp1 = powercomponents.ChargePoint(22, 3, 4, False)
ev1 = powercomponents.ElectricVehicle("Kia", "Niro", 60, 55)

print(cp1)
print(ev1)