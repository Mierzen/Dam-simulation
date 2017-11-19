import modules.pumpingsystem as ps
import numpy as np

pump_system = ps.PumpSystem('D2')
pump_system.add_level(ps.PumpingLevel('0', 1000000, 0, 15, 0, np.zeros((1, 3)), 0, 18,
                                      n_mode_max_pumps=2, n_mode_min_level=15, n_mode_control_range=5,
                                      n_mode_bottom_offset=5, n_mode_top_offset=2.5))

pump_system.perform_simulation('n-factor', save=True)
