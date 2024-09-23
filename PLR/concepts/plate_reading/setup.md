# Intro

Plate readers are devices that can read luminescence,
absorbance, or fluorescence from a plate.

Plate readers are asynchronous, meaning that their methods will return immediately and
will not block.

Here's an example of how to use this class in a Jupyter Notebook:

```python
from pylabrobot.plate_reading.clario_star import CLARIOStar
pr = PlateReader(backend=CLARIOStar())
pr.setup()
await pr.read_luminescence()
# [[value1, value2, value3, ...], [value1, value2, value3, ...], ...
```

# Setup

Backend options:

- CLARIOStar

Here's and example of how to setup a plate reader. setup() must be called to create connection with plate reader before using other methods.

```python
from pylabrobot.plate_reading.clario_star import CLARIOStar
pr = PlateReader(backend=CLARIOStar())
pr.setup()
```

# Methods

Building off of the setup, these are the following methods for plate readers.

## stop()

Close all connections to the plate reader and make sure setup() can be called again.

```python
await pr.stop()
```

## open()

Open the plate reader. Also known as plate out.

```python
await pr.open()
```

## close()

Close the plate reader. Also known as plate in.

```python
await pr.close()
```

## read_luminescence(focal_height: float)

Plate reader must be opened, using open(), before calling this method.
Read the luminescence from the plate reader. This should return a list of lists, where the outer list is the columns of the plate and the inner list is the rows of the plate.

```python
await pr.read_luminescence(self, focal_height = 1)
```

## read_absorbance(wavelength: int, report: Literal["OD. "transmittance])

Plate reader must be opened, using open(), before calling this method.
Read the absorbance from the plate reader. This should return a list of lists, where the
outer list is the columns of the plate and the inner list is the rows of the plate.

```python
await pr.read_absorbance( wavelength = 1,report = )
```
