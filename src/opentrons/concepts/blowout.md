# Blow Out

The `blow_out` command expels any remaining liquid or air from the tip.

- By default, it expels the pipette's maximum volume
- Can be performed at the same location as dispense or at a separate location

## Usage

```python
# Basic blow out (at current location)
pipette.blow_out()

# Blow out at a specific location
pipette.blow_out(plate['A1'])

# Blow out as part of a transfer
pipette.transfer(
    100,
    source,
    dest,
    blow_out=True
)

# Control air volume (not directly supported)
# To approximate, aspirate air before blow out
pipette.aspirate(10, source.top())  # Aspirate 10µL of air
pipette.blow_out(dest)
```