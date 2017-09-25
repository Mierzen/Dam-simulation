import math


class PumpingLevel:
    def __init__(self, name, capacity, initial_level, pump_flow, pump_power, pump_schedule_table, fissure_water_inflow,
                 hysteresis=5.0, UL_LL=95.0, UL_HL=100.0, fed_to_level=None):
        self.name = name
        self.capacity = capacity
        self.pump_flow = pump_flow
        self.pump_power = pump_power
        self.pump_schedule_table = pump_schedule_table
        self.fissure_water_inflow = fissure_water_inflow
        self.level_history = []
        self.level_history.append(initial_level)
        self.pump_status_history = []
        self.fed_to_level = fed_to_level  # to which level does this one pump?
        self.last_outflow = 0
        self.hysteresis = hysteresis
        self.UL_LL = UL_LL
        self.UL_HL = UL_HL
        self.UL_100 = False
        self.max_pumps = len([1 for r in pump_schedule_table if [150, 150, 150] not in r])

    def get_level_history(self, index=None):
        return self.level_history if index is None else self.level_history[index]

    # @levelHistory.setter
    def set_latest_level(self, value):
        self.level_history.append(value)

    def get_pump_status_history(self, index=None):
        return self.pump_status_history if index is None else self.pump_status_history[index]

    # @levelHistory.setter
    def set_latest_pump_status(self, value):
        self.pump_status_history.append(value)

    def get_scada_pump_schedule_table_level(self, pump_index, tariff_index):
        return self.pump_schedule_table[pump_index, tariff_index]

    def get_last_outflow(self):
        return 0 if self.fed_to_level is None else self.last_outflow

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

    def set_UL_100(self, bool_):
        self.UL_100 = bool_


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

    def perform_simulation(self, mode, seconds=86400):
        # 86400 = seconds in one day

        if mode not in ['1-factor', '2-factor', 'verification']:
            raise ValueError('Invalid simulation mode specified')

        for t in range(seconds):
            cd = math.floor(t / 86400)  # cd = current day
            ch = (t - cd * 86400) / (60 * 60)  # ch = current hour
            cm = (t - cd * 86400 - math.floor(ch) * 60 * 60) / 60  # cm = current minute

            if (7 <= ch < 10) or (18 <= ch < 20):  # Eskom peak
                tou_time_slot = 1
            elif (0 <= ch < 6) or (22 <= ch < 24):  # Eskom off-peak
                tou_time_slot = 3
            else:  # Eskom standard
                tou_time_slot = 2

            for level in self.levels:
                upstream_dam_name = level.get_upstream_level_name()
                if mode == '1-factor' or upstream_dam_name is None:
                    upper_dam_level = 45
                else:
                    upper_dam_level = self.get_level_from_name(upstream_dam_name).get_level_history(t - 1)

                if upper_dam_level >= level.UL_HL:
                    level.set_UL_100(True)
                if upper_dam_level <= level.UL_LL:
                    level.set_UL_100(False)

                if not level.UL_100:
                    pumps_required = 0 if t == 0 else level.get_pump_status_history(t - 1)

                    do_next_check = False

                    for p in range(1, level.max_pumps + 1):
                        dam_level = level.get_level_history(t - 1)
                        pump_level = level.get_scada_pump_schedule_table_level(p - 1, tou_time_slot - 1)

                        if dam_level >= pump_level:
                            pumps_required_temp = p
                            do_next_check = True

                        if dam_level < (
                            level.get_scada_pump_schedule_table_level(0, tou_time_slot - 1) - level.hysteresis):
                            pumps_required = 0
                            do_next_check = False

                    if pumps_required >= (pumps_required_temp + 2):
                        pumps_required = pumps_required_temp + 1
                    if do_next_check:
                        if pumps_required_temp > pumps_required:
                            pumps_required = pumps_required_temp
                else:
                    pumps_required = 0

                # calculate and update simulation values
                pumps = pumps_required
                outflow = pumps * level.pump_flow

                level.set_last_outflow(outflow)

                additional_in_flow = 0
                for level2 in self.levels:
                    if level2.fed_to_level == level.name:
                        additional_in_flow += level2.get_last_outflow()

                level_new = level.get_level_history(t - 1) + 100 / level.capacity * (
                    level.get_fissure_water_inflow(ch, cm, pumps) + additional_in_flow - outflow)
                level.set_latest_level(level_new)
                level.set_latest_pump_status(pumps)
