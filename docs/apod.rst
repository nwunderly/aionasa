.. currentmodule:: aionasa.apod

APOD API Reference
==================

This page provides a breakdown of the aionasa APOD module.

Parameters for APOD API:

- date: The date of the APOD image to retrieve. Defaults to 'today'.
- start_date: The first date to return when requesting a list of dates.
- end_date: The last date to return when requesting a list of dates. Range is inclusive.
- hd: Bool indicating whether to retrieve the URL for the high resolution image. Defaults to 'False'.
  This is present for legacy purposes, it is always ignored by the service and high-resolution urls are returned regardless.
- concept_tags: DISABLED FOR THIS ENDPOINT.

Client
------

.. autoclass:: APOD
    :members:

Data Class
----------

.. autoclass:: AstronomyPicture
    :members:

Example Code
--------------

This is a simple script that will return the title, explanation, and url from the most recent Astronomy Picture of the Day page,
then download and save the image.

.. code-block:: python
    :linenos:

    import asyncio
    from aionasa import APOD

    async def main():
        async with APOD() as apod:
            apod_entry = await apod.get()
            print(f'{apod_entry.title}\n{apod_entry.explanation}\n{apod_entry.hdurl}')
            await apod_entry.save()

    asyncio.run(main())

CLI Example
-----------

This command, like the above python script, will print data returned by the APOD API, then download and save the image.

.. code-block:: sh

    python3 -m aionasa.apod --print --download .
