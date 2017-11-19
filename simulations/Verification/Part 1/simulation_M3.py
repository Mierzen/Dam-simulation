import numpy as np

import modules.pumpingsystem as ps

pump_system = ps.PumpSystem('M3')
pump_system.add_level(ps.PumpingLevel('0', 1000000, 0, 40, 0, np.zeros((1, 3)), 1, 50))

pump_system.perform_simulation('1-factor', save=True)
