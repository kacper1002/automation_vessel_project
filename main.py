import os
import matplotlib.pyplot as plt

from src.tank import Tank
from src.pump import Pump
from src.valve import Valve
from src.system import BallastSystem
from control.logic import apply_control_logic

SEQUENCE_STATE_MAP = {
    'IDLE': 0,
    'OPENING_VALVES': 1,
    'TRANSFERRING': 2,
    'STOPPING': 3,
}

def scenario_operator_valve_closure_recovery(i):
    if i < 10:
        return{
            'manual_pump_command': True,
            'manual_suction_valve_command': True,
            'manual_discharge_valve_command': True,
            'v2_stuck_closed': False,
            'pump_failed_to_start': False,
        }
    elif 10 <= i < 16:
        return{
            'manual_pump_command': True,
            'manual_suction_valve_command': True,
            'manual_discharge_valve_command': False,
            'v2_stuck_closed': False,
            'pump_failed_to_start': False,
        }
    else:
        return{
            'manual_pump_command': True,
            'manual_suction_valve_command': True,
            'manual_discharge_valve_command': True,
            'v2_stuck_closed': False,
            'pump_failed_to_start': False,
        }
    
def scenario_valve_fail_to_open(i):
    if i < 10:
        return{
            'manual_pump_command': True,
            'manual_suction_valve_command': True,
            'manual_discharge_valve_command': True,
            'v2_stuck_closed': False,
            'pump_failed_to_start': False,
        }
    elif 10 <= i < 16:
        return{
            'manual_pump_command': True,
            'manual_suction_valve_command': True,
            'manual_discharge_valve_command': True,
            'v2_stuck_closed': True,
            'pump_failed_to_start': False,
        }
    else:
        return{
            'manual_pump_command': True,
            'manual_suction_valve_command': True,
            'manual_discharge_valve_command': True,
            'v2_stuck_closed': False,
            'pump_failed_to_start': False,
        }
    
def scenario_pump_fail_start(i):
    if i < 10:
        return{
            'manual_pump_command': True,
            'manual_suction_valve_command': True,
            'manual_discharge_valve_command': True,
            'v2_stuck_closed': False,
            'pump_failed_to_start': False,
        }
    elif 10 <= i < 16:
        return{
            'manual_pump_command': True,
            'manual_suction_valve_command': True,
            'manual_discharge_valve_command': True,
            'v2_stuck_closed': False,
            'pump_failed_to_start': True,
        }
    else:
        return{
            'manual_pump_command': True,
            'manual_suction_valve_command': True,
            'manual_discharge_valve_command': True,
            'v2_stuck_closed': False,
            'pump_failed_to_start': False,
        }
    
def scenario_normal_manual_transfer(i):
    return{
            'manual_pump_command': True,
            'manual_suction_valve_command': True,
            'manual_discharge_valve_command': True,
            'v2_stuck_closed': False,
            'pump_failed_to_start': False,
        }

SCENARIOS = {
    'normal_manual_transfer': scenario_normal_manual_transfer,
    'operator_valve_closure_recovery': scenario_operator_valve_closure_recovery,
    'valve_fail_to_open': scenario_valve_fail_to_open,
    'pump_fail_to_start': scenario_pump_fail_start
}

