#Test case: Manual intervention during transfer

**Objective**

Verify that the ballast transfer system safely blocks flow when the operator closes the discharge valve during manual operation and resumes transfer when the valve is reopened.

**Initial conditions**

- Port tank level: 70m3
- Starboard tank level: 20 m3
- Pump command: ON
- Suction valve: OPEN
- Discharge valve: OPEN
- Mode: MANUAL

**Test actions**

- Steps 1-9: normal transfer
- Steps 10-15: operator closes discharge valve
- Steps 16-30: operator reopens discharge valve

**Expected results**

- Flow occurs during the normal operation
- Flow stops when discharge valve is closed
- Interlock prevents transfer while valve is closed
- Transfer resumes when discharge valve is reopened

**Observed results**

- Flow remained 2m3/s during steps 1-9
- Flow dropped to 0 during steps 10-15
- Tank level remained constant while valve was closed
- Flow returned to 2 m3/s after reopening the valve
- Tank levels resumed changing accordingly

**Conclusion**
System correctly blocked transfer during unsafe operator action and resumed normal operation after correction.