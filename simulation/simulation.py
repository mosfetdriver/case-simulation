import powercomponents
import pandas as pd

#CONSTANTS
cable_ampacity        = 115                                       # [A]
single_phase_voltage  = 230                                       # [V]
three_phase_voltage   = 380                                       # [V]
informatics_max_power = 3 * single_phase_voltage * cable_ampacity # [W]
electricity_price     = 150                                       # [CLP/kWh]

profiles = pd.read_excel('C:/Users/cmsan/OneDrive/Documents/GitHub/case-simulation/simulation/data.xlsx')