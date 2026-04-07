from control.interlocks import check_transfer_interlocks
from alarms.alarm_manager import AlarmManager

class BallastSystem:
    def __init__(
        self,
        source_tank,
        destination_tank,
        pump,
        suction_valve,
       discharge_valve,
        min_source_level=10.0,
        max_destination_level=90.0,
    ):
        self.source_tank = source_tank
        self.destination_tank = destination_tank
        self.pump = pump
        self.suction_valve = suction_valve
        self.discharge_valve = discharge_valve

        self.min_source_level = min_source_level
        self.max_destination_level = max_destination_level

        self.last_interlock_reason = "No interlock"
        self.last_flow = 0.0

        self.sequence_state = "IDLE"

        self.alarm_manager = AlarmManager(
            valve_timeout_steps=3,
            pump_timeout_steps=3,
        )

        self.alarms = self.alarm_manager.get_alarm_states()

    def update_alarms(self, step_index):
        self.alarm_manager.update(self, step_index)
        self.alarms = self.alarm_manager.get_alarm_states()


    def step(self, dt, step_index):
        """
        Advance simulation by dt seconds.
        """
        
        self.update_alarms(step_index)

        self.suction_valve.update()
        self.discharge_valve.update()
        self.pump.update()

        allowed, reason = check_transfer_interlocks(
            pump=self.pump,
            suction_valve=self.suction_valve,
            discharge_valve=self.discharge_valve,
            source_tank=self.source_tank,
            destination_tank=self.destination_tank,
            min_source_level=self.min_source_level,
            max_destination_level=self.max_destination_level,
        )

        self.last_interlock_reason = reason
        flow = 0.0

        if allowed:
            requested_flow = self.pump.get_flow()

            max_source_flow = self.source_tank.level / dt
            max_destination_flow = (
                self.destination_tank.capacity - self.destination_tank.level
            ) / dt

            flow = min(requested_flow, max_source_flow, max_destination_flow)

        self.source_tank.update(inflow=0.0, outflow=flow, dt=dt)
        self.destination_tank.update(inflow=flow, outflow=0.0, dt=dt)

        self.last_flow = flow
        self.update_alarms(step_index)

        return flow

    def get_status(self):
        return {
            "source_tank_name": self.source_tank.name,
            "source_tank_level_m3": round(self.source_tank.level, 2),
            "source_tank_level_pct": round(self.source_tank.level_percent(), 1),
            "destination_tank_name": self.destination_tank.name,
            "destination_tank_level_m3": round(self.destination_tank.level, 2),
            "destination_tank_level_pct": round(self.destination_tank.level_percent(), 1),
            "pump_name": self.pump.name,
            "pump_commanded_on": self.pump.commanded_on,
            "pump_running": self.pump.is_running,
            "suction_valve_name": self.suction_valve.name,
            "suction_valve_open": self.suction_valve.is_open,
            "discharge_valve_name": self.discharge_valve.name,
            "discharge_valve_open": self.discharge_valve.is_open,
            "flow_m3s": round(self.last_flow, 2),
            "interlock_reason": self.last_interlock_reason,
            "alarms": self.alarms.copy(),
            'sequence_state': self.sequence_state,
        }
        