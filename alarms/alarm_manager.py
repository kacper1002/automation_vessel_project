class AlarmManager:
    SOURCE_LOW_LOW = "source_low_low"
    DESTINATION_HIGH_HIGH = "destination_high_high"
    DISCHARGE_VALVE_FAIL_TO_OPEN = "discharge_valve_fail_to_open"
    PUMP_FAIL_TO_START = "pump_fail_to_start"

    def __init__(self, valve_timeout_steps=3, pump_timeout_steps=3):
        self.valve_timeout_steps = valve_timeout_steps
        self.pump_timeout_steps = pump_timeout_steps

        self.alarms = {
            self.SOURCE_LOW_LOW: False,
            self.DESTINATION_HIGH_HIGH: False,
            self.DISCHARGE_VALVE_FAIL_TO_OPEN: False,
            self.PUMP_FAIL_TO_START: False,
        }

        self.history = []

        self._discharge_valve_mismatch_counter = 0
        self._pump_mismatch_counter = 0

    def update(self, system, step):
        self._update_tank_level_alarms(system, step)
        self._update_discharge_valve_alarm(system, step)
        self._update_pump_alarm(system, step)

    def _update_tank_level_alarms(self, system, step):
        self._set_alarm(
            self.SOURCE_LOW_LOW,
            system.source_tank.level <= system.min_source_level,
            step,
        )

        self._set_alarm(
            self.DESTINATION_HIGH_HIGH,
            system.destination_tank.level >= system.max_destination_level,
            step,
        )

    def _update_discharge_valve_alarm(self, system, step):
        commanded_open = system.discharge_valve.commanded_open
        actual_open = system.discharge_valve.is_open

        self._discharge_valve_mismatch_counter = self._next_counter(
            self._discharge_valve_mismatch_counter,
            condition=commanded_open and not actual_open,
        )

        self._set_alarm(
            self.DISCHARGE_VALVE_FAIL_TO_OPEN,
            self._discharge_valve_mismatch_counter >= self.valve_timeout_steps,
            step,
        )

    def _update_pump_alarm(self, system, step):
        commanded_on = system.pump.commanded_on
        running = system.pump.is_running

        self._pump_mismatch_counter = self._next_counter(
            self._pump_mismatch_counter,
            condition=commanded_on and not running,
        )

        self._set_alarm(
            self.PUMP_FAIL_TO_START,
            self._pump_mismatch_counter >= self.pump_timeout_steps,
            step,
        )

    @staticmethod
    def _next_counter(counter, condition):
        return counter + 1 if condition else 0

    def _set_alarm(self, alarm_name, active, step):
        was_active = self.alarms[alarm_name]
        self.alarms[alarm_name] = active

        if was_active != active:
            self.history.append(
                {
                    "step": step,
                    "alarm": alarm_name,
                    "active": active,
                    "event": "RAISED" if active else "CLEARED",
                }
            )

    def get_alarm_states(self):
        return self.alarms.copy()

    def get_active_alarms(self):
        return [name for name, active in self.alarms.items() if active]

    def get_alarm_history(self):
        return self.history.copy()

    def clear_history(self):
        self.history.clear()