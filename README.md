# aio-nasa
 An async python wrapper for NASA open APIs.

### Disclaimer:
This module is still in the testing phase.

### Installing
aionasa can be installed directly from source with
```
pip install git+https://github.com/nwunderly/aio-nasa.git
```

### Python Example - APOD
This is a simple script that will return the title, explanation, and url from the most recent Astronomy Picture of the Day site,
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
```shell script
python3 -m aionasa.apod --print --download .
```