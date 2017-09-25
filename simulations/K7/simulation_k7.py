import modules.pumpingsystem as ps
import pandas as pd
import numpy as np

# Pump schedule as per SCADA. rows = pumps, columns 1:=Peak, 2:=Standard, 3:Off-peak
pump_schedule_41 = np.array([[65, 50, 30],
                             [70, 60, 40],
                             [80, 70, 50],
                             [90, 80, 60],
                             [150, 150, 150]])
pump_schedule_31 = np.array([[80, 75, 30],
                             [85, 80, 40],
                             [90, 85, 50],
                             [95, 95, 90]])
pump_schedule_20 = np.array([[80, 65, 30],
                             [85, 75, 40],
                             [90, 85, 50],
                             [95, 95, 90]])
pump_schedule_IPC = np.array([[80, 75, 30],
                              [85, 80, 40],
                              [90, 85, 50],
                              [95, 95, 65],
                              [150, 150, 150]])

# Inflows into dams
dam_inflow_profiles = pd.read_csv('K7_dam_inflow_profiles.csv.gz')
inflow_41 = np.reshape(dam_inflow_profiles['41L Inflow'].values, (24, 2))
inflow_31 = np.reshape(dam_inflow_profiles['31L Inflow'].values, (24, 2))
inflow_20 = np.reshape(dam_inflow_profiles['20L Inflow'].values, (24, 2))
inflow_IPC = np.reshape(dam_inflow_profiles['IPC Inflow'].values, (24, 2))

# Read actual data for initial conditions and verification
actual_values = pd.read_csv('K7_data_for_verification.csv.gz')
actual_status_41 = actual_values['41L Status'].values
actual_status_31 = actual_values['31L Status'].values
actual_status_20 = actual_values['20L Status'].values
actual_status_IPC = actual_values['IPC Status'].values
initial_level_41 = actual_values['41L Level'][0]
initial_level_31 = actual_values['31L Level'][0]
initial_level_20 = actual_values['20L Level'][0]
initial_level_IPC = actual_values['IPC Level'][0]

# Create pump system
pump_system = ps.PumpSystem('K7')
pump_system.add_level(ps.PumpingLevel("41L", 3000000, initial_level_41,
                                      216.8, 3508.4, pump_schedule_41, 1,
                                      inflow_41, fed_to_level="31L"))
pump_system.add_level(ps.PumpingLevel("31L", 3000000, initial_level_31,
                                      146.8, 3283.6, pump_schedule_31, 3,
                                      inflow_31, fed_to_level="20L"))
pump_system.add_level(ps.PumpingLevel("20L", 3000000, initial_level_20,
                                      171.8, 3821.0, pump_schedule_20, 3,
                                      inflow_20, fed_to_level="IPC"))
pump_system.add_level(ps.PumpingLevel("IPC", 3000000, initial_level_IPC,
                                      147.4, 3572.8, pump_schedule_IPC, 3,
                                      inflow_IPC))


# Perform simulations
# pump_system.perform_simulation(mode='verification')
pump_system.perform_simulation(mode='1-factor', save=True)
# pump_system.perform_simulation(mode='2-factor')
