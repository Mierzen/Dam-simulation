import modules.pumpingsystem as ps
import numpy as np
import pandas as pd

# Inflow into dam
inflow = pd.read_csv('M2_dam_inflow_profiles.csv.gz')
inflow = np.reshape(inflow['0 Inflow'].values, (24, 2))

pump_system = ps.PumpSystem('M2')
pump_system.add_level(ps.PumpingLevel('0', 1000000, 10, 0, 0, np.zeros((1, 3)), 0, inflow))

pump_system.perform_simulation('1-factor', save=True)