def plot_results(
    output_path,
    time,
    source,
    destination,
    flow,
    suction_valve_actual,
    discharge_valve_actual,
    suction_valve_command,
    discharge_valve_command,
    pump_actual,
    pump_command,
    sequence_state_numeric,
):
    os.makedirs("outputs", exist_ok=True)

    fig, axes = plt.subplots(3, 1, figsize=(11, 10), sharex=True)

    # --- Tank levels ---
    axes[0].plot(time, source, label="Port Tank [m3]")
    axes[0].plot(time, destination, label="Starboard Tank [m3]")
    axes[0].set_ylabel("Level [m3]")
    axes[0].set_title("Tank Levels")
    axes[0].grid(alpha=0.3)
    axes[0].legend()

    # --- Flow ---
    axes[1].plot(time, flow, label="Flow [m3/s]")
    axes[1].set_ylabel("Flow [m3/s]")
    axes[1].set_title("Flow Rate")
    axes[1].grid(alpha=0.3)
    axes[1].legend()

    # --- Commands vs actual states ---
    axes[2].step(
        time,
        [v + 0.10 for v in suction_valve_actual],
        where="post",
        label="Suction Valve Actual",
        alpha=0.6,
    )
    axes[2].step(
        time,
        [v + 0.10 for v in suction_valve_command],
        where="post",
        linestyle="--",
        label="Suction Valve Command",
    )

    axes[2].step(
        time,
        discharge_valve_actual,
        where="post",
        label="Discharge Valve Actual",
        alpha=0.6,
    )
    axes[2].step(
        time,
        discharge_valve_command,
        where="post",
        linestyle="--",
        label="Discharge Valve Command",
    )

    axes[2].step(
        time,
        [v - 0.10 for v in pump_actual],
        where="post",
        linestyle=":",
        label="Pump Actual",
    )
    axes[2].step(
        time,
        [v - 0.10 for v in pump_command],
        where="post",
        linestyle="--",
        label="Pump Command",
    )

    axes[2].set_ylabel("State")
    axes[2].set_xlabel("Time step")
    axes[2].set_title("Commands vs Actual States")
    axes[2].grid(alpha=0.3)
    axes[2].set_ylim(-0.3, 1.3)
    axes[2].set_yticks([0, 1])
    axes[2].legend(ncol=2)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def run_scenario(scenario_name, steps = 30, dt=1.0):
    scenario_fn = SCENARIOS[scenario_name]

    tank_port = Tank('Port Tank', 100.0, 70.0)
    tank_starboard = Tank('Starboard Tank', 100.0, 20.0)

    pump = Pump(
        'P1',
        flow_rate=2.0,
        is_running=False,
        start_delay_steps=2,
        stop_delay_steps=1
    )

    v1 = Valve(
        'V1',
        is_open=False,
        opening_delay_steps=2,
        closing_delay_steps=2,
    )

    v2 = Valve(
        'V2',
        is_open=False,
        opening_delay_steps=2,
        closing_delay_steps=2,
    )

    system = BallastSystem(
        tank_port,
        tank_starboard,
        pump,
        v1,
        v2,
        min_source_level=10.0,
        max_destination_level=90.0
    )

    t_hist = []
    src_hist = []
    dst_hist = []
    flow_hist = []

    suction_valve_actual_hist = []
    discharge_valve_actual_hist = []
    suction_valve_command_hist = []
    discharge_valve_command_hist = []

    pump_actual_hist = []
    pump_command_hist = []
    sequence_hist = []

    previous_reason = None
    previous_sequence = None
    previous_alarm_snapshot = None

    print(f'\n---- Running scenario: {scenario_name} -----')
    
    
    for i in range(1, steps + 1):
        commands = scenario_fn(i)

        # Apply scenario fault states
        v2.stuck_closed = commands["v2_stuck_closed"]
        pump.failed_to_start = commands["pump_failed_to_start"]

        apply_control_logic(
            system,
            mode="manual",
            manual_pump_command=commands["manual_pump_command"],
            manual_suction_valve_command=commands["manual_suction_valve_command"],
            manual_discharge_valve_command=commands["manual_discharge_valve_command"],
        )

        flow = system.step(dt, i)

        if system.last_interlock_reason != previous_reason:
            print(f"Step {i}: interlock -> {system.last_interlock_reason}")
            previous_reason = system.last_interlock_reason

        if system.sequence_state != previous_sequence:
            print(f"Step {i}: sequence -> {system.sequence_state}")
            previous_sequence = system.sequence_state

        current_alarm_snapshot = system.alarms.copy()
        if current_alarm_snapshot != previous_alarm_snapshot:
            active_alarms = [name for name, active in current_alarm_snapshot.items() if active]
            if active_alarms:
                print(f"Step {i}: active alarms -> {active_alarms}")
            previous_alarm_snapshot = current_alarm_snapshot.copy()

        t_hist.append(i)
        src_hist.append(system.source_tank.level)
        dst_hist.append(system.destination_tank.level)
        flow_hist.append(flow)

        suction_valve_actual_hist.append(int(system.suction_valve.is_open))
        discharge_valve_actual_hist.append(int(system.discharge_valve.is_open))
        suction_valve_command_hist.append(int(system.suction_valve.commanded_open))
        discharge_valve_command_hist.append(int(system.discharge_valve.commanded_open))

        pump_actual_hist.append(int(system.pump.is_running))
        pump_command_hist.append(int(system.pump.commanded_on))
        sequence_hist.append(SEQUENCE_STATE_MAP[system.sequence_state])

    output_path = f"outputs/{scenario_name}.png"
    plot_results(
        output_path,
        t_hist,
        src_hist,
        dst_hist,
        flow_hist,
        suction_valve_actual_hist,
        discharge_valve_actual_hist,
        suction_valve_command_hist,
        discharge_valve_command_hist,
        pump_actual_hist,
        pump_command_hist,
        sequence_hist,
    )

    print(f"Saved plot: {output_path}")

def simulate_scenario(scenario_name, steps=30, dt=1.0):
    scenario_fn = SCENARIOS[scenario_name]

    tank_port = Tank('Port Tank', 100.0, 70.0)
    tank_starboard = Tank('Starboard Tank', 100.0, 20.0)
    pump = Pump('P1', flow_rate=2.0, is_running=False, start_delay_steps=2, stop_delay_steps=1)
    v1 = Valve('V1', is_open=False, opening_delay_steps=2, closing_delay_steps=2)
    v2 = Valve('V2', is_open=False, opening_delay_steps=2, closing_delay_steps=2)

    system = BallastSystem(
        tank_port, tank_starboard, pump, v1, v2,
        min_source_level=10.0,
        max_destination_level=90.0
    )

    flow_hist = []
    alarm_snapshots = []
    sequence_history = []

    for i in range(1, steps+1):
        commands = scenario_fn(i)

        v2.stuck_closed = commands['v2_stuck_closed']
        pump.failed_to_start = commands['pump_failed_to_start']

        apply_control_logic(
            system,
            model = 'annual',
            manual_pump_command=['manual_pump_command'],
            manual_suction_valve_command=['manual_suction_valve_command'],
            manual_discharge_valve_command=['manual_discharge_valve_command']
        )

        flow = system.step(dt,i)
        flow_hist.append(flow)
        alarm_snapshots.append(system.alarms.copy())
        sequence_history.append(system.sequence_state)

        return{
            'final_source_level': system.source_tank.level,
            'final_destination_level': system.destination_tank.level,
            'final_alarms': system.alarms.copy(),
            'alarm_history': system.alarm_manager.get_alarm_history(),
            'flow_hist': flow_hist,
            'sequence_hist': sequence_history,
            'last_interlock_reason': system.last_interlock_reason,
        }

def main():
    # Choose one scenario here
    scenario_to_run = 'valve_fail_to_open'

    # Other options:
    # "normal_manual_transfer"
    # "operator_valve_closure_recovery"
    # "valve_fail_to_open"
    # "pump_fail_to_start"

    run_scenario(scenario_to_run)


if __name__ == "__main__":
    main()