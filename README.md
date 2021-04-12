# aionasa
An async python wrapper for NASA open APIs. ([api.nasa.gov](https://api.nasa.gov/))


[![PyPI version](https://badge.fury.io/py/aionasa.svg)](https://pypi.org/project/aionasa)


#### Disclaimer
This module is still in the development/testing phase.
Bugs are still being worked out and breaking changes are common.


#### Current Progress: 8/17 APIs
- APOD: NASA Astronomy Picture of the Day
- InSight: Mars Weather Data
- EPIC: Earth Polychromatic Imaging Camera
- Asteroids-NeoWs: Near Earth Object Web Service
- Exoplanet: NASA Exoplanet Database
- Mars Rover Photos
- DONKI: Space Weather Database Of Notifications, Knowledge, Information
- EONET: Earth Observatory Natural Event Tracker


#### Installing
aionasa can be installed from pypi with the command:
```sh
# Linux
python3 -m pip install -U aionasa

# Windows
python -m pip install -U aionasa
```

To install the development version of the library directly from source:
```sh
$ git clone https://github.com/nwunderly/aionasa
$ cd aionasa
$ python3 -m pip install -U .
```

#### Quickstart
We'll be using IPython because it supports `await` expressions directly from the console.
```sh
$ pip install aionasa ipython
$ ipython
```

```python
from aionasa import APOD

async with APOD() as apod:
    picture = await apod.get()

picture.url # this will be the most recent APOD image URL.
```
