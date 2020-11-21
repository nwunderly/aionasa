# aio-nasa
An async python wrapper for NASA open APIs. ([api.nasa.gov](https://api.nasa.gov/))

#### Disclaimer
This module is still in the development/testing phase.
Bugs are still being worked out and breaking changes are common.

#### Current Progress: 2/17 APIs
- APOD: NASA Astronomy Picture of the Day
    - API: **complete**
    - CLI: **complete**
    - Documentation: **complete**
- InSight: Mars Weather Data
    - API: **complete**
    - Documentaion: **complete**
- Exoplanet: NASA Exoplanet Database
    - API: **incomplete**
- Asteroids-NeoWs: Near Earth Object Web Service
    - API: **incomplete**

### Installing
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

### Quickstart
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

### Python Script Example - APOD
This is a simple script that will return the title, explanation, and url from the most recent Astronomy Picture of the Day page,
then download and save the image.
```python
import asyncio
from aionasa import APOD

async def main():
    async with APOD() as apod:
        apod_entry = await apod.get()
        print(f'{apod_entry.title}\n{apod_entry.explanation}\n{apod_entry.hdurl}')
        await apod_entry.save()

asyncio.run(main())
```

### CLI Example - APOD
This command, like the above python script, will print data returned by the APOD API, then download and save the image.
```
python3 -m aionasa.apod --print --download .
```

#### Feedback
I'd love to hear any feedback on this project so far. It's early in development so the library's design is still being worked out.
Any design ideas or feature requests would be very helpful.