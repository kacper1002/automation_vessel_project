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
        self.history = []

        self._dicharge_valve_mismatch_counter = 0 
        self._discharge_valve_mismatch_counter = 0
        self._pump_mismatch_counter = 0

    def update(self, system, step):
        self._set_alarm(
            'source_low_low',
            system.source_tank.level <= system.min_source_level,
            step
        )

        self._set_alarm(
            'destination_high_high',
            system.destination_tank.level >= system.max_destination_level,
            step
        )

        # ---- Valve fail-to-open alarm
        discharge_valve_command_open = system.discharge_valve.commanded_open
        discharge_valve_actual_open = system.discharge_valve.is_open

        if discharge_valve_command_open and not discharge_valve_actual_open:
            self._dicharge_valve_mismatch_counter += 1
        else:
            self._dicharge_valve_mismatch_counter = 0

        self._set_alarm(
            'discharge_valve_fail_to_open',
            self._dicharge_valve_mismatch_counter >= self.valve_timeout_steps,
            step
        )

        # ------ Pump fail-to-start alarm -----
        pump_commanded_on = system.pump.commanded_on
        pump_running = system.pump.is_running

        if pump_commanded_on and not pump_running:
            self._pump_mismatch_counter += 1
        else:
            self._pump_mismatch_counter = 0
    def _set_alarm(self, alarm_name, active, step):
        was_active = self.alarms[alarm_name]
        self.alarms[alarm_name] = active

        if was_active != active:
            self.history.append(
                {
                    "step": step,
                    "alarm": alarm_name,
                    "active": active,
                }
            )

    def get_alarm_states(self):
        return self.alarms.copy()

    def update(self, system, step):
        self._set_alarm(
            'source_low_low',
            system.source_tank.level <= system.min_source_level,
            step
        )

        self._set_alarm(
            'destination_high_high',
            system.destination_tank.level >= system.max_destination_level,
            step
        )

        # ---- Valve fail-to-open alarm
        discharge_valve_command_open = system.discharge_valve.commanded_open
        discharge_valve_actual_open = system.discharge_valve.is_open

        if discharge_valve_command_open and not discharge_valve_actual_open:
            self._discharge_valve_mismatch_counter += 1
        else:
            self._discharge_valve_mismatch_counter = 0

        self._set_alarm(
            'discharge_valve_fail_to_open',
            self._discharge_valve_mismatch_counter >= self.valve_timeout_steps,
            step
        )

        # ------ Pump fail-to-start alarm -----
        pump_commanded_on = system.pump.commanded_on
        pump_running = system.pump.is_running

        if pump_commanded_on and not pump_running:
            self._pump_mismatch_counter += 1
        else:
            self._pump_mismatch_counter = 0

        self._set_alarm(
            'pump_fail_to_start',
            self._pump_mismatch_counter >= self.pump_timeout_steps,
            step
        )

        self._set_alarm(
            'pump_fail_to_start',
            self._pump_mismatch_counter >= self.pump_timeout_steps,
            step
        )
def get_alarm_history(self):
    return self.history.copy()
    def get_alarm_history(self):
        return self.history.copy()