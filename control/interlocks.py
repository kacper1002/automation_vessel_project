def check_transfer_interlocks(
    pump,
    suction_valve,
    discharge_valve,
    source_tank,
    destination_tank,
    min_source_level,
    max_destination_level,
):
    if not pump.is_running:
        return False, "Pump is OFF"

    if not suction_valve.is_open:
        return False, "Suction valve is CLOSED"

    if not discharge_valve.is_open:
        return False, "Discharge valve is CLOSED"

    if source_tank.level <= min_source_level:
        return False, "Source tank LOW-LOW level reached"

    if destination_tank.level >= max_destination_level:
        return False, "Destination tank HIGH-HIGH level reached"

    if source_tank.level <= 0:
        return False, "Source tank is empty"

    if destination_tank.level >= destination_tank.capacity:
        return False, "Destination tank is full"

    return True, "Transfer allowed"