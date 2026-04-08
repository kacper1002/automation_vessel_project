from main import simulate_scenario

def test_normal_manual_transfer_moves_liquid():
    result = simulate_scenario('normal_manual_transfer', steps=30)

    assert result['final_source_level'] < 70.0
    assert result['final_destination_level'] > 20.0
    assert result['final_alarms']['pump_fail_to_start'] is False
    assert result['final_alarms']['discharge_valve_fail_to_open'] is False

def test_valve_fail_to_open_alarm_trigger():
    result = simulate_scenario('valve_fail_to_open', steps=30)

    assert any (
        event['alarm'] == 'discharge_valve_fail_to_open' and event['active'] is True
        for event in result['alarm_history']
     )
    
def test_pump_fail_to_start_alarm_triggers():
    result = simulate_scenario("pump_fail_to_start", steps=30)

    assert any(
        event["alarm"] == "pump_fail_to_start" and event["active"] is True
        for event in result["alarm_history"]
    )


def test_pump_fail_to_start_does_not_stop_entire_scenario():
    result = simulate_scenario("pump_fail_to_start", steps=30)

    assert result["final_source_level"] < 70.0
    assert result["final_destination_level"] > 20.0

def test_source_low_low_alarm_triggers():
    result = simulate_scenario("source_low_low_trip", steps=50)

    assert any(
        event["alarm"] == "source_low_low" and event["active"] is True
        for event in result["alarm_history"]
    )

def test_destination_high_high_alarm_triggers():
    result = simulate_scenario(
        "destination_high_high_trip",
        steps=20,
        destination_level=88.0,
    )

    assert any(
        event["alarm"] == "destination_high_high" and event["active"] is True
        for event in result["alarm_history"]
    )