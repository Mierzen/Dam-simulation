import modules.pumpingsystem as ps
import pandas as pd
import numpy as np

# Pump schedule as per SCADA. rows = pumps, columns 1:=Peak, 2:=Standard, 3:Off-peak
pump_schedule_27 = np.array([[80, 30, 30],
                            [85, 40, 40],
                            [90, 85, 80],
                            [150, 150, 150],
                            [150, 150, 150]])
pump_schedule_12 = np.array([[80, 30, 30],
                            [85, 40, 40],
                            [90, 50, 50],
                            [150, 150, 150],
                            [150, 150, 150]])

# Inflows into dams
dam_inflow_profiles = pd.read_csv('input/K10_dam_inflow_profiles.csv.gz')
inflow_27 = np.reshape(dam_inflow_profiles['27L Inflow'].values, (24, 2))
inflow_12 = np.reshape(dam_inflow_profiles['12L Inflow'].values, (24, 2))

# Read actual data for initial conditions and verification
actual_values = pd.read_csv('input/K10_data_for_verification.csv.gz')
actual_status_27 = actual_values['27L Status'].values
actual_status_12 = actual_values['12L Status'].values
initial_level_27 = actual_values['27L Level'][0]
initial_level_12 = actual_values['12L Level'][0]

# Create pump system
pump_system = ps.PumpSystem('K10')
pump_system.add_level(ps.PumpingLevel("27L", 3000000, initial_level_27,
                                      236.1, 2925.6, pump_schedule_27, actual_status_27[0],
                                      inflow_27, fed_to_level="12L", pump_statuses_for_verification=actual_status_27,
                                      n_mode_max_pumps=2, n_mode_control_range=20))
pump_system.add_level(ps.PumpingLevel("12L", 3000000, initial_level_12,
                                      194.6, 2656.6, pump_schedule_12, actual_status_12[0],
                                      inflow_12, pump_statuses_for_verification=actual_status_12, n_mode_max_pumps=3,
                                      n_mode_control_range=20, n_mode_min_level=36, n_mode_max_level=80))


# Perform simulations
pump_system.perform_simulation(mode='verification', save=True)
pump_system.perform_simulation(mode='1-factor', save=True)
pump_system.perform_simulation(mode='2-factor', save=True)
pump_system.perform_simulation(mode='n-factor', save=True)
