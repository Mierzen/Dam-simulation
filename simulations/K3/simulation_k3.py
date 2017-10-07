import modules.pumpingsystem as ps
import pandas as pd
import numpy as np

# Pump schedule as per SCADA. rows = pumps, columns 1:=Peak, 2:=Standard, 3:Off-peak
pump_schedule_44 = np.array([[80, 50, 30],
                            [85, 60, 40],
                            [150, 150, 150],
                            [150, 150, 150]])

# Inflows into dams
dam_inflow_profiles = pd.read_csv('input/K3_dam_inflow_profiles.csv.gz')
inflow_44 = np.reshape(dam_inflow_profiles['44L Inflow'].values, (24, 2))

# Read actual data for initial conditions and verification
actual_values = pd.read_csv('input/K3_data_for_verification.csv.gz')
actual_status_44 = actual_values['44L Status'].values
initial_level_44 = actual_values['44L Level'][0]

# Create pump system
pump_system = ps.PumpSystem('K3')
pump_system.add_level(ps.PumpingLevel("44L", 5000000, initial_level_44,
                                      143, 1900, pump_schedule_44, actual_status_44[0],
                                      inflow_44, pump_statuses_for_verification=actual_status_44,
                                      n_mode_max_pumps=2, n_mode_min_level=30, n_mode_max_level=80))


# Perform simulations
pump_system.perform_simulation(mode='verification', save=True)
pump_system.perform_simulation(mode='1-factor', save=True)
pump_system.perform_simulation(mode='2-factor', save=True)
pump_system.perform_simulation(mode='n-factor', save=True)
