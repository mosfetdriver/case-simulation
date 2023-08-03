class Building:
    def __init__(self, designator, power_consumption):
        self.designator = designator
        self.power_consumption = power_consumption

    def __str__(self):
        return f"Building {self.designator}."

class ChargingStation:
    def __init__(self, designator, power_consumption):
        self.designator = designator
        self.power_consumption = power_consumption

    def __str__(self):
        return f"Charging Station {self.designator}."

class ChargePoint:
    def __init__(self, max_power, charging_station, designator, reserved_status):  
        self.max_power = max_power
        self.charging_station = charging_station
        self.designator = designator
        self.reserved_status = reserved_status

    def __str__(self):
        return f"Charge Point {self.designator} on Charge Station {self.designator} with {self.max_power} kW of maximum charge power.\nReserved: {self.reserved_status}\n"
    
class ElectricVehicle:
    def __init__(self, brand, model, battery_capacity, battery_soc, min_charging_power, max_charging_power, energy_demand, departure_time):
        self.brand = brand
        self.model = model
        self.battery_capacity = battery_capacity
        self.battery_soc = battery_soc
        self.min_charging_power = min_charging_power
        self.max_charging_power = max_charging_power
        self.energy_demand = energy_demand
        self.departure_time = departure_time

    def __str__(self):
        return f"{self.brand} {self.model} EV with {self.battery_capacity} kWh of battery capacity and {self.battery_soc} % of charge.\n"