import modules.pumpingsystem as ps
import numpy as np

pump_system = ps.PumpSystem('M1')
pump_system.add_level(ps.PumpingLevel('0', 1000000, 0, 0, 0, np.zeros((1, 3)), 0, 10))

pump_system.perform_simulation('1-factor', save=True)
