# Thermocycler

The Thermocycler module for Opentrons allows precise temperature control and cycling.

- Can be loaded on deck positions 7, 8, or 9
- Occupies slots 7, 8, 10, and 11 when loaded

## Usage

```python
# Load the module
tc_module = protocol.load_module('thermocycler', '7')

# Load labware onto the module
tc_plate = tc_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

# Set temperature
tc_module.set_temperature(95)

# Wait for temperature
tc_module.wait_for_temperature()

# Run a profile
profile = [
    {'temperature': 95, 'hold_time_seconds': 30},
    {'temperature': 55, 'hold_time_seconds': 30},
    {'temperature': 72, 'hold_time_seconds': 60}
]
tc_module.execute_profile(steps=profile, repetitions=30)

# Deactivate at the end of the protocol
tc_module.deactivate()