import os
import matplotlib.pyplot as plt
import csv

from src.tank import Tank
from src.pump import Pump
from src.valve import Valve
from src.system import BallastSystem
from control.logic import apply_control_logic


SEQUENCE_STATE_MAP = {
    "IDLE": 0,
    "OPENING_VALVES": 1,
    "TRANSFERRING": 2,
    "STOPPING": 3,
}


def scenario_operator_valve_closure_recovery(i):
    if i < 10:
        return {
            "manual_pump_command": True,
            "manual_suction_valve_command": True,
            "manual_discharge_valve_command": True,
            "v2_stuck_closed": False,
            "pump_failed_to_start": False,
        }
    elif 10 <= i < 16:
        return {
            "manual_pump_command": True,
            "manual_suction_valve_command": True,
            "manual_discharge_valve_command": False,
            "v2_stuck_closed": False,
            "pump_failed_to_start": False,
        }
    else:
        return {
            "manual_pump_command": True,
            "manual_suction_valve_command": True,
            "manual_discharge_valve_command": True,
            "v2_stuck_closed": False,
            "pump_failed_to_start": False,
        }


def scenario_valve_fail_to_open(i):
    if i < 10:
        return {
            "manual_pump_command": True,
            "manual_suction_valve_command": True,
            "manual_discharge_valve_command": True,
            "v2_stuck_closed": False,
            "pump_failed_to_start": False,
        }
    elif 10 <= i < 16:
        return {
            "manual_pump_command": True,
            "manual_suction_valve_command": True,
            "manual_discharge_valve_command": True,
            "v2_stuck_closed": True,
            "pump_failed_to_start": False,
        }
    else:
        return {
            "manual_pump_command": True,
            "manual_suction_valve_command": True,
            "manual_discharge_valve_command": True,
            "v2_stuck_closed": False,
            "pump_failed_to_start": False,
        }


def scenario_pump_fail_to_start(i):
    if i < 10:
        return {
            "manual_pump_command": True,
            "manual_suction_valve_command": True,
            "manual_discharge_valve_command": True,
            "v2_stuck_closed": False,
            "pump_failed_to_start": False,
        }
    elif 10 <= i < 16:
        return {
            "manual_pump_command": True,
            "manual_suction_valve_command": True,
            "manual_discharge_valve_command": True,
            "v2_stuck_closed": False,
            "pump_failed_to_start": True,
        }
    else:
        return {
            "manual_pump_command": True,
            "manual_suction_valve_command": True,
            "manual_discharge_valve_command": True,
            "v2_stuck_closed": False,
            "pump_failed_to_start": False,
        }


def scenario_normal_manual_transfer(i):
    return {
        "manual_pump_command": True,
        "manual_suction_valve_command": True,
        "manual_discharge_valve_command": True,
        "v2_stuck_closed": False,
        "pump_failed_to_start": False,
    }


SCENARIOS = {
    "normal_manual_transfer": scenario_normal_manual_transfer,
    "operator_valve_closure_recovery": scenario_operator_valve_closure_recovery,
    "valve_fail_to_open": scenario_valve_fail_to_open,
    "pump_fail_to_start": scenario_pump_fail_to_start,
}


def build_default_system():
    tank_port = Tank("Port Tank", 100.0, 70.0)
    tank_starboard = Tank("Starboard Tank", 100.0, 20.0)

    pump = Pump(
        "P1",
        flow_rate=2.0,
        is_running=False,
        start_delay_steps=2,
        stop_delay_steps=1,
    )

    v1 = Valve(
        "V1",
        is_open=False,
        opening_delay_steps=2,
        closing_delay_steps=2,
    )

    v2 = Valve(
        "V2",
        is_open=False,
        opening_delay_steps=2,
        closing_delay_steps=2,
    )

    return BallastSystem(
        tank_port,
        tank_starboard,
        pump,
        v1,
        v2,
        min_source_level=10.0,
        max_destination_level=90.0,
    )


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

    axes[0].plot(time, source, label="Port Tank [m3]")
    axes[0].plot(time, destination, label="Starboard Tank [m3]")
    axes[0].set_ylabel("Level [m3]")
    axes[0].set_title("Tank Levels")
    axes[0].grid(alpha=0.3)
    axes[0].legend()

    axes[1].plot(time, flow, label="Flow [m3/s]")
    axes[1].set_ylabel("Flow [m3/s]")
    axes[1].set_title("Flow Rate")
    axes[1].grid(alpha=0.3)
    axes[1].legend()

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


def simulate_scenario(scenario_name, steps=30, dt=1.0):
    scenario_fn = SCENARIOS[scenario_name]
    system = build_default_system()

    flow_hist = []
    alarm_snapshots = []
    sequence_hist = []

    for i in range(1, steps + 1):
        commands = scenario_fn(i)

        system.discharge_valve.stuck_closed = commands["v2_stuck_closed"]
        system.pump.failed_to_start = commands["pump_failed_to_start"]

        apply_control_logic(
            system,
            mode="manual",
            manual_pump_command=commands["manual_pump_command"],
            manual_suction_valve_command=commands["manual_suction_valve_command"],
            manual_discharge_valve_command=commands["manual_discharge_valve_command"],
        )

        flow = system.step(dt, i)

        flow_hist.append(flow)
        alarm_snapshots.append(system.alarms.copy())
        sequence_hist.append(system.sequence_state)

    return {
        "scenario_name": scenario_name,
        "final_source_level": system.source_tank.level,
        "final_destination_level": system.destination_tank.level,
        "final_alarms": system.alarms.copy(),
        "alarm_history": system.alarm_manager.get_alarm_history(),
        "alarm_snapshots": alarm_snapshots,
        "flow_hist": flow_hist,
        "sequence_hist": sequence_hist,
        "final_sequence_state": system.sequence_state,
        "last_interlock_reason": system.last_interlock_reason,
    }


