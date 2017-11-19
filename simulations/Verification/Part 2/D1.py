import modules.pumpingsystem as ps
import numpy as np

schedule = np.array([[70, 70, 70],
                     [75, 75, 75]])

pump_system = ps.PumpSystem('D1')
pump_system.add_level(ps.PumpingLevel('0', 1000000, 0, 15, 0, schedule, 0, 20))

pump_system.perform_simulation('1-factor', save=True)
