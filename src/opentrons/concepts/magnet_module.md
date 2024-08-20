# Magnetic Module

The Magnetic Module is used for magnetic bead-based separations and purifications.

- Can be loaded on any deck slot
- Features a retractable magnet for bead manipulation

## Usage

```python
# Load the module
mag_module = protocol.load_module('magnetic module', '1')

# Load labware onto the module
mag_plate = mag_module.load_labware('biorad_96_wellplate_200ul_pcr')

# Engage the magnet
mag_module.engage()

# Wait for beads to separate
protocol.delay(minutes=2)

# Transfer supernatant
pipette.transfer(100, mag_plate['A1'], waste)

# Disengage the magnet
mag_module.disengage()

# Resuspend beads
pipette.transfer(100, reagent, mag_plate['A1'], mix_after=(3, 50))