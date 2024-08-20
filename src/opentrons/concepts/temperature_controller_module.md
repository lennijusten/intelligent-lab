# Temperature Module

The Temperature Module allows precise temperature control for samples and reagents.

- Can be loaded on any deck slot
- Supports temperatures from 4°C to 95°C with 1°C precision

## Usage

```python
# Load the module
temp_module = protocol.load_module('temperature module', '3')

# Load labware onto the module
temp_plate = temp_module.load_labware('corning_96_wellplate_360ul_flat')

# Set temperature
temp_module.set_temperature(4)

# Wait for temperature
temp_module.await_temperature(4)

# Perform actions at set temperature
pipette.transfer(100, source, temp_plate['A1'])

# Change temperature
temp_module.set_temperature(37)
temp_module.await_temperature(37)

# Deactivate at the end of the protocol
temp_module.deactivate()
```