def summarize_result(result):
    alarms_raised = sorted(
        {event["alarm"] for event in result["alarm_history"] if event["active"] is True}
    )

    final_active_alarms = sorted(
        [name for name, active in result["final_alarms"].items() if active]
    )

    transfer_occurred = result["final_destination_level"] > 20.0
    alarm_lifecycle = summarize_alarm_lifecycle(result["alarm_history"])

    return {
        "scenario_name": result["scenario_name"],
        "final_source_level": round(result["final_source_level"], 2),
        "final_destination_level": round(result["final_destination_level"], 2),
        "transfer_occurred": transfer_occurred,
        "alarms_raised": alarms_raised,
        "alarm_lifecycle": alarm_lifecycle,
        "final_active_alarms": final_active_alarms,
        "final_sequence_state": result["final_sequence_state"],
        "last_interlock_reason": result["last_interlock_reason"],
    }

def print_summary_table(summaries):
    print("\n=== Scenario Summary Report ===")
    print(
        f"{'Scenario':35}"
        f"{'Src Final':>10}"
        f"{'Dst Final':>10}"
        f"{'Transfer':>10}"
        f"{'Final Seq':>15}"
    )
    print("-" * 80)

    for summary in summaries:
        print(
            f"{summary['scenario_name']:35}"
            f"{summary['final_source_level']:>10.2f}"
            f"{summary['final_destination_level']:>10.2f}"
            f"{str(summary['transfer_occurred']):>10}"
            f"{summary['final_sequence_state']:>15}"
        )

        print(f"  alarms_raised      : {summary['alarms_raised']}")
        print(f"  alarm_lifecycle    : {summary['alarm_lifecycle']}")
        print(f"  final_active_alarms: {summary['final_active_alarms']}")
        print(f"  last_interlock     : {summary['last_interlock_reason']}")
        print("-" * 80)


def run_all_scenarios(steps=30, dt=1.0, save_plots=False, save_csv=True):
    summaries = []

    for scenario_name in SCENARIOS:
        result = simulate_scenario(scenario_name, steps=steps, dt=dt)
        summaries.append(summarize_result(result))

        if save_plots:
            run_scenario(scenario_name, steps=steps, dt=dt) 


    print_summary_table(summaries)

    if save_csv:
        save_summary_csv(summaries)
    return summaries


def run_scenario(scenario_name, steps=30, dt=1.0):
    scenario_fn = SCENARIOS[scenario_name]
    system = build_default_system()

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

    print(f"\n---- Running scenario: {scenario_name} -----")

    for i in range(1, steps + 1):
        commands = scenario_fn(i)

        system.discharge_valve.stuck_closed = commands["v2_stuck_closed"]
        system.pump.failed_to_start = commands["pump_failed_to_start"]

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

    print("Cleaned alarm lifecycle:")
    for item in summarize_alarm_lifecycle(system.alarm_manager.get_alarm_history()):
        print(item)
    print(f"Saved plot: {output_path}")


def save_summary_csv(summaries, output_path="outputs/scenario_summary.csv"):
    os.makedirs("outputs", exist_ok=True)

    fieldnames = [
        "scenario",
        "source_final_m3",
        "destination_final_m3",
        "transfer_occurred",
        "alarms_raised",
        "alarm_durations",
        "active_alarms_at_end",
        "final_sequence",
        "last_interlock",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for summary in summaries:
            alarms_raised = ", ".join(summary["alarms_raised"]) if summary["alarms_raised"] else "None"

            alarm_durations = "; ".join(
                f"{item['alarm']} ({item['duration_steps']} steps, {item['start_step']}->{item['cleared_step']})"
                for item in summary["alarm_lifecycle"]
            ) if summary["alarm_lifecycle"] else "None"

            active_alarms_at_end = ", ".join(summary["final_active_alarms"]) if summary["final_active_alarms"] else "None"

            row = {
                "scenario": summary["scenario_name"],
                "source_final_m3": summary["final_source_level"],
                "destination_final_m3": summary["final_destination_level"],
                "transfer_occurred": summary["transfer_occurred"],
                "alarms_raised": alarms_raised,
                "alarm_durations": alarm_durations,
                "active_alarms_at_end": active_alarms_at_end,
                "final_sequence": summary["final_sequence_state"],
                "last_interlock": summary["last_interlock_reason"],
            }

            writer.writerow(row)

    print(f"Saved summary CSV: {output_path}")

def summarize_alarm_lifecycle(alarm_history):
    lifecycle = []

    for event in alarm_history:
        if event['event'] != 'CLEARED':
            continue

        duration = event.get('duration_steps')

        if duration is None or duration <= 0:
            continue

        lifecycle.append(
            {
                'alarm': event['alarm'],
                'start_step': event.get('start_step'),
                'cleared_step': event['step'],
                'duration_steps': duration,
            }
        )

    return lifecycle


def main():
    mode = 'batch'      #'batch' or 'single'
    # Batch = summary + csv
    # Single = debug + plot

    if mode == 'batch':
        run_all_scenarios(save_plots=True)
    elif mode == 'single':
        scenario_to_run = 'pump_fail_to_start'
        run_scenario(scenario_to_run)


if __name__ == "__main__":
    main()