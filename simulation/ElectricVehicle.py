class ElectricVehicle:
    def __init__(self, model, autonomy, max_speed, fast_charge, battery, min_charge, max_charge, arrival_time, departure_time):
        self.model = model
        self.autonomy = autonomy
        self.max_speed = max_speed
        self.fast_charge = fast_charge
        self.battery = battery
        self.min_charge = min_charge
        self.max_charge = max_charge
        self.arrival_time = arrival_time
        self.departure_time = departure_time

    def show_info(self):
        print(f"Model: {self.model}")
        print(f"Autonomy: {self.autonomy} km")
        print(f"Max Speed: {self.max_speed} km/h")
        print(f"Fast Charge: {'Yes' if self.fast_charge else 'No'}")
        print(f"Battery: {self.battery}")
        print(f"Min Charge: {self.min_charge}%")
        print(f"Max Charge: {self.max_charge}%")
        print(f"Arrival Time: {self.arrival_time}")
        print(f"Departure Time: {self.departure_time}")


# Create instances for Nissan Leaf, Tesla Model S, Hyundai Ioniq Electric, and BYD Yuan Plus EV
nissan_leaf = ElectricVehicle(
    model="Nissan Leaf",
    autonomy=350,
    max_speed=150,
    fast_charge=True,
    battery=40,  # Battery capacity in kWh
    min_charge=20,  # in percentage
    max_charge=80,  # in percentage
    arrival_time="18:00",
    departure_time="08:00"
)

tesla_model_s = ElectricVehicle(
    model="Tesla Model S",
    autonomy=600,
    max_speed=250,
    fast_charge=True,
    battery=100,  # Battery capacity in kWh
    min_charge=20,  # in percentage
    max_charge=80,  # in percentage
    arrival_time="18:00",
    departure_time="08:00"
)

ioniq_electric = ElectricVehicle(
    model="Hyundai Ioniq Electric",
    autonomy=311,  # Data for the 2022 version
    max_speed=165,
    fast_charge=True,
    battery=38.3,  # Battery capacity in kWh
    min_charge=20,  # in percentage
    max_charge=80,  # in percentage
    arrival_time="18:00",
    departure_time="08:00"
)

byd_yuan_plus_ev = ElectricVehicle(
    model="BYD Yuan Plus EV",
    autonomy=303,  # Data for the 2022 version
    max_speed=150,
    fast_charge=True,
    battery=53.2,  # Battery capacity in kWh
    min_charge=20,  # in percentage
    max_charge=80,  # in percentage
    arrival_time="18:00",
    departure_time="08:00"
)

# Show information for all vehicles
print("Characteristics of the Nissan Leaf:")
nissan_leaf.show_info()

print("\nCharacteristics of the Tesla Model S:")
tesla_model_s.show_info()

print("\nCharacteristics of the Hyundai Ioniq Electric:")
ioniq_electric.show_info()

print("\nCharacteristics of the BYD Yuan Plus EV:")
byd_yuan_plus_ev.show_info()


