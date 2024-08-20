# Discard Tip

The drop_tip or discard_tip commands are used to dispose of the current pipette tip.

- By default, tips are discarded in the fixed trash bin (usually in slot 12)
- Can specify a custom location for tip disposal

## Usage

```python
# Default tip discard (to fixed trash)
pipette.drop_tip()

# Discard to a specific location
pipette.drop_tip(tiprack['A1'])

# Discard as part of a transfer
pipette.transfer(
    100,
    source,
    dest,
    new_tip='always',
    trash=True  # Discard to default trash
)

# Return tip to tiprack
pipette.transfer(
    100,
    source,
    dest,
    new_tip='always',
    trash=False  # Return tip to tiprack
)