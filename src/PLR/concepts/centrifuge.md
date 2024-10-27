# Intro

Centrifuges are devices used to apply centrifugal force to samples, often for separation purposes. PyLabRobot supports controlling centrifuges with different backends, such as the VSpin.

Centrifuges are asynchronous, meaning that their methods will return immediately and will not block.

Here’s an example of how to use this class in a Jupyter Notebook:

```python
from pylabrobot.centrifuge import Centrifuge, VSpin
cf = Centrifuge(backend=VSpin())
await cf.setup()
await cf.start_spin_cycle(g=800, duration=60)
```

# Setup

Backend options:

- VSpin

Here’s an example of how to set up a centrifuge. `setup()` must be called to create a connection with the centrifuge before using other methods.

```python
from pylabrobot.centrifuge import Centrifuge, VSpin
cf = Centrifuge(backend=VSpin())
await cf.setup()
```

# Methods

Building off the setup, here are the available methods for centrifuges.

## stop()

Close all connections to the centrifuge and make sure `setup()` can be called again.

```python
await cf.stop()
```

## open_door()

Open the centrifuge door.

```python
await cf.open_door()
```

## close_door()

Close the centrifuge door.

```python
await cf.close_door()
```

## lock_door()

Lock the centrifuge door.

```python
await cf.lock_door()
```

## unlock_door()

Unlock the centrifuge door.

```python
await cf.unlock_door()
```

## lock_bucket()

Lock centrifuge buckets.

```python
await cf.lock_bucket()
```

## unlock_bucket()

Unlock centrifuge buckets.

```python
await cf.unlock_bucket()
```

## go_to_bucket1()

Rotate to Bucket 1.

```python
await cf.go_to_bucket1()
```

## go_to_bucket2()

Rotate to Bucket 2.

```python
await cf.go_to_bucket2()
```

## rotate_distance(distance: int)

Rotate the buckets a specified distance (e.g., 8000 for 360 degrees).

```python
await cf.rotate_distance(distance=8000)
```

## start_spin_cycle(g: float, duration: int)

Start the centrifuge spin cycle with specified `g` force and duration in seconds.

```python
await cf.start_spin_cycle(g=800, duration=60)
```

# VSpin

The VSpin centrifuge is controlled by the `VSpin` backend.

```python
from pylabrobot.centrifuge import Centrifuge, VSpin
cf = Centrifuge(name='centrifuge', backend=VSpin(bucket_1_position=0), size_x=1, size_y=1, size_z=1)
```