PROJECT CONTEXT – BALLAST AUTOMATION SIMULATOR

Project summary:
This project is a Python-based simulation of a marine ballast transfer automation system. It models control logic, equipment behavior, interlocks, alarms, and fault scenarios in a structured way similar to real industrial automation systems.

Current implementation status:

Core system:

* Two tanks (source and destination)
* Pump and two valves (suction + discharge)
* Flow-based transfer simulation

Control logic:

* Manual control mode implemented
* Sequenced operation via state machine:
  IDLE → OPENING_VALVES → TRANSFERRING → STOPPING

Command vs actual modeling:

* All actuators have:

  * commanded state (control request)
  * actual state (physical response)
* Enables mismatch detection

Delays:

* Valve opening/closing delays implemented
* Pump start/stop delays implemented

Interlocks:

* Transfer allowed only if:

  * pump running
  * valves open (actual state)
  * source level above minimum
  * destination level below maximum

Alarms:

* AlarmManager implemented with:

  * source_low_low
  * destination_high_high
  * discharge_valve_fail_to_open
  * pump_fail_to_start
* Alarms based on:

  * command vs actual mismatch
  * time-based thresholds

Scenarios (via scenario runner):

* normal_manual_transfer
* operator_valve_closure_recovery
* valve_fail_to_open
* pump_fail_to_start

Visualization:

* Multi-subplot output:

  1. Tank levels
  2. Flow rate
  3. Command vs actual states
  4. Sequence state (mapped to numeric)

Project structure:

* src/ → system + components
* control/ → logic, interlocks, modes
* alarms/ → alarm manager
* docs/ → functional description, FAT, cause/effect
* outputs/ → scenario plots

---

NEXT DEVELOPMENT GOALS

1. Pump fault validation (short-term – already partially done)

* Verify pump_fail_to_start behavior fully
* Confirm:

  * command ON
  * actual OFF
  * zero flow
  * alarm triggers after timeout

2. Improve alarm system (medium priority)

* Add:

  * alarm history (event log with step/time)
  * alarm activation + clearing tracking
* Optional:

  * alarm latching
  * acknowledgment concept

3. Scenario expansion (high value)
   Add more realistic FAT-style cases:

* Combined faults (e.g. valve fault + operator action)
* Low source level during transfer
* Destination tank reaching high-high during operation
* Sequence interruption mid-transfer

4. Scenario runner improvements

* Option to run all scenarios in batch
* Save outputs per scenario automatically
* Possibly generate summary (pass/fail style)

5. Documentation (important for portfolio)
   Improve docs/:

* system_description.md → explain architecture
* fat_procedure.md → structured test cases
* cause_effect.md → link conditions to responses
* add images from outputs/

6. Optional: Sequence state refinement

* Add clearer transitions:

  * e.g. WAITING_FOR_FEEDBACK states
* Possibly include timing constraints in sequence logic

7. Optional: HMI (later stage)

* Simple UI (e.g. Streamlit)
* Display:

  * tank levels
  * actuator states
  * active alarms
  * current mode
* Allow manual control inputs

---

MAIN ENGINEERING FOCUS

This project is intended to demonstrate:

* Industrial automation logic design
* Sequencing and state machines
* Interlocks based on real feedback
* Command vs actual mismatch handling
* Fault detection and alarm systems
* Scenario-based validation (FAT-style testing)

---

8. Update to v4
* Now alarm system gives clear outputs in CSV
* Added run loop, that runs all of the scenarios and produces report in csv
* Ran pytest tests on tests folder, to keep track of changes and if system is working. Allowing for easier control of if things are working. 

9. Adding 2 more scenarios
* Source low-low protection scenario
Goal:
- Keep transfer running until source tank reaches the low-low threshold
- Confirm source_low_low alarm appears
- Confirm transfer stop or is blocked by interlock

* Destination high-high protection scenario
Goal:
- Keep transfer running until destination tank reaches the high-high threshold
- Confirm destination_high_high alarm appears
- Confirm transfer stops or is blocked

* Also adding testing scenarios for those
- test_source_low_low_alarm_triggers
- test_destination_high_high_alarm_triggers

Avoid:

* jumping to UI before logic is stable
* overcomplicating architecture too early

Keep:

* modular structure
* scenario-driven testing approach

