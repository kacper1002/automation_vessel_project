class AlarmManager:
    def __init__(self, valve_timeout_steps=3, pump_timeout_steps=3):
        self.valve_timeout_steps = valve_timeout_steps
        self.pump_timeout_steps = pump_timeout_steps

        self.alarms = {
            'source_low_low': False,
            'destination_high_high': False,
            'discharge_valve_fail_to_open': False,
            'pump_fail_to_start': False
        }

        self._dicharge_valve_mismatch_counter = 0 
        self._pump_mismatch_counter = 0

    def update(self, system):
        self.alarms['source_low_low'] = (
            system.source_tank.level <= system.min_source_level
        )

        self.alarms['destination_high_high'] = (
            system.destination_tank.level >= system.max_destination_level
        )

        # ---- Valve fail-to-open alarm
        discharge_valve_command_open = system.discharge_valve.commanded_open
        discharge_valve_actual_open = system.discharge_valve.is_open

        if discharge_valve_command_open and not discharge_valve_actual_open:
            self._dicharge_valve_mismatch_counter += 1
        else:
            self._dicharge_valve_mismatch_counter = 0

        self.alarms['discharge_valve_fail_to_open'] = (
            self._dicharge_valve_mismatch_counter >= self.valve_timeout_steps
        )

        # ------ Pump fail-to-start alarm -----
        pump_commanded_on = system.pump.commanded_on
        pump_running = system.pump.is_running

        if pump_commanded_on and not pump_running:
            self._pump_mismatch_counter += 1
        else:
            self._pump_mismatch_counter = 0

        self.alarms['pump_fail_to_start'] = (
            self._pump_mismatch_counter >= self.pump_timeout_steps
        )

    def get_alarm_states(self):
        return self.alarms.copy()