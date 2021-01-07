# aionasa
An async python wrapper for NASA open APIs. ([api.nasa.gov](https://api.nasa.gov/))

#### Disclaimer
This module is still in the development/testing phase.
Bugs are still being worked out and breaking changes are common.


#### Current Progress: 5/17 APIs
- APOD: NASA Astronomy Picture of the Day
    - API: **complete**
    - CLI: **complete**
    - Documentation: **complete**
- InSight: Mars Weather Data
    - API: **complete**
    - Documentation: **complete**
- EPIC: Earth Polychromatic Imaging Camera
    - API: **complete**
    - Documentation: **complete**
- Asteroids-NeoWs: Near Earth Object Web Service
    - API: **complete**
    - Documentation: **complete**
- Exoplanet: NASA Exoplanet Database
    - API: **complete**


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
from aionasa import APOD, InSight

async with APOD() as apod:
    picture = await apod.get()

picture.url # this will be the most recent APOD image URL.

async with InSight() as insight:
    data = await insight.get()

data # this will be a dict containing the JSON data returned by the API.
```
Where `pip` is the pip command relevant to your machine's Python 3.8 installation.
This could be `pip`, `pip3`, `python -m pip`, or `python3 -m pip`.

