import math


class PumpingLevel:
    def __init__(self, name, capacity, initial_level, pump_flow, pump_power, pump_schedule, fissure_water_inflow,
                 hysteresis=5.0, UL_LL=95.0, UL_HL=100.0, fed_to_level=None):
        self.name = name
        self.capacity = capacity
        self.pump_flow = pump_flow
        self.pump_power = pump_power
        self.pump_schedule = pump_schedule
        self.fissure_water_inflow = fissure_water_inflow
        self.level_history = []
        self.level_history.append(initial_level)
        self.pumping_schedule = []
        self.fed_to_level = fed_to_level  # to which level does this one pump?
        self.last_outflow = 0
        self.hysteresis = hysteresis
        self.UL_LL = UL_LL
        self.UL_HL = UL_HL
        self.UL_100 = False

    def get_level_history(self):
        return self.level_history

    def get_level_history_from_index(self, index):
        return self.level_history[index]

    # @levelHistory.setter
    def set_level_history(self, index, value):
        self.level_history[index] = value

    def get_pumping_schedule(self):
        return self.pumping_schedule

    def getpumping_schedule_from_index(self, index):
        return self.pumping_schedule[index]

    # @levelHistory.setter
    def set_pumping_schedule(self, index, value):
        self.pumping_schedule[index] = value

    def get_last_outflow(self):
        if self.fed_to_level is None:
            return 0
        else:
            return self.last_outflow

    def set_last_outflow(self, value):
        self.last_outflow = value

    def get_upstream_level_name(self):
        return self.fed_to_level

    def get_fissure_water_inflow(self, current_hour=None, current_minute=None, pumps=None):
        if isinstance(self.fissure_water_inflow, int) or isinstance(self.fissure_water_inflow, float):  # it is constant
            return self.fissure_water_inflow
        else:
            if self.fissure_water_inflow.shape[1] == 2:  # if 2 columns. Not f(pump)
                f1 = 0
                f2 = 1
                row = math.floor(current_hour)
            else:  # 3 columns. Is f(pump)
                f1 = 1
                f2 = 2
                row = pumps * 24 - 1 + math.floor(current_hour)

            if math.floor(current_minute) <= 30:
                col = f1
            else:
                col = f2

            return self.fissure_water_inflow[int(row), int(col)]

    def set_UL_100(self, _bool):
        self.UL_100 = _bool


class PumpSystem:
    def __init__(self, name):
        self.name = name
        self.levels = []

    def add_level(self, pumping_level):
        self.levels.append(pumping_level)

    def get_level_from_index(self, level_number):
        return self.levels[level_number]

    def get_level_from_name(self, level_name):
        for l in self.levels:
            if l.name == level_name:
                return l

    def __iter__(self):
        return iter(self.levels)
