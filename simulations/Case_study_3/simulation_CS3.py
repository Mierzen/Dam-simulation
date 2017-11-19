import modules.pumpingsystem as ps
import pandas as pd
import numpy as np

# Pump schedule as per SCADA. rows = pumps, columns 1:=Peak, 2:=Standard, 3:Off-peak
pump_schedule_41 = np.array([[72, 42, 50],
                             [95, 78, 86],
                             [110, 110, 110],
                             [120, 120, 120],
                             [150, 150, 150]])
pump_schedule_31 = np.array([[77, 45, 45],
                             [92, 70, 60],
                             [110, 110, 110],
                             [120, 120, 120]])
pump_schedule_20 = np.array([[72, 47, 55],
                             [82, 70, 70],
                             [91, 87, 92],
                             [110, 110, 110]])
pump_schedule_IPC = np.array([[80, 45, 45],
                              [85, 70, 60],
                              [90, 82, 82],
                              [110, 110, 110],
                              [150, 150, 150]])
dummy_pump_schedule_surface = np.array([[150, 150, 150]])

# Inflows into dams
dam_inflow_profiles = pd.read_csv('input/CS3_dam_inflow_profiles.csv.gz')
inflow_41 = np.reshape(dam_inflow_profiles['41L Inflow'].values, (24, 2))
inflow_31 = np.reshape(dam_inflow_profiles['31L Inflow'].values, (24, 2))
inflow_20 = np.reshape(dam_inflow_profiles['20L Inflow'].values, (24, 2))
inflow_IPC = np.reshape(dam_inflow_profiles['IPC Inflow'].values, (24, 2))
inflow_surface = np.reshape(dam_inflow_profiles['Surface Inflow'].values, (24, 2))

# Read actual data for initial conditions and validation
actual_values = pd.read_csv('input/CS3_data_for_validation.csv.gz')
actual_status_41 = actual_values['41L Status'].values
actual_status_31 = actual_values['31L Status'].values
actual_status_20 = actual_values['20L Status'].values
actual_status_IPC = actual_values['IPC Status'].values
initial_level_41 = actual_values['41L Level'][0]
initial_level_31 = actual_values['31L Level'][0]
initial_level_20 = actual_values['20L Level'][0]
initial_level_IPC = actual_values['IPC Level'][0]
initial_level_surface = actual_values['Surface Level'][0]

# Create pump system
pump_system = ps.PumpSystem('CS3')
pump_system.add_level(ps.PumpingLevel("41L", 3000000, initial_level_41,
                                      216.8, 3508.4, pump_schedule_41, actual_status_41[0],
                                      inflow_41, fed_to_level="31L", pump_statuses_for_validation=actual_status_41,
                                      n_mode_max_pumps=2, n_mode_max_level=80, n_mode_control_range=30,
                                      n_mode_top_offset=5))
pump_system.add_level(ps.PumpingLevel("31L", 3000000, initial_level_31,
                                      146.8, 3283.6, pump_schedule_31, actual_status_31[0],
                                      inflow_31, fed_to_level="20L", pump_statuses_for_validation=actual_status_31,
                                      n_mode_max_pumps=2, n_mode_max_level=80, n_mode_control_range=20,
                                      n_mode_top_offset=5, n_mode_bottom_offset=5))
pump_system.add_level(ps.PumpingLevel("20L", 3000000, initial_level_20,
                                      171.8, 3821.0, pump_schedule_20, actual_status_20[0],
                                      inflow_20, fed_to_level="IPC", pump_statuses_for_validation=actual_status_20,
                                      n_mode_max_pumps=2, n_mode_control_range=20, n_mode_top_offset=7,
                                      n_mode_bottom_offset=5))
pump_system.add_level(ps.PumpingLevel("IPC", 3000000, initial_level_IPC,
                                      147.4, 3572.8, pump_schedule_IPC, actual_status_IPC[0],
                                      inflow_IPC, fed_to_level="Surface",
                                      pump_statuses_for_validation=actual_status_IPC,
                                      n_mode_max_pumps=2, n_mode_max_level=80, n_mode_control_range=10,
                                      n_mode_top_offset=5, n_mode_bottom_offset=3))
pump_system.add_level(ps.PumpingLevel("Surface", 5000000, initial_level_surface,
                                      0, 0, dummy_pump_schedule_surface, 0, inflow_surface,
                                      pump_statuses_for_validation=actual_status_IPC,
                                      n_mode_max_pumps=0))  # the status data doesn't matter


# Perform simulations
pump_system.perform_simulation(mode='validation', save=True)
pump_system.perform_simulation(mode='1-factor', save=True)
pump_system.perform_simulation(mode='2-factor', save=True)
pump_system.perform_simulation(mode='n-factor', save=True)
