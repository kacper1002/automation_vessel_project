from main import simulate_scenario

def test_normal_manual_transfer_moves_liquid():
    result = simulate_scenario('normal_manual_transfer', steps=30)

    assert result['final_source_level'] < 70.0
    assert result['final_destination_level'] > 20.0
    assert result['final alarms']['pump_fail_to_start'] is False
    assert result['final_alarms']['discharge_valve_fail_to_open'] is False

def test_valve_fail_to_open_alarm_trigger():
    result = simulate_scenario('valve_fail_to_open', steps=30)

    assert any (
        event['alarm'] == 'discharge_valve_fail_to_open' and event['active'] is True
        for event in result['alarm_history']
     )