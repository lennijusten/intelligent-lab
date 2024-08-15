# Transfer

Transfer commands move liquid from one location to another.

## Single-channel pipette

```python
# Load pipette
pipette = protocol.load_instrument('p300_single', 'right')

# Simple transfer
pipette.transfer(100, plate['A1'], plate['B1'])

# Transfer with options
pipette.transfer(
    100,
    plate['A1'],
    plate['B1'],
    new_tip='always',
    touch_tip=True,
    blow_out=True
)
```

# Multi-channel pipette
```python
# Load pipette
multi_pipette = protocol.load_instrument('p300_multi', 'left')

# Transfer to multiple wells
multi_pipette.transfer(
    100,
    reservoir['A1'],
    plate.rows()[0]  # Transfers to the first row (A1, A2, ..., A12)
)
```
