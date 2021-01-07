.. currentmodule:: aionasa.epic


EPIC API Reference
==================

This page provides a breakdown of the aionasa EPIC module.

The documentation for NASA's EPIC API can be found `here <https://epic.gsfc.nasa.gov/about/api>`_.


Client
------

.. autoclass:: EPIC
    :members:


Data Class
----------

.. autoclass:: EarthImage
    :members:


Example Code
------------

This is a sample script that will print out some data on all
images from the most recent available date.

.. code-block:: python

    import asyncio
    from aionasa import EPIC

    async def main():
        async with EPIC() as epic:
            images = await epic.natural_images()
            for i, image in enumerate(images):
                print(f"Image {i+1} of {len(images)}\n"
                      f"Url: {image.png_url}\n"
                      f"Caption: {image.caption}\n")

    if __name__ == "__main__":
        asyncio.run(main())

