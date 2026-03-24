def apply_control_logic(
    system,
    mode="manual",
    auto_target_level=60.0,
    manual_pump_command=True,
    manual_suction_valve_command=True,
    manual_discharge_valve_command=True,
):
    if mode == "manual":
        transfer_requested = manual_pump_command

        if manual_suction_valve_command:
            system.suction_valve.open()
        else:
            system.suction_valve.close()

        if manual_discharge_valve_command:
            system.discharge_valve.open()
        else:
            system.discharge_valve.close()

        if system.sequence_state == "IDLE":
            system.pump.stop()
            if transfer_requested:
                system.sequence_state = "OPENING_VALVES"

        elif system.sequence_state == "OPENING_VALVES":
            system.pump.stop()
            if not transfer_requested:
                system.sequence_state = "IDLE"
            elif system.suction_valve.is_open and system.discharge_valve.is_open:
                system.sequence_state = "TRANSFERRING"

        elif system.sequence_state == "TRANSFERRING":
            system.pump.start()
            if not transfer_requested:
                system.sequence_state = "STOPPING"

        elif system.sequence_state == "STOPPING":
            system.pump.stop()
            if not system.suction_valve.is_open and not system.discharge_valve.is_open:
                system.sequence_state = "IDLE"

    elif mode == "auto":
        transfer_requested = system.destination_tank.level < auto_target_level

        if system.sequence_state == "IDLE":
            system.pump.stop()
            system.suction_valve.close()
            system.discharge_valve.close()

            if transfer_requested:
                system.sequence_state = "OPENING_VALVES"

        elif system.sequence_state == "OPENING_VALVES":
            system.pump.stop()
            system.suction_valve.open()
            system.discharge_valve.open()

            if not transfer_requested:
                system.sequence_state = "STOPPING"
            elif system.suction_valve.is_open and system.discharge_valve.is_open:
                system.sequence_state = "TRANSFERRING"

        elif system.sequence_state == "TRANSFERRING":
            system.suction_valve.open()
            system.discharge_valve.open()
            system.pump.start()

            if not transfer_requested:
                system.sequence_state = "STOPPING"

        elif system.sequence_state == "STOPPING":
            system.pump.stop()
            system.discharge_valve.close()
            system.suction_valve.close()

            if not system.suction_valve.is_open and not system.discharge_valve.is_open:
                system.sequence_state = "IDLE"

    else:
        raise ValueError(f"Unknown control mode: {mode}")